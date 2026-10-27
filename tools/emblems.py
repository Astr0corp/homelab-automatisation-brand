"""Astrocorp emblems for the Discord notifications: one round badge per division.

    python tools/emblems.py     -> svg/<division>.svg, discord/<division>.png (256 px, still),
                                   discord/<division>.gif (160 px, animated loop)

Night sky of the homelab portal (dark teal, twinkling stars, amber Milky Way core), a ring in the
division accent, a white glyph that moves. Rendered by headless Chrome (CHROME to override its
path): every frame of a loop is drawn on one page, then cut and assembled. Discord shows neither
SVG nor animated avatars: the still PNG is the avatar, the GIF the card thumbnail.
"""
import math
import os
import pathlib
import random
import subprocess

from PIL import Image

ROOT = pathlib.Path(__file__).resolve().parent.parent
CHROME = os.environ.get("CHROME", r"C:\Program Files\Google\Chrome\Application\chrome.exe")
SIZE = 512
FRAMES, FRAME_MS, GIF_SIZE = 30, 70, 160

DIVISIONS = {
    # slug: (name, accent, glyph)
    "astrocorp": ("Astrocorp", "#e0a458", "seal"),
    "astrops": ("AstrOps", "#4fd1c5", "observatory"),
    "astro-security": ("Astro Security", "#a78bfa", "shield"),
    "astro-forge": ("Astro Forge", "#e0a458", "rocket"),
    "astro-core": ("Astro Core", "#60a5fa", "planet"),
    "astro-update": ("Astro Update", "#4ade80", "comet"),
    "jarvis": ("Jarvis", "#fbbf24", "sunrise"),
}

W = 'fill="none" stroke="#f4f7f8" stroke-linecap="round" stroke-linejoin="round"'
TAU = 2 * math.pi


def wave(t, phase=0.0):
    """0..1 then back, once per loop."""
    return 0.5 - 0.5 * math.cos(TAU * (t + phase))


# Glyphs: functions of the loop position t in [0, 1); t = 0 is the still emblem
def observatory(a, t):
    # Satellite on the orbit; behind the planet on the far half of the ellipse
    ang = TAU * t - 0.6
    x, y = 150 * math.cos(ang), 62 * math.sin(ang)
    r = math.radians(-24)
    sx, sy = 256 + x * math.cos(r) - y * math.sin(r), 256 + x * math.sin(r) + y * math.cos(r)
    sat = f'<circle cx="{sx:.1f}" cy="{sy:.1f}" r="20" fill="{a}" stroke="#f4f7f8" stroke-width="8"/>'
    behind = math.sin(ang) < 0
    orbit = f'<ellipse cx="256" cy="256" rx="150" ry="62" transform="rotate(-24 256 256)" {W} stroke-width="16"/>'
    planet = '<circle cx="256" cy="256" r="58" fill="#f4f7f8"/>'
    return orbit + (sat + planet if behind else planet + sat)


def shield(a, t):
    s = 1 + 0.12 * wave(t)
    shine_x = -160 + 520 * t
    return f'''<defs><clipPath id="sh"><path d="M256 108 L370 150 V250 C370 330 318 382 256 410 C194 382 142 330 142 250 V150 Z"/></clipPath></defs>
      <g clip-path="url(#sh)"><rect x="{shine_x:.1f}" y="60" width="46" height="420" fill="{a}" opacity=".35" transform="rotate(24 256 256)"/></g>
      <path d="M256 108 L370 150 V250 C370 330 318 382 256 410 C194 382 142 330 142 250 V150 Z" {W} stroke-width="18"/>
      <g transform="translate(256 256) scale({s:.3f}) translate(-256 -256)"><path d="M256 186 L272 240 L326 256 L272 272 L256 326 L240 272 L186 256 L240 240 Z" fill="#f4f7f8"/></g>'''


def rocket(a, t):
    dy = -8 * math.sin(TAU * t)
    f = 1 + 0.25 * math.sin(TAU * 3 * t) * 0.8
    return f'''<g transform="translate(0 {dy:.1f})">
      <path d="M226 318 C232 {318 + 34 * f:.1f} 244 {318 + 54 * f:.1f} 256 {318 + 74 * f:.1f} C268 {318 + 54 * f:.1f} 280 {318 + 34 * f:.1f} 286 318" fill="{a}" stroke="#f4f7f8" stroke-width="8" stroke-linejoin="round"/>
      <path d="M256 104 C306 150 326 214 318 300 L194 300 C186 214 206 150 256 104 Z" fill="#071a20" {W.replace('fill="none" ', '')} stroke-width="16"/>
      <circle cx="256" cy="204" r="26" fill="{a}" stroke="#f4f7f8" stroke-width="8"/>
      <path d="M194 262 L150 318 L194 312 M318 262 L362 318 L318 312" {W} stroke-width="14"/></g>'''


def planet(a, t):
    ang = TAU * t
    mx, my = 256 + 170 * math.cos(ang), 256 + 54 * math.sin(ang) - 40
    moon = f'<circle cx="{mx:.1f}" cy="{my:.1f}" r="14" fill="{a}" stroke="#f4f7f8" stroke-width="6"/>'
    body = f'''<circle cx="256" cy="256" r="84" fill="#f4f7f8"/>
      <path d="M150 300 C112 330 104 356 128 366 C170 384 288 344 372 278 C416 244 430 214 410 202 C394 192 362 198 330 210" {W} stroke-width="16"/>
      <path d="M214 228 C238 214 266 212 290 222" fill="none" stroke="{a}" stroke-width="10" stroke-linecap="round"/>'''
    return (moon + body) if math.sin(ang) < 0 else (body + moon)


def comet(a, t):
    # The comet travels up the diagonal and comes back from the corner, trails flickering
    k = (t * 1.0) % 1.0
    off = -60 + 120 * k
    head = f'<circle cx="{338 + off:.1f}" cy="{190 - off:.1f}" r="46" fill="#f4f7f8"/>'
    arrow = f'<path d="M{338 + off:.1f} {166 - off:.1f} V{214 - off:.1f} M{314 + off:.1f} {190 - off:.1f} L{338 + off:.1f} {166 - off:.1f} L{362 + off:.1f} {190 - off:.1f}" fill="none" stroke="{a}" stroke-width="12" stroke-linecap="round" stroke-linejoin="round"/>'
    trails = "".join(
        f'<path d="M{x1 + off:.1f} {y1 - off:.1f} L{x2 + off:.1f} {y2 - off:.1f}" {W} stroke-width="{w}" opacity="{o * (0.6 + 0.4 * wave(t, p)):.2f}"/>'
        for (x1, y1, x2, y2, w, o, p) in [(150, 380, 322, 208, 14, .55, 0), (186, 392, 330, 248, 10, .35, .3), (138, 344, 286, 196, 10, .35, .6)])
    fade = min(1.0, 4 * min(k, 1 - k) + 0.15)
    return f'<g opacity="{fade:.2f}">{trails}{head}{arrow}</g>'


def seal(a, t):
    s = 1 + 0.18 * wave(t)
    rot = -12 + 8 * math.sin(TAU * t)
    return f'''<path d="M170 380 L256 132 L342 380" {W} stroke-width="22"/>
      <ellipse cx="256" cy="300" rx="132" ry="34" transform="rotate({rot:.1f} 256 300)" fill="none" stroke="{a}" stroke-width="12" stroke-dasharray="60 18" stroke-dashoffset="{-78 * t * 4:.1f}"/>
      <g transform="translate(256 114) scale({s:.3f}) rotate({45 * t:.1f}) translate(-256 -114)"><path d="M256 70 L266 104 L300 114 L266 124 L256 158 L246 124 L212 114 L246 104 Z" fill="#f4f7f8"/></g>'''


def sunrise(a, t):
    s = 1 + 0.06 * wave(t)
    rays = "".join(
        f'<path d="M256 {262 - 92 - 10 * wave(t, i / 7):.1f} V{262 - 120 - 10 * wave(t, i / 7):.1f}" {W} stroke-width="14" transform="rotate({ang} 256 262)"/>'
        for i, ang in enumerate(range(-90, 91, 30)))
    return f'''<g transform="rotate({12 * math.sin(TAU * t):.1f} 256 262)">{rays}</g>
      <g transform="translate(256 262) scale({s:.3f}) translate(-256 -262)"><circle cx="256" cy="262" r="64" fill="{a}"/></g>
      <g clip-path="url(#disc)"><circle cx="256" cy="610" r="300" fill="#071a20" stroke="#f4f7f8" stroke-width="14"/>
      <path d="M120 360 C200 336 312 336 392 360" fill="none" stroke="{a}" stroke-width="8" stroke-linecap="round" opacity="{.4 + .4 * wave(t):.2f}"/></g>'''


GLYPHS = {"observatory": observatory, "shield": shield, "rocket": rocket, "planet": planet,
          "comet": comet, "seal": seal, "sunrise": sunrise}
# Moment of the loop drawn for the still emblem (the comet is fading out at t = 0)
STILL = {"comet": 0.5}


def stars(seed, t):
    """Stars inside the disc, the same for a division at every run, twinkling over the loop."""
    rng = random.Random(seed)
    out = []
    for _ in range(70):
        x, y = rng.uniform(40, 472), rng.uniform(40, 472)
        r, base, phase = rng.choice([1.1, 1.4, 1.8, 2.4]), rng.uniform(.35, .95), rng.random()
        if (x - 256) ** 2 + (y - 256) ** 2 > 205 ** 2:
            continue
        o = base * (0.45 + 0.55 * wave(t, phase)) if t is not None else base
        out.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r}" fill="#ffffff" opacity="{o:.2f}"/>')
    return "".join(out)


def svg(slug, accent, glyph, t=None, size=SIZE):
    tt = STILL.get(glyph, 0.0) if t is None else t
    glow = 1.0 if t is None else 0.85 + 0.15 * wave(t)
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 512 512">
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
  <g clip-path="url(#disc)"><ellipse cx="300" cy="320" rx="260" ry="90" transform="rotate(-32 300 320)" fill="url(#core)" opacity="{glow:.2f}"/>{stars(slug, t)}</g>
  <circle cx="256" cy="256" r="232" fill="none" stroke="#02080b" stroke-width="6" opacity=".6"/>
  {GLYPHS[glyph](accent, tt)}
</svg>
'''


def chrome(page: pathlib.Path, shot: pathlib.Path, width: int, height: int):
    subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars", "--default-background-color=00000000",
                    f"--window-size={width},{height}", f"--screenshot={shot}", page.as_uri()], check=True, capture_output=True)


def main():
    work = ROOT / "discord"
    for slug, (name, accent, glyph) in DIVISIONS.items():
        drawing = svg(slug, accent, glyph)
        (ROOT / "svg" / f"{slug}.svg").write_text(drawing, encoding="utf-8", newline="\n")
        # Still emblem (avatar)
        page, shot = work / f"{slug}.html", work / f"{slug}-shot.png"
        page.write_text(f'<html><body style="margin:0;background:transparent">{drawing}</body></html>', encoding="utf-8")
        chrome(page, shot, SIZE, SIZE)
        Image.open(shot).convert("RGBA").resize((256, 256), Image.LANCZOS).save(work / f"{slug}.png", optimize=True)
        # Animated loop: every frame on one page (a column), one screenshot, then cut
        size = GIF_SIZE * 2
        frames_svg = "".join(f'<div style="height:{size}px">{svg(slug, accent, glyph, i / FRAMES, size)}</div>' for i in range(FRAMES))
        page.write_text(f'<html><body style="margin:0;background:transparent">{frames_svg}</body></html>', encoding="utf-8")
        chrome(page, shot, size, size * FRAMES)
        sheet = Image.open(shot).convert("RGBA")
        frames = [sheet.crop((0, i * size, size, (i + 1) * size)).resize((GIF_SIZE, GIF_SIZE), Image.LANCZOS) for i in range(FRAMES)]
        frames[0].save(work / f"{slug}.gif", save_all=True, append_images=frames[1:], duration=FRAME_MS, loop=0,
                       disposal=2, optimize=True)
        page.unlink()
        shot.unlink()
        print(f"{name}: discord/{slug}.png, discord/{slug}.gif ({(work / f'{slug}.gif').stat().st_size // 1024} Ko)")


if __name__ == "__main__":
    main()
