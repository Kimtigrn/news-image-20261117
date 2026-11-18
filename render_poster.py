#!/usr/bin/env python3
"""Render the news poster for Tuesday 17 November 2026.

Draws a 1024x1024 front-page style image with PIL and writes it to
entry.png next to this file. Fully deterministic: fixed layout, fixed
text, no timestamps, no randomness. Run:  python3 render_poster.py

The entry program (main.py) only copies the rendered entry.png to the
output directory; this script is the tool that produced the image, kept
in the repository so the image can be reproduced and checked.
"""

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024

PAPER = (246, 241, 231, 255)
INK = (26, 26, 26, 255)
NAVY = (31, 58, 95, 255)
RED = (179, 39, 30, 255)
GREY = (90, 86, 78, 255)
RULE = (26, 26, 26, 255)
SKY = (191, 211, 230, 255)
SEA = (47, 93, 124, 255)
SEA_DARK = (31, 68, 96, 255)
STEEL = (58, 68, 78, 255)

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, width):
    """Greedy word wrap; returns list of lines that fit in `width` px."""
    lines, cur = [], ""
    for word in text.split(" "):
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def para(draw, xy, text, fnt, width, fill, leading=None):
    """Draw wrapped paragraph; returns y just below the last line."""
    x, y = xy
    lh = leading or int(fnt.size * 1.28)
    for line in wrap(draw, text, fnt, width):
        draw.text((x, y), line, font=fnt, fill=fill)
        y += lh
    return y


def rule(draw, x0, x1, y, width=2, fill=RULE):
    draw.line([(x0, y), (x1, y)], fill=fill, width=width)


def draw_bridge(draw, x0, y0, w, h):
    """Flat illustration: a bridge over a strait with its middle span down."""
    # sky
    draw.rectangle([x0, y0, x0 + w, y0 + h], fill=SKY)
    # sun
    cx, cy, r = x0 + w - 52, y0 + 42, 26
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(240, 196, 90, 255))
    # sea
    sea_y = y0 + int(h * 0.62)
    draw.rectangle([x0, sea_y, x0 + w, y0 + h], fill=SEA)
    for i in range(4):
        wy = sea_y + 14 + i * 16
        draw.arc([x0 + 8, wy - 7, x0 + 60, wy + 7], 200, 340, fill=(255, 255, 255, 255), width=3)
        draw.arc([x0 + w - 68, wy - 7, x0 + w - 8, wy + 7], 200, 340, fill=(255, 255, 255, 255), width=3)
    # deck height and towers
    deck_y = y0 + int(h * 0.52)
    t1, t2 = x0 + int(w * 0.22), x0 + int(w * 0.74)
    # towers
    for tx in (t1, t2):
        draw.rectangle([tx - 7, deck_y - 92, tx + 7, deck_y], fill=STEEL)
        draw.rectangle([tx - 16, deck_y - 100, tx + 16, deck_y - 92], fill=STEEL)
    # cables
    for tx in (t1, t2):
        for k in range(1, 4):
            fx = tx - k * 26
            if fx > x0 + 4:
                draw.line([(tx, deck_y - 96), (fx, deck_y)], fill=STEEL, width=2)
            fx = tx + k * 26
            if fx < x0 + w - 4:
                draw.line([(tx, deck_y - 96), (fx, deck_y)], fill=STEEL, width=2)
    # deck: left and right spans stand, middle span has collapsed
    gap_l, gap_r = x0 + int(w * 0.40), x0 + int(w * 0.60)
    draw.rectangle([x0, deck_y - 8, gap_l, deck_y + 4], fill=INK)
    draw.rectangle([gap_r, deck_y - 8, x0 + w, deck_y + 4], fill=INK)
    # collapsed span: tilted slab dropping into the water
    draw.polygon(
        [(gap_l + 2, deck_y - 6), (gap_r - 2, deck_y - 6),
         (gap_r - 26, sea_y + 26), (gap_l + 26, sea_y + 26)],
        fill=(120, 30, 24, 255),
    )
    draw.line([(gap_l + 2, deck_y - 6), (gap_l + 26, sea_y + 26)], fill=INK, width=2)
    draw.line([(gap_r - 2, deck_y - 6), (gap_r - 26, sea_y + 26)], fill=INK, width=2)
    # smoke over the gap
    midx = (gap_l + gap_r) // 2
    for (sx, sy, sr, col) in (
        (midx - 18, deck_y - 34, 16, (120, 120, 118, 255)),
        (midx + 6, deck_y - 52, 20, (140, 140, 138, 255)),
        (midx + 26, deck_y - 30, 13, (105, 105, 103, 255)),
    ):
        draw.ellipse([sx - sr, sy - sr, sx + sr, sy + sr], fill=col)
    # splash where the span hit the water
    for (sx, sy) in ((midx - 22, sea_y + 30), (midx + 18, sea_y + 34)):
        draw.arc([sx - 14, sy - 8, sx + 14, sy + 8], 180, 360, fill=(255, 255, 255, 255), width=3)


def icon_tanker(draw, x, y, s):
    """Oil tanker on waves, with a small blast star."""
    # hull
    draw.polygon([(x, y + s * 0.55), (x + s, y + s * 0.55),
                  (x + s * 0.88, y + s * 0.85), (x + s * 0.12, y + s * 0.85)],
                 fill=(58, 68, 78, 255))
    # deck + containers
    draw.rectangle([x + s * 0.10, y + s * 0.32, x + s * 0.38, y + s * 0.55], fill=(179, 39, 30, 255))
    draw.rectangle([x + s * 0.44, y + s * 0.38, x + s * 0.66, y + s * 0.55], fill=(240, 196, 90, 255))
    draw.rectangle([x + s * 0.72, y + s * 0.18, x + s * 0.86, y + s * 0.55], fill=(246, 241, 231, 255),
                   outline=(26, 26, 26, 255), width=2)
    # blast star
    bx, by = x + s * 0.55, y + s * 0.10
    draw.polygon([(bx, by - 10), (bx + 4, by - 3), (bx + 11, by - 3), (bx + 6, by + 2),
                  (bx + 8, by + 9), (bx, by + 5), (bx - 8, by + 9), (bx - 6, by + 2),
                  (bx - 11, by - 3), (bx - 4, by - 3)], fill=(230, 120, 20, 255))
    # waves
    for wy in (y + s * 0.92,):
        draw.arc([x, wy - 5, x + s * 0.5, wy + 5], 180, 360, fill=(47, 93, 124, 255), width=3)
        draw.arc([x + s * 0.5, wy - 5, x + s, wy + 5], 180, 360, fill=(47, 93, 124, 255), width=3)


def icon_flags(draw, x, y, s):
    """Three flagpoles."""
    cols = [(179, 39, 30, 255), (31, 58, 95, 255), (240, 196, 90, 255)]
    for i, col in enumerate(cols):
        px = x + s * (0.18 + i * 0.30)
        draw.line([(px, y + s * 0.08), (px, y + s * 0.88)], fill=(26, 26, 26, 255), width=3)
        draw.polygon([(px, y + s * 0.08), (px + s * 0.26, y + s * 0.16),
                      (px, y + s * 0.26)], fill=col)


def icon_pentagon(draw, x, y, s):
    """Pentagon outline with a red cross (failed audit)."""
    import math
    cx, cy, r = x + s / 2, y + s * 0.46, s * 0.36
    pts = []
    for i in range(5):
        a = -math.pi / 2 + i * 2 * math.pi / 5
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    draw.polygon(pts, outline=(31, 58, 95, 255), width=4)
    draw.line([(cx - 12, cy - 12), (cx + 12, cy + 12)], fill=(179, 39, 30, 255), width=5)
    draw.line([(cx - 12, cy + 12), (cx + 12, cy - 12)], fill=(179, 39, 30, 255), width=5)


def icon_sanction(draw, x, y, s):
    """A building under a prohibition circle."""
    draw.rectangle([x + s * 0.18, y + s * 0.30, x + s * 0.82, y + s * 0.88],
                   fill=(31, 58, 95, 255))
    for i in range(3):
        for j in range(2):
            draw.rectangle([x + s * (0.26 + i * 0.20), y + s * (0.40 + j * 0.20),
                            x + s * (0.38 + i * 0.20), y + s * (0.52 + j * 0.20)],
                           fill=(246, 241, 231, 255))
    cx, cy, r = x + s / 2, y + s * 0.48, s * 0.44
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], outline=(179, 39, 30, 255), width=5)
    draw.line([(cx - r * 0.72, cy + r * 0.72), (cx + r * 0.72, cy - r * 0.72)],
              fill=(179, 39, 30, 255), width=5)


def icon_jet(draw, x, y, s):
    """Fighter jet silhouette over a rising sun."""
    draw.ellipse([x + s * 0.58, y + s * 0.06, x + s * 0.98, y + s * 0.46],
                 fill=(230, 120, 20, 255))
    # fuselage + wings, pointing up-right
    draw.polygon([(x + s * 0.10, y + s * 0.78), (x + s * 0.72, y + s * 0.30),
                  (x + s * 0.82, y + s * 0.38), (x + s * 0.30, y + s * 0.88)],
                 fill=(58, 68, 78, 255))
    draw.polygon([(x + s * 0.34, y + s * 0.62), (x + s * 0.62, y + s * 0.60),
                  (x + s * 0.48, y + s * 0.86)], fill=(58, 68, 78, 255))
    draw.polygon([(x + s * 0.40, y + s * 0.56), (x + s * 0.66, y + s * 0.34),
                  (x + s * 0.80, y + s * 0.52)], fill=(58, 68, 78, 255))


ICONS = {
    "tanker": icon_tanker,
    "flags": icon_flags,
    "pentagon": icon_pentagon,
    "sanction": icon_sanction,
    "jet": icon_jet,
}

LEAD = {
    "kicker": "UKRAINE  ·  WAR IN EUROPE",
    "headline": "Kerch Bridge hit, span collapses",
    "deck": ("Ukraine calls its strike on the bridge to occupied Crimea "
             "\u201can unprecedented operation\u201d. Russia answered with "
             "missiles on Kyiv\u2019s bridges."),
}

STORIES = [
    {"icon": "tanker", "kicker": "IRAN  ·  THE GULF",
     "headline": "Iran fires drones at a US radar base in Bahrain",
     "body": ("Bahrain says the drones were intercepted, with no casualties. "
              "Iran also says tankers struck mines near Hormuz.")},
    {"icon": "flags", "kicker": "CHINA  ·  DIPLOMACY",
     "headline": "Xi, Trump and Putin to meet in Shenzhen",
     "body": ("China confirms the first three-way summit, on Thursday on the "
              "APEC sidelines. Trump is in Manila.")},
    {"icon": "pentagon", "kicker": "UNITED STATES",
     "headline": "Pentagon fails its ninth audit in a row",
     "body": ("Auditors could not verify accounts covering $4.8 trillion in "
              "assets \u2014 though 14 of 25 Pentagon units passed for the first time.")},
    {"icon": "sanction", "kicker": "BRITAIN  ·  WEST BANK",
     "headline": "UK sanctions firms building settlements",
     "body": ("London blacklists eight Israeli construction companies working "
              "in the occupied West Bank, and a group it says blocks aid to Gaza.")},
    {"icon": "jet", "kicker": "JAPAN",
     "headline": "Jets scrambled as Russian planes enter airspace",
     "body": ("Tokyo says two suspected Russian aircraft violated Japanese "
              "airspace early in the morning and protests \u201cstrongly\u201d.")},
]


def story_cell(draw, x, y, w, h, story):
    """One grid cell: icon top-right, kicker, headline, body."""
    icon = ICONS[story["icon"]]
    icon(draw, x + w - 44, y, 44)
    draw.text((x, y + 8), story["kicker"], font=font(SANS_B, 17), fill=RED)
    hy = y + 50
    hy = para(draw, (x, hy), story["headline"], font(SERIF_B, 26), w, INK,
              leading=31)
    para(draw, (x, hy + 6), story["body"], font(SANS, 18), w, (52, 52, 52, 255),
         leading=23)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    draw = ImageDraw.Draw(img)

    # frame
    draw.rectangle([10, 10, W - 11, H - 11], outline=INK, width=4)
    draw.rectangle([18, 18, W - 19, H - 19], outline=INK, width=1)

    # ---- masthead ----
    title = "THE WORLD IN ONE DAY"
    tf = font(SERIF_B, 60)
    tw = draw.textlength(title, font=tf)
    draw.text(((W - tw) / 2, 34), title, font=tf, fill=INK)
    rule(draw, 40, W - 40, 118, width=3)
    date = "TUESDAY,  17 NOVEMBER 2026"
    df = font(SANS_B, 30)
    dw = draw.textlength(date, font=df)
    draw.text(((W - dw) / 2, 130), date, font=df, fill=RED)
    sub = "SIX STORIES THAT DEFINED THE DAY  ·  FROM THE WORLD'S NEWS WIRES"
    sf = font(SANS, 18)
    sw = draw.textlength(sub, font=sf)
    draw.text(((W - sw) / 2, 168), sub, font=sf, fill=GREY)
    rule(draw, 40, W - 40, 198, width=2)

    # ---- lead story ----
    lx, lw = 40, 560
    ly = 216
    draw.text((lx, ly), LEAD["kicker"], font=font(SANS_B, 20), fill=RED)
    hy = para(draw, (lx, ly + 34), LEAD["headline"], font(SERIF_B, 44), lw, INK,
              leading=52)
    para(draw, (lx, hy + 10), LEAD["deck"], font(SANS, 22), lw,
         (52, 52, 52, 255), leading=29)

    # lead illustration, right of the text
    ix, iy, iw, ih = 632, 216, 352, 218
    draw_bridge(draw, ix, iy, iw, ih)
    draw.rectangle([ix, iy, ix + iw, iy + ih], outline=INK, width=2)
    cap = "The Kerch Bridge to occupied Crimea."
    cf = font(SANS, 15)
    cw = draw.textlength(cap, font=cf)
    draw.text((ix + (iw - cw) / 2, iy + ih + 8), cap, font=cf, fill=GREY)

    rule(draw, 40, W - 40, 466, width=2)

    # ---- grid of five stories: 3 on top, 2 below ----
    top_y, top_h = 482, 244
    cols3 = [40, 362, 684]
    col_w3 = 300
    for i in range(3):
        story_cell(draw, cols3[i], top_y, col_w3, top_h, STORIES[i])
        if i < 2:
            draw.line([(cols3[i] + col_w3 + 11, top_y + 4),
                       (cols3[i] + col_w3 + 11, top_y + top_h - 8)],
                      fill=(190, 185, 172, 255), width=1)

    rule(draw, 40, W - 40, 740, width=1, fill=(190, 185, 172, 255))

    bot_y = 758
    cols2 = [40, 522]
    col_w2 = 462
    for i in range(2):
        story_cell(draw, cols2[i], bot_y, col_w2, 200, STORIES[3 + i])
        if i == 0:
            draw.line([(cols2[0] + col_w2 + 10, bot_y + 4),
                       (cols2[0] + col_w2 + 10, bot_y + 192)],
                      fill=(190, 185, 172, 255), width=1)

    # ---- footer ----
    rule(draw, 40, W - 40, 972, width=2)
    foot = ("As reported on 17 November 2026 by BBC  ·  Reuters  ·  Al Jazeera  ·  "
            "AP  ·  The Hill")
    ff = font(SANS, 16)
    fw = draw.textlength(foot, font=ff)
    draw.text(((W - fw) / 2, 980), foot, font=ff, fill=GREY)

    img.save("entry.png", format="PNG", optimize=True)
    print("wrote entry.png")


if __name__ == "__main__":
    main()
