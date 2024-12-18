import argparse
import datetime
import math
import random
import textwrap
import time
from modules.configuration import bcolors
from modules import badpixels, coloroverlay, colorutils
from PIL import Image, ImageChops, ImageDraw, ImageEnhance, ImageFont, ImageOps

"""""" """""" """""" """""" """""" """""" """""" """""" """""" """""" ""
## Image layers


class unit:

    xPos = 0
    yPos = 0
    bgColor = (0, 0, 0)
    outlineColor = (0, 0, 0)
    tileSizeWidth = 64
    tileSizeHeight = 32
    coordinatedColorChange = True

    def __init__(self):

        self.unHideGrid = False

    def createUnitImage(self):
        self.image = Image.new("RGBA", (self.tileSizeWidth, self.tileSizeHeight))
        self.draw = ImageDraw.Draw(self.image)

    def setUp(self):
        self.colOverlay = coloroverlay.ColorOverlay()
        self.colOverlay.randomSteps = True
        self.colOverlay.steps = self.config.steps
        self.colOverlay.maxBrightness = self.config.brightness

        self.colOverlay.minHue = self.palette[0]
        self.colOverlay.maxHue = self.palette[1]
        self.colOverlay.minSaturation = self.palette[2]
        self.colOverlay.maxSaturation = self.palette[3]
        self.colOverlay.minValue = self.palette[4]
        self.colOverlay.maxValue = self.palette[5]
        self.colOverlay.maxBrightness = self.colOverlay.maxValue

        self.colOverlay.dropHueMin = self.dropHueMin
        self.colOverlay.dropHueMax = self.dropHueMax

        self.colOverlay.colorB = [0, 0, 0, 10]
        self.colOverlay.colorA = [0, 0, 0, 10]
        self.colOverlay.currentColor = [0, 0, 0, 10]		

        self.colOverlay.colorTransitionSetup()

    def drawUnit(self):
        # self.colOverlay.stepTransition()

        if self.unHideGrid == False and self.coordinatedColorChange == False:
            self.colOverlay.stepTransition(False, self.config.bgAlpha)

        if self.coordinatedColorChange == False:
            self.bgColor = tuple(
                int(a * self.config.brightness) for a in (self.colOverlay.currentColor)
            )

        fontColor = self.bgColor
        outlineColor = self.bgColor

        if self.unHideGrid == True:
            fontColor = self.config.fontColor
            outlineColor = self.config.outlineColor

        if self.config.showOutline == False:
            outlineColor = self.bgColor

        self.draw.rectangle(
            (0, 0, self.tileSizeWidth - 1, self.tileSizeHeight - 1),
            fill=self.bgColor,
            outline=outlineColor,
        )

        # u"\u000D"
        displyInfo1 = str(self.col) + ", " + str(self.row)
        displyInfo2 = (
            str(self.col * self.tileSizeWidth)
            + ", "
            + str(self.row * self.tileSizeHeight)
        )

        # displyInfo = displyInfo.encode('utf-8')
        if self.config.showText == True:
            self.draw.text((2, -1), (displyInfo1), fontColor, font=self.config.font)
            self.draw.text(
                (2, -1 + self.config.fontSize),
                (displyInfo2),
                fontColor,
                font=self.config.font,
            )


"""""" """""" """""" """""" """""" """""" """""" """""" """""" """""" ""


def makeGrid():
    global config
    unitNumber = 1
    if config.choosePaletteForEachTile == False :
        paletteNumber = math.floor(random.uniform(0,len(config.palettes)))
    for row in range(0, config.rows):
        for col in range(0, config.cols):
            if config.choosePaletteForEachTile == True :
                paletteNumber = math.floor(random.uniform(0,len(config.palettes)))
            u = unit()
            u.config = config
            u.tileSizeWidth = config.tileSizeWidth
            u.tileSizeHeight = config.tileSizeHeight
            u.xPos = config.magingSpacing + col * (config.tileSizeWidth + config.gridSpacing)
            u.yPos = config.magingSpacing + row * (config.tileSizeHeight + config.gridSpacing)
            u.row = row
            u.col = col
            u.coordinatedColorChange = config.coordinatedColorChange
            u.palette = config.palettes[paletteNumber]
            u.dropHueMin = config.paletteDropHueMin
            u.dropHueMax = config.paletteDropHueMax

            u.createUnitImage()
            if config.coordinatedColorChange == False:
                u.setUp()

            u.drawUnit()
            config.unitArray.append(u)
            unitNumber += 1


def redrawGrid():

    if config.coordinatedColorChange == True:
        config.colOverlay.stepTransition()

        # config.colOverlay.colorTransitionSetup(100)
    """
    if(random.random() < .002):
        config.unHideGrid = True
    if(random.random() < .02):
        config.unHideGrid = False
    """

    for u in config.unitArray:

        if random.random() < config.unhideRate:
            u.unHideGrid = True
        if random.random() < config.rehideRate:
            u.unHideGrid = False
        # u.unHideGrid = config.unHideGrid
        u.bgColor = tuple(
            int(a * config.brightness) for a in (config.colOverlay.currentColor)
        )
        u.drawUnit()
        config.image.paste(u.image, (u.xPos + config.imageXOffset, u.yPos), u.image)

    if random.random() < config.fullimageGiltchRate:
        glitchBox(config.image, -config.imageGlitchSize, config.imageGlitchSize)

        ## Also do random image rotation if set to True
        if config.randomRotation == True:
            config.rotation = random.uniform(-1, 1)

    # the overlay can fall apart independently of the overall image
    if config.useOverLayImage == True:
        if random.random() < config.overlayGlitchRate:
            glitchBox(
                config.loadedImage, -config.overlayGlitchSize, config.overlayGlitchSize
            )
        if random.random() < config.overlayResetRate:
            config.loadedImage.paste(config.loadedImageCopy)

        if random.random() < config.overlayGlitchRate:
            config.overLayXPos = round(config.overLayXPosInit * random.random())
        if random.random() < config.overlayGlitchRate:
            # config.overLayYPos = round(config.overLayYPosInit * random.random())
            config.overLayYPos = round(random.uniform(-30, 64))

        config.image.paste(
            config.loadedImage,
            (config.overLayXPos, config.overLayYPos),
            config.loadedImage,
        )

    ## Correct any random rotation more quickly
    if (
        random.random() < config.fullimageGiltchRate * 100
        and config.randomRotation == True
    ):
        config.rotation = config.baseRotation

    if config.useEdgeSeedColors == True:
        colorSeeds()

    config.render(config.image, 0, 0)

    if random.random() < config.paletteChangeProb  and len(config.palettes) > 1:
        config.unitArray = []
        makeGrid()


"""""" """""" """""" """""" """""" """""" """""" """""" """""" """""" ""
"Not really used"


def showGrid():
    global config

    # config.draw.rectangle((0,0,config.screenWidth, config.screenHeight), fill=(0,0,0), outline=(0,0,0))
    config.draw.rectangle(
        (0, 0, config.screenWidth - 1, config.screenHeight - 1),
        fill=(0, 0, 0),
        outline=config.outlineColor,
    )
    config.draw.rectangle(
        (1, 1, config.screenWidth - 2, config.screenHeight - 2),
        fill=(0, 0, 0),
        outline=(0, 0, int(220 * config.brightness)),
    )

    if config.unHideGrid == False:
        config.colOverlay.stepTransition()

    config.bgColor = tuple(
        int(a * config.brightness) for a in (config.colOverlay.currentColor)
    )
    fontColor = config.bgColor
    outlineColor = config.bgColor

    if random.random() < 0.002:
        config.unHideGrid = True
    if config.unHideGrid == True:
        fontColor = config.fontColor
        outlineColor = config.outlineColor
    if random.random() < 0.02:
        config.unHideGrid = False

    for row in range(0, config.rows):
        for col in range(0, config.cols):
            xPos = col * config.tileSizeWidth
            yPos = row * config.tileSizeHeight
            config.draw.rectangle(
                (
                    xPos,
                    yPos,
                    xPos + config.tileSizeWidth - 1,
                    yPos + config.tileSizeHeight - 1,
                ),
                fill=config.bgColor,
                outline=outlineColor,
            )

            # u"\u000D"
            displyInfo1 = str(col) + ", " + str(row)
            displyInfo2 = (
                str(col * config.tileSizeWidth)
                + ", "
                + str(row * config.tileSizeHeight)
            )

            # displyInfo = displyInfo.encode('utf-8')

            config.draw.text(
                (xPos + 2, yPos - 1), (displyInfo1), fontColor, font=config.font
            )
            config.draw.text(
                (xPos + 2, yPos - 1 + config.fontSize),
                (displyInfo2),
                fontColor,
                font=config.font,
            )

    # the overlay can fall apart independently of the overall image
    if config.useOverLayImage == True:
        if random.random() < config.overlayGlitchRate:
            glitchBox(
                config.loadedImage, -config.overlayGlitchSize, config.overlayGlitchSize
            )
        if random.random() < config.overlayResetRate:
            config.loadedImage.paste(config.loadedImageCopy)

        if random.random() < config.overlayGlitchRate:
            config.overLayXPos = round(config.overLayXPosInit * random.random())
        if random.random() < config.overlayGlitchRate:
            config.overLayYPos = round(config.overLayYPosInit * random.random())

        config.image.paste(
            config.loadedImage,
            (config.overLayXPos, config.overLayYPos),
            config.loadedImage,
        )

    if random.random() < config.fullimageGiltchRate:
        glitchBox(config.image, -config.imageGlitchSize, config.imageGlitchSize)

    config.render(config.image, 0, 0)


def displayTest():
    global config

    config.colOverlay.stepTransition()
    config.bgColor = tuple(
        int(a * config.brightness) for a in (config.colOverlay.currentColor)
    )
    # config.draw.rectangle((0,0,config.screenWidth, config.screenHeight), fill=(0,0,0), outline=(0,0,0))

    config.draw.rectangle(
        (0, 0, config.screenWidth - 1, config.screenHeight - 1),
        fill=config.bgColor,
        outline=config.outlineColor,
    )
    config.draw.rectangle(
        (1, 1, config.screenWidth - 2, config.screenHeight - 2),
        fill=config.bgColor,
        outline=config.outlineColor,
    )

    # config.draw.text((5,0),"TOP",config.fontColor,font=config.font)
    # config.draw.text((5,config.screenHeight-15),"BOTTOM",config.fontColor,font=config.font)

    tm = datetime.datetime.now()
    tm = time.ctime()
    # config.draw.text((10,24),tm,config.fontColor,font=config.font)

    w = 24
    h = 24
    xp = 10
    yp = 40

    rgbWheel = [
        (255, 0, 0),
        (255, 255, 0),
        (0, 255, 0),
        (0, 255, 255),
        (0, 0, 255),
        (255, 0, 255),
        (255, 255, 255),
    ]

    for i in range(0, len(rgbWheel)):
        colorBlock = tuple(map(lambda x: int(int(x) * config.brightness), rgbWheel[i]))
        # config.draw.rectangle((xp,yp,xp + w,yp+h), fill=colorBlock, outline=colorBlock)
        xp += w

    yp += h
    xp = 10

    for i in range(0, len(rgbWheel)):
        colorBlock = tuple(
            map(lambda x: int(int(x) * config.brightness * 0.5), rgbWheel[i])
        )
        # config.draw.rectangle((xp,yp,xp + w,yp+h), fill=colorBlock, outline=colorBlock)
        xp += w

    # the overlay can fall apart independently of the overall image
    if config.useOverLayImage == True:
        if random.random() < config.overlayGlitchRate:
            glitchBox(
                config.loadedImage, -config.overlayGlitchSize, config.overlayGlitchSize
            )
        if random.random() < config.overlayResetRate:
            config.loadedImage.paste(config.loadedImageCopy)

        if random.random() < config.overlayGlitchRate:
            config.overLayXPos = round(config.overLayXPosInit * random.random())
        if random.random() < config.overlayGlitchRate:
            config.overLayYPos = round(config.overLayYPosInit * random.random())

        config.image.paste(
            config.loadedImage,
            (config.overLayXPos, config.overLayYPos),
            config.loadedImage,
        )

    if random.random() < config.fullimageGiltchRate:
        glitchBox(config.image, -config.imageGlitchSize, config.imageGlitchSize)

    config.render(config.image, 0, 0)


"""""" """""" """""" """""" """""" """""" """""" """""" """""" """""" ""
## Image manipulation functions


def glitchBox(img, r1=-10, r2=10):
    apparentWidth = img.size[0]
    apparentHeight = img.size[1]
    dy = int(random.uniform(r1, r2))
    dx = int(random.uniform(1, config.imageGlitchSize))
    dx = 0

    # really doing "vertical" or y-axis glitching
    # block height is uniform but width is variable

    sectionHeight = int(random.uniform(2, apparentHeight - dy))
    sectionWidth = apparentWidth

    # 95% of the time they dance together as mirrors
    if random.random() < 0.97:
        cp1 = img.crop((dx, 0, dx + sectionWidth, sectionHeight))
        img.paste(cp1, (int(0 + dx), int(0 + dy)))


def ScaleRotateTranslate(
    image, angle, center=None, new_center=None, scale=None, expand=False
):
    if center is None:
        return image.rotate(angle)
    angle = -angle / 180.0 * math.pi
    nx, ny = x, y = center
    sx = sy = 1.0
    if new_center:
        (nx, ny) = new_center
    if scale:
        (sx, sy) = scale
    cosine = math.cos(angle)
    sine = math.sin(angle)
    a = cosine / sx
    b = sine / sx
    c = x - nx * a - ny * b
    d = -sine / sy
    e = cosine / sy
    f = y - nx * d - ny * e
    return image.transform(
        image.size, Image.AFFINE, (a, b, c, d, e, f), resample=Image.BICUBIC
    )


## Need someway to "cluster" the seeds
def colorSeeds():
    # Toggle the overall visibility of the color edge streaks
    if random.random() < config.edgeSeedColorsVisibleChangeProb:
        config.edgeSeedColorsVisible = (
            True if config.edgeSeedColorsVisible == False else False
        )

    if (
        random.random() < config.edgeSeedColorsDrawProb
        and config.edgeSeedColorsVisible == True
    ):
        num = round(random.uniform(1, 10))

        if random.random() < 0.02:
            config.yPosRangeMin = round(random.uniform(0, config.canvasImageHeight))
            config.yPosRangeMax = round(
                random.uniform(config.yPosRangeMin, config.canvasImageHeight)
            )

        for i in range(1, num):
            yPos = round(random.uniform(config.yPosRangeMin, config.yPosRangeMax))
            xPos = 0
            w = round(random.uniform(2, 3))
            h = round(random.uniform(2, 4))
            greenLevel = round(random.uniform(120, 200))
            config.draw.rectangle(
                (xPos, yPos, xPos + w, yPos + h),
                fill=(220, greenLevel, 0, 200),
                outline=None,
            )


"""""" """""" """""" """""" """""" """""" """""" """""" """""" """""" ""
## Setup and run functions


def main(run=True):
    global config, directionOrder
    global workConfig
    print("---------------------")
    print("SIGNAGE Loaded")

    colorutils.brightness = config.brightness
    config.canvasImageWidth = config.screenWidth
    config.canvasImageHeight = config.screenHeight
    config.canvasImageWidth -= 4
    config.canvasImageHeight -= 4
    config.delay = float(workConfig.get("signage", "redrawDelay"))

    config.baseRotation = config.rotation

    config.fontColorVals = (workConfig.get("signage", "fontColor")).split(",")
    config.fontColor = tuple(
        map(lambda x: int(int(x) * config.brightness), config.fontColorVals)
    )
    config.outlineColorVals = (workConfig.get("signage", "outlineColor")).split(",")
    config.outlineColor = tuple(
        map(lambda x: int(int(x) * config.brightness), config.outlineColorVals)
    )

    config.useOverLayImage = workConfig.getboolean("signage", "useOverLayImage")
    config.coordinatedColorChange = workConfig.getboolean(
        "signage", "coordinatedColorChange"
    )
    config.overLayImage = workConfig.get("signage", "overLayImage")
    config.overLayXPos = int(workConfig.get("signage", "overLayXPos"))
    config.overLayYPos = int(workConfig.get("signage", "overLayYPos"))
    config.overLayXPosInit = config.overLayXPos
    config.overLayYPosInit = config.overLayYPos

    config.imageGlitchSize = int(workConfig.get("signage", "imageGlitchSize"))
    config.overlayGlitchSize = int(workConfig.get("signage", "overlayGlitchSize"))
    config.overlayBrightness = float(workConfig.get("signage", "overlayBrightness"))
    config.overlayGlitchRate = float(workConfig.get("signage", "overlayGlitchRate"))
    config.fullimageGiltchRate = float(workConfig.get("signage", "fullimageGiltchRate"))
    config.overlayResetRate = float(workConfig.get("signage", "overlayResetRate"))
    config.unhideRate = float(workConfig.get("signage", "unhideRate"))
    config.rehideRate = float(workConfig.get("signage", "rehideRate"))

    config.timeTrigger = workConfig.getboolean("signage", "timeTrigger")
    config.tLimitBase = int(workConfig.get("signage", "tLimitBase"))
    config.colOverlay = coloroverlay.ColorOverlay()
    config.colOverlay.randomSteps = False
    config.colOverlay.timeTrigger = True
    config.colOverlay.tLimitBase = config.tLimitBase
    config.colOverlay.maxBrightness = config.brightness
    config.unHideGrid = False
    config.colOverlay.colorTransitionSetup()

    ## Used for side seed colors
    config.yPosRangeMin = round(random.uniform(0, config.canvasImageHeight))
    config.yPosRangeMax = round(
        random.uniform(config.yPosRangeMin, config.canvasImageHeight)
    )

    config.unitArray = []

    try:
        config.bgAlpha = int(workConfig.get("signage", "bgAlpha"))
    except Exception as e:
        print(str(e))
        config.bgAlpha = 216

    try:
        config.useEdgeSeedColors = workConfig.getboolean("signage", "useEdgeSeedColors")
        config.edgeSeedColorsDrawProb = float(
            workConfig.get("signage", "edgeSeedColorsDrawProb")
        )
        config.edgeSeedColorsVisibleChangeProb = float(
            workConfig.get("signage", "edgeSeedColorsVisibleChangeProb")
        )
        config.edgeSeedColorsVisible = True
    except Exception as e:
        print(str(e))
        config.useEdgeSeedColors = False
        config.edgeSeedColorsVisible = False

    try:
        config.randomRotation = workConfig.getboolean("signage", "randomRotation")
    except Exception as e:
        print(str(e))
        config.randomRotation = False

    try:
        config.showGrid = workConfig.getboolean("signage", "showGrid")
    except Exception as e:
        print(str(e))
        config.showGrid = False

    try:
        config.showText = workConfig.getboolean("signage", "showText")
    except Exception as e:
        print(str(e))
        config.showText = True

    try:
        config.showOutline = workConfig.getboolean("signage", "showOutline")
    except Exception as e:
        print(str(e))
        config.showOutline = True

    try:
        config.imageXOffset = int(workConfig.get("displayconfig", "imageXOffset"))
    except Exception as e:
        print(str(e))
        config.imageXOffset = 0

    try:
        config.steps = int(workConfig.get("displayconfig", "steps"))
    except Exception as e:
        print(str(e))
        config.steps = 200


    try:
        palettesToUse = (workConfig.get("signage", "palettesToUse")).split(',')
        config.paletteChangeProb = float(workConfig.get("signage", "paletteChangeProb"))

        config.palettes = []
        for i in range(0, len(palettesToUse)):
            name = palettesToUse[i]
            vals = (workConfig.get("signage", name)).split(",")
            config.palettes.append( tuple(map(lambda x: float(x), vals)))
        
        config.paletteDropHueMin = int(workConfig.get("signage", "dropHueMin"))
        config.paletteDropHueMax = int(workConfig.get("signage", "dropHueMax"))
    except Exception as e:
        print(str(e))
        palettesToUse = ['base']
        config.paletteChangeProb = .00

        config.palettes = []
        for i in range(0, len(palettesToUse)):
            name = palettesToUse[i]
            vals = [0,360,0,1.0,0,1.0]
            config.palettes.append( tuple(map(lambda x: float(x), vals)))
        
        config.paletteDropHueMin = 0
        config.paletteDropHueMax = 0


    config.colOverlay.steps = config.steps

    try:
        config.tileSizeWidth = int(workConfig.get("signage", "tileSizeWidth"))
        config.tileSizeHeight = int(workConfig.get("signage", "tileSizeHeight"))
    except Exception as e:
        print(str(e))
        config.tileSizeWidth = int(workConfig.get("displayconfig", "tileSizeWidth"))
        config.tileSizeHeight = int(workConfig.get("displayconfig", "tileSizeHeight"))

    try:
        config.rows = int(workConfig.get("signage", "rows"))
        config.cols = int(workConfig.get("signage", "cols"))
    except Exception as e:
        print(str(e))
        config.rows = int(workConfig.get("displayconfig", "rows"))
        config.cols = int(workConfig.get("displayconfig", "cols"))
        
    try:
        config.gridSpacing = int(workConfig.get("signage", "gridSpacing"))
        config.magingSpacing = int(workConfig.get("signage", "magingSpacing"))
    except Exception as e:
        print(str(e))
        config.gridSpacing = 0
        config.magingSpacing = 0
        
    try:
        config.choosePaletteForEachTile= workConfig.getboolean("signage", "choosePaletteForEachTile")
    except Exception as e:
        print(str(e))
        config.choosePaletteForEachTile = False

    """""" """""" """""" """""" """""" """""" """""" """""" """""" """"""

    config.canvasImage = Image.new(
        "RGBA", (config.canvasImageWidth, config.canvasImageHeight)
    )
    config.fontSize = 14
    config.font = ImageFont.truetype(
        config.path + "/assets/fonts/freefont/FreeSansBold.ttf", config.fontSize
    )

    setUp()

    if run:
        runWork()


def setUp():
    global config
    if config.useOverLayImage == True:
        arg = config.path + config.overLayImage
        config.loadedImage = Image.open(arg, "r")
        config.loadedImage.load()

        config.enhancer = ImageEnhance.Brightness(config.loadedImage)
        config.loadedImage = config.enhancer.enhance(config.overlayBrightness)
        config.loadedImageCopy = config.loadedImage.copy()
    makeGrid()


def runWork():
    global blocks
    print(bcolors.OKGREEN + "** " + bcolors.BOLD)
    print("RUNNING signage.py")
    print(bcolors.ENDC)
    # gc.enable()
    while True:
        iterate()
        time.sleep(config.delay)


def iterate():

    global config
    if config.showGrid == True:
        # showGrid()
        redrawGrid()


        if random.random() < config.filterRemappingProb:
            if config.useFilters == True and config.filterRemapping == True:
                config.filterRemap = True

                startX = round(random.uniform(0,config.canvasWidth - config.filterRemapminHoriSize) )
                startY = round(random.uniform(0,config.canvasHeight - config.filterRemapminVertSize) )
                endX = round(random.uniform(startX+config.filterRemapminHoriSize,config.canvasWidth) )
                endY = round(random.uniform(startY+config.filterRemapminVertSize,config.canvasHeight) )
                config.remapImageBlockSection = [startX,startY,endX,endY]
                config.remapImageBlockDestination = [startX,startY]
    else:
        displayTest()


"""""" """""" """""" """""" """""" """""" """""" """""" """""" """""" ""
