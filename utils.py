import os
import sys
import time
import subprocess
import io
import json
import urllib.request
from PIL import Image, ImageGrab

APP_VERSION = "1.3.0"
GITHUB_REPO = "fabionunesconsultorti-collab/GoHorseDocumentador"


def _parse_version(version: str) -> tuple:
    parts = []
    for chunk in version.split("."):
        digits = "".join(c for c in chunk if c.isdigit())
        parts.append(int(digits) if digits else 0)
    return tuple(parts)


def check_for_updates(timeout: int = 8) -> dict:
    """
    Consulta a API do GitHub pela última release publicada do repositório.
    Retorna um dict {"has_update", "current_version", "latest_version", "url"}.
    Levanta exceção em caso de falha de rede/parsing (sem conexão, repo sem releases, etc.).
    """
    url = f"https://api.github.com/repos/{GITHUB_REPO}/releases/latest"
    req = urllib.request.Request(url, headers={"Accept": "application/vnd.github+json"})
    with urllib.request.urlopen(req, timeout=timeout) as response:
        data = json.loads(response.read().decode("utf-8"))

    latest_version = data.get("tag_name", "").lstrip("vV")
    release_url = data.get("html_url", f"https://github.com/{GITHUB_REPO}/releases/latest")

    return {
        "has_update": _parse_version(latest_version) > _parse_version(APP_VERSION),
        "current_version": APP_VERSION,
        "latest_version": latest_version,
        "url": release_url,
    }


def grab_clipboard_image() -> Image.Image | None:
    """
    Tenta obter uma imagem da área de transferência de forma multiplataforma.
    Retorna um objeto PIL.Image ou None se nenhuma imagem estiver disponível.
    """
    # 1. Tentar método nativo do Pillow (geralmente funciona bem no Windows e macOS)
    try:
        img = ImageGrab.grabclipboard()
        if isinstance(img, Image.Image):
            # Força o carregamento da imagem para evitar problemas de lazy loading
            img.load()
            return img
    except Exception:
        pass

    # 2. Fallbacks específicos para Linux se o Pillow falhar (ex: ausência de xclip/wl-paste)
    if sys.platform.startswith('linux'):
        # 2.1 Tentar wl-paste (Wayland nativo)
        try:
            process = subprocess.Popen(['wl-paste', '-t', 'image/png'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            try:
                stdout, _ = process.communicate(timeout=1.5)
            except subprocess.TimeoutExpired:
                process.kill()
                process.communicate()
                stdout = b""
            if process.returncode == 0 and len(stdout) > 0:
                img = Image.open(io.BytesIO(stdout))
                img.load()
                return img
        except Exception:
            pass

        # 2.2 Tentar xclip (X11)
        try:
            process = subprocess.Popen(['xclip', '-selection', 'clipboard', '-t', 'image/png', '-o'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            try:
                stdout, _ = process.communicate(timeout=1.5)
            except subprocess.TimeoutExpired:
                process.kill()
                process.communicate()
                stdout = b""
            if process.returncode == 0 and len(stdout) > 0:
                img = Image.open(io.BytesIO(stdout))
                img.load()
                return img
        except Exception:
            pass

        # 2.3 Tentar subprocesso isolado com PyGObject (Gtk.Clipboard)
        # IMPORTANTE: Executado obrigatoriamente em SUBPROCESSO ISOLADO para evitar
        # conflito de memória/X11 entre GDK e Tkinter no processo principal.
        try:
            import shutil
            python_bin = sys.executable if not getattr(sys, 'frozen', False) else (shutil.which('python3') or 'python3')
            gtk_script = (
                "import sys\n"
                "try:\n"
                "    import gi\n"
                "    gi.require_version('Gtk', '3.0')\n"
                "    from gi.repository import Gtk, Gdk\n"
                "    cb = Gtk.Clipboard.get(Gdk.SELECTION_CLIPBOARD)\n"
                "    pix = cb.wait_for_image()\n"
                "    if pix:\n"
                "        ok, buf = pix.save_to_bufferv('png', [], [])\n"
                "        if ok and buf:\n"
                "            sys.stdout.buffer.write(buf)\n"
                "            sys.exit(0)\n"
                "except Exception:\n"
                "    pass\n"
                "sys.exit(1)\n"
            )
            process = subprocess.Popen([python_bin, '-c', gtk_script], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            try:
                stdout, _ = process.communicate(timeout=2.0)
            except subprocess.TimeoutExpired:
                process.kill()
                process.communicate()
                stdout = b""
            if process.returncode == 0 and len(stdout) > 0:
                img = Image.open(io.BytesIO(stdout))
                img.load()
                return img
        except Exception:
            pass

        # 2.4 Tentar xsel (X11)
        try:
            process = subprocess.Popen(['xsel', '--clipboard', '--output'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            try:
                stdout, _ = process.communicate(timeout=1.5)
            except subprocess.TimeoutExpired:
                process.kill()
                process.communicate()
                stdout = b""
            if process.returncode == 0 and len(stdout) > 0:
                try:
                    img = Image.open(io.BytesIO(stdout))
                    img.load()
                    return img
                except Exception:
                    pass
        except Exception:
            pass

    return None

def trigger_native_screenshot() -> bool:
    """
    Aciona a ferramenta nativa de captura de tela do sistema operacional.
    Retorna True se conseguir disparar o comando, False caso contrário.
    """
    if sys.platform.startswith('win32'):
        # Windows Snipping Tool (modo seleção rápida)
        try:
            subprocess.Popen(['cmd.exe', '/c', 'start', 'ms-screenclip:'])
            return True
        except Exception:
            pass
    elif sys.platform.startswith('darwin'):
        # macOS Captura interativa salvando na área de transferência (-c)
        try:
            subprocess.Popen(['/usr/sbin/screencapture', '-c', '-i'])
            return True
        except Exception:
            pass
    elif sys.platform.startswith('linux'):
        # Tenta diversas ferramentas nativas comuns no Linux
        # O objetivo é abrir a ferramenta interativa de recorte/cópia
        commands = [
            # 1. Desktop Portal oficial (Universal no Ubuntu 20/22/24, Wayland e X11, GNOME e KDE)
            ['gdbus', 'call', '--session', '--dest', 'org.freedesktop.portal.Desktop',
             '--object-path', '/org/freedesktop/portal/desktop',
             '--method', 'org.freedesktop.portal.Screenshot.Screenshot', '', "{'interactive': <true>}"],
            # 2. GNOME Screenshot
            ['gnome-screenshot', '-a', '-c'],
            ['gnome-screenshot', '-i'],
            # 3. Flameshot
            ['flameshot', 'gui'],
            # 4. KDE Spectacle
            ['spectacle', '-r'],
            # 5. XFCE Screenshooter
            ['xfce4-screenshooter', '-r', '-c'],
            # 6. Ksnip
            ['ksnip', '-r']
        ]
        for cmd in commands:
            try:
                subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                return True
            except FileNotFoundError:
                continue
            except Exception:
                continue
    return False

def take_screenshot(root) -> Image.Image | None:
    """
    Minimiza a janela principal do Tkinter, captura a tela inteira e restaura a janela.
    """
    try:
        # Minimizar a janela para não aparecer no print
        root.withdraw()
        root.update()
        
        # Esperar um breve momento para a animação do OS de minimizar terminar
        time.sleep(0.5)
        
        # Capturar a tela
        screenshot = ImageGrab.grab()
        if screenshot:
            screenshot.load()
            
    except Exception as e:
        print(f"Erro ao capturar tela: {e}")
        screenshot = None
    finally:
        # Restaurar a janela
        root.deiconify()
        root.update()
        
    return screenshot


def get_resource_path(relative_path):
    """
    Retorna o caminho absoluto para um recurso, funcionando em desenvolvimento
    e quando empacotado pelo PyInstaller.
    """
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_path, relative_path)


def get_autosave_dir():
    """
    Retorna (criando se necessário) o diretório gravável usado para o
    autosave de recuperação, em uma pasta de dados de usuário apropriada
    para cada sistema operacional.
    """
    if sys.platform.startswith("win"):
        base = os.environ.get("APPDATA", os.path.expanduser("~"))
    elif sys.platform == "darwin":
        base = os.path.expanduser("~/Library/Application Support")
    else:
        base = os.environ.get("XDG_DATA_HOME", os.path.expanduser("~/.local/share"))

    path = os.path.join(base, "GoHorseDocumentador", "autosave")
    os.makedirs(path, exist_ok=True)
    return path
