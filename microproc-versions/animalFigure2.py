# pip install pillow
from PIL import Image, ImageDraw
import random


def make_dog_icon(scale=16, bg=(150, 70, 60)):
    # draw tiny pixel-art, then scale up with nearest-neighbor
    W, H = 64, 64
    im = Image.new("RGB", (W, H), bg)
    px = im.load()

    OUT = (0, 0, 0)  # outline
    FUR = (205, 205, 190)  # light body
    OLIVE = (80, 95, 55)  # left square
    RUST = (150, 70, 60)  # center square (same as bg)
    BLUE = (95, 120, 150)  # right square

    xOff = 4
    yOff = 14

    imd = ImageDraw.Draw(im, "RGB")

    bottomY = 63
    startHoofX = random.randint(2, 12)

    hoofWidth = random.randint(0, 4)
    hoofHeight = random.randint(0, 4)

    neckTopY = 32
    backTopY = 37
    backWidth = random.randint(20, 32)
    bellyBottom = random.randint(44, 52)

    mouthX = random.randint(3, 6)
    noseX = random.randint(3, 6)
    noseY = random.randint(26, 30)
    
    foreHeadX = random.randint(12, 16)
    foreHeadY = random.randint(19, 22)
    headTopY = random.randint(18, 24)

    earBaseX = 25
    earBaseY = 20

    earBottomX = 25
    earBottomY = 25

    # also the chest
    neckX = startHoofX + hoofWidth
    neckWidth = random.randint(8, 11)
    earCutInWidth = random.randint(1, 4)

    tailCurlY = random.randint(30, 34)
    tailCurlTipY = random.randint(28, 36)
    tailCurlHeight = random.randint(2, 7)
    backCurlWidth = random.randint(2, 7)
    tailWidth = random.randint(2, 7)
    tailCurlBaseY = random.randint(18, 28)
    tailEndY = 43
    tailJoinY = 45
    backLegFarX = neckX + neckWidth + backWidth + tailWidth

    legWidth = random.randint(5, 10)
    legSeparation = random.randint(3, 3)

    polyOutline = [
        (startHoofX, bottomY),
        (startHoofX + hoofWidth, bottomY - hoofHeight),
        (startHoofX + hoofWidth, bellyBottom),
        (startHoofX + hoofWidth, neckTopY),
        (mouthX, neckTopY),
        (noseX, noseY),
        (foreHeadX, foreHeadY),
        (foreHeadX, headTopY),
        (earBaseX, earBaseY),
        (earBottomX, earBottomY),
        (neckX + neckWidth - earCutInWidth, earBottomY),
        (neckX + neckWidth, earBottomY),
        (neckX + neckWidth, backTopY),
        (neckX + neckWidth + backWidth, backTopY),
        (neckX + neckWidth + backWidth, tailCurlY),
        (neckX + neckWidth + backWidth - backCurlWidth, tailCurlTipY),
        (neckX + neckWidth + backWidth - backCurlWidth, tailCurlTipY - tailCurlHeight),
        (neckX + neckWidth + backWidth + tailWidth, tailCurlBaseY),
        (neckX + neckWidth + backWidth + tailWidth, tailEndY),
        (backLegFarX, tailJoinY),
        (backLegFarX, bottomY),
        (backLegFarX - legWidth, bottomY),
        (backLegFarX - legWidth + hoofWidth, bottomY - hoofHeight),
        (backLegFarX - legWidth + hoofWidth, bellyBottom),
        (backLegFarX - legWidth + hoofWidth - legSeparation, bellyBottom),
        (backLegFarX - legWidth + hoofWidth - legSeparation, bottomY),
        (backLegFarX - legWidth - legWidth - legSeparation, bottomY),
        (backLegFarX - legWidth - legWidth - legSeparation + hoofWidth * 2, bottomY - hoofHeight),
        (backLegFarX - legWidth - legWidth - legSeparation + hoofWidth * 2, bellyBottom),
        (neckX + legWidth + legWidth, bellyBottom),
        (neckX + legWidth + legWidth, bottomY),
        (neckX + legWidth, bottomY),
        (neckX + legWidth + hoofWidth, bottomY - hoofHeight),
        (neckX + legWidth + hoofWidth, bellyBottom),
        (neckX + legWidth - hoofWidth, bellyBottom),
        (neckX + legWidth - hoofWidth, bottomY),
        (startHoofX, bottomY),
    ]



    for p in range(0, len(polyOutline)-1, 2) :
        print(p, polyOutline[p], polyOutline[p+1])

    imd.polygon(polyOutline, fill=(100, 100, 100), outline=(0, 0, 0))

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
                bpx[x, y] = (max(0, min(255, r + n)), max(0, min(255, g + n)), max(0, min(255, b + n)))

    return big


img = make_dog_icon(scale=2, bg=(155, 80, 70))
img.save("dog_rug_icon2.png")
img.show()
