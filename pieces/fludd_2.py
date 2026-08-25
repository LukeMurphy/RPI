import math
import random
import time
from modules.configuration import bcolors, pieceLogger
from modules import colorutils
from PIL import Image, ImageDraw, ImageEnhance, ImageFont, ImageOps

lastRate = 0
colorutils.brightness = 1


# ----------------------------------------------------#
class Director:
    """docstring for Director"""

    slotRate = 0.5

    def __init__(self, config):
        super(Director, self).__init__()
        self.config = config
        self.tT = time.time()

    def checkTime(self):
        if (time.time() - self.tT) >= self.slotRate:
            self.tT = time.time()
            self.advance = True
        else:
            self.advance = False

    def next(self):
        self.checkTime()


class Fludd:

    outlineColor = (1, 1, 1)
    barColor = (200, 200, 000)
    barColorStart = (0, 200, 200)
    holderColor = (0, 0, 0)
    messageClr = (200, 0, 0)
    shadowColor = (0, 0, 0)

    xPos = 1
    yPos = 1
    boxHeight = 0
    boxWidth = 0
    boxWidthDisplay = 0
    status = 0
    boxMax = 0
    rateMultiplier = 0.1
    rate = rateMultiplier * random.random()
    numRate = rate
    percentage = 0
    boxMaxAlt = 0
    var = 10

    nothingLevel = 255
    nothingChangeProbability = 0.02

    borderModel = "prism"
    nothing = "void"
    varianceMode = "independent"
    prisimBrightness = 0.5
    blackOpacity = 255

    varianceRange = [10,10]

    def __init__(self, config, flddMngr):
        pieceLogger("init PB")

        self.boxMax = config.canvasWidth - 1
        # self.boxMaxAlt = self.boxMax + int(random.uniform(10, 30) * config.canvasWidth)
        self.boxHeight = config.canvasHeight - 2
        self.config = config

        tempImage = Image.new("RGBA", (640, 640))
        draw = ImageDraw.Draw(tempImage)
        self.mainImage = Image.new("RGBA", (config.canvasWidth, config.canvasHeight))


    def setUp(self, boxMax, boxHeight):
        self.boxMax = boxMax
        self.boxMaxAlt = self.boxMax + int(random.uniform(10, 30) * config.canvasWidth)
        self.boxHeight = boxHeight
        self.config = config
        self.mainImage = Image.new("RGBA", (round(self.boxMax), round(self.boxHeight)))
        self.draw = ImageDraw.Draw(self.mainImage)


    def reDraw(self):
        var = self.var

        gray = 126
        brightness = self.config.brightness * random.random()
        light = int(brightness * self.nothingLevel)

        if self.nothing == "void":
            gray = 0
        else:
            gray = int(self.config.brightness * random.random() * self.nothingLevel / 2)
            light = 0

        # config.draw.rectangle((0,0,self.boxMax,self.boxHeight), fill = (0,0,0,100))
        # config.draw.rectangle((0,0,self.boxMax,self.boxHeight), fill = (light,light,light))
        if self.borderModel == "prism":
            outerBorder = colorutils.randomColor(self.prisimBrightness)
        else:
            outerBorder = (light, light, light)

        self.draw.rectangle((0, 0, self.boxMax, self.boxHeight), fill=outerBorder)

        if self.varianceMode == "independent":
            self._polygonDrawing(var, gray)
        elif self.varianceMode == "symmetrical":
            svar = random.uniform(0, var)
            symBoxWidth = self.boxMax - svar
            symBoxHeight = self.boxHeight - svar
            xy0 = svar

            self.draw.rectangle(
                (xy0, xy0, max(symBoxWidth,xy0), max(symBoxHeight,xy0)),
                fill=(gray, gray, gray, self.blackOpacity),
            )

        elif self.varianceMode == "asymmetrical":
            self._asymmetricalDrawing(var, gray)

        if random.random() < self.nothingChangeProbability:
            self.nothingLevel = random.uniform(1, 255)
            # pieceLogger(f"self.nothingLevel changed to : {self.nothingLevel}")

        if random.random() < self.blacknessChangeProbability:
            self.blackOpacity = int(random.uniform(1, 255))
            # pieceLogger(f"self.blackOpacity changed to : {self.blackOpacity}")


    def _asymmetricalDrawing(self, var, gray):
        svarw = random.uniform(0, var)
        svarh = random.uniform(0, var)
        symBoxWidth = self.boxMax - svarw
        symBoxHeight = self.boxHeight - svarh
        xPos1 = self.boxMax - symBoxWidth
        yPos1 = self.boxHeight - symBoxHeight
        self.draw.rectangle(
            (xPos1, yPos1, max(symBoxWidth,xPos1), max(symBoxHeight,yPos1)),
            fill=(gray, gray, gray, self.blackOpacity),
        )


    def _polygonDrawing(self, var, gray):
        xPos1 = random.uniform(-var / 2, var)
        yPos1 = random.uniform(-var / 2, var)

        xPos2 = random.uniform(self.boxMax - var, self.boxMax + var)
        yPos2 = random.uniform(-var / 2, var)

        xPos3 = random.uniform(self.boxMax - var, self.boxMax + var)
        yPos3 = random.uniform(self.boxHeight - var, self.boxHeight + var)

        xPos4 = random.uniform(-var / 2, var)
        yPos4 = random.uniform(self.boxHeight - var, self.boxHeight + var)

        self.draw.polygon(
            (xPos1, yPos1, xPos2, yPos2, xPos3, yPos3, xPos4, yPos4),
            fill=(gray, gray, gray, self.blackOpacity),
        )

        # Finally composite full image
        # config.image.paste(self.mainImage, (numXPos, numYPos), self.scrollImage)


    def change(self):
        if self.varianceMode == "independent":
            self.varianceMode = "symmetrical"
        elif self.varianceMode == "symmetrical":
            self.varianceMode = "asymmetrical"
        elif self.varianceMode == "asymmetrical":
            self.varianceMode = "independent"

        self.var = int(self.varianceRange[0] + random.random() * self.varianceRange[1])

        pieceLogger(f"Change mode to {self.varianceMode} current color: {self.borderModel} variance {self.var}")


    def changeColor(self):
        self.borderModel = "plenum" if self.borderModel == "prism" else "prism"
        pieceLogger(f"New color model {self.borderModel}")
        # self.prisimBrightness = max(config.brightness * random.random(), 0.1)
        # if(self.config.demoMode != 0) : pieceLogger(self.varianceMode, self.borderModel)


class FluddManager:
    def __init__(self, config):
        self.config = config

    def setUp(self, workConfig):
        self.figureRows = 1
        self.figureCols = 1

        self.progressiveVar = 0
        self.initialVar = 0
        self.var = 0
        self.varDelta = 0
        self.varRepeatCountInitial = 0
        self.varRepeatCount = 0
        self.animationChangeRepeatCount = 0
        self.animationChangeRepeatCountInitial = 0
        self.progressiveRateVar = 0.0

        self.initialAnimationRate = 0.0
        self.animationRateDelta = 0.0
        self.animationRate = 0.0

        self.borderChangeProb = 1.0
        self.figureChangeTime = 0
        self.changeOnlyColor = False

        self.changeFigureControllerTime = 0
        self.figures = []

        # initial Fludd values
        self.borderModel = "prism"
        self.nothing = "void"
        # varianceMode = symmetrical, asymmetrical, independent
        self.varianceMode = "independent"
        # if demoMode == 0, no rotation of variants
        # demoMode > 0 is seconds/variant
        self.demoMode = 0
        self.bgOpacity = 0

        self.blackOpacity = 20
        self.blacknessChangeProbability = 0
        self.nothingChangeProbability = 0 
        self.colorChangeProbability = 1.0

        self._load_config_value(workConfig, "fludd", "figureRows", 1, int)
        self._load_config_value(workConfig, "fludd", "figureCols", 1, int)

        self._load_config_value(workConfig, "fludd", "progressiveVar", 0, float)
        self._load_config_value(workConfig, "fludd", "initialVar", 0, int)
        self._load_config_value(workConfig, "fludd", "var", 0, int)
        self._load_config_value(workConfig, "fludd", "varDelta", 0, int)
        self._load_config_value(workConfig, "fludd", "finalVar", 32, int)
        self._load_config_value(workConfig, "fludd", "varRepeatCountInitial", 0, int)
        self._load_config_value(workConfig, "fludd", "varRepeatCount", 0, int)

        self._load_config_value(workConfig, "fludd", "animationChangeRepeatCount", 0, int)
        self._load_config_value(workConfig, "fludd", "animationChangeRepeatCountInitial", 0, int)
        self._load_config_value(workConfig, "fludd", "initialAnimationRate", 0, float)
        self._load_config_value(workConfig, "fludd", "animationRate", 0, float)
        self._load_config_value(workConfig, "fludd", "animationRateDelta", 0, float)
        self._load_config_value(workConfig, "fludd", "progressiveRateVar", 0, float)

        self._load_config_value(workConfig, "fludd", "borderChangeProb", 1.0, float)
        self._load_config_value(workConfig, "fludd", "bgOpacity", 0, int)
        self._load_config_value(workConfig, "fludd", "figureChangeTime", 0, int)
        self._load_config_value(workConfig, "fludd", "changeOnlyColor", True, bool)

        self._load_config_value(workConfig, "fludd", "figureChangeProbability", 1.0, float)
        self._load_config_value(workConfig, "fludd", "blacknessChangeProbability", .0, float)
        self._load_config_value(workConfig, "fludd", "nothingChangeProbability", .0, float)
        self._load_config_value(workConfig, "fludd", "colorChangeProbability", .0, float)

        self._load_config_value(workConfig, "fludd", "borderModel", 1.0, str)
        self._load_config_value(workConfig, "fludd", "nothing", 1.0, str)
        self._load_config_value(workConfig, "fludd", "varianceMode", 1.0, str)
        self._load_config_value(workConfig, "fludd", "demoMode", .0, float)
        self._load_config_value(workConfig, "fludd", "blackOpacity", 20, int)
        

        self._load_config_value(workConfig, "fludd", "varianceRangeVals", f"{self.initialVar},{self.initialVar}", str)
        self.varianceRange = list(int(x) for x in self.varianceRangeVals.split(","))



    def _load_config_value(self, workConfig, section, option, default, type_converter):
        try:
            if type_converter == bool:
                setattr(self, option, type_converter(workConfig.getboolean(section, option)))
            else:
                setattr(self, option, type_converter(workConfig.get(section, option)))
        except Exception as e:
            pieceLogger(f" ==> Config value not loaded: {option} ==> will be set to {default}  {e}")
            setattr(self, option, default)


# ----------------------------------------------------#


def callBack():
    return True


def runWork():
    pieceLogger(f"**************************", 2)
    pieceLogger("Running fludd.py", 2)
    pieceLogger(f"**************************", 2)

    while True:
        # _refreshCanvas()
        _handle_director_advance()
        _check_adjust_animation_rate()
        _check_change_fludd_figure()
        _check_change_fludd_variance()
        _renderFigure()
        time.sleep(config.refreshRate)


def _handle_director_advance():
    config.directorController.checkTime()
    if config.directorController.advance:
        iterate()


def _check_adjust_animation_rate():
    if flddMngr.progressiveRateVar != 0:
        config.rateController.checkTime()
        if config.rateController.advance:
            if config.directorController.slotRate != flddMngr.animationRate:
                config.directorController.slotRate += flddMngr.animationRateDelta

            if abs(config.directorController.slotRate - flddMngr.animationRate) <= 0.01 and flddMngr.animationRate != config.directorController.slotRate:
                pieceLogger(f"setting directorController.slotRate to flddMngr.animationRate : {flddMngr.animationRate}")
                config.directorController.slotRate = flddMngr.animationRate

                if flddMngr.animationChangeRepeatCount >= flddMngr.animationChangeRepeatCountInitial and flddMngr.animationChangeRepeatCountInitial != -1:
                    pieceLogger(f"flddMngr.animationChangeRepeatCount {flddMngr.animationChangeRepeatCount} : {flddMngr.animationChangeRepeatCountInitial}")
                    config.directorController.slotRate = flddMngr.initialAnimationRate
                    pieceLogger(f"New main refresh rate (slotrate) : {config.directorController.slotRate}")
                    flddMngr.animationChangeRepeatCount = 0
                elif flddMngr.animationChangeRepeatCountInitial != -1:
                    flddMngr.animationChangeRepeatCount += 1



def _changeTheFigure():
    pieceLogger(f" Doing figure change")
    for f in flddMngr.figures:
        _fRef: Fludd = f
        if flddMngr.changeOnlyColor:
            if random.random() < flddMngr.colorChangeProbability :
                _fRef.changeColor()
        else :
            if random.random() < flddMngr.colorChangeProbability :
                _fRef.changeColor()
            _fRef.change()



def _check_change_fludd_figure():
    if flddMngr.figureChangeTime != 0:
        config.changeFigureController.checkTime()
        if config.changeFigureController.advance:
            if random.random() < flddMngr.figureChangeProbability :
                _changeTheFigure()


def _check_change_fludd_variance() :
    if flddMngr.progressiveVar != 0:
        config.varController.checkTime()
        if config.varController.advance:
            if fluddSquare.var != flddMngr.finalVar:
                fluddSquare.var += flddMngr.varDelta
            else:
                if flddMngr.varRepeatCount >= flddMngr.varRepeatCountInitial and flddMngr.varRepeatCountInitial != -1:
                    fluddSquare.var = flddMngr.initialVar
                    flddMngr.varRepeatCount = 0
                elif flddMngr.varRepeatCountInitial != -1:
                    flddMngr.varRepeatCount += 1


def _renderFigure():
    for f in flddMngr.figures:
        config.image.paste(f.mainImage, (f.xPosition, f.yPosition), f.mainImage)
    config.render(config.image, 0, 0, config.canvasWidth, config.canvasHeight)


def iterate():
    config.draw.rectangle((0, 0, config.canvasWidth, config.canvasHeight), fill=(0, 0, 0, flddMngr.bgOpacity))
    for f in flddMngr.figures:
        if random.random() < flddMngr.borderChangeProb:
            f.reDraw()



def main(run=True):
    global config
    global workConfig
    global fluddSquare
    global flddMngr
    config.image = Image.new("RGBA", (config.canvasWidth, config.canvasHeight))
    config.draw = ImageDraw.Draw(config.image)

    flddMngr = FluddManager(config)
    flddMngr.setUp(workConfig)

    # Timing and refresh are on the config variable, all the rest on the FluddManager flddMngr
    config.refreshRate = float(workConfig.get("fludd", "refreshRate", fallback=0.03))

    _boxWidth = config.canvasWidth / flddMngr.figureCols
    _boxHeight = config.canvasHeight / flddMngr.figureRows

    for c in range(flddMngr.figureCols):
        for r in range(flddMngr.figureRows):
            fluddSquare = Fludd(config, flddMngr)
            # Prism is all colors, Plenum is white
            fluddSquare.borderModel = flddMngr.borderModel
            fluddSquare.nothing = flddMngr.nothing
            fluddSquare.var = flddMngr.initialVar
            fluddSquare.varianceMode = flddMngr.varianceMode
            fluddSquare.blackOpacity = flddMngr.blackOpacity
            fluddSquare.blacknessChangeProbability = flddMngr.blacknessChangeProbability
            fluddSquare.nothingChangeProbability = flddMngr.nothingChangeProbability
            fluddSquare.prisimBrightness = config.brightness
            fluddSquare.varianceRange = flddMngr.varianceRange
            fluddSquare.xPosition = round(_boxWidth * c)
            fluddSquare.yPosition = round(_boxHeight * r)
            fluddSquare.setUp(_boxWidth, _boxHeight)
            flddMngr.figures.append(fluddSquare)

    config.directorController = Director(config)
    config.directorController.slotRate = flddMngr.initialAnimationRate

    config.changeFigureController = Director(config)
    config.changeFigureController.slotRate = flddMngr.figureChangeTime

    config.rateController = Director(config)
    config.rateController.slotRate = flddMngr.progressiveRateVar

    config.varController = Director(config)
    config.varController.slotRate = flddMngr.progressiveVar

    config.cycleTiming = 1
    config.t1 = time.time()
    config.t2 = time.time()

    config.calibrated = False
    config.cycleCount = 0
    config.calibrationCount = 500

    # -----------------------------------------------------------------------
    # Demo mode means the piece cycles through its 6 base
    # variation plenum | prism  X  independent | asymmetrical | symmetrical
    # -----------------------------------------------------------------------

    config.count = 0
    config.countMax = 1000

    # var sets the points offset from the corners - i.e. the larger var is, the wider the borders
    """
    ************
    *           *
     *           *
      *          *
       ***********

    """

    if run:
        runWork()
