#!/usr/bin/env python3
"""Draw a broadsheet front page summing up Saturday 21 November 2026's
world news and write it to /output/entry.png (or $MAKEFUN_OUTPUT_DIR).

Pure Pillow, standard library only, no network, no randomness: two runs
write identical bytes.
"""
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (248, 244, 233)   # off-white newsprint
INK = (26, 26, 26)
RED = (164, 30, 34)       # kicker / rule red
NAVY = (31, 58, 95)       # sea blue
SEA = (46, 84, 130)
STEEL = (58, 66, 76)
TICKER_BG = (32, 36, 42)
TICKER_FG = (240, 236, 224)
GREY = (90, 86, 76)

FONTS = "/usr/share/fonts/truetype/dejavu"


def font(name, size):
    return ImageFont.truetype(os.path.join(FONTS, name), size)


F_MAST = font("DejaVuSerif-Bold.ttf", 66)
F_DATE = font("DejaVuSans-Bold.ttf", 24)
F_TAG = font("DejaVuSans.ttf", 16)
F_KICK = font("DejaVuSans-Bold.ttf", 16)
F_HEAD = font("DejaVuSans-Bold.ttf", 34)
F_HEAD2 = font("DejaVuSans-Bold.ttf", 26)
F_HEAD3 = font("DejaVuSans-Bold.ttf", 24)
F_BODY = font("DejaVuSans.ttf", 18)
F_BODY2 = font("DejaVuSans.ttf", 17)
F_TICK = font("DejaVuSans-Bold.ttf", 15)


def wrap(text, fnt, max_w):
    """Wrap text to lines no wider than max_w pixels."""
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if fnt.getlength(trial) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_wrapped(d, x, y, lines, fnt, fill, leading):
    for line in lines:
        d.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def kicker_head_body(d, x, y, w, kick, head, body, head_font=F_HEAD2,
                     body_font=F_BODY2, head_leading=32, body_leading=24):
    d.text((x, y), kick, font=F_KICK, fill=RED)
    y += 26
    y = draw_wrapped(d, x, y, wrap(head, head_font, w), head_font, INK,
                     head_leading)
    y += 6
    y = draw_wrapped(d, x, y, wrap(body, body_font, w), body_font, INK,
                     body_leading)
    return y


def panel_rule(d, x, y, w):
    d.line([(x, y), (x + w, y)], fill=INK, width=2)


def draw_sea_scene(d, x, y, w, h):
    """Simple geometric Strait of Hormuz scene: sea, two tankers, a drone
    and a dashed missile arc. No flags, no text inside the scene."""
    d.rectangle([x, y, x + w, y + h], fill=SEA)
    # horizon shimmer
    for i in range(0, w, 46):
        d.line([(x + i, y + 14), (x + i + 22, y + 14)], fill=(120, 160, 200),
               width=2)
    # tanker 1 (left)
    hx, hy = x + 24, y + h - 58
    d.rectangle([hx, hy, hx + 190, hy + 34], fill=(30, 34, 40))
    d.polygon([(hx + 190, hy), (hx + 214, hy + 14), (hx + 190, hy + 34)],
              fill=(30, 34, 40))
    for i, col in enumerate([(164, 30, 34), (200, 160, 60), (60, 120, 90)]):
        d.rectangle([hx + 14 + i * 52, hy - 22, hx + 52 + i * 52, hy - 2],
                    fill=col)
    d.rectangle([hx + 168, hy - 30, hx + 182, hy - 2], fill=(220, 220, 210))
    # tanker 2 (right, smaller)
    hx2, hy2 = x + w - 210, y + h - 50
    d.rectangle([hx2, hy2, hx2 + 150, hy2 + 28], fill=(24, 28, 34))
    d.polygon([(hx2 + 150, hy2), (hx2 + 170, hy2 + 12), (hx2 + 150, hy2 + 28)],
              fill=(24, 28, 34))
    for i, col in enumerate([(200, 160, 60), (164, 30, 34)]):
        d.rectangle([hx2 + 12 + i * 46, hy2 - 18, hx2 + 46 + i * 46, hy2 - 2],
                    fill=col)
    # drone above the sea (quad-rotor)
    dx, dy = x + w // 2 - 12, y + 14
    d.rectangle([dx, dy + 6, dx + 24, dy + 14], fill=(20, 22, 26))
    d.line([(dx - 10, dy + 4), (dx + 34, dy + 4)], fill=(20, 22, 26), width=3)
    d.line([(dx - 10, dy + 16), (dx + 34, dy + 16)], fill=(20, 22, 26),
           width=3)
    d.ellipse([dx - 14, dy, dx - 4, dy + 8], outline=(20, 22, 26), width=2)
    d.ellipse([dx + 28, dy, dx + 38, dy + 8], outline=(20, 22, 26), width=2)
    d.ellipse([dx - 14, dy + 12, dx - 4, dy + 20], outline=(20, 22, 26),
              width=2)
    d.ellipse([dx + 28, dy + 12, dx + 38, dy + 20], outline=(20, 22, 26),
              width=2)
    # mine-strike starburst above the right tanker
    sx, sy = x + w - 120, y + 42
    for ang in range(0, 360, 45):
        import math
        r1, r2 = 6, 20
        a = math.radians(ang)
        d.line([(sx + r1 * math.cos(a), sy + r1 * math.sin(a)),
                (sx + r2 * math.cos(a), sy + r2 * math.sin(a))],
               fill=(255, 190, 60), width=3)
    d.ellipse([sx - 5, sy - 5, sx + 5, sy + 5], fill=(255, 120, 40))
    d.text((x + w - 118, y + 6), "HORMUZ", font=F_KICK, fill=(255, 255, 255))


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    # outer frame
    d.rectangle([14, 14, W - 15, H - 15], outline=INK, width=3)

    # ---- masthead ----
    title = "THE WORLD"
    tw = d.textlength(title, font=F_MAST)
    d.text(((W - tw) / 2, 30), title, font=F_MAST, fill=INK)
    d.line([(28, 118), (W - 28, 118)], fill=INK, width=2)
    d.line([(28, 122), (W - 28, 122)], fill=INK, width=1)
    date = "Saturday 21 November 2026"
    dw = d.textlength(date, font=F_DATE)
    d.text(((W - dw) / 2, 132), date, font=F_DATE, fill=RED)
    tag = "The world's news, in one picture"
    gw = d.textlength(tag, font=F_TAG)
    d.text(((W - gw) / 2, 164), tag, font=F_TAG, fill=GREY)

    # ---- lead story (left) ----
    lx, ly, lw = 28, 196, 632
    d.text((lx, ly), "STRAIT OF HORMUZ", font=F_KICK, fill=RED)
    y = ly + 26
    y = draw_wrapped(d, lx, y, wrap("War in the Strait of Hormuz", F_HEAD, lw),
                     F_HEAD, INK, 40)
    y += 4
    y = draw_wrapped(
        d, lx, y,
        wrap("Iran downs a US drone over Hormuz. Two tankers are attacked "
             "off Oman and one strikes a naval mine. Three missiles are "
             "downed over Riyadh and 41 are killed in Yemen airstrikes.",
             F_BODY, lw),
        F_BODY, INK, 25)
    draw_sea_scene(d, lx, y + 10, lw, 128)
    panel_rule(d, lx, 516, lw)

    # ---- right column, two stories ----
    rx, rw = 688, 308
    y = 196
    y = kicker_head_body(
        d, rx, y, rw, "RUSSIA - UKRAINE", "Missiles land in Poland",
        "400 drones, 110 missiles hit Ukraine overnight. Two land in "
        "Poland; Tusk calls it a deliberate provocation.",
        head_font=F_HEAD3, head_leading=29, body_leading=22)
    d.line([(rx, y + 10), (rx + rw, y + 10)], fill=GREY, width=1)
    y += 22
    kicker_head_body(
        d, rx, y, rw, "UNITED NATIONS", "'Killer robot' rules off to 2028",
        "Geneva talks end with a two-year extension, no binding deal.",
        head_font=F_HEAD3, head_leading=29, body_leading=22)

    # ---- second row: two panels ----
    y0 = 532
    c1, c2, cw = 28, 520, 476
    panel_rule(d, c1, y0, cw)
    panel_rule(d, c2, y0, cw)
    kicker_head_body(
        d, c1, y0 + 14, cw, "CLIMATE - COP31", "Talks run past deadline",
        "Antalya negotiations go into overtime. No fossil-fuel deal in "
        "the draft.")
    kicker_head_body(
        d, c2, y0 + 14, cw, "EUROPEAN UNION", "Brussels proposes Big Tech tax",
        "A levy on the world's biggest digital firms is put forward.")

    # ---- third row: two panels ----
    y0 = 700
    panel_rule(d, c1, y0, cw)
    panel_rule(d, c2, y0, cw)
    kicker_head_body(
        d, c1, y0 + 14, cw, "SPORT - CRICKET", "India 486/4, lead 118",
        "Day 3 of the 1st Test against New Zealand.")
    kicker_head_body(
        d, c2, y0 + 14, cw, "BANGLADESH", "Armed Forces Day marked",
        "PM Tarique Rahman honours the heroes of 1971.")

    # ---- ticker (two lines) ----
    ty = 884
    d.rectangle([28, ty, W - 28, ty + 82], fill=TICKER_BG)
    ticker_lines = [
        "HORMUZ: tanker hits mine   •   RIYADH: 3 missiles downed   •   "
        "YEMEN: 41 killed in strikes",
        "COX'S BAZAR: train crash kills 4   •   GENEVA: robot rules off "
        "to 2028",
    ]
    ty_line = ty + 16
    for line in ticker_lines:
        lw = d.textlength(line, font=F_TICK)
        d.text((28 + (W - 56 - lw) / 2, ty_line), line, font=F_TICK,
               fill=TICKER_FG)
        ty_line += 26

    outdir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(outdir, exist_ok=True)
    img.save(os.path.join(outdir, "entry.png"))


if __name__ == "__main__":
    main()
