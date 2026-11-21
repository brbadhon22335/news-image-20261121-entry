"""The World -- Saturday 21 November 2026.

A broadsheet front page drawn with Pillow: standard library plus Pillow
only, no network, no randomness, no system fonts. The program writes
/output/entry.png (or $MAKEFUN_OUTPUT_DIR/entry.png), a 1024x1024 PNG
summing up the world's news of Saturday 21 November 2026.

Fonts: Pillow's bundled default font only (ImageFont.load_default), so the
program runs the same in any container that has Pillow. No font files are
read from the system and none are shipped in the repository.
"""

import os

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (248, 244, 232)
PANEL = (253, 251, 243)
INK = (28, 28, 28)
SOFT = (90, 84, 70)
RED = (185, 28, 28)
RULE = (190, 182, 160)
NAVY = (28, 30, 46)
SKY = (205, 226, 240)
SEA = (46, 95, 138)
SEA_DARK = (32, 70, 104)
HULL = (31, 41, 55)
DECK = (226, 232, 240)
BURST = (245, 158, 11)
BURST_RED = (220, 68, 48)

_fonts = {}


def font(size):
    """Pillow's bundled font at the given size, with a plain fallback."""
    if size not in _fonts:
        try:
            _fonts[size] = ImageFont.load_default(size=size)
        except TypeError:
            _fonts[size] = ImageFont.load_default()
    return _fonts[size]


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap of text to lines no wider than max_w."""
    lines = []
    cur = ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if not cur or draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_tracked(draw, cx, y, text, fnt, fill, tracking):
    """Draw text centred on cx with extra tracking between letters."""
    widths = [draw.textlength(ch, font=fnt) for ch in text]
    total = sum(widths) + tracking * max(0, len(text) - 1)
    x = cx - total / 2.0
    for ch, cw in zip(text, widths):
        draw.text((x, y), ch, font=fnt, fill=fill)
        x += cw + tracking


def draw_centered(draw, cx, y, text, fnt, fill):
    draw.text((cx, y), text, font=fnt, fill=fill, anchor="ma")


def rule(draw, x0, x1, y, fill=RULE, width=1):
    draw.line([(x0, y), (x1, y)], fill=fill, width=width)


def draw_masthead(draw):
    draw_tracked(draw, W / 2, 20, "THE WORLD", font(76), INK, 16)
    rule(draw, 36, 988, 102, INK, 2)
    rule(draw, 36, 988, 107, INK, 1)
    date = "SATURDAY 21 NOVEMBER 2026"
    df = font(20)
    dw = draw.textlength(date, font=df)
    mid = 116 + 10
    rule(draw, 36, 512 - dw / 2 - 18, mid, RULE, 1)
    rule(draw, 512 + dw / 2 + 18, 988, mid, RULE, 1)
    draw_centered(draw, 512, 116, date, df, RED)
    rule(draw, 36, 988, 150, INK, 1)


def draw_sea_scene(draw, x0, y0, x1, y1):
    """A simple geometric sea scene: two tankers, a drone, a mine strike."""
    draw.rectangle([x0, y0, x1, y1], fill=SKY, outline=RULE, width=1)
    horizon = y0 + 88
    draw.rectangle([x0, horizon, x1, y1], fill=SEA)
    draw.line([(x0, horizon), (x1, horizon)], fill=SEA_DARK, width=2)
    # waves
    for wy in (horizon + 34, horizon + 62, horizon + 92):
        for wx in range(x0 + 12, x1 - 30, 46):
            draw.arc([wx, wy, wx + 30, wy + 10], 180, 360, fill=(150, 190, 220), width=2)
    # far tanker (right, smaller)
    fx0, fy0 = x1 - 128, horizon + 6
    draw.rectangle([fx0, fy0, fx0 + 104, fy0 + 20], fill=HULL)
    draw.rectangle([fx0 + 58, fy0 - 14, fx0 + 88, fy0], fill=DECK)
    draw.rectangle([fx0 + 70, fy0 - 24, fx0 + 76, fy0 - 14], fill=HULL)
    # near tanker (left, larger)
    nx0, ny0 = x0 + 22, horizon + 26
    draw.rectangle([nx0, ny0, nx0 + 168, ny0 + 30], fill=HULL)
    draw.rectangle([nx0 + 12, ny0 - 20, nx0 + 52, ny0], fill=DECK)
    draw.rectangle([nx0 + 96, ny0 - 14, nx0 + 148, ny0], fill=DECK)
    draw.rectangle([nx0 + 120, ny0 - 30, nx0 + 128, ny0 - 14], fill=HULL)
    # mine-strike starburst at the near tanker's bow
    bx, by = nx0 + 168, ny0 + 8
    for ang in range(0, 360, 30):
        import math
        r = 26 if ang % 60 == 0 else 15
        ex = bx + r * math.cos(math.radians(ang))
        ey = by + r * math.sin(math.radians(ang))
        draw.line([(bx, by), (ex, ey)], fill=BURST, width=3)
    draw.ellipse([bx - 12, by - 12, bx + 12, by + 12], fill=BURST_RED)
    draw.ellipse([bx - 6, by - 6, bx + 6, by + 6], fill=(255, 220, 120))
    # quad-rotor drone in the sky
    dx, dy = x0 + 218, y0 + 34
    draw.line([(dx - 26, dy - 10), (dx + 26, dy + 10)], fill=INK, width=3)
    draw.line([(dx - 26, dy + 10), (dx + 26, dy - 10)], fill=INK, width=3)
    for cx, cy in ((dx - 26, dy - 10), (dx + 26, dy + 10),
                   (dx - 26, dy + 10), (dx + 26, dy - 10)):
        draw.ellipse([cx - 8, cy - 3, cx + 8, cy + 3], outline=INK, width=2)
    draw.rectangle([dx - 9, dy - 6, dx + 9, dy + 6], fill=INK)


def draw_lead(draw):
    x0, y0, x1, y1 = 36, 160, 988, 424
    draw.rectangle([x0, y0, x1, y1], fill=PANEL, outline=RULE, width=1)
    tx = 60
    draw.text((tx, 182), "MIDDLE EAST", font=font(16), fill=RED)
    draw.text((tx, 206), "War in the Strait of Hormuz", font=font(34), fill=INK)
    body = ("Iran downs a US drone over the strait; two tankers are "
            "attacked off Oman and one strikes a naval mine. Three "
            "missiles are downed over Riyadh; 41 are killed in Yemen "
            "airstrikes.")
    y = 258
    for line in wrap(draw, body, font(18), 540):
        draw.text((tx, y), line, font=font(18), fill=INK)
        y += 27
    draw_sea_scene(draw, 636, 182, 964, 402)


PANELS = [
    ("RUSSIA-UKRAINE", "Missiles land in Poland",
     "400 drones, 110 missiles hit Ukraine overnight; two land in "
     "Poland. Tusk calls it a provocation."),
    ("UNITED NATIONS", "'Killer robot' rules off to 2028",
     "Geneva talks end with a two-year extension and no binding deal "
     "on autonomous weapons."),
    ("CLIMATE", "COP31 talks run past deadline",
     "Antalya negotiations go into overtime with no fossil-fuel deal "
     "in the draft text."),
    ("EUROPEAN UNION", "Brussels proposes Big Tech tax",
     "A levy on the world's biggest digital firms is put forward in "
     "Brussels."),
    ("CRICKET", "India 486/4, lead 118",
     "Day three of the first Test against New Zealand."),
    ("BANGLADESH", "Armed Forces Day marked",
     "PM Tarique Rahman honours the heroes of 1971."),
]

TICKER = ("TANKER HITS MINE IN HORMUZ  |  3 MISSILES DOWNED OVER "
          "RIYADH  |  41 KILLED IN YEMEN  |  TRAIN CRASH KILLS 4 "
          "IN COX'S BAZAR  |  ROBOT RULES OFF TO 2028")


def draw_panel(draw, x0, y0, x1, y1, kicker, headline, body):
    draw.rectangle([x0, y0, x1, y1], fill=PANEL, outline=RULE, width=1)
    tx = x0 + 18
    draw.text((tx, y0 + 14), kicker, font=font(16), fill=RED)
    draw.text((tx, y0 + 36), headline, font=font(26), fill=INK)
    y = y0 + 68
    for line in wrap(draw, body, font(17), x1 - x0 - 36):
        draw.text((tx, y), line, font=font(17), fill=INK)
        y += 23


def draw_grid(draw):
    top = 440
    row_h, gap = 134, 12
    col_w = 468
    for i, (kicker, headline, body) in enumerate(PANELS):
        col = i % 2
        row = i // 2
        x0 = 36 + col * (col_w + 16)
        y0 = top + row * (row_h + gap)
        draw_panel(draw, x0, y0, x0 + col_w, y0 + row_h,
                   kicker, headline, body)


def draw_ticker(draw):
    x0, y0, x1, y1 = 36, 882, 988, 962
    draw.rectangle([x0, y0, x1, y1], fill=NAVY)
    fnt = font(15)
    lines = wrap(draw, TICKER, fnt, x1 - x0 - 32)
    total = len(lines) * 24
    y = y0 + (y1 - y0 - total) / 2 + 4
    for line in lines:
        draw_centered(draw, 512, y, line, fnt, (245, 244, 232))
        y += 24


def draw_footer(draw):
    draw_centered(draw, 512, 976,
                  "All stories reported on Saturday 21 November 2026",
                  font(13), SOFT)


def main():
    outdir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(outdir, exist_ok=True)
    img = Image.new("RGB", (W, H), PAPER)
    draw = ImageDraw.Draw(img)
    draw_masthead(draw)
    draw_lead(draw)
    draw_grid(draw)
    draw_ticker(draw)
    draw_footer(draw)
    img.save(os.path.join(outdir, "entry.png"))


if __name__ == "__main__":
    main()
