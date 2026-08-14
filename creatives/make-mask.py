#!/usr/bin/env python3
"""Build the alpha mask that hides the burned-in captions.

The old text sits at y 960-1090, x 142-581 (measured by bbox.py). The mask's
*opaque core* has to cover that box, so the band cannot simply be made shorter:
a 940-1112 band with a 45px ramp is only solid between 985 and 1067, i.e. inside
the old text. To read as a soft halo rather than a bar, the band is instead made
taller with a much longer ramp, plus a horizontal falloff so it never touches the
frame edges.
"""
from PIL import Image

BAND_TOP, BAND_BOT = 905, 1145        # 240px tall; overlay is placed at BAND_TOP
V_FEATHER = 45                        # -> solid core 950..1100, covers 960..1090
H_SOLID = 100                         # solid from x=100 to x=620
W = 720
H = BAND_BOT - BAND_TOP


def smoothstep(t):
    t = max(0.0, min(1.0, t))
    return t * t * (3 - 2 * t)


img = Image.new("L", (W, H), 0)
px = img.load()

col = [smoothstep(min(x, W - 1 - x) / H_SOLID) for x in range(W)]
for y in range(H):
    v = smoothstep(min(y, H - 1 - y) / V_FEATHER)
    for x in range(W):
        px[x, y] = int(round(255 * v * col[x]))

img.save("feather.png")

solid = [y + BAND_TOP for y in range(H) if px[W // 2, y] >= 250]
print(f"feather.png {img.size}  band y {BAND_TOP}-{BAND_BOT}")
print(f"opaque core y {solid[0]}-{solid[-1]}  (must cover 960-1090)")
assert solid[0] <= 960 and solid[-1] >= 1090, "core does not cover the old captions"
