#!/usr/bin/env python3
"""Composite v4 for the main Bonnie & Clyde meme.

Changes vs v3 (per Bayu, round 4):
- ONLY the two caption bubbles restyled to look like WhatsApp chat
  bubbles. Base image and ghost UNCHANGED (same photorealistic base,
  same real press-kit mark-1024.png at (150, 310) d=280).
- WhatsApp style: Jason (left) "AGENT GOT PAID." = outgoing bubble,
  WhatsApp light green #dcf8c6. Lucia (right) "CANCEL THE HEIST." =
  incoming bubble, white #ffffff. Dark text #111b21 on both, WA-style
  rounded corners, small tail pointing down at the speaker, soft drop
  shadow, no border. Font stays XS 56px.
- Timestamp / double-check marks SKIPPED on purpose: at 480px they
  would shrink to ~7px noise. The green+white colours alone read as
  WhatsApp, and the bubbles stay clean and readable.
"""
from PIL import Image, ImageDraw, ImageFont, ImageFilter

BASE = "/home/hatch/workspace/makefun/gta6-meme-x-01/assets"
OUT = "/home/hatch/workspace/makefun/gta6-meme-x-01"
GHOST = f"{BASE}/mark-1024.png"
FONT = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
SRC = f"{BASE}/media-generation-media-generation-base-main-v2-0-50ce7a5f-063c-4db2-a3e6-960bc42f950c.png"

FONT_SIZE = 56  # XS: smallest still clearly readable at 480px wide
WA_GREEN = (220, 248, 198)      # #dcf8c6 outgoing
WA_WHITE = (255, 255, 255)      # incoming
WA_TEXT = (17, 27, 33)          # #111b21

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


def draw_bubble(img, text, tail_x, top_y, font_size, fill):
    """WhatsApp bubble: opaque light fill, WA radius, small tail down
    at tail_x, soft drop shadow, dark text. Returns the bubble box."""
    f = ImageFont.truetype(FONT, font_size)
    tw = int(f.getlength(text))
    th = f.getbbox(text)[3] - f.getbbox(text)[1]
    pad_x, pad_y = 38, 26
    bw, bh = tw + pad_x * 2, th + pad_y * 2
    # center bubble horizontally on tail_x, clamped inside canvas
    x0 = max(16, min(tail_x - bw // 2, img.width - bw - 16))
    y0, y1 = top_y, top_y + bh
    x1 = x0 + bw
    radius = 24
    # soft drop shadow (bubble + tail silhouette, blurred)
    sh = Image.new("RGBA", img.size, (0, 0, 0, 0))
    ds = ImageDraw.Draw(sh)
    ds.polygon([(tail_x - 26, y1 - 8), (tail_x + 26, y1 - 8),
                (tail_x, y1 + 34)], fill=(0, 0, 0, 90))
    ds.rounded_rectangle([x0, y0, x1, y1], radius=radius,
                         fill=(0, 0, 0, 90))
    sh = sh.filter(ImageFilter.GaussianBlur(12))
    img.alpha_composite(sh)
    # bubble body + tail (same fill so the tail blends in)
    layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    d.polygon([(tail_x - 26, y1 - 8), (tail_x + 26, y1 - 8),
               (tail_x, y1 + 34)], fill=fill + (255,))
    d.rounded_rectangle([x0, y0, x1, y1], radius=radius,
                        fill=fill + (255,))
    img.alpha_composite(layer)
    # dark text, no stroke
    d2 = ImageDraw.Draw(img)
    tx = x0 + pad_x
    ty = y0 + pad_y - f.getbbox(text)[1]
    d2.text((tx, ty), text, font=f, fill=WA_TEXT)
    print(f"bubble '{text}' font={font_size}px fill=#{fill[0]:02x}"
          f"{fill[1]:02x}{fill[2]:02x} box=({x0},{y0})-({x1},{y1}) "
          f"tail_x={tail_x}")
    return (x0, y0, x1, y1)


img = Image.open(SRC).convert("RGBA")
print("base size:", img.size)
paste_ghost(img, 150, 310, 280)
# Jason (left, face centre ~x580) speaks first; Lucia (right, ~x1450) answers.
draw_bubble(img, "AGENT GOT PAID.", tail_x=580, top_y=64,
            font_size=FONT_SIZE, fill=WA_GREEN)
draw_bubble(img, "CANCEL THE HEIST.", tail_x=1450, top_y=64,
            font_size=FONT_SIZE, fill=WA_WHITE)
img.convert("RGB").save(f"{OUT}/meme.png", "PNG")
img.convert("RGB").resize((480, 320), Image.LANCZOS).save(
    f"{OUT}/meme-480.png", "PNG")
print("wrote", f"{OUT}/meme.png", "and meme-480.png")
