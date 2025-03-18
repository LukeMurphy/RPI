# ################################################### #
import math
import random
import sys
import time

from numpy import true_divide
from modules.configuration import bcolors
from modules import coloroverlay, colorutils
from modules.holder_director import Holder
from modules.holder_director import Director
from PIL import Image, ImageDraw, ImageEnhance, ImageFont, ImageOps, ImageChops


class Marquee:

    pattern = []
    perimeter = []
    clrs = []
    p0 = []

    innerWidth = 0
    innerHeight = 0
    marqueeWidth = 0
    step = 1
    offset = 0
    speed = 1

    reverse = False
    proportionalPatternSize = False
    aliasMode = True

    advanceStep = 0
    advanceStepMax = 2
    aliasAlpha = 255
    # colOverlayA = coloroverlay.ColorOverlay()
    # colOverlayB = coloroverlay.ColorOverlay()

    def __init__(self):
        self.p0 = []

    def setUp(self):
        pass

    ## Creates a series of little boxes -- not efficient but useful if you wanted to make some kind of chasing
    ## gradient marquee and better to get animation travel speed down as slow as possible

    def makeMarquee(self):

        o = 0
        self.perimeter = []
        # self.stepSize = round(self.step / self.marqueeWidth)
        self.stepSize = round(self.marqueeWidth / self.step)
        if self.stepSize == 0:
            self.stepSize = 1

        if self.proportionalPatternSize:
            self.stepSize = 1

        # self.stepSize = 5

        self.speed = max(1 / self.stepSize, 1)
        self.speed = 1
        self.stepSize = 1

        # Right
        self.perimeter.extend(
            [self.p0[0] + self.innerWidth, i, self.marqueeWidth, self.stepSize]
            for i in range(
                self.p0[1],
                self.p0[1] + self.innerHeight + self.marqueeWidth,
                self.stepSize,
            )
        )
        # Bottom
        self.perimeter.extend([i, self.p0[1] + self.innerHeight, self.stepSize, self.marqueeWidth] for i in range(self.p0[0] + self.innerWidth - 1, self.p0[0] - 1, -self.stepSize))
        # Left
        self.perimeter.extend([self.p0[0], i, self.marqueeWidth, self.stepSize] for i in range(self.p0[1] + self.innerHeight, self.p0[1], -self.stepSize))
        # Top
        self.perimeter.extend(
            [i, self.p0[1], self.stepSize, self.marqueeWidth]
            for i in range(
                self.p0[0],
                self.p0[0] + self.innerWidth + self.marqueeWidth,
                self.stepSize,
            )
        )


    def advance(self):
        count = 0
        perim = reversed(self.perimeter) if self.reverse == True else self.perimeter
        _alpha = 255
        l = len(self.pattern)
        patternA = self.pattern[: l - round(self.offset)]
        patternB = self.pattern[(l - round(self.offset)) : l]
        pattern = patternB + patternA

        self.colOverlayA.stepTransition()
        self.colOverlayB.stepTransition()

        for p in perim:
            if pattern[count] == 1:
                clr = self.colOverlayA.currentColor
            else:
                clr = self.colOverlayB.currentColor
            # print(clr)
            self.configDraw.rectangle(
                (p[0], p[1], p[0] + p[2], p[1] + p[3]),
                outline=None,
                fill=(round(clr[0]), round(clr[1]), round(clr[2]), _alpha),
            )
            if self.aliasMode:
                # just x pseudo anti-aliasing for now
                self.configDraw.rectangle(
                    (p[0] - 1, p[1] - 1, p[0] + p[2] + 0, p[1] + p[3] + 0),
                    outline=None,
                    fill=(round(clr[0]), round(clr[1]), round(clr[2]), round(self.aliasAlpha)),
                )
            count += 1
            if count >= len(pattern):
                count = 0

        if self.advanceStep == self.advanceStepMax - 2:
            self.offset += self.speed
            self.advanceStep = 0
        else:
            self.offset += 0
            self.advanceStep += 1

        if self.offset >= len(pattern):
            self.offset = 0




def setTwoColors(_index = 0):  # sourcery skip: extract-duplicate-method
    _palette1 = config.palettes[_index][0]
    colOverlayA = coloroverlay.ColorOverlay()
    colOverlayA.minHue = _palette1.minHue
    colOverlayA.maxHue = _palette1.maxHue
    colOverlayA.minSaturation = _palette1.minSaturation
    colOverlayA.maxSaturation = _palette1.maxSaturation
    colOverlayA.minValue = _palette1.minValue 
    colOverlayA.maxValue = _palette1.maxValue
    colOverlayA.randomRange = (config.randomRangeMin, config.randomRangeMax)
    # colOverlayA.steps = 225 + round(125 * random.random())
    colOverlayA.tLimit = 2 + round(15 * random.random())
    colOverlayA.tLimitBase = 2 + round(25 * random.random())
    colOverlayA.colorTransitionSetup()


    _palette2 = config.palettes[_index][1]
    colOverlayB = coloroverlay.ColorOverlay()
    colOverlayB.minHue = _palette2.minHue
    colOverlayB.maxHue = _palette2.maxHue
    colOverlayB.minSaturation = _palette2.minSaturation
    colOverlayB.maxSaturation = _palette2.maxSaturation
    colOverlayB.minValue = _palette2.minValue 
    colOverlayB.maxValue = _palette2.maxValue 
    colOverlayB.randomRange = (config.randomRangeMin, config.randomRangeMax)
    # colOverlayB.steps = 225 + round(125 * random.random())
    colOverlayB.tLimit = 2 + round(15 * random.random())
    colOverlayB.tLimitBase = 2 + round(25 * random.random())
    colOverlayB.colorTransitionSetup()


    return (colOverlayA, colOverlayB)


def loadPalette(_paletteName):
    paletteObj = Holder()
    # background
    # tLimitBase = int(workConfig.get(palette, "tLimitBase"))
    paletteObj.minHue = float(workConfig.get(_paletteName, "minHue"))
    paletteObj.maxHue = float(workConfig.get(_paletteName, "maxHue"))
    paletteObj.minSaturation = float(workConfig.get(_paletteName, "minSaturation"))
    paletteObj.maxSaturation = float(workConfig.get(_paletteName, "maxSaturation"))
    paletteObj.minValue = float(workConfig.get(_paletteName, "minValue"))
    paletteObj.maxValue = float(workConfig.get(_paletteName, "maxValue"))
    paletteObj.name = _paletteName
    return paletteObj


def changePalettes():
    # palette = math.floor(random.uniform(0, len(list(config.palettes.keys()))))
    # config.usePalette = list(config.palettes.keys())[palette]
    # print("New Palette:{}".format(config.usePalette))

    _newPaletteIndex = math.floor(random.uniform(0,len(config.palettes)))
    for _m in config.marquees:
        # print(f"marqee {_m} {_m.colOverlayA} {_m.colOverlayB}")
        newUnitColors = setTwoColors(_newPaletteIndex)
        _m.colOverlayA = newUnitColors[0]
        _m.colOverlayB = newUnitColors[1]

    setBackgroundColor(newUnitColors[0])

    if random.random() < config.rebuildAllProb and config.maxRandomGap != 0:
        config.marqueeGap = round(random.uniform(1, config.maxRandomGap))
        init()
    

def setBackgroundColor(_overlay = None):
    if _overlay :
        config.bgColor = _overlay
    else :
        config.bgColor = coloroverlay.ColorOverlay()
        config.bgColor.randomRange = (config.randomRangeMin, config.randomRangeMax)
        config.bgColor.colorTransitionSetup()

## The pattern controls the dash size - each 1 or 0 represents the width of one small
## building block for the two-color dash

# pattern = [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
# if(config.step > 2) : pattern = [1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0]
# pattern = [1,1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0]
# pattern = [1,1,1,0,0,0]
# pattern = [1,0,1,0,0,1,0,0,1,0,1]

def init():
    global config
    config.draw.rectangle((0, 0, config.screenWidth, config.screenHeight), fill=(0, 0, 0, 255))

    pattern = []
    pattern.extend(1 for _ in range(config.baseDashSize))
    pattern.extend((0 for _ in range(config.baseDashSize)))

    p0 = [config.imageXOffset, config.imageYOffset]
    marqueeWidth = config.marqueeWidth
    innerWidth = config.screenWidth - marqueeWidth
    innerHeight = config.screenHeight - marqueeWidth
    marqueeWidthPrev = marqueeWidth

    step = config.step
    decrement = config.decrement

    config.marquees = []

    _newPaletteIndex = math.floor(random.uniform(0,len(config.palettes)))
    unitColors = setTwoColors(_newPaletteIndex)
    setBackgroundColor(unitColors[0])

    # If this is 1 then offsets the gap...
    eveningGap = 2

    for i in range(config.marqueeNum):
        clrs = [colorutils.randomColor(), colorutils.randomColorAlpha(255, 255)]

        if config.multiColor :
            unitColors = setTwoColors()

        if i != 0:
            marqueeWidth = marqueeWidthPrev - decrement

        marqueeWidth = max(marqueeWidth, 2)
        if innerWidth < 32 or i > 6:
            step = 1

        mq = Marquee()
        mq.pattern = pattern
        mq.p0 = p0
        mq.innerWidth = innerWidth
        mq.innerHeight = innerHeight
        mq.marqueeWidth = marqueeWidth
        mq.step = i + 1 if config.proportionalPatternSize else config.step
        mq.clrs = clrs
        mq.colOverlayA = unitColors[0]
        mq.colOverlayB = unitColors[1]
        mq.configDraw = config.draw
        mq.reverse = i % 2 > 0
        mq.proportionalPatternSize = config.proportionalPatternSize
        mq.advanceStepMax = config.advanceStepMax
        mq.aliasMode = config.aliasMode
        mq.aliasAlpha = config.aliasAlpha
        mq.makeMarquee()
        config.marquees.append(mq)

        p0[0] += marqueeWidth + config.marqueeGap
        p0[1] += marqueeWidth + config.marqueeGap
        marqueeWidthPrev = marqueeWidth + 1

        innerWidth = innerWidth - 2 * (marqueeWidth) - config.marqueeGap * eveningGap + decrement
        innerHeight = innerHeight - 2 * (marqueeWidth) - config.marqueeGap * eveningGap + decrement

        if config.marqueeGap > 0:
            innerWidth -= decrement
            innerHeight -= decrement

        if marqueeWidth == 2:
            innerWidth -= 1
            innerHeight -= 1

        if len(pattern) >= 4 and random.random() > 0.1:
            pattern = pattern[1:]
            pattern = pattern[:-1]


def animate():
    config.animationController.checkTime()
    if config.animationController.advance:
        config.bgColor.stepTransition()
        bgColor = tuple(round(c) for c in config.bgColor.currentColor)
        # config.draw.rectangle((0, 0, config.screenWidth, config.screenHeight), fill=(0, 0, 0, 10))
        config.draw.rectangle((0, 0, config.screenWidth, config.screenHeight), fill=bgColor)
        for mq in config.marquees:
            mq.advance()


def redraw():
    global config
    mcount = 0

    # if config.interImages != 0:

    #     # config.interImage1 = Image.blend(config.interImage1, config.image, 1/config.interImages)

    #     if config.interImageState == 0 :
    #         # config.displayImage.paste(config.image, (0,0), config.image)
    #         # animate()
    #         # print("Animate")
    #         # config.interImage1 = Image.blend(config.interImage1, config.image, 1/config.interImages)
    #         # config.interImage1.paste(config.displayImage, (0,0), config.displayImage)
    #         temp = Image.blend(config.displayImage, config.image, config.interImageState/config.interImages)
    #     if config.interImageState > 0:
    #         temp = Image.blend(config.displayImage, config.image, config.interImageState/config.interImages)

    #     config.interImageState += 1
    #     if config.interImageState == config.interImages :
    #         animate()
    #         config.interImageState = 0
    #         # config.interImage1.paste(config.image, (0,0), config.image)
    #         # temp.paste(config.image, (0,0), config.image)
    #         # animate()
    #         config.displayImage.paste(config.image, (0,0), config.image)
    #         # print("paste\n")
    #     config.render(temp, 0, 0, config.screenWidth, config.screenHeight)
    # else :
    animate()
    config.render(config.image, 0, 0, config.screenWidth, config.screenHeight)


def runWork():
    global config
    print(f"{bcolors.OKGREEN}** {bcolors.BOLD}")
    print("Running marquee_2.py")
    print(bcolors.ENDC)

    while config.isRunning:
        config.directorController.checkTime()
        if config.directorController.advance:
            iterate()
        time.sleep(config.redrawSpeed)
        if config.standAlone == False:
            config.callBack()


def iterate():
    global config
    # animate()
    redraw()
    checkTime()

    if config.marqueeTimerDelta > config.changePaletteInterval:
        if random.random() < 0.5:
            changePalettes()

        config.marqueeTimerDelta = 0
        config.marqueeTimer1 = time.time()


def main(run=True):
    global config
    global workConfig
    config.image = Image.new("RGBA", (config.screenWidth, config.screenHeight))
    config.displayImage = Image.new("RGBA", (config.screenWidth, config.screenHeight))
    config.interImage1 = Image.new("RGBA", (config.screenWidth, config.screenHeight))
    config.interImageState = 0

    config.draw = ImageDraw.Draw(config.image)
    config.redrawSpeed = float(workConfig.get("marquee", "redrawSpeed"))
    config.marqueeWidth = int(workConfig.get("marquee", "marqueeWidth"))
    config.baseDashSize = int(workConfig.get("marquee", "baseDashSize"))
    config.marqueeGap = int(workConfig.get("marquee", "gap"))
    config.maxRandomGap = int(workConfig.get("marquee", "maxRandomGap"))
    config.rebuildAllProb = float(workConfig.get("marquee", "rebuildAllProb"))

    config.step = int(workConfig.get("marquee", "step"))
    config.advanceStepMax = int(workConfig.get("marquee", "advanceStepMax"))
    config.aliasAlpha = int(workConfig.get("marquee", "aliasAlpha"))
    config.aliasMode = workConfig.getboolean("marquee", "aliasMode")
    if not config.aliasMode:
        config.advanceStepMax = 2
    config.animationRate = float(workConfig.get("marquee", "animationRate"))
    # config.interImages = int(workConfig.get("marquee", "interImages"))

    config.proportionalPatternSize = workConfig.getboolean("marquee", "proportionalPatternSize")
    config.multiColor = workConfig.getboolean("marquee", "multiColor")
    config.changePaletteInterval = int(workConfig.get("marquee", "changePaletteInterval"))
    config.decrement = int(workConfig.get("marquee", "decrement"))
    config.marqueeNum = int(workConfig.get("marquee", "marqueeNum"))
    config.randomRangeMin = int(workConfig.get("marquee", "randomRangeMin"))
    config.randomRangeMax = int(workConfig.get("marquee", "randomRangeMax"))
    config.proportionalPatternSize = workConfig.getboolean("marquee", "proportionalPatternSize")

    colorutils.brightness = float(workConfig.get("displayconfig", "brightness"))
    config.xOffset = 15

    config.paletteSets = workConfig.get("marquee", "paletteSets").split("|")
    config.paletteSetNames = workConfig.get("marquee", "paletteSets").split(",")
    config.palettes = []

    for _ps in config.paletteSets:
        _paletteSetNames = _ps.split(",")
        _palette = []
        for i in range(2):
            _psm = _paletteSetNames[i].replace(" ", "")
            _p = loadPalette(_psm)
            _palette.append(_p)
            print(f" ==> Loaded this palette (grouped in twos): {_p.name}")
        config.palettes.append(_palette)


    config.marqueeTimerDelta = 0
    config.marqueeTimer1 = time.time()

    config.directorController = Director(config)
    config.redrawSpeed = float(workConfig.get("marquee", "redrawSpeed"))
    config.directorController.slotRate = float(workConfig.get("marquee", "slotRate"))

    config.animationController = Director(config)
    config.animationController.slotRate = config.animationRate

    init()

    if run:
        runWork()


def checkTime():
    global config
    t = time.time()
    config.marqueeTimerDelta = t - config.marqueeTimer1


#########
