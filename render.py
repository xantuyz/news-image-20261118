#!/usr/bin/env python3
"""Render the world news of Wednesday 18 November 2026 as a one-page
newspaper front page, 1024x1024 PNG.

Pure PIL: flat vector-style spot illustrations drawn with polygons and
arcs, all copy set in DejaVu. Run: python3 render.py
Writes entry.png next to this script.

Stories (all reported on 18 Nov 2026, verified against Reuters /
Al Jazeera / CNBC coverage that morning):
  1. Trump meets Marcos Jr. in Manila, then flies to Shenzhen for
     APEC and a trilateral with Xi Jinping and Vladimir Putin.
  2. US-Iran exchanges in the Gulf: Iranian drones target a US radar
     in Bahrain, the US hits a site on Qeshm, Kuwait intercepts drones.
  3. Nvidia posts a record $115.8bn quarter; its board rules out
     Jensen Huang's return as CEO.
  4. Canada and China extend trade deals as Xi meets Carney before APEC.
  5. Cyclone Akvan strengthens over the Bay of Bengal.
  6. The US loses its measles-elimination status amid the worst
     outbreak since 1991.
"""
import os

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")

# --- palette -------------------------------------------------------------
PAPER = (248, 244, 236)
INK = (24, 24, 24)
ACCENT = (164, 50, 38)        # brick red
MUTED = (110, 104, 94)
RULE = (203, 195, 178)
SKY = (214, 230, 236)
SEA = (44, 96, 124)
SEA_DK = (28, 66, 88)
SAND = (232, 214, 178)
LEAF = (46, 120, 70)
CHIP = (18, 110, 62)
GOLD = (198, 148, 44)
CLOUD = (255, 255, 255)

FONT_DIR = "/usr/share/fonts/truetype/dejavu/"


def _font(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


def serif_b(size):
    return _font("DejaVuSerif-Bold.ttf", size)


def sans_b(size):
    return _font("DejaVuSans-Bold.ttf", size)


def sans(size):
    return _font("DejaVuSans.ttf", size)


def sans_i(size):
    # No oblique face ships with DejaVuSans here; plain sans reads the same.
    return _font("DejaVuSans.ttf", size)


canvas = Image.new("RGB", (W, H), PAPER)
pen = ImageDraw.Draw(canvas)

MARGIN = 36
CW = W - 2 * MARGIN  # 952 usable


def width_of(text, fnt):
    return pen.textlength(text, font=fnt)


def split_lines(text, fnt, max_w):
    """Greedy wrap; returns a list of lines that fit max_w."""
    out, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if pen.textlength(trial, font=fnt) <= max_w or not cur:
            cur = trial
        else:
            out.append(cur)
            cur = word
    if cur:
        out.append(cur)
    return out


def block(x, y, text, fnt, max_w, leading, color=INK):
    """Draw a wrapped paragraph; return y below the last line."""
    for line in split_lines(text, fnt, max_w):
        pen.text((x, y), line, font=fnt, fill=color)
        y += leading
    return y


def headline(x, y, lines, size, leading=None):
    """Draw headline lines (list of strings) in bold sans."""
    fnt = sans_b(size)
    step = leading or int(size * 1.08)
    for line in lines:
        pen.text((x, y), line, font=fnt, fill=INK)
        y += step
    return y


def kicker(x, y, text, size=18):
    pen.text((x, y), text.upper(), font=sans_b(size), fill=ACCENT)
    return y + size + 8


def rule(y, x0=MARGIN, x1=W - MARGIN, color=INK, w=2):
    pen.line([(x0, y), (x1, y)], fill=color, width=w)
    return y


def vrule(x, y0, y1, color=RULE, w=1):
    pen.line([(x, y0), (x, y1)], fill=color, width=w)


# --- spot illustrations (flat, no text inside) ---------------------------

def art_plane(x, y, w, h):
    """Jet on final approach over Manila Bay at dusk."""
    pen.rectangle([x, y, x + w, y + h], fill=SKY)
    pen.ellipse([x + w - 78, y + 12, x + w - 18, y + 72], fill=(250, 205, 110))
    # distant skyline
    base = y + h - 46
    for bx, bw, bh in [(8, 34, 52), (48, 26, 78), (80, 40, 44), (126, 30, 66),
                       (162, 36, 40), (204, 28, 58), (238, 34, 46)]:
        pen.rectangle([x + bx, base - bh, x + bx + bw, base], fill=(150, 172, 186))
    # sea
    pen.rectangle([x, base, x + w, y + h], fill=SEA)
    pen.line([(x, base), (x + w, base)], fill=SEA_DK, width=2)
    # jet: fuselage, tail, wing, windows
    jx, jy = x + 52, y + 58
    pen.polygon([(jx, jy + 14), (jx + 150, jy + 2), (jx + 196, jy + 10),
                 (jx + 150, jy + 22), (jx, jy + 26)], fill=(250, 250, 250))
    pen.polygon([(jx + 8, jy + 12), (jx + 34, jy - 22), (jx + 52, jy - 20),
                 (jx + 44, jy + 12)], fill=ACCENT)
    pen.polygon([(jx + 78, jy + 24), (jx + 108, jy + 52), (jx + 126, jy + 50),
                 (jx + 112, jy + 22)], fill=(210, 210, 210))
    for i in range(5):
        pen.ellipse([jx + 62 + i * 16, jy + 8, jx + 70 + i * 16, jy + 14],
                    fill=SEA_DK)
    # runway lights
    for i in range(6):
        pen.ellipse([x + 14 + i * 46, y + h - 14, x + 22 + i * 46, y + h - 6],
                    fill=GOLD)
    # clouds
    for cx, cy, cw in [(20, 18, 74), (150, 30, 58), (230, 12, 66)]:
        pen.ellipse([x + cx, y + cy, x + cx + cw, y + cy + 20], fill=CLOUD)


def art_radar(x, y, w, h):
    """Radar dish sweeping under drone silhouettes, Gulf at night."""
    pen.rectangle([x, y, x + w, y + h], fill=(26, 34, 48))
    for i in range(3):
        pen.ellipse([x + 14 + i * 8, y + 12 + i * 8, x + w - 14 - i * 8,
                     y + h - 40 - i * 8], outline=(90, 140, 120), width=2)
    # dish
    cx, cy = x + w // 2, y + h - 52
    pen.pieslice([cx - 46, cy - 46, cx + 46, cy + 46], 180, 360, fill=SEA)
    pen.line([(cx, cy), (cx + 40, cy - 40)], fill=GOLD, width=3)
    pen.rectangle([cx - 4, cy, cx + 4, y + h - 8], fill=(140, 140, 140))
    pen.rectangle([cx - 26, y + h - 10, cx + 26, y + h - 4], fill=(90, 90, 90))
    # drones: small quadcopters with blinking lights
    for dx, dy, s in [(18, 22, 10), (w - 58, 30, 12), (w // 2 - 30, 12, 9)]:
        pen.line([(x + dx, y + dy + s // 2), (x + dx + s, y + dy + s // 2)],
                 fill=(220, 220, 220), width=2)
        pen.line([(x + dx + s // 2, y + dy), (x + dx + s // 2, y + dy + s)],
                 fill=(220, 220, 220), width=2)
        pen.ellipse([x + dx + s // 2 - 2, y + dy + s // 2 - 2,
                     x + dx + s // 2 + 2, y + dy + s // 2 + 2], fill=ACCENT)
    # sea line
    pen.rectangle([x, y + h - 22, x + w, y + h], fill=(16, 50, 70))


def art_chip(x, y, w, h):
    """AI chip with circuit traces and a rising bar chart."""
    pen.rectangle([x, y, x + w, y + h], fill=(232, 240, 236))
    # circuit traces
    for tx, ty, tl in [(12, 22, 46), (12, 52, 30), (12, 82, 52),
                       (w - 58, 30, 40), (w - 42, 66, 30)]:
        pen.line([(x + tx, y + ty), (x + tx + tl, y + ty)], fill=(120, 160, 130),
                 width=2)
        pen.ellipse([x + tx + tl - 3, y + ty - 3, x + tx + tl + 3, y + ty + 3],
                    fill=CHIP)
    # chip body
    bx, by, bw, bh = x + w // 2 - 52, y + 34, 104, 84
    for px in range(bx - 16, bx + bw + 16, 18):
        pen.line([(px, by - 12), (px, by)], fill=(120, 120, 120), width=3)
        pen.line([(px, by + bh), (px, by + bh + 12)], fill=(120, 120, 120),
                 width=3)
    pen.rectangle([bx, by, bx + bw, by + bh], fill=CHIP)
    pen.rectangle([bx + 14, by + 14, bx + bw - 14, by + bh - 14],
                  outline=(200, 230, 205), width=2)
    pen.text((bx + 30, by + 30), "AI", font=sans_b(30), fill=(255, 255, 255))
    # rising bars at the bottom
    base = y + h - 12
    for i, bh2 in enumerate([14, 22, 18, 30]):
        pen.rectangle([x + 16 + i * 22, base - bh2, x + 32 + i * 22, base],
                      fill=GOLD)


def art_flags(x, y, w, h):
    """Canadian and Chinese flags flying side by side."""
    pen.rectangle([x, y, x + w, y + h], fill=SKY)
    pen.rectangle([x, y + h - 26, x + w, y + h], fill=LEAF)
    # poles
    pen.line([(x + 34, y + 14), (x + 34, y + h - 26)], fill=(90, 90, 90), width=3)
    pen.line([(x + w - 34, y + 14), (x + w - 34, y + h - 26)], fill=(90, 90, 90),
             width=3)
    # Canada: red-white-red with maple leaf
    pen.rectangle([x + 38, y + 16, x + w // 2 - 6, y + 62], fill=(255, 255, 255))
    pen.rectangle([x + 38, y + 16, x + 46, y + 62], fill=ACCENT)
    pen.rectangle([x + w // 2 - 14, y + 16, x + w // 2 - 6, y + 62], fill=ACCENT)
    cx, cy = x + (38 + w // 2 - 6) // 2, y + 39
    pen.polygon([(cx, cy - 12), (cx + 4, cy - 4), (cx + 11, cy - 6),
                 (cx + 7, cy + 1), (cx + 12, cy + 5), (cx + 4, cy + 5),
                 (cx + 3, cy + 12), (cx - 3, cy + 12), (cx - 4, cy + 5),
                 (cx - 12, cy + 5), (cx - 7, cy + 1), (cx - 11, cy - 6),
                 (cx - 4, cy - 4)], fill=ACCENT)
    # China: red field, gold stars
    pen.rectangle([x + w // 2 + 6, y + 16, x + w - 38, y + 62], fill=(206, 32, 28))
    sx, sy = x + w // 2 + 22, y + 30
    pen.polygon([(sx, sy - 8), (sx + 2, sy - 2), (sx + 8, sy - 2),
                 (sx + 3, sy + 2), (sx + 5, sy + 8), (sx, sy + 4),
                 (sx - 5, sy + 8), (sx - 3, sy + 2), (sx - 8, sy - 2),
                 (sx - 2, sy - 2)], fill=GOLD)
    for sxx, syy in [(sx + 22, sy + 2), (sx + 28, sy + 10), (sx + 22, sy + 18),
                     (sx + 12, sy + 22)]:
        pen.ellipse([sxx - 2, syy - 2, sxx + 2, syy + 2], fill=GOLD)


def art_cyclone(x, y, w, h):
    """Cyclone spiral over a dark sea."""
    pen.rectangle([x, y, x + w, y + h], fill=(30, 48, 66))
    pen.rectangle([x, y + h - 30, x + w, y + h], fill=SEA)
    cx, cy = x + w // 2, y + h // 2 - 6
    for r, col in [(52, (220, 225, 230)), (40, (170, 190, 200)),
                   (28, (130, 160, 175)), (16, (240, 240, 240))]:
        pen.arc([cx - r, cy - r, cx + r, cy + r], 20, 330, fill=col, width=7)
    pen.ellipse([cx - 7, cy - 7, cx + 7, cy + 7], fill=(250, 250, 250))
    # rain streaks
    for rx in range(10, w - 10, 18):
        pen.line([(x + rx, y + h - 26), (x + rx - 5, y + h - 12)],
                 fill=(140, 170, 190), width=2)


def art_shield(x, y, w, h):
    """A cracked shield: measles-elimination status lost."""
    pen.rectangle([x, y, x + w, y + h], fill=(238, 232, 222))
    cx = x + w // 2
    pen.polygon([(cx - 52, y + 12), (cx + 52, y + 12), (cx + 52, y + 62),
                 (cx, y + h - 14), (cx - 52, y + 62)], fill=(58, 96, 140))
    pen.polygon([(cx - 40, y + 22), (cx + 40, y + 22), (cx + 40, y + 58),
                 (cx, y + h - 26), (cx - 40, y + 58)], outline=(255, 255, 255),
                width=3)
    # crack through the shield
    pen.line([(cx + 6, y + 18), (cx - 4, y + 44), (cx + 8, y + 62),
              (cx - 2, y + 84)], fill=(255, 255, 255), width=3)
    # virus dots
    for vx, vy, vr in [(x + 18, y + 22, 5), (x + w - 22, y + 30, 6),
                       (x + 24, y + h - 26, 4), (x + w - 18, y + h - 20, 5)]:
        pen.ellipse([vx - vr, vy - vr, vx + vr, vy + vr], fill=ACCENT)


# --- page layout ----------------------------------------------------------

# masthead
title = "THE WORLD TODAY"
tf = serif_b(60)
pen.text(((W - width_of(title, tf)) / 2, 22), title, font=tf, fill=INK)
pen.rectangle([MARGIN, 100, W - MARGIN, 104], fill=ACCENT)
rule(110, color=INK, w=1)
dateline = "WEDNESDAY 18 NOVEMBER 2026  ·  THE WORLD IN ONE PAGE"
df = sans_b(20)
pen.text(((W - width_of(dateline, df)) / 2, 120), dateline, font=df, fill=INK)
rule(150, color=RULE, w=1)

# --- lead story: Trump meets Marcos, flies to Shenzhen --------------------
ly = 166
kicker(MARGIN, ly, "Manila · Diplomacy")
hy = headline(MARGIN, ly + 30, ["TRUMP MEETS", "MARCOS IN MANILA"], 46)
art_plane(MARGIN + 560, ly + 26, 392, 210)
block(MARGIN, hy + 4,
      "The US president meets Ferdinand Marcos Jr. for a bilateral and "
      "state luncheon on Wednesday, then flies to Shenzhen for APEC and "
      "a much-anticipated trilateral with Xi Jinping and Vladimir Putin.",
      sans(21), 520, 27)
rule(ly + 258, color=RULE, w=1)

# --- middle row: Gulf + Nvidia ------------------------------------------
my = ly + 276
col_w = (CW - 24) // 2
# left: Gulf
kicker(MARGIN, my, "Gulf · US–Iran")
headline(MARGIN, my + 28, ["GULF ON EDGE"], 30)
block(MARGIN, my + 66,
      "Iranian drones target a US radar in Bahrain; the US hits a missile "
      "site on Qeshm island, and Kuwait's defences intercept drones.",
      sans(19), col_w - 150, 24)
art_radar(MARGIN + col_w - 148, my + 62, 148, 128)
# right: Nvidia
rx = MARGIN + col_w + 24
vrule(rx - 12, my, my + 216)
kicker(rx, my, "Business · Tech")
headline(rx, my + 28, ["NVIDIA'S $115.8BN", "RECORD QUARTER"], 30)
block(rx, my + 100,
      "Revenue doubles in its first results without Jensen Huang — and the "
      "board says the ousted chief will not return.",
      sans(19), col_w - 150, 24)
art_chip(rx + col_w - 148, my + 96, 148, 128)
rule(my + 232, color=RULE, w=1)

# --- bottom row: three short stories ------------------------------------
by = my + 238
bw = (CW - 48) // 3
bx1, bx2, bx3 = MARGIN, MARGIN + bw + 24, MARGIN + 2 * bw + 48

kicker(bx1, by, "Trade · APEC", 16)
headline(bx1, by + 26, ["CANADA–CHINA", "EXTEND TRADE", "DEALS"], 24, 27)
block(bx1, by + 112,
      "Xi meets Carney as the two sides widen trade cooperation ahead of "
      "the APEC summit.",
      sans(18), bw, 23)
art_flags(bx1, by + 196, bw, 84)

vrule(bx2 - 12, by, by + 292)
kicker(bx2, by, "Weather · Asia", 16)
headline(bx2, by + 26, ["CYCLONE AKVAN", "BEARS DOWN"], 24, 27)
block(bx2, by + 84,
      "The Bay of Bengal storm strengthens toward severe-cyclone force.",
      sans(18), bw, 23)
art_cyclone(bx2, by + 172, bw, 108)

vrule(bx3 - 12, by, by + 292)
kicker(bx3, by, "Health · USA", 16)
headline(bx3, by + 26, ["US LOSES", "MEASLES-FREE", "STATUS"], 24, 27)
block(bx3, by + 112,
      "The country loses its elimination status amid the worst outbreak "
      "since 1991.",
      sans(18), bw, 23)
art_shield(bx3, by + 196, bw, 84)

# --- footer ---------------------------------------------------------------
rule(by + 292, color=INK, w=2)
foot = "Wednesday 18 November 2026 — the day's world news in one page."
ff = sans_i(17)
pen.text(((W - width_of(foot, ff)) / 2, by + 300), foot, font=ff, fill=MUTED)

if __name__ == "__main__":
    canvas.save(OUT, "PNG")
    print("wrote", OUT, os.path.getsize(OUT), "bytes")
