"""Erzeugt ein Zelda-Ocarina-of-Time-artiges Hintergrundbild (zelda-bg.jpg)."""
from PIL import Image, ImageDraw, ImageFilter
import random, math

W, H = 1920, 1080
img = Image.new("RGBA", (W, H), (0, 0, 0, 255))
d = ImageDraw.Draw(img, "RGBA")

# ---------- Himmel: Abenddämmerung über Hyrule ----------
top = (26, 32, 44)
mid = (58, 62, 58)
low = (120, 96, 48)
for y in range(H):
    t = y / H
    if t < 0.55:
        k = t / 0.55
        c = tuple(int(top[i] + (mid[i] - top[i]) * k) for i in range(3))
    else:
        k = (t - 0.55) / 0.45
        c = tuple(int(mid[i] + (low[i] - mid[i]) * k) for i in range(3))
    d.line([(0, y), (W, y)], fill=c + (255,))

# ---------- Sterne ----------
random.seed(7)
for _ in range(160):
    x = random.randint(0, W)
    y = random.randint(0, int(H * 0.42))
    r = random.choice([1, 1, 1, 2])
    a = random.randint(90, 220)
    d.ellipse([x, y, x + r, y + r], fill=(255, 250, 220, a))

# ---------- Mond mit Schein ----------
mx, my, mr = int(W * 0.78), int(H * 0.20), 130
glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
gd = ImageDraw.Draw(glow)
for rr in range(mr * 3, mr, -6):
    alpha = int(38 * (1 - (rr - mr) / (mr * 2)))
    gd.ellipse([mx - rr, my - rr, mx + rr, my + rr], fill=(255, 236, 170, max(0, alpha)))
glow = glow.filter(ImageFilter.GaussianBlur(28))
img.alpha_composite(glow)
d.ellipse([mx - mr, my - mr, mx + mr, my + mr], fill=(252, 243, 200, 235))
d.ellipse([mx - mr, my - mr, mx + mr, my + mr], outline=(232, 197, 71, 200), width=3)
# Krater
for (cx, cy, cr) in [(-40, -30, 26), (35, 15, 18), (-10, 55, 14), (55, -55, 10)]:
    d.ellipse([mx + cx - cr, my + cy - cr, mx + cx + cr, my + cy + cr], fill=(238, 228, 180, 150))

# ---------- Ferne Berge (Death Mountain rechts) ----------
def ridge(y_base, amp, color, seed, step=90):
    rnd = random.Random(seed)
    pts = [(0, H)]
    x = 0
    h = y_base
    while x <= W + step:
        h = y_base - rnd.randint(0, amp)
        pts.append((x, h))
        x += step
    pts.append((W, H))
    d.polygon(pts, fill=color)

ridge(int(H * 0.52), 90, (30, 38, 34, 255), 3, 130)
ridge(int(H * 0.62), 120, (22, 28, 24, 255), 11, 110)

# Death Mountain mit Vulkan-Silhouette
dmx, dmy = int(W * 0.86), int(H * 0.60)
d.polygon([(dmx - 260, H), (dmx - 40, dmy - 150), (dmx, dmy - 190), (dmx + 60, dmy - 140), (dmx + 280, H)],
          fill=(16, 20, 17, 255))
# glühende Lava-Adern
for i in range(9):
    sx = dmx + random.randint(-120, 120)
    sy = dmy - 150 + random.randint(0, 120)
    d.line([(sx, sy), (sx + random.randint(-16, 16), sy + random.randint(30, 90))],
           fill=(214, 96, 34, 170), width=2)

# ---------- Schloss Hyrule (Silhouette, links) ----------
cx0, cy0 = int(W * 0.28), int(H * 0.60)
wall = (20, 25, 21, 255)
gold = (232, 197, 71, 120)

# Hauptmauer
d.rectangle([cx0 - 190, cy0, cx0 + 190, H], fill=wall)
# Zinnen
for x in range(cx0 - 190, cx0 + 191, 38):
    d.rectangle([x, cy0 - 22, x + 20, cy0], fill=wall)
# Mittelturm
d.rectangle([cx0 - 46, cy0 - 210, cx0 + 46, cy0], fill=wall)
d.polygon([(cx0 - 62, cy0 - 210), (cx0, cy0 - 300), (cx0 + 62, cy0 - 210)], fill=wall)
# Seitentürme
for off in (-150, 150):
    d.rectangle([cx0 + off - 30, cy0 - 130, cx0 + off + 30, cy0], fill=wall)
    d.polygon([(cx0 + off - 42, cy0 - 130), (cx0 + off, cy0 - 205), (cx0 + off + 42, cy0 - 130)], fill=wall)
    # goldene Turmspitze
    d.polygon([(cx0 + off - 42, cy0 - 130), (cx0 + off, cy0 - 205), (cx0 + off + 42, cy0 - 130)],
              outline=gold, width=2)
# Fenster, warm beleuchtet
for (wx, wy) in [(cx0 - 20, cy0 - 150), (cx0 + 8, cy0 - 120), (cx0 - 12, cy0 - 60),
                 (cx0 - 150, cy0 - 70), (cx0 + 130, cy0 - 70)]:
    d.rounded_rectangle([wx, wy, wx + 16, wy + 26], radius=8, fill=(250, 208, 120, 190))
# Tor
d.rounded_rectangle([cx0 - 26, cy0 + 40, cx0 + 26, cy0 + 130], radius=24, fill=(240, 198, 110, 200))

# ---------- Wald (Vordergrund, links) ----------
random.seed(21)
for _ in range(46):
    bx = random.randint(-40, int(W * 0.46))
    by = random.randint(int(H * 0.62), H + 40)
    th = random.randint(90, 210)
    tw = random.randint(16, 34)
    d.polygon([(bx - tw, by), (bx, by - th), (bx + tw, by)], fill=(12, 16, 13, 255))
    d.rectangle([bx - 4, by - 10, bx + 4, by + 30], fill=(10, 13, 11, 255))

# ---------- Wiesenlinie / Nebel ----------
fog = Image.new("RGBA", (W, H), (0, 0, 0, 0))
fd = ImageDraw.Draw(fog)
fd.rectangle([0, int(H * 0.66), W, int(H * 0.80)], fill=(180, 175, 140, 46))
fog = fog.filter(ImageFilter.GaussianBlur(40))
img.alpha_composite(fog)

# ---------- Triforce, dezent oben links ----------
def triforce(cx, cy, size, color):
    h = size * math.sqrt(3) / 2
    top = [(cx, cy - h * 0.66), (cx - size / 2, cy + h * 0.34), (cx + size / 2, cy + h * 0.34)]
    left = [(cx - size / 2 - size / 2, cy + h * 0.34), (cx - size / 2, cy + h * 0.34),
            (cx - size / 2, cy + h * 0.34 + h)]
    right = [(cx + size / 2 + size / 2, cy + h * 0.34), (cx + size / 2, cy + h * 0.34),
             (cx + size / 2, cy + h * 0.34 + h)]
    for tri in (top, left, right):
        d.polygon(tri, outline=color, width=4)

tri_layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
td = ImageDraw.Draw(tri_layer)
triforce(220, 200, 150, (232, 197, 71, 150))
tri_layer = tri_layer.filter(ImageFilter.GaussianBlur(1.2))
img.alpha_composite(tri_layer)

# ---------- Vignette ----------
vig = Image.new("L", (W, H), 0)
vd = ImageDraw.Draw(vig)
vd.ellipse([-int(W * 0.25), -int(H * 0.25), int(W * 1.25), int(H * 1.25)], fill=255)
vig = vig.filter(ImageFilter.GaussianBlur(220))
dark = Image.new("RGBA", (W, H), (6, 8, 5, 235))
dark.putalpha(Image.eval(vig, lambda v: int((255 - v) * 0.85)))
img.alpha_composite(dark)

# ---------- leichte Körnung ----------
noise = Image.effect_noise((W, H), 12).convert("L")
noise_rgba = Image.merge("RGBA", (noise, noise, noise, Image.new("L", (W, H), 16)))
img.alpha_composite(noise_rgba)

img.convert("RGB").save("zelda-bg.jpg", quality=92)
print("zelda-bg.jpg geschrieben:", img.size)
