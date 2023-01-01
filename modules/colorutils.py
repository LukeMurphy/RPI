# colorutils
import math
import operator
import random
import sys

from PIL import ImageChops, ImageOps

colorWheel = [
    "RED",
    "VERMILLION",
    "ORANGE",
    "AMBER",
    "YELLOW",
    "CHARTREUSE",
    "GREEN",
    "TEAL",
    "BLUE",
    "VIOLET",
    "PURPLE",
    "MAGENTA",
]
wheel = [
    (255, 2, 2),
    (253, 83, 8),
    (255, 153, 1),
    (250, 188, 2),
    (255, 255, 0),
    (0, 125, 0),
    (146, 206, 0),
    (0, 255, 255),
    (0, 0, 255),
    (65, 0, 165),
    (135, 0, 175),
    (167, 25, 75),
]

# rgbColorWheel = ["RED","GREEN","BLUE","YELLOW","MAGENTA","CYAN"]
# rgbWheel = [(255,0,0),(0,255,0),(0,0,255),(255,255,0),(255,0,255),(0,255,255)]

rgbColorWheel = ["RED", "YELLOW", "GREEN", "CYAN", "BLUE", "MAGENTA"]
rgbWheel = [
    (255, 0, 0),
    (255, 0, 0),
    (255, 255, 0),
    (0, 255, 0),
    (0, 255, 255),
    (0, 0, 255),
    (255, 0, 255),
]

sunset = dict(
    drk1=(57, 36, 25),
    drk2=(124, 77, 56),
    drk3=(153, 95, 56),
    mid1=(177, 177, 78),
    mid2=(173, 104, 51),
    yellow=(218, 172, 71),
    ltyellow=(246, 232, 171),
    ltorange=(221, 144, 82),
    warmwht=(255, 255, 238),
)
sky = dict(coolblue=(254, 254, 248), ltblue=(190, 200, 202), grayblue=(182, 186, 182))
# sorted_sunset = {k: (sum(v)/3) for k, v in sunset.iteritems()}
# sorted_sunset = sorted({k: (sum(v)/3) for k, v in sunset.iteritems()}.items(), key=operator.itemgetter(1))

brightness = 1


klimt = ([48, 48, 48],
         [96, 96, 72],
         [120, 120, 48],
         [168, 168, 120],
         [120, 120, 120],
         [216, 120, 48],
         [168, 120, 120],
         [168, 48, 0],
         [48, 0, 0],
         [0, 48, 48],
         [168, 48, 48],
         [216, 168, 48],
         [120, 48, 48],
         [168, 120, 48],
         [120, 120, 0],
         [168, 168, 168],
         [168, 168, 0],
         [0, 0, 48],
         [200, 180, 8],
         [0, 0, 120])

testPalette =([255,0,0],[255,100,100],[255,0,200])


def getNamedPalette(arg, brtns=1, a=255):
    if arg == "klimt" :
    	return getKlimt(brtns, a)
    if arg == "testPalette" :
        return getTest(brtns, a)


def getKlimt(brtns=1, a=255):
    choice = round(
        random.uniform(0, len((klimt))-1)
    )

    c = klimt[choice]
    return (round(c[0] * brtns), round(c[1] * brtns), round(c[2] * brtns), a)

def getTest(brtns=1, a=255):
    choice = round(
        random.uniform(0, len((testPalette))-1)
    )

    c = testPalette[choice]
    return (round(c[0] * brtns), round(c[1] * brtns), round(c[2] * brtns), a)


def getRedShiftedColors(brtns=1):
    global brightness, sunset, sorted_sunset
    if brtns == 1:
        brtns = brightness
    r = round((random.uniform(0, 255)) * brtns)
    g = round((random.uniform(0, 50)) * brtns)
    b = round((random.uniform(0, 50)) * brtns)
    rRange = 255 - r
    r = round(r + random.uniform(0, rRange))
    return (r, g, b)


def getSunsetColors(brtns=1):
    global brightness, sunset, sorted_sunset
    if brtns == 1:
        brtns = brightness
    indx = math.floor(random.uniform(0, len(sunset)))

    vals = list(sunset.values())
    clr = vals[indx]
    r = round(clr[0] * brtns)
    g = round(clr[1] * brtns)
    b = round(clr[2] * brtns)
    return (r, g, b)


def getRandomRGB(brtns=1):
    global brightness, rgbColorWheel, rgbWheel
    if brtns == 1:
        brtns = brightness
    indx = math.floor(random.uniform(0, len(rgbWheel)))
    clr = rgbWheel[indx]
    r = round(clr[0] * brtns)
    g = round(clr[1] * brtns)
    b = round(clr[2] * brtns)
    return (r, g, b, 255)


def getRandomColorWheel(brtns=1):
    global brightness, colorWheel, wheel
    if brtns == 1:
        brtns = brightness
    indx = math.floor(random.uniform(0, len(colorWheel)))
    clr = wheel[indx]
    r = round(clr[0] * brtns)
    g = round(clr[1] * brtns)
    b = round(clr[2] * brtns)
    return (r, g, b, 255)


def randomColor(brtns=1):
    global brightness
    if brtns == 1:
        brtns = brightness
    r = round((random.uniform(0, 255)) * brtns)
    g = round((random.uniform(0, 255)) * brtns)
    b = round((random.uniform(0, 255)) * brtns)
    return (r, g, b, 255)


def randomYellowsAlpha(brtns=1, maxTransparency=255, minTransparency=0, sMax=1.0, sMin=0.5):
    global brightness
    if brtns == 1:
        brtns = brightness

    h = (random.uniform(42, 60))
    s = (random.uniform(sMin, sMax))
    v = .5

    col = HSVToRGB(h, s, v, a=255)

    a = round(random.uniform(minTransparency, maxTransparency))
    return (col[0], col[1], col[2], a)


def randomColorAlpha(brtns=1, maxTransparency=255, minTransparency=0):
    global brightness
    if brtns == 1:
        brtns = brightness
    r = round((random.uniform(0, 255)) * brtns)
    g = round((random.uniform(0, 255)) * brtns)
    b = round((random.uniform(0, 255)) * brtns)
    a = round(random.uniform(minTransparency, maxTransparency))
    return (r, g, b, a)


def randomGrayAlpha(brtns=1, maxTransparency=255, minTransparency=0):
    global brightness
    if brtns == 1:
        brtns = brightness
    r = round((random.uniform(0, 255)) * brtns)
    g = r
    b = r
    a = round(random.uniform(minTransparency, maxTransparency))
    return (r, g, b, a)

# Yup, same function that should have been called this
# to start with...    ;(


def getRandomColor(brtns=1):
    global brightness
    if brtns == 1:
        brtns = brightness
    r = round((random.uniform(0, 255)) * brtns)
    g = round((random.uniform(0, 255)) * brtns)
    b = round((random.uniform(0, 255)) * brtns)
    a = 255
    return (r, g, b)


def getRandomColorHSV(
        hMin=0.0,
        hMax=360.0,
        sMin=0.0,
        sMax=1.0,
        vMin=0.0,
        vMax=1.0,
        dropHueMin=0,
        dropHueMax=0,
        a=255,
        brtns=1.0
):

    # adjust for 360 degrees ranges
    degreeRange = hMax - hMin

    if hMin > hMax:
        degreeRange = 360.0 - hMin + hMax
    h = hMin + random.uniform(0.0, degreeRange)

    # an option to exclude a range of colors
    if dropHueMax != dropHueMin:
        h = hMin + random.uniform(0.0, degreeRange)
        if h > 360.0:
            h -= 360.0
        while h > dropHueMin and h < dropHueMax:
            h = hMin + random.uniform(0.0, degreeRange)
            if h > 360.0:
                h -= 360.0
    if h > 360.0:
        h -= 360.0

    #print("New hue: " + str(h))

    # h = random.uniform(hMin,hMax)
    # print(hMin,hMax,degreeRange, h)
    s = random.uniform(sMin, sMax)
    v = random.uniform(vMin, vMax)
    #print(vMin, vMax, v)
    rgb = HSVToRGB(h, s, v)
    return (round(rgb[0] * brtns), round(rgb[1] * brtns), round(rgb[2] * brtns), a)


def getRandomColorHSL(
        hMin=0.0,
        hMax=360.0,
        sMin=0.0,
        sMax=1.0,
        lMin=0.0,
        lMax=1.0,
        dropHueMin=0,
        dropHueMax=0,
        a=255,
):

    # adjust for 360 degrees ranges
    degreeRange = hMax - hMin

    if hMin > hMax:
        degreeRange = 360.0 - hMin + hMax
    h = hMin + random.uniform(0.0, degreeRange)

    if h > 360.0:
        h -= 360.0

    # an option to exclude a range of colors
    if dropHueMax != dropHueMin:
        h = dropHueMin + 1
        while h > dropHueMin and h < dropHueMax:
            h = hMin + random.uniform(0.0, degreeRange)
            if h > 360.0:
                h -= 360.0

    # h = random.uniform(hMin,hMax)
    # print(hMin,hMax,degreeRange, h)
    s = random.uniform(sMin, sMax)
    l = random.uniform(lMin, lMax)
    #print(lMin, lMax, l)
    rgb = HSVToRGB(h, s, l)
    return (rgb[0], rgb[1], rgb[2], a)


def randomBaseColor(brtns=1):
    global brightness
    if brtns == 1:
        brtns = brightness
    b = round((random.uniform(0, 255)) * brtns)
    r = round((random.uniform(0, 100)) * brtns)
    g = round((random.uniform(0, 100)) * brtns)
    return (r, g, b)


def colorCompliment(rgb, brtns=1):
    r = rgb[0]
    g = rgb[1]
    b = rgb[2]
    global brightness
    if brtns == 1:
        brtns = brightness
    minRGB = min(r, min(g, b))
    maxRGB = max(r, max(g, b))
    minmax = minRGB + maxRGB
    r = round((minmax - r) * brtns)
    g = round((minmax - g) * brtns)
    b = round((minmax - b) * brtns)
    return (r, g, b)


def randomGray(brtns=1):
    global brightness
    if brtns == 1:
        brtns = brightness
    grey = round((random.uniform(0, 255)) * brtns)
    r = grey
    g = grey
    b = grey
    return (r, g, b)


# Find the closest poround
def closestRBYfromRGB(rgb):
    global brightness, wheel
    r = rgb[0]
    g = rgb[1]
    b = rgb[2]
    # d = sqrt( x2-x1 ^ 2 ....)
    dMax = 0
    dArray = []
    for n in range(0, len(wheel)):
        d = round(
            math.sqrt(
                (r - wheel[n][0]) ** 2 + (g - wheel[n][1]) ** 2 + (b - wheel[n][2]) ** 2
            )
        )
        dArray.append([n, d])
    dArray = sorted(dArray, key=lambda n: n[1], reverse=False)
    return wheel[dArray[0][0]]


def rgb_to_hsv(r, g, b):
    r /= 255
    g /= 255
    b /= 255
    maxc = max(r, g, b)
    minc = min(r, g, b)
    v = maxc
    if minc == maxc:
        return 0.0, 0.0, v
    s = (maxc-minc) / maxc
    rc = (maxc-r) / (maxc-minc)
    gc = (maxc-g) / (maxc-minc)
    bc = (maxc-b) / (maxc-minc)
    if r == maxc:
        h = 0.0+bc-gc
    elif g == maxc:
        h = 2.0+rc-bc
    else:
        h = 4.0+gc-rc
    h = (h/6.0) % 1.0

    hue = h * 360
    sat = s * 1
    val = v * 1

    return (hue, sat, val)


def HSVToRGB(h, s, v, a=255):
    c = v * s
    huex = h / 60.0
    x = c * (1 - abs(huex % 2 - 1))
    r1 = g1 = b1 = 0
    if huex <= 1 and huex >= 0:
        (r1, g1, b1) = (c, x, 0)
    if huex <= 2 and huex >= 1:
        (r1, g1, b1) = (x, c, 0)
    if huex <= 3 and huex >= 2:
        (r1, g1, b1) = (0, c, x)
    if huex <= 4 and huex >= 3:
        (r1, g1, b1) = (0, x, c)
    if huex <= 5 and huex >= 4:
        (r1, g1, b1) = (x, 0, c)
    if huex <= 6 and huex >= 5:
        (r1, g1, b1) = (c, 0, x)
    m = v - c
    rgb = [r1 + m, g1 + m, b1 + m, a]

    rgbCol = tuple(abs(round(i * 255)) for i in rgb)
    return (rgbCol[0], rgbCol[1], rgbCol[2], a)


def HSLToRGB(h, s, l, a=255):
    c = s * (1 - abs(2 * l - 1))
    huex = h / 60.0
    x = c * (1 - abs(huex % 2 - 1))
    r1 = g1 = b1 = 0
    if huex <= 1 and huex >= 0:
        r1, g1, b1 = c, x, 0
    if huex <= 2 and huex >= 1:
        r1, g1, b1 = x, c, 0
    if huex <= 3 and huex >= 2:
        r1, g1, b1 = 0, c, x
    if huex <= 4 and huex >= 3:
        r1, g1, b1 = 0, x, c
    if huex <= 5 and huex >= 4:
        r1, g1, b1 = x, 0, c
    if huex <= 6 and huex >= 5:
        r1, g1, b1 = c, 0, x
    # m = l - (.3 * r1 + .59 * g1 + .11 * b1)
    m = l - c / 2
    rgb = [r1 + m, g1 + m, b1 + m, a]
    rgbCol = tuple(round(round(i * 255)) for i in rgb)
    return rgbCol


def subtractiveColors(arg):
    color = (0, 0, 0)
    if arg == "RED":
        color = tuple(round(a * brightness) for a in ((255, 2, 2)))
    if arg == "VERMILLION":
        color = tuple(round(a * brightness) for a in ((253, 83, 8)))
    if arg == "ORANGE":
        color = tuple(round(a * brightness) for a in ((255, 153, 1)))
    if arg == "AMBER":
        color = tuple(round(a * brightness) for a in ((250, 188, 2)))
    if arg == "YELLOW":
        color = tuple(round(a * brightness) for a in ((255, 255, 0)))
    if arg == "CHARTREUSE":
        color = tuple(round(a * brightness) for a in ((0, 255, 0)))
    if arg == "GREEN":
        color = tuple(round(a * brightness) for a in ((0, 125, 0)))
    if arg == "TEAL":
        color = tuple(round(a * brightness) for a in ((146, 206, 0)))
    if arg == "BLUE":
        color = tuple(round(a * brightness) for a in ((0, 0, 255)))
    if arg == "VIOLET":
        color = tuple(round(a * brightness) for a in ((65, 0, 165)))
    if arg == "PURPLE":
        color = tuple(round(a * brightness) for a in ((135, 0, 175)))
    if arg == "MAGENTA":
        color = tuple(round(a * brightness) for a in ((167, 25, 75)))
    return color


def colorComplimentRBY(arg):
    global colorWheel
    l = len(colorWheel) / 2
    indx = colorWheel.index(arg)
    oppIndx = indx + l
    if oppIndx > 11:
        oppIndx -= l * 2
    return subtractiveColors(colorWheel[oppIndx])


def changeColor(rnd=False):
    global brightness
    if rnd == False:
        if r == 255:
            r = 0
            g = 255
            b = 0
        else:
            g = 0
            r = 255
            b = 0
    else:
        r = round(random.uniform(0, 255) * brightness)
        g = round(random.uniform(0, 255) * brightness)
        b = round(random.uniform(0, 255) * brightness)
