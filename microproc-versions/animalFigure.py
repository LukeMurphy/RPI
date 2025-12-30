# pip install pillow
from PIL import Image, ImageDraw
import random

def make_dog_icon(scale=16, bg=(150, 70, 60)):
    # draw tiny pixel-art, then scale up with nearest-neighbor
    W, H = 32, 32
    im = Image.new("RGB", (W, H), bg)
    px = im.load()

    OUT = (0, 0, 0)          # outline
    FUR = (205, 205, 190)    # light body
    OLIVE = (80, 95, 55)     # left square
    RUST = (150, 70, 60)     # center square (same as bg)
    BLUE = (95, 120, 150)    # right square

    xOff = 4
    yOff = 14

    def setp(x, y, c):
        if 0 <= x < W and 0 <= y < H:
            px[x, y] = c

    def fill_rect(x0, y0, x1, y1, c):
        for y in range(y0, y1):
            for x in range(x0, x1):
                setp(x+xOff, y+yOff, c)

    def outline_rect(x0, y0, x1, y1, c=OUT):
        for x in range(x0, x1):
            setp(x+xOff, y0+yOff, c); setp(x+xOff, y1-1+yOff, c)
        for y in range(y0, y1):
            setp(x0+xOff, y+yOff, c); setp(x1-1+xOff, y+yOff, c)

    # --- body silhouette (simple blocky dog) ---
    # body
    outline_rect(4, 6, 20, 14)
    fill_rect(5, 7, 19, 13, FUR)

    # head / neck block + snout
    outline_rect(3, 2, 8, 10)
    fill_rect(4, 3, 7, 9, FUR)
    outline_rect(1, 3, 6, 6)       # snout
    fill_rect(2, 4, 5, 5, FUR)

    # tail block
    outline_rect(19, 3, 22, 9)
    fill_rect(20, 4, 21, 8, FUR)

    # legs
    for x0 in (5, 8, 15, 18):
        outline_rect(x0, 14, x0+2, 18)
        fill_rect(x0+1, 15, x0+1, 17, FUR)  # (does nothing, but keeps symmetry)
        fill_rect(x0+1, 15, x0+1+1, 17, FUR)

    # --- colored squares inside body ---
    # (leave a black border like the rug icon)
    outline_rect(6, 8, 9, 11);  fill_rect(7, 9, 8, 10, OLIVE)
    outline_rect(11, 9, 13, 11); fill_rect(12, 10, 12+1, 10+1, RUST)
    outline_rect(16, 8, 19, 11); fill_rect(17, 9, 18, 10, BLUE)

    # --- upscale ---
    big = im.resize((W * scale, H * scale), Image.Resampling.NEAREST)

    # --- add simple “rug” texture to background ---
    bpx = big.load()
    for y in range(big.height):
        for x in range(big.width):
            r, g, b = bpx[x, y]
            # only texture the background-ish pixels (close to bg color)
            if abs(r - bg[0]) + abs(g - bg[1]) + abs(b - bg[2]) < 25:
                n = random.randint(-18, 18)
                bpx[x, y] = (max(0, min(255, r + n)),
                             max(0, min(255, g + n)),
                             max(0, min(255, b + n)))

    return big

img = make_dog_icon(scale=2, bg=(155, 80, 70))
img.save("dog_rug_icon.png")
img.show()