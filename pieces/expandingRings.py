# ################################################### #
import math
import random
import time
from modules.configuration import bcolors
from modules import coloroverlay, colorutils
from PIL import Image, ImageDraw, ImageEnhance, ImageFont, ImageOps


colorutils.brightness = 1
expandingRingss = []
mode = 1

""" ----------------------------------------------------------------------------------- """


class expandingRing:

    expanding = True
    center = (0, 0)

    def __init__(self, config, i=0):
        self.config = config
        self.radialExpansion = 1
        self.color = colorutils.randomColorAlpha(1, 255, 125)
        self.colorTuple = tuple(int(i) for i in self.color)
        self.angularRotation = 0  # random.uniform(-math.pi/100,math.pi/100)
        self.unitBoxWidthExpansionRate = 0.5
        self.unitBoxHeightExpansionRate = 0.5
        self.mode = 1

    def initializeUnits(self):
        self.unitArray = []
        self.radius = 30 + round(random.uniform(10, 100))
        self.numUnits = 6 + round(
            random.uniform(config.numUnitsPerRingMin, config.numUnitsPerRingMax)
        )
        self.radians = 2 * math.pi / self.numUnits

        for i in range(0, self.numUnits):
            u = unit(self.config)
            self.unitArray.append(u)
            u.angle = self.radians * i
            u.xPos = round(self.radius * math.cos(u.angle)) + self.center[0]
            u.yPos = round(self.radius * math.sin(u.angle)) + self.center[1]
            u.center = self.center
            u.color = self.color
            u.colorTuple = tuple(int(n) for n in self.color)
            u.boxWidth = u.boxHeight = 10
            u.reDraw()

    def cleanup(self):
        del self.unitArray

    def regreshRingParameters(self):

        if self.mode == 1:
            self.color = colorutils.randomColorAlpha()
        if self.mode == 2:
            self.color = colorutils.getRedShiftedColors()
        if self.mode == 3:
            self.color = colorutils.randomGrayAlpha()

        self.radialExpansion = random.uniform(0.02, 5)
        self.angularRotation = 0  # random.uniform(-math.pi/100,math.pi/100)
        unitSizeExpansionRate = random.random()
        self.unitBoxWidthExpansionRate = unitSizeExpansionRate
        self.unitBoxHeightExpansionRate = unitSizeExpansionRate

    def expand(self):
        if self.expanding == True:
            self.radius += self.radialExpansion
            self.radialExpansion += 0.05

            if self.radius > self.config.screenWidth / 2 + 100:
                self.radius = 0
                self.regreshRingParameters()
                reset = True

            else:
                reset = False

            for u in self.unitArray:
                u.angle += self.angularRotation

                if reset == True:
                    u.boxWidth = 1
                    u.boxHeight = 1
                    u.colorTuple = tuple(int(n) for n in self.color)
                    u.length = 1

                u.boxWidth += self.unitBoxWidthExpansionRate
                u.boxHeight += self.unitBoxHeightExpansionRate
                u.xPos = round(self.radius * math.cos(u.angle)) + self.center[0]
                u.yPos = round(self.radius * math.sin(u.angle)) + self.center[1]
                u.reDraw()


""" ----------------------------------------------------------------------------------- """


class unit:
    def __init__(self, config, i=0):
        self.config = config
        self.boxWidth = 10
        self.boxHeight = 10
        self.length = 2
        self.setUp()

    def setUp(self):
        pass

    def transition(self):
        self.fillColor = tuple(
            round(a * self.config.brightness) for a in self.colOverlay.currentColor
        )
        fillColorTemp = tuple(
            round(a * self.config.brightness) for a in self.colOverlay.currentColor
        )

    def reDraw(self):
        # self.config.draw.ellipse((self.xPos - self.boxWidth/2, self.yPos -self.boxHeight/2, self.xPos + self.boxWidth/2, self.yPos + self.boxHeight/2), fill=self.colorTuple)
        # self.config.draw.rectangle((self.xPos - self.boxWidth/2, self.yPos -self.boxHeight/2, self.xPos + self.boxWidth/2, self.yPos + self.boxHeight/2), fill=self.colorTuple)

        xPos = round(self.length * math.cos(self.angle)) + self.xPos
        yPos = round(self.length * math.sin(self.angle)) + self.yPos
        self.config.draw.line(
            [(self.xPos, self.yPos), (xPos, yPos)], fill=self.colorTuple
        )
        self.length += self.config.lineRate

        if self.length <= 0.0:
            self.length = 0.1


""" ----------------------------------------------------------------------------------- """


def runWork():
    global config
    print(bcolors.OKGREEN + "** " + bcolors.BOLD)
    print("Running expandingRings.py")
    print(bcolors.ENDC)
    while True:
        iterate()
        time.sleep(config.redrawSpeed)


def iterate():
    global config, expandingRingsRing, lastRate, calibrated, cycleCount
    # config.image = Image.new("RGBA", (config.canvasWidth, config.canvasHeight))
    config.draw.rectangle(
        (0, 0, config.screenWidth, config.screenHeight), fill=(0, 0, 0, config.bgAlpha)
    )
    for ringGroup in config.ringSets:
        for ring in ringGroup["rings"]:
            ring.expand()

    config.render(config.image, 0, 0, config.screenWidth, config.screenHeight)

    if random.random() < config.modeChangeProb:
        mode = math.floor(random.uniform(0, 3)) + 1
        ringSet = math.floor(random.uniform(0, len(config.ringSets)))
        for r in config.ringSets[ringSet]["rings"]:
            r.mode = mode

            r.cleanup()
            r.initializeUnits()


def main(run=True):
    global config
    global expandingRingss
    global workConfig
    expandingRingss = []
    config.image = Image.new("RGBA", (config.canvasWidth, config.canvasHeight))
    config.draw = ImageDraw.Draw(config.image)

    config.redrawSpeed = float(workConfig.get("expandingRings", "redrawSpeed"))
    config.lineRate = float(workConfig.get("expandingRings", "lineRate"))
    config.numUnitsPerRingMax = int(
        workConfig.get("expandingRings", "numUnitsPerRingMax")
    )
    config.numUnitsPerRingMin = int(
        workConfig.get("expandingRings", "numUnitsPerRingMin")
    )
    config.bgAlpha = int(workConfig.get("expandingRings", "bgAlpha"))
    ringSets = workConfig.get("expandingRings", "ringSets")
    ringSets = ringSets.split(",")

    config.modeChangeProb = 0.01

    config.ringSets = []

    for ringGroup in ringSets:
        ringSetParams = {}
        rings = []
        numberOfRings = int(workConfig.get(ringGroup, "numberOfRings"))
        ringSetParams["numberOfRings"] = numberOfRings
        center = workConfig.get(ringGroup, "center")
        ringSetParams["center"] = tuple(int(p) for p in center.split(","))
        ringSetParams["rings"] = rings
        ringSetParams["mode"] = 3

        for n in range(0, numberOfRings):
            er = expandingRing(config)
            er.mode = ringSetParams["mode"]
            if n > 2:
                er.expanding = True
            er.center = ringSetParams["center"]
            er.initializeUnits()
            rings.append(er)

        config.ringSets.append(ringSetParams)
