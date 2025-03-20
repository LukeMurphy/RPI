# ################################################### #
import math
import random
import time
from modules.configuration import bcolors
from modules import coloroverlay, colorutils
from PIL import Image, ImageDraw, ImageEnhance, ImageFont, ImageOps


""" ----------------------------------------------------------------------------------- """


class ColorPalette:

    def __init__(self):
        pass


class SlotMaker:
    """docstring for SlotMaker"""

    numberOfSlots = 0
    slotHeight = 100
    slotWidth = 4
    slotSpacing = 1
    xPos = 0
    yPos = 0

    def __init__(self, config):

        super(SlotMaker, self).__init__()
        self.config = config
        self.directorArray = []
        self.angleOffset = 0
        self.angleGap = 1
        self.innerRadius = 10
        self.outerRadius = 100
        self.orientation = 1

    def setUpLinears(self):
        self.slotArray = []
        for _ in range(self.numberOfSlots):
            s = Slot()
            self.slotArray.append(s)

        self.setUpPositions()

    def setUpPositions(self):

        jitterAmount = round(random.uniform(0, config.jitterAmount))
        for i in range(len(self.slotArray)):
            s = self.slotArray[i]
            jitter = 0
            s.width = self.slotWidth
            s.height = self.slotHeight
            spacing = self.slotSpacing

            s.width -= 1
            if i % self.config.jitterFreq == 0:
                jitter = jitterAmount
            s.xPos = self.xPos + s.width * i + spacing * i
            s.yPos = self.yPos + jitter

            s.xPos2 = self.xPos + s.width * i + spacing * i + s.width
            s.yPos2 = self.yPos + jitter

            s.xPos3 = self.xPos + s.width * i + spacing * i + s.width
            s.yPos3 = self.yPos + s.height + jitter

            s.xPos4 = self.xPos + s.width * i + spacing * i
            s.yPos4 = self.yPos + s.height + jitter

            if self.orientation == -1:
                s.xPos = self.xPos + jitter
                s.yPos = self.yPos + s.width * i + spacing * i
                s.xPos2 = self.xPos + jitter
                s.yPos2 = self.yPos + s.width * i + spacing * i + s.width
                s.xPos3 = self.xPos + s.height + jitter
                s.yPos3 = self.yPos + s.width * i + spacing * i + s.width
                s.xPos4 = self.xPos + s.height + jitter
                s.yPos4 = self.yPos + s.width * i + spacing * i

    def setUpRadials(self):

        rads = 2 * math.pi / self.numberOfSlots
        for i in range(self.numberOfSlots):
            s = Slot()
            s.width = self.slotWidth
            s.height = self.slotHeight
            spacing = self.slotSpacing
            a1 = i * rads + self.angleOffset
            a2 = (i + self.angleGap) * rads + self.angleOffset
            s.xPos = self.xPos + math.cos(a1) * self.innerRadius
            s.yPos = self.yPos + math.sin(a1) * self.innerRadius
            s.xPos2 = self.xPos + math.cos(a1) * self.outerRadius
            s.yPos2 = self.yPos + math.sin(a1) * self.outerRadius

            s.xPos3 = self.xPos + math.cos(a2) * self.outerRadius
            s.yPos3 = self.yPos + math.sin(a2) * self.outerRadius
            s.xPos4 = self.xPos + math.cos(a2) * self.innerRadius
            s.yPos4 = self.yPos + math.sin(a2) * self.innerRadius

            s.angle = i * rads
            self.slotArray.append(s)


class Slot:
    """docstring for Slot"""

    def __init__(self):

        super(Slot, self).__init__()
        self.xPos = 0
        self.yPos = 0
        self.width = 0
        self.height = 0
        self.backgroundColor = (0, 0, 0, 0)
        self.r = 0
        self.g = 0
        self.b = 0
        self.a = 0

    def renderRect(self, ref):

        self.backgroundColor = tuple(round(x) for x in [self.r, self.g, self.b, self.a])
        p1 = (self.xPos, self.yPos)
        p2 = (self.xPos + self.width, self.yPos)
        p3 = (self.xPos + self.width, self.yPos + self.height)
        p4 = (self.xPos, self.yPos + self.height)

        ref.polygon((p1, p2, p3, p4), fill=self.backgroundColor)
        # ref.rectangle((self.xPos, self.yPos, self.xPos + self.width, self.yPos + self.height), fill=self.backgroundColor)

    def render(self, ref):

        self.backgroundColor = tuple(round(x) for x in [self.r, self.g, self.b, self.a])
        p1 = (self.xPos, self.yPos)
        p2 = (self.xPos2, self.yPos2)
        p3 = (self.xPos3, self.yPos3)
        p4 = (self.xPos4, self.yPos4)

        ref.polygon((p1, p2, p3, p4), fill=self.backgroundColor)
        # ref.rectangle((self.xPos, self.yPos, self.xPos + self.width, self.yPos + self.height), fill=self.backgroundColor)


class Director:
    """docstring for Director"""

    targetSlotArray = []
    currentSlot = 0
    totalSlots = 0
    slotRate = 0.02
    advance = False
    color = [255, 255, 255]
    direction = 1

    def __init__(self, config):
        super(Director, self).__init__()
        self.config = config
        self.tT = time.time()

    def setUpSlots(self):
        s = SlotMaker(self.config)
        s.numberOfSlots = config.numerOfSlotsMin + round(random.random() * config.numerOfSlotsMax)
        s.slotSpacing = round(random.uniform(config.slotSpacingMin, config.slotSpacingMax))
        s.slotWidth = round(random.uniform(config.slotWidthMin, config.slotWidthMax))
        s.slotHeight = round(random.uniform(config.slotHeightMin, config.slotHeightMax))

        s.orientation = 1 if random.random() > config.orientationProb else -1

        if s.orientation == 1:
            s.yPos = round(random.random() * config.yRange)
            s.xPos = 0
            s.numberOfSlots = round(config.canvasWidth / (s.slotWidth + s.slotSpacing / 2))
        else:
            s.xPos = round(random.random() * config.xRange)
            s.yPos = 0
            s.numberOfSlots = round(config.canvasHeight / (s.slotWidth + s.slotSpacing / 2))

        s.setUpLinears()

        self.slotMakerRef = s
        self.orientation = s.orientation
        self.targetSlotArray = s.slotArray
        self.color = newColor(config.activeColorPalette) if self.orientation == 1 else newColorAlt(config.activeColorPalette)
        self.direction = 1 if random.random() > 0.5 else -1
        if self.orientation == 1:
            self.slotRate = random.uniform(self.config.slotSpeed2Min, self.config.slotSpeed2Max)
        else:
            self.slotRate = random.uniform(self.config.slotSpeedMin, self.config.slotSpeedMax)
        # s.directorArray.append(d)

    def checkTime(self):
        if (time.time() - self.tT) >= self.slotRate:
            self.tT = time.time()
            self.advance = True
        else:
            self.advance = False

    def next(self):

        self.checkTime()

        if self.advance == True:
            # self.targetSlotArray[self.currentSlot].backgroundColor = (0,0,255,255)
            self.currentSlot += self.direction
            reset = False

            if self.currentSlot >= len(self.targetSlotArray):
                self.currentSlot = 0
                reset = True

            if self.currentSlot < 0:
                self.currentSlot = len(self.targetSlotArray) - 1
                reset = True

            if reset:
                if self.orientation == 1:
                    self.slotRate = random.uniform(self.config.slotSpeed2Min, self.config.slotSpeed2Max)
                else:
                    self.slotRate = random.uniform(self.config.slotSpeedMin, self.config.slotSpeedMax)
                # self.direction *= -1

                if self.orientation == 1:
                    self.color = newColor(config.activeColorPalette)
                    self.slotMakerRef.yPos = round(random.random() * self.config.yRange)
                else:
                    self.color = newColorAlt(config.activeColorPalette)
                    self.slotMakerRef.xPos = round(random.random() * self.config.xRange)
                self.slotMakerRef.setUpPositions()
            self.targetSlotArray[self.currentSlot].r = self.color[0]
            self.targetSlotArray[self.currentSlot].g = self.color[1]
            self.targetSlotArray[self.currentSlot].b = self.color[2]
            self.targetSlotArray[self.currentSlot].a = self.color[3]

            self.targetSlotArray[self.currentSlot].r = min(self.targetSlotArray[self.currentSlot].r, 255)
            self.targetSlotArray[self.currentSlot].g = min(self.targetSlotArray[self.currentSlot].g, 255)
            self.targetSlotArray[self.currentSlot].b = min(self.targetSlotArray[self.currentSlot].b, 255)
            self.targetSlotArray[self.currentSlot].a = min(self.targetSlotArray[self.currentSlot].a, 255)

        self.targetSlotArray[self.currentSlot].render(self.config.draw)


""" ----------------------------------------------------------------------------------- """


def newColor(arg=0):

    cp = config.colorPalettes[arg]
    return colorutils.getRandomColorHSV(
        cp.bg_minHue,
        cp.bg_maxHue,
        cp.bg_minSaturation,
        cp.bg_maxSaturation,
        cp.bg_minValue,
        cp.bg_maxValue,
        cp.bg_dropHueMinValue,
        cp.bg_dropHueMaxValue,
        round(random.uniform(cp.bg_minAlpha, cp.bg_maxAlpha)),
    )


def newColorAlt(arg=0):
    cp = config.colorPalettes[arg]
    return colorutils.getRandomColorHSV(
        cp.lines_minHue,
        cp.lines_maxHue,
        cp.lines_minSaturation,
        cp.lines_maxSaturation,
        cp.lines_minValue,
        cp.lines_maxValue,
        cp.lines_dropHueMinValue,
        cp.lines_dropHueMaxValue,
        round(random.uniform(cp.lines_minAlpha, cp.lines_maxAlpha)),
    )


def main(run=True):
    global config
    global expandingRingss
    global workConfig

    expandingRingss = []
    config.image = Image.new("RGBA", (config.canvasWidth, config.canvasHeight))
    config.draw = ImageDraw.Draw(config.image)

    config.redrawSpeed = float(workConfig.get("forms", "redrawSpeed"))

    config.colorPaletteSets = workConfig.get("forms", "sets").split(",")

    config.colorPalettes = []

    for s in config.colorPaletteSets:

        colorSet = ColorPalette()

        colorSet.bg_minHue = float(workConfig.get(s, "bg_minHue"))
        colorSet.bg_maxHue = float(workConfig.get(s, "bg_maxHue"))
        colorSet.bg_minSaturation = float(workConfig.get(s, "bg_minSaturation"))
        colorSet.bg_maxSaturation = float(workConfig.get(s, "bg_maxSaturation"))
        colorSet.bg_minValue = float(workConfig.get(s, "bg_minValue"))
        colorSet.bg_maxValue = float(workConfig.get(s, "bg_maxValue"))
        colorSet.bg_dropHueMinValue = float(workConfig.get(s, "bg_dropHueMinValue"))
        colorSet.bg_dropHueMaxValue = float(workConfig.get(s, "bg_dropHueMaxValue"))
        colorSet.bg_minAlpha = float(workConfig.get(s, "bg_minAlpha"))
        colorSet.bg_maxAlpha = float(workConfig.get(s, "bg_maxAlpha"))

        colorSet.lines_minHue = float(workConfig.get(s, "lines_minHue"))
        colorSet.lines_maxHue = float(workConfig.get(s, "lines_maxHue"))
        colorSet.lines_minSaturation = float(workConfig.get(s, "lines_minSaturation"))
        colorSet.lines_maxSaturation = float(workConfig.get(s, "lines_maxSaturation"))
        colorSet.lines_minValue = float(workConfig.get(s, "lines_minValue"))
        colorSet.lines_maxValue = float(workConfig.get(s, "lines_maxValue"))
        colorSet.lines_dropHueMinValue = float(workConfig.get(s, "lines_dropHueMinValue"))
        colorSet.lines_dropHueMaxValue = float(workConfig.get(s, "lines_dropHueMaxValue"))
        colorSet.lines_minAlpha = float(workConfig.get(s, "lines_minAlpha"))
        colorSet.lines_maxAlpha = float(workConfig.get(s, "lines_maxAlpha"))

        config.colorPalettes.append(colorSet)

    config.activeColorPalette = 0
    config.orientationProb = float(workConfig.get("forms", "orientationProb"))

    config.slotSpeedMultiplier = float(workConfig.get("forms", "slotSpeedMultiplier"))
    config.slotSpeedMin = float(workConfig.get("forms", "slotSpeedMin")) * config.slotSpeedMultiplier
    config.slotSpeedMax = float(workConfig.get("forms", "slotSpeedMax")) * config.slotSpeedMultiplier
    config.slotSpeed2Min = float(workConfig.get("forms", "slotSpeed2Min")) * config.slotSpeedMultiplier
    config.slotSpeed2Max = float(workConfig.get("forms", "slotSpeed2Max")) * config.slotSpeedMultiplier
    config.bgFlashRate = float(workConfig.get("forms", "bgFlashRate"))

    config.numerOfSlotsMax = int(workConfig.get("forms", "numerOfSlotsMax"))
    config.numerOfSlotsMin = int(workConfig.get("forms", "numerOfSlotsMin"))
    config.jitterAmount = int(workConfig.get("forms", "jitterAmount"))
    config.jitterAmountInit = int(workConfig.get("forms", "jitterAmount"))
    config.jitterFreq = int(workConfig.get("forms", "jitterFreq"))
    config.slotSpacingMin = int(workConfig.get("forms", "slotSpacingMin"))
    config.slotSpacingMax = int(workConfig.get("forms", "slotSpacingMax"))
    config.slotWidthMin = int(workConfig.get("forms", "slotWidthMin"))
    config.slotWidthMax = int(workConfig.get("forms", "slotWidthMax"))
    config.slotHeightMin = int(workConfig.get("forms", "slotHeightMin"))
    config.slotHeightMax = int(workConfig.get("forms", "slotHeightMax"))
    config.innerRadius = int(workConfig.get("forms", "innerRadius"))
    config.outerRadius = int(workConfig.get("forms", "outerRadius"))
    config.linesCreated = int(workConfig.get("forms", "linesCreated"))
    config.yRange = int(workConfig.get("forms", "yRange"))
    config.xRange = int(workConfig.get("forms", "xRange"))

    # alpha = less persistent images
    config.bgFillAlpha = int(workConfig.get("forms", "bgFillAlpha"))
    backgroundColor = (workConfig.get("forms", "backgroundColor")).split(",")
    config.backgroundColor = tuple(int(x) for x in backgroundColor)
    config.backgroundColorBase = tuple(int(x) for x in backgroundColor)

    backgroundFlashcolor = (workConfig.get("forms", "backgroundFlashcolor")).split(",")
    config.backgroundFlashcolor = tuple(int(x) for x in backgroundFlashcolor)
    config.backgroundFlashcolorBase = tuple(int(x) for x in backgroundFlashcolor)

    config.filterPatchProb = float(workConfig.get("forms", "filterPatchProb"))
    config.filterPatchProbOff = float(workConfig.get("forms", "filterPatchProbOff"))

    config.drawingPaths = []

    for _ in range(config.linesCreated):
        d = Director(config)
        d.setUpSlots()
        config.drawingPaths.append(d)

    """
    Every set of slots is first built or drawn out and then can have 
    any number of directors running its slots

    Each set of slots only has one SlotManager

    Each Director should probably only talk to one SlotManager because the 
    Director has to know how many slots are available etc


    """


def reDraw(config):

    for d in range(len(config.drawingPaths)):
        director = config.drawingPaths[d]
        director.next()

    if random.random() < config.bgFlashRate:
        config.draw.rectangle((0, 0, config.canvasWidth, config.canvasHeight), fill=config.backgroundFlashcolor)
        if random.random() < .5 : 
            config.backgroundColor = config.backgroundFlashcolor  
        else: 
            config.backgroundColor = config.backgroundColorBase
        config.activeColorPalette = math.floor(random.uniform(0, len(config.colorPalettes)))
        config.drawingPaths = []

        for _ in range(config.linesCreated):
            d = Director(config)
            d.setUpSlots()
            config.drawingPaths.append(d)
        """
        for d in range(len(config.drawingPaths)) :
            director = config.drawingPaths[d]
            director.currentSlot = 0

        if config.jitterAmount == 0 :
            config.jitterAmount = config.jitterAmountInit 
        else:
            config.jitterAmount = 0
        """


def iterate():
    global config, expandingRingsRing, lastRate, calibrated, cycleCount
    # config.image = Image.new("RGBA", (config.canvasWidth, config.canvasHeight))
    config.draw.rectangle((0, 0, config.canvasWidth, config.canvasHeight), fill=(config.backgroundColor[0],config.backgroundColor[1],config.backgroundColor[2], config.bgFillAlpha))

    reDraw(config)

    if random.random() < config.filterPatchProb:
        _filterPatchAction(config)
    # Don't want the patch to always be there - just little interruptions
    if random.random() < config.filterPatchProbOff:
        _noFiltering(config)
    # Do the final rendering of the composited image
    config.render(config.image, 0, 0, config.screenWidth, config.screenHeight)


def _noFiltering(config):
    # print("turning off remapping")
    config.useFilters = False
    x2 = 0
    y1 = 0
    y2 = 0

    config.remapImageBlock = True
    x1 = 0
    config.remapImageBlockSection = (x1, y1, x2, y2)
    config.remapImageBlockDestination = (x1, y1)


def _filterPatchAction(config):
    # print("should be remapping")
    config.useFilters = True
    x1 = round(random.uniform(0, config.canvasWidth))
    x2 = round(random.uniform(x1, config.canvasWidth))
    y1 = round(random.uniform(0, config.canvasHeight))
    y2 = round(random.uniform(y1, config.canvasHeight))

    config.remapImageBlock = True
    config.remapImageBlockSection = (x1, y1, x2, y2)
    config.remapImageBlockDestination = (x1, y1)


def runWork():
    global config
    print(f"{bcolors.OKGREEN}** {bcolors.BOLD}")
    print("Running slots.py")
    print(bcolors.ENDC)
    while True:
        iterate()
        time.sleep(config.redrawSpeed)
