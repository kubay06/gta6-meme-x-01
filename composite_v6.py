#!/usr/bin/env python3
"""Composite v6 for the main Bonnie & Clyde meme.

Changes vs v5 (per Bayu, round 6 — V5 with V1 outfits):
- Base image regenerated: Jason now in the olive-green tank top and
  Lucia in the pink long-sleeve top + black vest + fingerless gloves
  of v1, same poses, same muted cinematic grade (no v1 neon).
- Bubbles + ghost IDENTICAL to v5: Jason white incoming
  "AGENT GOT PAID." 09:12 (left), Lucia green outgoing
  "CANCEL THE HEIST." 09:13 + blue double-check (right), XS 56px,
  corner tails; real press-kit ghost at (150, 310) d=280.
"""
from PIL import Image, ImageDraw, ImageFont, ImageFilter

BASE = "/home/hatch/workspace/makefun/gta6-meme-x-01/assets"
OUT = "/home/hatch/workspace/makefun/gta6-meme-x-01"
GHOST = f"{BASE}/mark-1024.png"
FONT_BOLD = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
FONT_REG = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"
FONT_CHECK = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SRC = "/home/hatch/workspace/makefun/gta6-meme-x-01/assets/media-generation-base-main-v6-v1-outfits-0-77ac6b3a-fd2a-4f1f-8f0e-62e455b0b01b.png"

FONT_SIZE = 56   # XS main caption (as v3/v4)
TIME_SIZE = 34   # timestamp / checks (~0.6x caption, WA proportion)
WA_GREEN = (220, 248, 198)      # #dcf8c6 outgoing
WA_WHITE = (255, 255, 255)      # incoming
WA_TEXT = (17, 27, 33)          # #111b21
WA_TIME_GRAY = (102, 119, 129)  # #667781 incoming time
WA_TIME_GREEN = (84, 101, 111)  # #54656f outgoing time
WA_BLUE_TICK = (83, 189, 235)   # #53bdeb read double-check

ghost_src = Image.open(GHOST).convert("RGBA")


def paste_ghost(img, cx, cy, diameter):
    g = ghost_src.resize((diameter, diameter), Image.LANCZOS)
    r, gg, b, a = g.split()
    a = a.filter(ImageFilter.GaussianBlur(1.2))
    g = Image.merge("RGBA", (r, gg, b, a))
    shadow = Image.new("RGBA", img.size, (0, 0, 0, 0))
    sd = ImageDraw.Draw(shadow)
    sd.ellipse([cx - diameter // 2 + 8, cy - diameter // 2 + 12,
                cx + diameter // 2 + 8, cy + diameter // 2 + 12],
               fill=(0, 0, 0, 90))
    shadow = shadow.filter(ImageFilter.GaussianBlur(16))
    img.alpha_composite(shadow)
    img.alpha_composite(g, (cx - diameter // 2, cy - diameter // 2))


def corner_tail_polygon(x0, x1, y1, side):
    """WhatsApp corner tail: a small triangle hugging the bottom
    corner of the bubble, pointing down. side 'left' -> bottom-left
    corner (incoming), 'right' -> bottom-right (outgoing)."""
    if side == "left":
        return [(x0 + 4, y1 - 4), (x0 + 54, y1 - 4), (x0 + 4, y1 + 32)]
    return [(x1 - 54, y1 - 4), (x1 - 4, y1 - 4), (x1 - 4, y1 + 32)]


def draw_bubble(img, text, time_str, tail_side, top_y, center_x, fill,
                time_color, with_ticks):
    """WhatsApp bubble: rounded body, corner tail, caption + inline
    timestamp (and blue double-check for outgoing) on one baseline."""
    f = ImageFont.truetype(FONT_BOLD, FONT_SIZE)
    ft = ImageFont.truetype(FONT_REG, TIME_SIZE)
    fc = ImageFont.truetype(FONT_CHECK, TIME_SIZE)
    tw = int(f.getlength(text))
    time_w = int(ft.getlength(time_str))
    tick_w = int(fc.getlength("\u2713\u2713")) if with_ticks else 0
    gap = 20
    tick_gap = 10 if with_ticks else 0
    pad_x, pad_y = 38, 22
    bw = tw + gap + time_w + tick_gap + tick_w + pad_x * 2
    asc, desc = f.getmetrics()
    bh = asc + desc + pad_y * 2
    x0 = max(16, min(center_x - bw // 2, img.width - bw - 16))
    y0, y1 = top_y, top_y + bh
    x1 = x0 + bw
    radius = 24
    tail = corner_tail_polygon(x0, x1, y1, tail_side)
    # soft drop shadow (bubble + tail silhouette, blurred)
    sh = Image.new("RGBA", img.size, (0, 0, 0, 0))
    ds = ImageDraw.Draw(sh)
    ds.polygon(tail, fill=(0, 0, 0, 90))
    ds.rounded_rectangle([x0, y0, x1, y1], radius=radius,
                         fill=(0, 0, 0, 90))
    sh = sh.filter(ImageFilter.GaussianBlur(12))
    img.alpha_composite(sh)
    # bubble body + tail (same fill so the tail blends in)
    layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    d.polygon(tail, fill=fill + (255,))
    d.rounded_rectangle([x0, y0, x1, y1], radius=radius,
                        fill=fill + (255,))
    img.alpha_composite(layer)
    # caption + timestamp + ticks on one shared baseline
    d2 = ImageDraw.Draw(img)
    baseline = y0 + pad_y + asc
    tx = x0 + pad_x
    d2.text((tx, baseline), text, font=f, fill=WA_TEXT, anchor="ls")
    txx = tx + tw + gap
    d2.text((txx, baseline), time_str, font=ft, fill=time_color,
            anchor="ls")
    if with_ticks:
        d2.text((txx + time_w + tick_gap, baseline), "\u2713\u2713",
                font=fc, fill=WA_BLUE_TICK, anchor="ls")
    print(f"bubble '{text}' {time_str}{' + ticks' if with_ticks else ''} "
          f"font={FONT_SIZE}px fill=#{fill[0]:02x}{fill[1]:02x}"
          f"{fill[2]:02x} box=({x0},{y0})-({x1},{y1}) tail={tail_side}")
    return (x0, y0, x1, y1)


img = Image.open(SRC).convert("RGBA")
print("base size:", img.size)
paste_ghost(img, 150, 310, 280)
# Jason (left, face centre ~x580) speaks first 09:12, incoming white.
draw_bubble(img, "AGENT GOT PAID.", "09:12", tail_side="left", top_y=64,
            center_x=580, fill=WA_WHITE, time_color=WA_TIME_GRAY,
            with_ticks=False)
# Lucia (right, ~x1450) answers 09:13, outgoing green + blue ticks.
draw_bubble(img, "CANCEL THE HEIST.", "09:13", tail_side="right",
            top_y=64, center_x=1450, fill=WA_GREEN,
            time_color=WA_TIME_GREEN, with_ticks=True)
img.convert("RGB").save(f"{OUT}/meme.png", "PNG")
img.convert("RGB").resize((480, 320), Image.LANCZOS).save(
    f"{OUT}/meme-480.png", "PNG")
print("wrote", f"{OUT}/meme.png", "and meme-480.png")
