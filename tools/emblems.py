"""Astrocorp emblems for the Discord notifications: one round badge per division, SVG then PNG.

    python tools/emblems.py     -> svg/<division>.svg, discord/<division>.png (256 px)

Night sky of the homelab portal (dark teal, stars, amber Milky Way core), a ring in the division
accent, a white glyph. Rendered to PNG by headless Chrome (CHROME to override its path): Discord
does not show SVG avatars.
"""
import os
import pathlib
import random
import subprocess

from PIL import Image

ROOT = pathlib.Path(__file__).resolve().parent.parent
CHROME = os.environ.get("CHROME", r"C:\Program Files\Google\Chrome\Application\chrome.exe")
SIZE = 512

DIVISIONS = {
    # slug: (name, accent, glyph)
    "astrocorp": ("Astrocorp", "#e0a458", "seal"),
    "astrops": ("AstrOps", "#4fd1c5", "observatory"),
    "astro-security": ("Astro Security", "#a78bfa", "shield"),
    "astro-forge": ("Astro Forge", "#e0a458", "rocket"),
    "astro-core": ("Astro Core", "#60a5fa", "planet"),
    "astro-update": ("Astro Update", "#4ade80", "comet"),
}

W = 'fill="none" stroke="#f4f7f8" stroke-linecap="round" stroke-linejoin="round"'
GLYPHS = {
    # Observatory: an orbit around a planet, a satellite on it
    "observatory": f'''<ellipse cx="256" cy="256" rx="150" ry="62" transform="rotate(-24 256 256)" {W} stroke-width="16"/>
      <circle cx="256" cy="256" r="58" fill="#f4f7f8"/>
      <circle cx="384" cy="196" r="20" fill="{{accent}}" stroke="#f4f7f8" stroke-width="8"/>''',
    # Shield with a four-pointed star
    "shield": f'''<path d="M256 108 L370 150 V250 C370 330 318 382 256 410 C194 382 142 330 142 250 V150 Z" {W} stroke-width="18"/>
      <path d="M256 186 L272 240 L326 256 L272 272 L256 326 L240 272 L186 256 L240 240 Z" fill="#f4f7f8"/>''',
    # Rocket
    "rocket": f'''<path d="M256 104 C306 150 326 214 318 300 L194 300 C186 214 206 150 256 104 Z" {W} stroke-width="16"/>
      <circle cx="256" cy="204" r="26" fill="{{accent}}" stroke="#f4f7f8" stroke-width="8"/>
      <path d="M194 262 L150 318 L194 312 M318 262 L362 318 L318 312" {W} stroke-width="14"/>
      <path d="M226 318 C232 352 244 372 256 392 C268 372 280 352 286 318" fill="{{accent}}" stroke="#f4f7f8" stroke-width="8" stroke-linejoin="round"/>''',
    # Ringed planet
    "planet": f'''<circle cx="256" cy="256" r="84" fill="#f4f7f8"/>
      <path d="M150 300 C112 330 104 356 128 366 C170 384 288 344 372 278 C416 244 430 214 410 202 C394 192 362 198 330 210" {W} stroke-width="16"/>
      <path d="M214 228 C238 214 266 212 290 222" fill="none" stroke="{{accent}}" stroke-width="10" stroke-linecap="round"/>''',
    # Comet going up: head and trail
    "comet": f'''<path d="M150 380 L322 208" {W} stroke-width="14" opacity=".55"/>
      <path d="M186 392 L330 248" {W} stroke-width="10" opacity=".35"/>
      <path d="M138 344 L286 196" {W} stroke-width="10" opacity=".35"/>
      <circle cx="338" cy="190" r="46" fill="#f4f7f8"/>
      <path d="M338 166 V214 M314 190 L338 166 L362 190" fill="none" stroke="{{accent}}" stroke-width="12" stroke-linecap="round" stroke-linejoin="round"/>''',
    # Astrocorp seal: an A circled by an orbit, a star above it
    "seal": f'''<path d="M170 380 L256 132 L342 380" {W} stroke-width="22"/>
      <ellipse cx="256" cy="300" rx="132" ry="34" transform="rotate(-12 256 300)" fill="none" stroke="{{accent}}" stroke-width="12"/>
      <path d="M256 70 L266 104 L300 114 L266 124 L256 158 L246 124 L212 114 L246 104 Z" fill="#f4f7f8"/>''',
}


def stars(seed):
    """Stars inside the disc, the same for a division at every run."""
    rng = random.Random(seed)
    out = []
    for _ in range(70):
        x, y = rng.uniform(40, 472), rng.uniform(40, 472)
        if (x - 256) ** 2 + (y - 256) ** 2 > 205 ** 2:
            continue
        r = rng.choice([1.1, 1.4, 1.8, 2.4])
        out.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r}" fill="#ffffff" opacity="{rng.uniform(.35, .95):.2f}"/>')
    return "".join(out)


def svg(slug, accent, glyph):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{SIZE}" height="{SIZE}" viewBox="0 0 512 512">
  <defs>
    <radialGradient id="sky" cx="42%" cy="38%" r="70%">
      <stop offset="0" stop-color="#123842"/><stop offset=".55" stop-color="#071a20"/><stop offset="1" stop-color="#02080b"/>
    </radialGradient>
    <radialGradient id="core" cx="64%" cy="66%" r="38%">
      <stop offset="0" stop-color="#e0a458" stop-opacity=".55"/><stop offset=".5" stop-color="#b8743a" stop-opacity=".18"/><stop offset="1" stop-color="#b8743a" stop-opacity="0"/>
    </radialGradient>
    <clipPath id="disc"><circle cx="256" cy="256" r="232"/></clipPath>
  </defs>
  <circle cx="256" cy="256" r="248" fill="{accent}"/>
  <circle cx="256" cy="256" r="232" fill="url(#sky)"/>
  <g clip-path="url(#disc)"><ellipse cx="300" cy="320" rx="260" ry="90" transform="rotate(-32 300 320)" fill="url(#core)"/>{stars(slug)}</g>
  <circle cx="256" cy="256" r="232" fill="none" stroke="#02080b" stroke-width="6" opacity=".6"/>
  {GLYPHS[glyph].replace("{accent}", accent)}
</svg>
'''


def main():
    for slug, (name, accent, glyph) in DIVISIONS.items():
        drawing = svg(slug, accent, glyph)
        (ROOT / "svg" / f"{slug}.svg").write_text(drawing, encoding="utf-8", newline="\n")
        page = ROOT / "discord" / f"{slug}.html"
        page.write_text(f'<html><body style="margin:0;background:transparent">{drawing}</body></html>', encoding="utf-8")
        big = ROOT / "discord" / f"{slug}-512.png"
        subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars", "--default-background-color=00000000",
                        f"--window-size={SIZE},{SIZE}", f"--screenshot={big}", page.as_uri()], check=True, capture_output=True)
        page.unlink()
        # Discord shows avatars at 40 px and author icons at 24 px: 256 px is plenty
        Image.open(big).convert("RGBA").resize((256, 256), Image.LANCZOS).save(ROOT / "discord" / f"{slug}.png", optimize=True)
        big.unlink()
        print(f"{name}: discord/{slug}.png")


if __name__ == "__main__":
    main()
