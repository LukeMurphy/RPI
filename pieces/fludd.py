# ################################################### #
import math
import random
import time
from modules.configuration import bcolors
from modules import colorutils
from PIL import Image, ImageDraw, ImageEnhance, ImageFont, ImageOps

lastRate = 0
colorutils.brightness = 1


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


# Really no need for a class here - it's always a singleton and besides
# with Python everthing is an object already .... some kind of OOP
# holdover anxiety I guess


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

    def __init__(self, config):
        print("init PB")

        self.boxMax = config.canvasWidth - 1
        # self.boxMaxAlt = self.boxMax + int(random.uniform(10, 30) * config.canvasWidth)
        self.boxHeight = config.canvasHeight - 2
        self.config = config

        tempImage = Image.new("RGBA", (640, 640))
        draw = ImageDraw.Draw(tempImage)
        self.mainImage = Image.new("RGBA", (config.canvasWidth, config.canvasHeight))

    def setUp(self, boxMax, boxHeight) :
        self.boxMax = boxMax
        self.boxMaxAlt = self.boxMax + int(random.uniform(10, 30) * config.canvasWidth)
        self.boxHeight = boxHeight
        self.config = config

        tempImage = Image.new("RGBA", (640, 640))
        draw = ImageDraw.Draw(tempImage)
        self.mainImage = Image.new("RGBA", (round(self.boxMax), round(self.boxHeight)))
        self.draw = ImageDraw.Draw(self.mainImage)


    def changeAction(self):
        return False

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
                (xy0, xy0, symBoxWidth, symBoxHeight),
                fill=(gray, gray, gray, self.blackOpacity),
            )

        elif self.varianceMode == "asymmetrical":
            self._asymmetricalDrawing(var, gray)
        if random.random() < self.nothingChangeProbability:
            self.nothingLevel = random.uniform(0, 255)
        if random.random() < self.blacknessChangeProbability:
            self.blackOpacity = round(random.uniform(0, 255))

    def _asymmetricalDrawing(self, var, gray):
        svarw = random.uniform(0, var)
        svarh = random.uniform(0, var)
        symBoxWidth = self.boxMax - svarw
        symBoxHeight = self.boxHeight - svarh
        xPos1 = self.boxMax - symBoxWidth
        yPos1 = self.boxHeight - symBoxHeight
        self.draw.rectangle(
            (xPos1, yPos1, symBoxWidth, symBoxHeight),
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

    def changeColor(self):
        self.borderModel = "plenum" if self.borderModel == "prism" else "prism"
        self.prisimBrightness = max(config.brightness * random.random(), .1)
        # if(self.config.demoMode != 0) : print(self.varianceMode, self.borderModel)

    def done(self):
        return True


def drawElement():
    global config
    return True


def redraw():
    global config, fluddSquare
    for f in config.figures :
        if random.random() < config.borderChangeProb:
            f.reDraw()


def changeColor():
    return True


def changeCall():
    return True


def callBack():
    global config


def runWork():
    global config, fluddSquare
    print(f"{bcolors.OKGREEN}** {bcolors.BOLD}")
    print("Running fludd.py")
    print(bcolors.ENDC)
    while True:
        _runLoopFunctions(config)


# TODO Rename this here and in `runWork`
def _runLoopFunctions(config):
    _refreshCanvas()
    _handle_director_advance()
    _adjust_animation_rate()
    _adjust_fludd_variance()
    _renderFigure()
    time.sleep(config.refreshRate)

def _refreshCanvas() :
     config.draw.rectangle((0, 0, config.canvasWidth, config.canvasHeight),fill=(0, 0, 0, config.bgOpacity))


def _handle_director_advance():
    global config, fluddSquare
    config.directorController.checkTime()
    if config.directorController.advance:
        iterate()


def _adjust_animation_rate():
    global config
    if config.progressiveRateVar != 0:
        config.rateController.checkTime()
        if config.rateController.advance:
            if config.directorController.slotRate != config.animationRate:
                config.directorController.slotRate += config.animationRateDelta

            if abs(config.directorController.slotRate - config.animationRate) <= 0.01:
                config.directorController.slotRate = config.animationRate

                if config.animationChangeRepeatCount >= config.animationChangeRepeatCountInitial and config.animationChangeRepeatCountInitial != -1:
                    config.directorController.slotRate = config.initialAnimationRate
                    config.animationChangeRepeatCount = 0
                elif config.animationChangeRepeatCountInitial != -1:
                    config.animationChangeRepeatCount += 1


def _adjust_fludd_variance():
    global config, fluddSquare
    if config.figureChangeTime != 0:
        config.changeFigureController.checkTime()
        if config.changeFigureController.advance:
            _changeTheFigure()
    if config.progressiveVar != 0:
        config.varController.checkTime()
        if config.varController.advance:
            if fluddSquare.var != config.finalVar:
                fluddSquare.var += config.varDelta
            else:
                if config.varRepeatCount >= config.varRepeatCountInitial and config.varRepeatCountInitial != -1:
                    fluddSquare.var = config.initialVar
                    config.varRepeatCount = 0
                elif config.varRepeatCountInitial != -1:
                    config.varRepeatCount += 1

def _renderFigure() :
    for f in config.figures :
        config.image.paste(f.mainImage, (f.xPosition, f.yPosition), f.mainImage)
    config.render(config.image, 0, 0, config.canvasWidth, config.canvasHeight)


def iterate():
    global config, fluddSquare, lastRate, calibrated, cycleCount
    redraw()

# deprecating for now
def _calibrationTest(config):
    config.t2 = time.time()
    config.timeToComplete = config.t2 - config.t1
    config.timeItShouldHaveTaken = config.calibrationCount * config.redrawSpeed

    config.cycleTiming = config.timeToComplete / config.timeItShouldHaveTaken

    config.countMax = config.demoMode * config.calibrationCount / config.timeToComplete
    config.calibrated = True

    print(config.timeItShouldHaveTaken, config.timeToComplete, config.countMax )

    config.t1 = time.time()
    config.t2 = time.time()


def _changeTheFigure():
    config.count = 0
    config.t2 = time.time()
    config.timeToComplete = config.t2 - config.t1
    # print (config.timeToComplete)
    config.t1 = time.time()
    config.t2 = time.time()
    for f in config.figures :
        if not config.figureChangeOnlyColor :
            f.change()
        f.changeColor()


def main(run=True):
    global config
    global workConfig
    global fluddSquare
    config.image = Image.new("RGBA", (config.canvasWidth, config.canvasHeight))
    config.draw = ImageDraw.Draw(config.image)
    config.figures = []

    _load_config_value(config, workConfig, "fludd", "figureRows", 1, int)
    _load_config_value(config, workConfig, "fludd", "figureCols", 1, int)
    _load_config_value(config, workConfig, "fludd", "progressiveVar", 0, float)
    _load_config_value(config, workConfig, "fludd", "redrawSpeed", 0.03, float)
    _load_config_value(config, workConfig, "fludd", "initialVar", 0, int)
    _load_config_value(config, workConfig, "fludd", "var", 0, int)
    _load_config_value(config, workConfig, "fludd", "varDelta", 0, int)
    _load_config_value(config, workConfig, "fludd", "varRepeatCountInitial", 0, int)
    _load_config_value(config, workConfig, "fludd", "varRepeatCount", 0, int)
    _load_config_value(config, workConfig, "fludd", "animationChangeRepeatCount", 0, int)
    _load_config_value(config, workConfig, "fludd", "animationChangeRepeatCountInitial", 0, int)
    _load_config_value(config, workConfig, "fludd", "progressiveRateVar", 0.0, float)
    _load_config_value(config, workConfig, "fludd", "refreshRate", 0.03, float)
    _load_config_value(config, workConfig, "fludd", "animationRate", 0.0, float)
    _load_config_value(config, workConfig, "fludd", "initialAnimationRate", 0.0, float)
    _load_config_value(config, workConfig, "fludd", "animationRateDelta", 0.0, float)
    _load_config_value(config, workConfig, "fludd", "borderChangeProb", 1.0, float)
    _load_config_value(config, workConfig, "fludd", "bgOpacity", 0, int)
    _load_config_value(config, workConfig, "fludd", "figureChangeTime", 0, int)
    _load_config_value(config, workConfig, "fludd", "figureChangeOnlyColor", True, bool)
    _load_config_value(config, workConfig, "fludd", "changeFigureControllerTime", config.figureChangeTime, int)

    _boxWidth = config.canvasWidth / config.figureCols
    _boxHeight = config.canvasHeight / config.figureRows

    for c in range(config.figureCols):
        for r in range(config.figureRows):
            fluddSquare = Fludd(config)
            # Prism is all colors, Plenum is white
            fluddSquare.borderModel = workConfig.get("fludd", "borderModel")
            fluddSquare.nothing = workConfig.get("fludd", "nothing")
            fluddSquare.var = int(workConfig.get("fludd", "var"))
            fluddSquare.varianceMode = workConfig.get("fludd", "varianceMode")
            fluddSquare.blackOpacity = int(workConfig.get("fludd", "blackOpacity"))
            fluddSquare.blacknessChangeProbability = float(workConfig.get("fludd", "blacknessChangeProbability"))
            fluddSquare.nothingChangeProbability = float(workConfig.get("fludd", "nothingChangeProbability"))
            # fluddSquare.prisimBrightness  = float(workConfig.get("fludd", 'prisimBrightness'))
            # More uniform brightness control
            fluddSquare.prisimBrightness = float(workConfig.get("displayconfig", "brightness"))
            fluddSquare.xPosition = round(_boxWidth * c)
            fluddSquare.yPosition = round(_boxHeight * r)
            fluddSquare.setUp(_boxWidth,_boxHeight)
            config.figures.append(fluddSquare)



    config.directorController = Director(config)
    config.directorController.slotRate = config.initialAnimationRate

    config.changeFigureController = Director(config)
    config.changeFigureController.slotRate = config.changeFigureControllerTime

    config.rateController = Director(config)
    config.rateController.slotRate = config.progressiveRateVar

    config.varController = Director(config)
    config.varController.slotRate = config.progressiveVar

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


def _load_config_value(obj, workConfig, section, option, default, type_converter):
    try:
        if type_converter == bool:
            setattr(obj, option, type_converter(workConfig.getboolean(section, option)))
        else:
            setattr(obj, option, type_converter(workConfig.get(section, option)))
    except Exception as e:
        print(f" ==> Config value not loaded: {option} ==> will be set to {default} \n  {e}\n")
        setattr(obj, option, default)
