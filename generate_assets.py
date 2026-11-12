#!/usr/bin/env python3
"""
generate_assets.py
Gera os assets visuais oficiais do GoHorseDocumentador:
- img/icone.svg (Vetor mestre do ícone)
- img/icone.png (Ícone 512x512 de alta resolução)
- img/icone.ico (Ícone multi-tamanho para Windows)
- img/logo.svg (Vetor mestre do logotipo completo)
- img/logo.png (Logotipo horizontal de alta resolução)
- icone.png (Raiz do repositório)
"""

import os
import subprocess
from PIL import Image

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
IMG_DIR = os.path.join(BASE_DIR, "img")
os.makedirs(IMG_DIR, exist_ok=True)

# ─── 1. SVG DO ÍCONE / LOGOMARCA (512x512) ──────────────────────────────────
ICONE_SVG = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512" width="512" height="512">
  <defs>
    <!-- Gradiente de fundo do ícone estilo GNOME / Ubuntu -->
    <linearGradient id="bgGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#2d1527" />
      <stop offset="50%" stop-color="#1e1e24" />
      <stop offset="100%" stop-color="#141416" />
    </linearGradient>

    <!-- Gradiente Laranja Ubuntu Yaru -->
    <linearGradient id="orangeGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#ff7844" />
      <stop offset="100%" stop-color="#e95420" />
    </linearGradient>

    <!-- Gradiente Crina / Fogo Go Horse -->
    <linearGradient id="maneGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#ff944d" />
      <stop offset="100%" stop-color="#c64600" />
    </linearGradient>

    <!-- Gradiente Azul Processo Adwaita -->
    <linearGradient id="blueGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#62a0ea" />
      <stop offset="100%" stop-color="#1c71d8" />
    </linearGradient>

    <!-- Gradiente do Documento de Processos -->
    <linearGradient id="docGrad" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#ffffff" />
      <stop offset="100%" stop-color="#f2f2f5" />
    </linearGradient>

    <!-- Sombras para profundidade -->
    <filter id="dropShadow" x="-10%" y="-10%" width="130%" height="130%">
      <feDropShadow dx="0" dy="12" stdDeviation="16" flood-color="#000000" flood-opacity="0.5" />
    </filter>
    <filter id="subtleShadow" x="-10%" y="-10%" width="130%" height="130%">
      <feDropShadow dx="0" dy="6" stdDeviation="8" flood-color="#000000" flood-opacity="0.35" />
    </filter>
  </defs>

  <!-- Base Squircle Estilo GNOME/Ubuntu -->
  <rect x="36" y="36" width="440" height="440" rx="96" ry="96" fill="url(#bgGrad)" filter="url(#dropShadow)" />
  <rect x="36" y="36" width="440" height="440" rx="96" ry="96" fill="none" stroke="#ffffff" stroke-opacity="0.12" stroke-width="2.5" />

  <!-- Prancheta / Documento de Mapeamento de Processos (Em perspectiva suave) -->
  <g transform="translate(196, 76) rotate(6)" filter="url(#subtleShadow)">
    <!-- Base da folha/prancheta -->
    <rect x="0" y="0" width="206" height="280" rx="16" ry="16" fill="url(#docGrad)" />
    <!-- Faixa superior técnica -->
    <rect x="0" y="0" width="206" height="34" rx="16" ry="16" fill="url(#orangeGrad)" />
    <!-- Grampo superior da prancheta -->
    <rect x="63" y="-12" width="80" height="22" rx="7" ry="7" fill="#2d2d34" />
    <circle cx="103" cy="-1" r="4.5" fill="#ffffff" />

    <!-- Etapa 1: Captura -->
    <circle cx="32" cy="62" r="9" fill="url(#orangeGrad)" />
    <text x="32" y="66" font-family="Ubuntu, 'Noto Sans', sans-serif" font-size="11" font-weight="bold" fill="#ffffff" text-anchor="middle">1</text>
    <rect x="52" y="58" width="118" height="8" rx="4" ry="4" fill="#deddda" />
    <rect x="52" y="70" width="75" height="5" rx="2.5" ry="2.5" fill="#e6e6e6" />

    <!-- Linha conectora pontilhada -->
    <line x1="32" y1="73" x2="32" y2="108" stroke="#3584e4" stroke-width="3" stroke-dasharray="4,3" />

    <!-- Etapa 2: Anotação / Seta -->
    <circle cx="32" cy="119" r="9" fill="url(#blueGrad)" />
    <text x="32" y="123" font-family="Ubuntu, 'Noto Sans', sans-serif" font-size="11" font-weight="bold" fill="#ffffff" text-anchor="middle">2</text>
    <rect x="52" y="115" width="130" height="8" rx="4" ry="4" fill="#deddda" />
    <rect x="52" y="127" width="95" height="5" rx="2.5" ry="2.5" fill="#e6e6e6" />

    <!-- Linha conectora pontilhada -->
    <line x1="32" y1="130" x2="32" y2="165" stroke="#26a269" stroke-width="3" stroke-dasharray="4,3" />

    <!-- Etapa 3: Exportação / Concluído -->
    <circle cx="32" cy="176" r="9" fill="#26a269" />
    <path d="M27 176 L30.5 179.5 L37 172.5" stroke="#ffffff" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" fill="none" />
    <rect x="52" y="172" width="105" height="8" rx="4" ry="4" fill="#deddda" />
    <rect x="52" y="184" width="65" height="5" rx="2.5" ry="2.5" fill="#e6e6e6" />

    <!-- Carimbo de validação rápida do Processo -->
    <rect x="28" y="222" width="148" height="28" rx="6" ry="6" fill="none" stroke="#e95420" stroke-width="2" stroke-dasharray="7,3" />
    <text x="102" y="240" font-family="Ubuntu, 'Noto Sans', sans-serif" font-size="11" font-weight="bold" fill="#e95420" text-anchor="middle" letter-spacing="1.5">PROCESSO OK</text>
  </g>

  <!-- Cavalo Xtreme Go Horse (Silhueta icônica, dinâmica e minimalista) -->
  <g id="horse-figure" filter="url(#subtleShadow)">
    <!-- Crina veloz XGH -->
    <path d="M 148 135 C 130 155, 102 180, 92 210 C 110 205, 128 200, 140 205 C 115 225, 96 255, 92 285 C 112 275, 132 270, 148 278 C 124 305, 110 345, 114 385 C 138 355, 166 335, 188 328 Z" fill="url(#maneGrad)" />
    <path d="M 166 140 C 144 165, 118 195, 110 225 C 128 220, 146 215, 156 220 C 132 245, 116 275, 112 305 C 132 295, 152 290, 168 298 C 142 330, 130 370, 136 405 C 160 375, 186 355, 208 348 Z" fill="url(#orangeGrad)" />

    <!-- Cabeça e Busto do Cavalo -->
    <path d="
      M 175 125 
      C 185 105, 205 92, 218 92 
      C 222 92, 224 100, 220 115 
      C 235 110, 255 112, 275 128 
      C 298 148, 335 195, 348 230 
      C 355 248, 350 262, 332 268 
      C 315 274, 292 268, 278 255 
      L 272 268 
      C 255 295, 240 335, 245 425 
      L 155 425 
      C 152 380, 158 310, 172 250 
      C 162 230, 156 195, 162 165 
      Z" 
      fill="url(#orangeGrad)" stroke="#ffffff" stroke-width="2.5" stroke-linejoin="round" />

    <!-- Narina -->
    <ellipse cx="332" cy="248" rx="6" ry="9" transform="rotate(25 332 248)" fill="#5c1e00" />

    <!-- Maxilar esculpido -->
    <path d="M 325 264 C 300 275, 275 268, 260 250" stroke="#ba3e03" stroke-width="3.5" stroke-linecap="round" fill="none" />

    <!-- Olho focado e óculos de hacker/documentador XGH -->
    <polygon points="252,158 274,166 256,174" fill="#1e1e24" />
    <circle cx="260" cy="166" r="2.5" fill="#ffffff" />

    <path d="M 235 158 L 285 168" stroke="#1e1e24" stroke-width="3.5" stroke-linecap="round" />
    <rect x="244" y="152" width="36" height="25" rx="6" ry="6" fill="rgba(53, 132, 228, 0.4)" stroke="#ffffff" stroke-width="2.2" />
    <line x1="248" y1="157" x2="265" y2="157" stroke="#ffffff" stroke-width="2" stroke-linecap="round" opacity="0.85" />

    <!-- Caneta Técnica de Processos em Diagonal -->
    <g transform="translate(250, 310) rotate(-35)">
      <path d="M 0 0 L 135 0 L 150 10 L 135 20 L 0 20 Z" fill="#ffffff" stroke="#2d2d34" stroke-width="2" />
      <path d="M 0 0 L 38 0 L 38 20 L 0 20 Z" fill="#3584e4" />
      <polygon points="150,10 172,10 162,15" fill="#e95420" />
      <circle cx="170" cy="10" r="3" fill="#e95420" />
    </g>

    <!-- Seta circular dinâmica de fluxo de processo -->
    <path d="M 135 435 C 195 458, 305 458, 375 418 C 412 395, 430 358, 430 315" fill="none" stroke="url(#orangeGrad)" stroke-width="7" stroke-linecap="round" stroke-dasharray="14 7" />
    <polygon points="428,300 442,324 418,324" fill="#e95420" />
  </g>
</svg>'''


# ─── 2. SVG DO LOGOTIPO HORIZONTAL (800x220) ─────────────────────────────────
LOGO_SVG = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 220" width="800" height="220">
  <defs>
    <!-- Gradiente Laranja Ubuntu Yaru -->
    <linearGradient id="logoOrange" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#ff7844" />
      <stop offset="100%" stop-color="#e95420" />
    </linearGradient>

    <!-- Gradiente Crina -->
    <linearGradient id="logoMane" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#ff944d" />
      <stop offset="100%" stop-color="#c64600" />
    </linearGradient>

    <!-- Gradiente Azul Processo -->
    <linearGradient id="logoBlue" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#62a0ea" />
      <stop offset="100%" stop-color="#1c71d8" />
    </linearGradient>

    <!-- Gradiente do fundo do ícone em miniatura -->
    <linearGradient id="logoBadgeBg" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#2d1527" />
      <stop offset="50%" stop-color="#1e1e24" />
      <stop offset="100%" stop-color="#141416" />
    </linearGradient>

    <filter id="logoShadow" x="-10%" y="-10%" width="130%" height="130%">
      <feDropShadow dx="0" dy="5" stdDeviation="7" flood-color="#000000" flood-opacity="0.3" />
    </filter>
  </defs>

  <!-- Símbolo / Ícone à Esquerda (escala 0.38, centralizado em 110, 110) -->
  <g transform="translate(15, 15) scale(0.37)" filter="url(#logoShadow)">
    <!-- Base Squircle -->
    <rect x="36" y="36" width="440" height="440" rx="96" ry="96" fill="url(#logoBadgeBg)" />
    <rect x="36" y="36" width="440" height="440" rx="96" ry="96" fill="none" stroke="#ffffff" stroke-opacity="0.15" stroke-width="3" />

    <!-- Documento de Processos -->
    <g transform="translate(196, 76) rotate(6)">
      <rect x="0" y="0" width="206" height="280" rx="16" ry="16" fill="#ffffff" />
      <rect x="0" y="0" width="206" height="34" rx="16" ry="16" fill="url(#logoOrange)" />
      <rect x="63" y="-12" width="80" height="22" rx="7" ry="7" fill="#2d2d34" />
      <circle cx="103" cy="-1" r="4.5" fill="#ffffff" />

      <circle cx="32" cy="62" r="9" fill="url(#logoOrange)" />
      <rect x="52" y="58" width="118" height="8" rx="4" ry="4" fill="#deddda" />
      <circle cx="32" cy="119" r="9" fill="url(#logoBlue)" />
      <rect x="52" y="115" width="130" height="8" rx="4" ry="4" fill="#deddda" />
      <circle cx="32" cy="176" r="9" fill="#26a269" />
      <path d="M27 176 L30.5 179.5 L37 172.5" stroke="#ffffff" stroke-width="2.5" stroke-linecap="round" fill="none" />
      <rect x="52" y="172" width="105" height="8" rx="4" ry="4" fill="#deddda" />
    </g>

    <!-- Cavalo Go Horse -->
    <g>
      <path d="M 148 135 C 130 155, 102 180, 92 210 C 110 205, 128 200, 140 205 C 115 225, 96 255, 92 285 C 112 275, 132 270, 148 278 C 124 305, 110 345, 114 385 C 138 355, 166 335, 188 328 Z" fill="url(#logoMane)" />
      <path d="M 166 140 C 144 165, 118 195, 110 225 C 128 220, 146 215, 156 220 C 132 245, 116 275, 112 305 C 132 295, 152 290, 168 298 C 142 330, 130 370, 136 405 C 160 375, 186 355, 208 348 Z" fill="url(#logoOrange)" />

      <path d="
        M 175 125 
        C 185 105, 205 92, 218 92 
        C 222 92, 224 100, 220 115 
        C 235 110, 255 112, 275 128 
        C 298 148, 335 195, 348 230 
        C 355 248, 350 262, 332 268 
        C 315 274, 292 268, 278 255 
        L 272 268 
        C 255 295, 240 335, 245 425 
        L 155 425 
        C 152 380, 158 310, 172 250 
        C 162 230, 156 195, 162 165 
        Z" 
        fill="url(#logoOrange)" stroke="#ffffff" stroke-width="2.5" stroke-linejoin="round" />

      <ellipse cx="332" cy="248" rx="6" ry="9" transform="rotate(25 332 248)" fill="#5c1e00" />
      <polygon points="252,158 274,166 256,174" fill="#1e1e24" />
      <circle cx="260" cy="166" r="2.5" fill="#ffffff" />
      <path d="M 235 158 L 285 168" stroke="#1e1e24" stroke-width="3.5" stroke-linecap="round" />
      <rect x="244" y="152" width="36" height="25" rx="6" ry="6" fill="rgba(53, 132, 228, 0.4)" stroke="#ffffff" stroke-width="2.2" />

      <g transform="translate(250, 310) rotate(-35)">
        <path d="M 0 0 L 135 0 L 150 10 L 135 20 L 0 20 Z" fill="#ffffff" stroke="#2d2d34" stroke-width="2" />
        <path d="M 0 0 L 38 0 L 38 20 L 0 20 Z" fill="#3584e4" />
        <polygon points="150,10 172,10 162,15" fill="#e95420" />
      </g>
      <path d="M 135 435 C 195 458, 305 458, 375 418 C 412 395, 430 358, 430 315" fill="none" stroke="url(#logoOrange)" stroke-width="7" stroke-linecap="round" stroke-dasharray="14 7" />
      <polygon points="428,300 442,324 418,324" fill="#e95420" />
    </g>
  </g>

  <!-- Tipografia do Logotipo -->
  <g transform="translate(210, 0)">
    <!-- Título Principal -->
    <text x="0" y="105" font-family="Ubuntu, 'Noto Sans', 'Segoe UI', sans-serif" font-size="52" font-weight="900" letter-spacing="-1">
      <tspan fill="#2e3436">Go</tspan><tspan fill="#e95420">Horse</tspan><tspan fill="#2e3436">Documentador</tspan>
    </text>

    <!-- Linha Divisória de Estilo -->
    <rect x="0" y="124" width="560" height="3" rx="1.5" ry="1.5" fill="url(#logoOrange)" />

    <!-- Subtítulo Técnico e Badges de Funcionalidade -->
    <g transform="translate(0, 156)">
      <!-- Badge de Processos -->
      <rect x="0" y="-18" width="165" height="26" rx="6" ry="6" fill="#f0f2f5" stroke="#d5d8dc" stroke-width="1.2" />
      <circle cx="14" cy="-5" r="4.5" fill="#e95420" />
      <text x="26" y="-1" font-family="Ubuntu, 'Noto Sans', sans-serif" font-size="12" font-weight="700" fill="#2e3436" letter-spacing="0.5">MAPEAMENTO ERP</text>

      <!-- Badge de Captura Rápida -->
      <rect x="175" y="-18" width="155" height="26" rx="6" ry="6" fill="#f0f2f5" stroke="#d5d8dc" stroke-width="1.2" />
      <circle cx="189" cy="-5" r="4.5" fill="#3584e4" />
      <text x="201" y="-1" font-family="Ubuntu, 'Noto Sans', sans-serif" font-size="12" font-weight="700" fill="#2e3436" letter-spacing="0.5">AUTOCOLAR PRINTS</text>

      <!-- Badge Multi-formato -->
      <rect x="340" y="-18" width="170" height="26" rx="6" ry="6" fill="#f0f2f5" stroke="#d5d8dc" stroke-width="1.2" />
      <circle cx="354" cy="-5" r="4.5" fill="#26a269" />
      <text x="366" y="-1" font-family="Ubuntu, 'Noto Sans', sans-serif" font-size="12" font-weight="700" fill="#2e3436" letter-spacing="0.5">PDF • HTML • WIKI • SVG</text>
    </g>
  </g>
</svg>'''


def main():
    icone_svg_path = os.path.join(IMG_DIR, "icone.svg")
    icone_png_path = os.path.join(IMG_DIR, "icone.png")
    icone_ico_path = os.path.join(IMG_DIR, "icone.ico")
    root_icone_png = os.path.join(BASE_DIR, "icone.png")

    logo_svg_path = os.path.join(IMG_DIR, "logo.svg")
    logo_png_path = os.path.join(IMG_DIR, "logo.png")

    # 1. Salvar SVGs
    print("-> Gravando img/icone.svg...")
    with open(icone_svg_path, "w", encoding="utf-8") as f:
        f.write(ICONE_SVG)

    print("-> Gravando img/logo.svg...")
    with open(logo_svg_path, "w", encoding="utf-8") as f:
        f.write(LOGO_SVG)

    # 2. Renderizar PNGs via convert (ImageMagick)
    print("-> Renderizando img/icone.png (512x512)...")
    cmd_icon = ["convert", "-background", "none", "-density", "200", icone_svg_path, "-resize", "512x512", icone_png_path]
    subprocess.run(cmd_icon, check=True)

    print("-> Copiando icone.png para a raiz do repositório...")
    cmd_copy_root = ["cp", icone_png_path, root_icone_png]
    subprocess.run(cmd_copy_root, check=True)

    print("-> Renderizando img/logo.png (800x220)...")
    cmd_logo = ["convert", "-background", "none", "-density", "200", logo_svg_path, "-resize", "800x220", logo_png_path]
    subprocess.run(cmd_logo, check=True)

    # 3. Gerar img/icone.ico multi-resolução com Pillow
    print("-> Gerando img/icone.ico (16, 32, 48, 64, 128, 256)...")
    img_icon = Image.open(icone_png_path)
    img_icon.save(
        icone_ico_path,
        format="ICO",
        sizes=[(16, 16), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)]
    )

    print("Assets gerados com sucesso!")
    print(f"  - {icone_svg_path}")
    print(f"  - {icone_png_path} ({os.path.getsize(icone_png_path)} bytes)")
    print(f"  - {icone_ico_path} ({os.path.getsize(icone_ico_path)} bytes)")
    print(f"  - {logo_svg_path}")
    print(f"  - {logo_png_path} ({os.path.getsize(logo_png_path)} bytes)")
    print(f"  - {root_icone_png}")

if __name__ == "__main__":
    main()

