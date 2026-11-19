#!/usr/bin/env python3
"""Composite v3 for the main Bonnie & Clyde meme.

Changes vs v2 (per Bayu, round 3):
- Classic Impact captions REMOVED. Replaced by two modern chat bubbles:
  "CANCEL THE HEIST." (Lucia, right) and "AGENT GOT PAID." (Jason, left).
  Dark semi-transparent rounded bubbles with a thin light border, small
  tail pointing down at the speaker, clean bold sans text.
- Font XS: smallest size that stays clearly readable at 480px wide
  (judge view). Start 56px; verify on meme-480.png and bump only if
  it is not clearly readable.
- Base image and ghost UNCHANGED (same photorealistic base, same real
  press-kit mark-1024.png at (150, 310) d=280 with v2 shadow/feather).
- Bubbles sit in the dark headliner band at the top, near each speaker,
  and never cover a face or the ghost.
"""
from PIL import Image, ImageDraw, ImageFont, ImageFilter

BASE = "/home/hatch/workspace/makefun/gta6-meme-x-01/assets"
OUT = "/home/hatch/workspace/makefun/gta6-meme-x-01"
GHOST = f"{BASE}/mark-1024.png"
FONT = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
SRC = f"{BASE}/media-generation-media-generation-base-main-v2-0-50ce7a5f-063c-4db2-a3e6-960bc42f950c.png"

FONT_SIZE = 56  # XS: smallest still clearly readable at 480px wide

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


def draw_bubble(img, text, tail_x, top_y, font_size):
    """Modern chat bubble: dark semi-transparent rounded rect + tail
    pointing down at tail_x. Returns the bubble box."""
    f = ImageFont.truetype(FONT, font_size)
    tw = int(f.getlength(text))
    th = f.getbbox(text)[3] - f.getbbox(text)[1]
    pad_x, pad_y = 38, 26
    bw, bh = tw + pad_x * 2, th + pad_y * 2
    # center bubble horizontally on tail_x, clamped inside canvas
    x0 = max(16, min(tail_x - bw // 2, img.width - bw - 16))
    y0, y1 = top_y, top_y + bh
    x1 = x0 + bw
    layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    # tail first (triangle below the bubble, tip toward the speaker)
    d.polygon([(tail_x - 26, y1 - 8), (tail_x + 26, y1 - 8),
               (tail_x, y1 + 34)], fill=(32, 32, 40, 215))
    # body
    d.rounded_rectangle([x0, y0, x1, y1], radius=38,
                        fill=(32, 32, 40, 215),
                        outline=(255, 255, 255, 70), width=3)
    img.alpha_composite(layer)
    # text (drawn on the composited image, white, no stroke)
    d2 = ImageDraw.Draw(img)
    tx = x0 + pad_x
    ty = y0 + pad_y - f.getbbox(text)[1]
    d2.text((tx, ty), text, font=f, fill="white")
    print(f"bubble '{text}' font={font_size}px text_w={tw}px "
          f"box=({x0},{y0})-({x1},{y1}) tail_x={tail_x}")
    return (x0, y0, x1, y1)


img = Image.open(SRC).convert("RGBA")
print("base size:", img.size)
paste_ghost(img, 150, 310, 280)
# Jason (left, face centre ~x580) speaks first; Lucia (right, ~x1450) answers.
draw_bubble(img, "AGENT GOT PAID.", tail_x=580, top_y=64,
            font_size=FONT_SIZE)
draw_bubble(img, "CANCEL THE HEIST.", tail_x=1450, top_y=64,
            font_size=FONT_SIZE)
img.convert("RGB").save(f"{OUT}/meme.png", "PNG")
img.convert("RGB").resize((480, 320), Image.LANCZOS).save(
    f"{OUT}/meme-480.png", "PNG")
print("wrote", f"{OUT}/meme.png", "and meme-480.png")
