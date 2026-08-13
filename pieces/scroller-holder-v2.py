#!/usr/bin/python
# import modules
# ################################################### #
import math
import random
import time
from collections import OrderedDict

from matplotlib.pyplot import pie
from modules.configuration import pieceLogger
from modules import colorutils, continuous_scroller, panelDrawing
from modules.blanks_and_dither_rempping import BlanksAndDitherRemapping

from modules.faderclass import FaderObj
from PIL import (
    Image,
    ImageChops,
    ImageDraw,
    ImageEnhance,
    ImageFilter,
    ImageFont,
    ImageOps,
    ImageChops
)

global config, overlayControls


class ScrollerManager:
    def __init__(self, config):
        self.config = config

    def setUp(self, workConfig):
        config = self.config
        pieceLogger("SINGLETON SCROLLER HOLDER INIT")

        config.redrawSpeed = float(workConfig.get("scroller", "redrawSpeed"))

        config.windowWidth = float(workConfig.get("displayconfig", "windowWidth"))
        config.windowHeight = float(workConfig.get("displayconfig", "windowHeight"))

        self.xOffset = int(workConfig.get("scroller", "xOffset"))
        self.yOffset = int(workConfig.get("scroller", "yOffset"))

        self.displayRows = int(workConfig.get("scroller", "displayRows"))
        self.displayCols = int(workConfig.get("scroller", "displayCols"))

        # ********* HARD CODING VALUES  ***********************

        self.bandHeight = int(round(config.canvasHeight / self.displayRows))
        self.bgBackGroundColor = (0, 0, 0, 0)
        self.arrowBgBackGroundColor = (0, 0, 0, 200)

        config.canvasImage = Image.new("RGBA", (config.canvasWidth * 10, config.canvasHeight))
        config.canvasImageDraw = ImageDraw.Draw(config.canvasImage)

        config.textImage = Image.new("RGBA", (config.canvasWidth * 10, config.canvasHeight))
        config.textImageDraw = ImageDraw.Draw(config.textImage)

        config.imageLayer = Image.new("RGBA", (config.canvasWidth * 10, config.canvasHeight))
        config.imageLayerDraw = ImageDraw.Draw(config.canvasImage)

        config.workImage = Image.new("RGBA", (config.canvasWidth, config.canvasHeight))
        config.workImageDraw = ImageDraw.Draw(config.workImage)

        self.overallBlur = float(workConfig.get("scroller", "overallBlur", vars=0, fallback=0))

        self.flip = False
        self.scrollArray = []

        ## Set up the scrolling layer

        self.useBackground = workConfig.getboolean("scroller", "useBackground")

        try:
            self.backgroundColorChangeProb = float(workConfig.get("scroller", "backgroundColorChangeProb"))
        except Exception as e:
            pieceLogger(f"Config not found: {e}", 1)
            self.backgroundColorChangeProb = 0.5

        try:
            self.setPatternColor = workConfig.getboolean("scroller", "setPatternColor")
            self.setPatternEndColor = list(map(lambda x: int(x), workConfig.get("scroller", "setPatternEndColor").split(",")))
        except Exception as e:
            self.setPatternColor = False
            pieceLogger(f"Config not found: {e}", 1)

        try:
            self.altDirectionScrolling = workConfig.getboolean("scroller", "altDirectionScrolling")
        except Exception as e:
            self.altDirectionScrolling = False
            pieceLogger(f"Config not found: {e}", 1)

        try:
            self.alwaysRandomPatternColor = workConfig.getboolean("scroller", "alwaysRandomPatternColor")
        except Exception as e:
            self.alwaysRandomPatternColor = False
            pieceLogger(f"Config not found: {e}", 1)

        try:
            self.alwaysRandomPattern = workConfig.getboolean("scroller", "alwaysRandomPattern")
        except Exception as e:
            self.alwaysRandomPattern = False
            pieceLogger(f"Config not found: {e}", 1)

        try:
            self.redGreenSwapProb = float(workConfig.get("scroller", "redGreenSwapProb"))
        except Exception as e:
            pieceLogger(f"Config not found: {e}", 1)
            self.redGreenSwapProb = 0
        try:
            self.redBlueSwapProb = float(workConfig.get("scroller", "redBlueSwapProb"))
        except Exception as e:
            pieceLogger(f"Config not found: {e}", 1)
            self.redBlueSwapProb = 0
        try:
            self.greenBlueSwapProb = float(workConfig.get("scroller", "greenBlueSwapProb"))
        except Exception as e:
            pieceLogger(f"Config not found: {e}", 1)
            self.greenBlueSwapProb = 0

        try:
            self.bg_dropHueMinValue = float(workConfig.get("scroller", "bg_dropHueMinValue"))
            self.bg_dropHueMaxValue = float(workConfig.get("scroller", "bg_dropHueMaxValue"))
            self.fg_dropHueMinValue = float(workConfig.get("scroller", "fg_dropHueMinValue"))
            self.fg_dropHueMaxValue = float(workConfig.get("scroller", "fg_dropHueMaxValue"))
        except Exception as e:
            self.bg_dropHueMinValue = 0
            self.bg_dropHueMaxValue = 0
            self.fg_dropHueMinValue = 0
            self.fg_dropHueMaxValue = 0
            pieceLogger(f"Config not found: {e}", 1)

        try:
            self.useHSV = True

            self.fg_minHue = int(workConfig.get("scroller", "fg_minHue"))
            self.fg_maxHue = int(workConfig.get("scroller", "fg_maxHue"))
            self.fg_minSaturation = float(workConfig.get("scroller", "fg_minSaturation"))
            self.fg_maxSaturation = float(workConfig.get("scroller", "fg_maxSaturation"))
            self.fg_minValue = float(workConfig.get("scroller", "fg_minValue"))
            self.fg_maxValue = float(workConfig.get("scroller", "fg_maxValue"))

            self.bg_minHue = int(workConfig.get("scroller", "bg_minHue"))
            self.bg_maxHue = int(workConfig.get("scroller", "bg_maxHue"))
            self.bg_minSaturation = float(workConfig.get("scroller", "bg_minSaturation"))
            self.bg_maxSaturation = float(workConfig.get("scroller", "bg_maxSaturation"))
            self.bg_minValue = float(workConfig.get("scroller", "bg_minValue"))
            self.bg_maxValue = float(workConfig.get("scroller", "bg_maxValue"))

        except Exception as e:

            pieceLogger(f"Config not found: {e}", 1)
            self.useHSV = False

            self.fg_minHue = 0
            self.fg_maxHue = 360
            self.fg_minSaturation = 1
            self.fg_maxSaturation = 1
            self.fg_minValue = 1
            self.fg_maxValue = 1

            self.bg_minHue = 0
            self.bg_maxHue = 360
            self.bg_minSaturation = 1
            self.bg_maxSaturation = 1
            self.bg_minValue = 1
            self.bg_maxValue = 1

        try:
            _harlequinColorsRaw = (workConfig.get("scroller", "harlequinColorsRaw")).split("|")
            self.harlequinColors = []
            for _set in _harlequinColorsRaw:
                _setVals = _set.split(",")
                _cSet = []
                _cSet.extend(int(_val) for _val in _setVals)
                self.harlequinColors.append(_cSet)

            pieceLogger(f"scrllrMngr.harlequinColors ==> {self.harlequinColors}")

        except Exception as e:
            self.harlequinColors = ((190, 0, 40, 55), (210, 153, 10, 55), (42, 24, 180, 55), (25, 108, 30, 55))
            pieceLogger(f"Config not found: {e}", 1)

        if self.useBackground == True:
            self._configureBackgroundScrolling(workConfig)

        try:
            self.useText = workConfig.getboolean("scroller", "useText")
            self.useAltText = workConfig.getboolean("scroller", "useAltText")
            if self.useText == True:
                self._configureMessageScrolling(workConfig)
            if self.useAltText == True:
                self._configureAltTextScrolling(workConfig)
        except Exception as e:
            pieceLogger(f"Config not found: {e}", 1)

        try:
            self.useOverLayImage = workConfig.getboolean("scroller", "useOverLayImage")
            if self.useOverLayImage == True:
                self._configureImageOverlay(workConfig)
        except Exception as e:
            self.useOverLayImage = False
            pieceLogger(f"Config not found: {e}", 1)

        try:
            self.useArrows = workConfig.getboolean("scroller", "useArrows")
            if self.useArrows == True:
                self._configureArrowScrolling(workConfig)
        except Exception as e:
            pieceLogger(f"Config not found: {e}", 1)

        try:
            self.useUltraSlowSpeed = workConfig.getboolean("scroller", "useUltraSlowSpeed")
        except Exception as e:
            self.useUltraSlowSpeed = False
            pieceLogger(f"Config not found: {e}", 1)

        try:
            self.useImages = workConfig.getboolean("scroller", "useImages")
            self.useTransparentImages = workConfig.getboolean("scroller", "useTransparentImages")
            if self.useImages == True:
                self._configureImageScrolling(workConfig)
        except Exception as e:
            pieceLogger(f"Config not found: {e}", 1)

        try:
            self.doingRefreshCount = float(workConfig.get("scroller", "doingRefreshCount"))
        except Exception as e:
            self.doingRefreshCount = 50
            pieceLogger(f"Config not found: {e}", 1)

        ### THIS IS USED AS WAY TO MOCKUP A CONFIGURATION OF RECTANGULAR PANELS
        panelDrawing.mockupBlock(config, workConfig)
        """
            ########### Need to add something like this at final render call  as well

            ########### RENDERING AS A MOCKUP OR AS REAL ###########
            if config.useDrawingPoints == True :
                config.panelDrawing.canvasToUse = config.renderImageFull
                config.panelDrawing.render()
            else :
                #config.render(config.canvasImage, 0, 0, config.canvasWidth, config.canvasHeight)
                #config.render(config.image, 0, 0)
                config.render(config.renderImageFull, 0, 0)
        """

        config.renderImageFull = config.workImage.copy()
        self.f = FaderObj()
        self.f.setUp(config.renderImageFull, config.workImage)
        self.f.doingRefreshCount = self.doingRefreshCount
        # config.workImageDraw.rectangle((0,0,100,100), fill=(100,0,0,100))
        self.renderImageFullOld = config.renderImageFull.copy()
        self.fadingDone = True

        self.useFadeThruAnimation = True
        self.deltaTimeDone = True

        try:
            self.useFadeThruAnimation = workConfig.getboolean("scroller", "useFadeThruAnimation")
        except Exception as e:
            pieceLogger(f"Config not found: {e}", 1)
            self.useFadeThruAnimation = True

        global overlayControls
        overlayControls = BlanksAndDitherRemapping(config, workConfig, "scroller")
        # for blanks
        overlayControls.destinationImageDraw = config.workImageDraw
        overlayControls.targetImageRef = config.workImage
        # for overlay
        # overlayControls.overlayImage = config.overlayImage
        # overlayControls.overlayImageDraw = config.overlayImageDraw
        # overlayControls.setPanelOverlays()

    def _configureBackgroundScrolling(self, workConfig):
        config = self.config
        pieceLogger("configureBackgroundScrolling")
        self.patternRows = int(workConfig.get("scroller", "patternRows"))
        self.patternCols = int(workConfig.get("scroller", "patternCols"))
        self.patternRowsOffset = int(workConfig.get("scroller", "patternRowsOffset"))
        self.patternColsOffset = int(workConfig.get("scroller", "patternColsOffset"))
        self.patternDrawProb = float(workConfig.get("scroller", "patternDrawProb"))
        self.bgBackGroundColor = workConfig.get("scroller", "bgBackGroundColor").split(",")
        self.bgBackGroundColor = tuple([int(i) for i in self.bgBackGroundColor])
        self.pattern = workConfig.get("scroller", "pattern")
        self.initialPattern = workConfig.get("scroller", "pattern")
        self.patternSpeed = float(workConfig.get("scroller", "patternSpeed"))

        if self.useHSV:

            self.bgBackGroundColor = colorutils.getRandomColorHSV(
                self.bg_minHue,
                self.bg_maxHue,
                self.bg_minSaturation,
                self.bg_maxSaturation,
                self.bg_minValue,
                self.bg_maxValue,
                self.bg_dropHueMinValue,
                self.bg_dropHueMaxValue,
                255,
                config.brightness,
            )

            self.bgBackGroundEndColor = colorutils.getRandomColorHSV(
                self.bg_minHue,
                self.bg_maxHue,
                self.bg_minSaturation,
                self.bg_maxSaturation,
                self.bg_minValue,
                self.bg_maxValue,
                self.bg_dropHueMinValue,
                self.bg_dropHueMaxValue,
                255,
                config.brightness,
            )

            self.patternColor = colorutils.getRandomColorHSV(
                self.fg_minHue, self.fg_maxHue, self.fg_minSaturation, self.fg_maxSaturation, self.fg_minValue, self.fg_maxValue, 0, 0, 255, config.brightness
            )

            self.patternEndColor = colorutils.getRandomColorHSV(
                self.fg_minHue,
                self.fg_maxHue,
                self.fg_minSaturation,
                self.fg_maxSaturation,
                self.fg_minValue,
                self.fg_maxValue,
                self.fg_dropHueMinValue,
                self.fg_dropHueMaxValue,
                255,
                config.brightness,
            )
        else:

            self.bgBackGroundColor = colorutils.randomColorAlpha(config.brightness)
            self.bgBackGroundEndColor = colorutils.randomColorAlpha(config.brightness)
            self.patternColor = colorutils.randomColorAlpha(config.brightness)
            self.patternEndColor = colorutils.randomColorAlpha(config.brightness)

            if self.alwaysRandomPatternColor == True:
                self.patternColor = colorutils.randomColorAlpha(config.brightness)
                self.patternEndColor = colorutils.randomColorAlpha(config.brightness)

            if self.setPatternColor == True:
                self.setPatternEndColor = colorutils.getRandomColorHSV(
                    self.fg_minHue,
                    self.fg_maxHue,
                    self.fg_minSaturation,
                    self.fg_maxSaturation,
                    self.fg_minValue,
                    self.fg_maxValue,
                    self.bg_dropHueMinValue,
                    self.bg_dropHueMaxValue,
                    255,
                    config.brightness,
                )
                self.patternColor = self.setPatternEndColor
                self.patternEndColor = self.setPatternEndColor

        self.currentPatternLength = 0

        self.scroller4 = continuous_scroller.ScrollObject()
        scrollerRef = self.scroller4
        scrollerRef.typeOfScroller = "bg"
        scrollerRef.canvasWidth = int(self.displayRows * config.canvasWidth)
        scrollerRef.xSpeed = self.patternSpeed
        scrollerRef.setUp()
        direction = 1 if scrollerRef.xSpeed > 0 else -1
        scrollerRef.callBack = {"func": remakePatternBlock, "direction": direction}

        try:
            self.maxSpeed = float(workConfig.get("scroller", "maxSpeed"))
        except Exception as e:
            self.maxSpeed = self.patternSpeed

        scrollerRef.xMaxSpeed = self.maxSpeed

        try:
            self.changeProb = float(workConfig.get("scroller", "changeProb"))
        except Exception as e:
            self.changeProb = 0.0
            pieceLogger(f"Config not found: {e}", 1)

        try:
            self.changeProbReleaseFactor = float(workConfig.get("scroller", "changeProbReleaseFactor"))
        except Exception as e:
            self.changeProbReleaseFactor = 1.0
            pieceLogger(f"Config not found: {e}", 1)

        makeBackGround(scrollerRef.bg1Draw, 1)
        makeBackGround(scrollerRef.bg2Draw, 1)

        self.t1 = time.time()
        self.t2 = time.time()
        self.timeToComplete = 1
        self.scrollerPauseBool = False

        self.scrollArray.append(scrollerRef)

    def _configureImageScrolling(self, workConfig):
        config = self.config
        self.imageSpeed = float(workConfig.get("scroller", "imageSpeed"))
        self.imageBlockImage = workConfig.get("scroller", "imageBlockImage")
        self.imageBlockBuffer = int(workConfig.get("scroller", "imageBlockBuffer"))
        self.imageDrawProb = float(workConfig.get("scroller", "imageDrawProb", fallback=1.0))
        self.imageBlockRemakeProb = float(workConfig.get("scroller", "imageBlockRemakeProb"))

        self.foregroundImageBrightnessAddition = float(workConfig.get("scroller", "foregroundImageBrightnessAddition", fallback=0))

        arg = config.path + self.imageBlockImage
        self.imageBlockImageLoaded = Image.open(arg, "r")
        self.imageBlockImageLoaded.load()
        self.imageBlockImageLoadedCopy = self.imageBlockImageLoaded.copy()

        self.scroller5 = continuous_scroller.ScrollObject()
        scrollerRef = self.scroller5
        scrollerRef.canvasWidth = int(self.displayCols * config.canvasWidth)
        # scrollerRef.canvasHeight = int(config.windowHeight)
        scrollerRef.xSpeed = self.imageSpeed
        scrollerRef.setUp()
        direction = 1 if scrollerRef.xSpeed > 0 else -1
        scrollerRef.callBack = {"func": remakeScrollBlock, "direction": direction}
        makeScrollBlock(scrollerRef.bg1, scrollerRef.bg1Draw, direction)
        makeScrollBlock(scrollerRef.bg2, scrollerRef.bg2Draw, direction)
        self.scrollArray.append(scrollerRef)

    def _configureArrowScrolling(self, workConfig):
        config = self.config
        self.arrowCols = int(workConfig.get("scroller", "arrowCols"))
        self.lineThickness = int(workConfig.get("scroller", "lineThickness"))
        self.arrowSpeed = int(workConfig.get("scroller", "arrowSpeed"))
        self.greyLevel = int(workConfig.get("scroller", "greyLevel"))
        self.redShift = int(workConfig.get("scroller", "redShift"))
        self.scroller1 = continuous_scroller.ScrollObject()

        scrollerRef = self.scroller1
        scrollerRef.canvasWidth = int(self.displayRows * config.canvasWidth)
        scrollerRef.xSpeed = self.arrowSpeed
        scrollerRef.setUp()
        direction = 1 if scrollerRef.xSpeed > 0 else -1
        scrollerRef.callBack = {"func": remakeArrowBlock, "direction": direction}
        makeArrows(scrollerRef.bg1Draw, -1)
        makeArrows(scrollerRef.bg2Draw, -1)
        self.scrollArray.append(scrollerRef)

    def _configureMessageScrolling(self, workConfig):
        self.colorMode = workConfig.get("scroller", "colorMode")
        self.sansSerif = workConfig.getboolean("scroller", "sansSerif")
        self.fontSize = int(workConfig.get("scroller", "fontSize"))
        self.textVOffest = int(workConfig.get("scroller", "textVOffest"))
        self.shadowSize = int(workConfig.get("scroller", "shadowSize"))
        self.textSpeed = float(workConfig.get("scroller", "textSpeed"))
        self.textSpeed2 = float(workConfig.get("scroller", "textSpeed2", fallback=self.textSpeed))
        self.msg1 = workConfig.get("scroller", "msg1")
        self.msg2 = workConfig.get("scroller", "msg2")
        self.msg3 = workConfig.get("scroller", "msg3")

        def _makeTextLayer(scrollerRef, txtMsg, dir=1, delta=0.25, textSlide=0, speed=self.textSpeed):
            scrollerRef.canvasWidth = int(self.displayCols * self.config.canvasWidth)
            scrollerRef.canvasWidth = int(len(txtMsg) * self.fontSize / 2)
            scrollerRef.xSpeed = dir * speed + delta
            scrollerRef.setUp()
            scrollerRef.typeOfScroller = "text"
            scrollerRef.textSlide = textSlide
            direction = 1 if scrollerRef.xSpeed > 0 else -1
            makeMessage(scrollerRef.bg1, txtMsg, direction)
            makeMessage(scrollerRef.bg2, txtMsg, direction)
            scrollerRef.callBack = {"func": remakeMessage, "direction": direction}
            self.scrollArray.append(scrollerRef)
            pieceLogger(f"-----------\n {scrollerRef.typeOfScroller} \n----------")

        self.textLayer_1 = continuous_scroller.ScrollObject()
        _makeTextLayer(self.textLayer_1, self.msg1, 1, 0.25, 1)

        self.textLayer_2 = continuous_scroller.ScrollObject()
        _makeTextLayer(self.textLayer_2, self.msg2, -1, 0.0, 0, self.textSpeed2)

        self.textLayer_3 = continuous_scroller.ScrollObject()
        # _makeTextLayer(self.textLayer_3, self.msg1, 1, 0.25, 1)

        self.textLayer_4 = continuous_scroller.ScrollObject()
        # _makeTextLayer(self.textLayer_4, self.msg2, -1, 0.0, 1)

    def _configureAltTextScrolling(self, workConfig):
        config = self.config
        self.colorMode = workConfig.get("scroller", "colorMode")
        self.sansSerif = workConfig.getboolean("scroller", "sansSerif")
        self.fontSize = int(workConfig.get("scroller", "fontSize"))
        self.textVOffest = int(workConfig.get("scroller", "textVOffest"))
        self.shadowSize = int(workConfig.get("scroller", "shadowSize"))
        self.textSpeed = float(workConfig.get("scroller", "textSpeed"))
        self.scroller6 = continuous_scroller.ScrollObject()
        scrollerRef = self.scroller6
        scrollerRef.canvasWidth = int(self.displayRows * config.canvasWidth)
        scrollerRef.xSpeed = -self.textSpeed
        scrollerRef.setUp()
        direction = 1 if scrollerRef.xSpeed > 0 else -1
        makeDaemonMessages(scrollerRef.bg1, direction)
        makeDaemonMessages(scrollerRef.bg2, direction)
        scrollerRef.callBack = {"func": remakeDaemonMessages, "direction": direction}
        self.scrollArray.append(scrollerRef)

    def _configureImageOverlay(self, workConfig):
        config = self.config
        self.overLayImage = workConfig.get("scroller", "overLayImage")
        self.overLayXPos = int(workConfig.get("scroller", "overLayXPos"))
        self.overLayYPos = int(workConfig.get("scroller", "overLayYPos"))
        self.overlayGlitchSize = int(workConfig.get("scroller", "overlayGlitchSize"))
        self.overlayBrightness = float(workConfig.get("scroller", "overlayBrightness"))
        self.overlayGlitchRate = float(workConfig.get("scroller", "overlayGlitchRate"))
        self.overlayResetRate = float(workConfig.get("scroller", "overlayResetRate"))

        arg = config.path + self.overLayImage
        self.loadedImage = Image.open(arg, "r")
        self.loadedImage.load()
        self.loadedImageCopy = self.loadedImage.copy()


## Image manipulations


def glitchBox(img, r1=-10, r2=10, dir="horizontal"):

    apparentWidth = img.size[0]
    apparentHeight = img.size[1]

    dx = int(random.uniform(r1, r2))
    dy = int(random.uniform(r1, r2))

    # dx = 0

    sectionWidth = int(random.uniform(2, apparentWidth - dx))
    sectionHeight = int(random.uniform(2, apparentHeight - dy))

    # sectionHeight = apparentWidth

    # 95% of the time they dance together as mirrors
    if random.random() < 0.97:
        if dir == "horizontal":
            cp1 = img.crop((0, dy, apparentWidth, dy + sectionHeight))
        else:
            cp1 = img.crop((dx, 0, dx + sectionWidth, sectionHeight))

        img.paste(cp1, (int(0 + dx), int(0 + dy)))


## Layer imagery
def makeDaemonMessages(imageRef, direction=1):
    global config, scrllrMngr

    demonsMale = [
        "Jealousy",
        "Wrath",
        "Tears",
        "Sighing",
        "Suffering",
        "Lamentation",
        "Bitter Weeping",
    ]
    demonsMaleModifier = [
        "Jealous",
        "Wrathful",
        "Tearful",
        "Sighing",
        "Suffering",
        "Lamenting",
        "Embittered Weeping",
    ]

    demonsFemale = [
        "Wrath",
        "Pain",
        "Lust",
        "Sighing",
        "Cursedness",
        "Bitterness",
        "Quarelsomeness",
    ]
    demonsFemaleModifier = [
        "Wrathful",
        "Painful",
        "Lusty",
        "Sighing",
        "Cursed",
        "Bitter",
        "Quarelsome",
    ]

    angelsMale = [
        "Unenviousness",
        "Blessedness",
        "Joy",
        "Truth",
        "Unbegrudgingness",
        "Belovedness",
        "Trustworthyness",
    ]
    angelsMaleModifier = [
        "Unenvious",
        "Blessed",
        "Joyful",
        "True",
        "Unbegrudging",
        "Beloved",
        "Trustworthy",
    ]

    angelsFemale = [
        "Peace",
        "Gladness",
        "Rejoicing",
        "Blessedness",
        "Truth",
        "Love",
        "Faith",
    ]
    angelsFemaleModifier = [
        "Peaceful",
        "Glad",
        "Rejoicing",
        "Blessed",
        "Truthful",
        "Lovely",
        "Faithful",
    ]

    maleDemons = [demonsMale, demonsMaleModifier]
    femaleDemons = [demonsFemale, demonsFemaleModifier]
    maleAngels = [angelsMale, angelsMaleModifier]
    femaleAngels = [angelsFemale, angelsFemaleModifier]

    md_fd = [maleDemons, femaleDemons]
    fd_md = [femaleDemons, maleDemons]

    ma_fa = [maleAngels, femaleAngels]
    fa_ma = [femaleAngels, maleAngels]

    md_fa = [maleDemons, femaleAngels]
    fa_md = [femaleAngels, maleDemons]

    ma_fd = [maleAngels, femaleDemons]
    fd_ma = [femaleDemons, maleAngels]

    demonArray = [md_fd, md_fa, ma_fd, ma_fa, fd_md, fd_ma, fa_md, fa_ma]

    combination = demonArray[int(math.floor(random.uniform(0, len(demonArray))))]
    arrayToUse = combination[int(math.floor(random.uniform(0, len(combination))))]
    messageString = ""

    if scrllrMngr.sansSerif:
        font = ImageFont.truetype(config.path + "/assets/fonts/freefont/FreeSansBold.ttf", scrllrMngr.fontSize)
    else:
        font = ImageFont.truetype(config.path + "/assets/fonts/freefont/FreeSerifBold.ttf", scrllrMngr.fontSize)

    for _ in range(4):
        adj = arrayToUse[1][int(math.floor(random.uniform(0, 7)))]
        noun = arrayToUse[0][int(math.floor(random.uniform(0, 7)))]
        messageString = messageString + adj.upper() + " " + noun.upper() + "           "

    # print(messageString)

    if random.random() < 0.15:
        messageString = ""
        font = ImageFont.truetype(config.path + "/assets/fonts/freefont/FreeSans.ttf", scrllrMngr.fontSize)
        for _ in range(23):
            xo = "X" if (random.random() < 0.5) else "O"
            messageString = messageString + xo
            messageString = messageString + " " if (random.random() < 0.5) else messageString

    if scrllrMngr.colorMode == "getRandomRGB":
        clr = colorutils.getRandomRGB(config.brightness)
    if scrllrMngr.colorMode == "randomColor":
        clr = colorutils.randomColor(config.brightness)
    if scrllrMngr.colorMode == "getRandomColorWheel":
        clr = colorutils.getRandomColorWheel(config.brightness)

    """""" """""" """""" """""" """""" """""" """""" """""" """""" """"""
    # draw the message to get its size

    tempImage = Image.new("RGBA", (1200, 196))
    draw = ImageDraw.Draw(tempImage)

    # pixLen = draw.textsize(messageString, font=font)

    pixLen = [100, 10]
    # For some reason textsize is not getting full height !
    fontHeight = int(pixLen[1] * 1.3)

    """""" """""" """""" """""" """""" """""" """""" """""" """""" """"""
    # make a new image with the right size
    scrollImage = Image.new("RGBA", (pixLen[0] + 2, fontHeight))
    draw = ImageDraw.Draw(scrollImage)
    iid = scrollImage.im.id

    """""" """""" """""" """""" """""" """""" """""" """""" """""" """"""
    # Draw the text with "borders"
    indent = int(0.05 * config.tileSize[0])
    for i in range(1, scrllrMngr.shadowSize):
        draw.text((indent + -i, -i), messageString, (0, 0, 0), font=font)
        draw.text((indent + i, i), messageString, (0, 0, 0), font=font)

    draw.text((2, 0), messageString, clr, font=font)

    refDraw = ImageDraw.Draw(imageRef)
    refDraw.rectangle((0, 0, pixLen[0] + 2, fontHeight), fill=scrllrMngr.bgBackGroundColor)
    imageRef.paste(scrollImage, (0, scrllrMngr.textVOffest), scrollImage)


def remakeDaemonMessages(imageRef, direction=1):
    ##
    makeDaemonMessages(imageRef=imageRef, direction=direction)


def makeScrollBlock(imageRef, imageDrawRef, direction):
    global config, scrllrMngr
    w = imageRef.size[0]
    # config.enhancer = ImageEnhance.Brightness(config.loadedImage)
    # config.loadedImage = config.enhancer.enhance(config.overlayBrightness)

    widthImage = scrllrMngr.imageBlockImageLoaded.size[0]
    heightImage = scrllrMngr.imageBlockImageLoaded.size[1]
    hBuffer = scrllrMngr.imageBlockBuffer
    numberOfUnits = int(round(w / (widthImage + hBuffer)))

    # pieceLogger(f"{widthImage}  {heightImage} {scrllrMngr.imageBlockImageLoaded}")

    for i in range(numberOfUnits):
        x = i * (widthImage + hBuffer)
        y = scrllrMngr.yOffset

        tempImage = scrllrMngr.imageBlockImageLoaded.copy()
        # tempImage = tempImage.resize((round(widthImage*.9),round(heightImage*.9)))
        tempEnhancer = ImageEnhance.Brightness(tempImage)
        tempImage = tempEnhancer.enhance(config.brightness + scrllrMngr.foregroundImageBrightnessAddition)

        clrBlock = Image.new("RGBA", (widthImage, heightImage))
        clrBlockDraw = ImageDraw.Draw(clrBlock)

        # Color overlay on b/w PNG sprite
        # EVERYTHING HAS TO BE PNG  / have ALPHA
        if scrllrMngr.useTransparentImages == True:
            clr = colorutils.randomColorAlpha(brtns=config.brightness, maxTransparency=200)
        else:
            clr = colorutils.randomColor()
        clrBlockDraw.rectangle((0, 0, widthImage, heightImage), fill=clr)

        tempImage = ImageChops.multiply(clrBlock, tempImage)
        if random.random() < scrllrMngr.imageDrawProb:
            imageRef.paste(tempImage, (x, y), tempImage)


def remakeScrollBlock(imageRef, direction):
    drawRef = ImageDraw.Draw(imageRef)
    if random.random() < scrllrMngr.imageBlockRemakeProb:
        makeScrollBlock(imageRef, drawRef, direction)


def makeArrows(drawRef, direction=1):

    rows = scrllrMngr.displayCols * 2
    cols = scrllrMngr.arrowCols * 2

    xDiv = int(scrllrMngr.displayRows * config.windowWidth) / cols
    yDiv = config.canvasHeight / rows

    xStart = 0  # config.canvasWidth / 2
    yStart = scrllrMngr.bandHeight / 2  # config.canvasHeight / 2

    bufferDistance = 15
    arrowLength = cols * 2
    blade = cols / 3

    clr = (int(220 * config.brightness), 0, 0)

    drawRef.rectangle(
        (0, 0, int(scrllrMngr.displayRows * config.windowWidth), config.canvasHeight),
        fill=scrllrMngr.bgBackGroundColor,
    )

    for c in range(cols):
        yArrowEnd = yStart  # yStart + arrowLength
        xArrowEnd = xStart + arrowLength

        # the blades
        xDisplace = xArrowEnd - blade
        yDisplace = blade * math.tan(math.pi / 4)
        # the horizontal
        if random.random() < 0.5:
            drawRef.line(
                (xStart, yStart, xArrowEnd, yArrowEnd),
                fill=clr,
                width=scrllrMngr.lineThickness,
            )

            if direction == 1:
                drawRef.line(
                    (xArrowEnd - blade, yArrowEnd - yDisplace, xArrowEnd, yArrowEnd),
                    fill=clr,
                    width=scrllrMngr.lineThickness,
                )
                drawRef.line(
                    (xArrowEnd - blade, yArrowEnd + yDisplace, xArrowEnd, yArrowEnd),
                    fill=clr,
                    width=scrllrMngr.lineThickness,
                )
            else:
                drawRef.line(
                    (xStart + blade, yArrowEnd - yDisplace, xStart, yArrowEnd),
                    fill=clr,
                    width=scrllrMngr.lineThickness,
                )
                drawRef.line(
                    (xStart + blade, yArrowEnd + yDisplace, xStart, yArrowEnd),
                    fill=clr,
                    width=scrllrMngr.lineThickness,
                )

        # yStart += arrowLength + bufferDistance
        xStart += arrowLength + bufferDistance


def remakeArrowBlock(imageRef, direction):
    drawRef = ImageDraw.Draw(imageRef)
    makeArrows(drawRef, direction)


def makeMessage(imageRef, messageString="FooBar", direction=1):
    global config, scrllrMngr

    if scrllrMngr.colorMode == "getRandomRGB":
        clr = colorutils.getRandomRGB(config.brightness)
    if scrllrMngr.colorMode == "randomColor":
        clr = colorutils.randomColor(config.brightness)
    if scrllrMngr.colorMode == "getRandomColorWheel":
        clr = colorutils.getRandomColorWheel(config.brightness)


    """""" """""" """""" """""" """""" """""" """""" """""" """""" """"""
    # draw the message to get its size
    if scrllrMngr.sansSerif:
        # font = ImageFont.truetype(config.path + "/assets/fonts/freefont/FreeSansBold.ttf", scrllrMngr.fontSize)
        font = ImageFont.truetype(config.path + "/assets/fonts/roboto/RobotoCondensed-Bold.ttf", scrllrMngr.fontSize)
    else:
        font = ImageFont.truetype(config.path + "/assets/fonts/freefont/FreeSerifBold.ttf", scrllrMngr.fontSize)

    tempImage = Image.new("RGBA", (1200, 196))
    draw = ImageDraw.Draw(tempImage)
    # pixLen = draw.textsize(messageString, font=font)
    pixelLength = int(draw.textlength(messageString, font=font))

    # pieceLogger(pixelLength)
    # For some reason textsize is not getting full height !
    pixLen = [pixelLength + 2, scrllrMngr.fontSize]
    fontHeight = int(pixLen[1] * 1.3)

    """""" """""" """""" """""" """""" """""" """""" """""" """""" """"""
    # make a new image with the right size
    scrollImage = Image.new("RGBA", (pixLen[0] + 2, fontHeight))
    draw = ImageDraw.Draw(scrollImage)
    iid = scrollImage.im.id

    """""" """""" """""" """""" """""" """""" """""" """""" """""" """"""
    # Draw the text with "borders"
    indent = int(0.01 * config.tileSize[0])
    for i in range(0, scrllrMngr.shadowSize):
        draw.text((indent + -i, -i), messageString, (0, 0, 0, 180), font=font)
        draw.text((indent + i, i), messageString, (0, 0, 0, 180), font=font)

    pieceLogger(f"makeMesage called: {messageString}")
    draw.text((2, 0), messageString, clr, font=font)

    refDraw = ImageDraw.Draw(imageRef)
    # refDraw.rectangle((0, 0, pixLen[0] + 2, fontHeight), fill=None)

    imageRef.paste(scrollImage, (0, scrllrMngr.textVOffest), scrollImage)


def remakeMessage(imageRef, messageString="FooBar", direction=1):
    messageString = scrllrMngr.msg1 if random.random() < 0.5 else scrllrMngr.msg2
    # config.textVOffest = round(random.uniform(-12, -30))
    scrllrMngr.colorMode = "randomColor" if random.random() < 0.5 else "getRandomRGB"
    # makeMessage(imageRef=imageRef, messageString=messageString, direction=direction)


def makeBackGround(drawRef, n=1):
    def _draw_background(drawRef, cols, xDiv, steps):
        drawRef.rectangle((0, 0, (round(scrllrMngr.displayRows * config.canvasWidth)), config.canvasHeight), fill=scrllrMngr.bgBackGroundColor)
        rDelta = (scrllrMngr.bgBackGroundEndColor[0] - scrllrMngr.bgBackGroundColor[0]) / steps
        gDelta = (scrllrMngr.bgBackGroundEndColor[1] - scrllrMngr.bgBackGroundColor[1]) / steps
        bDelta = (scrllrMngr.bgBackGroundEndColor[2] - scrllrMngr.bgBackGroundColor[2]) / steps
        xPos = 0
        transitionCount = 0
        scrllrMngr.patternLengthTransition = 8
        lengthDelta = round((xDiv - scrllrMngr.currentPatternLength) / scrllrMngr.patternLengthTransition)
        patternLength = xDiv
        for c in range(cols):
            rCol = scrllrMngr.bgBackGroundColor[0] + rDelta
            gCol = scrllrMngr.bgBackGroundColor[1] + gDelta
            bCol = scrllrMngr.bgBackGroundColor[2] + bDelta
            scrllrMngr.bgBackGroundColor = (rCol, gCol, bCol)
            fillClr = (
                (round(scrllrMngr.bgBackGroundEndColor[0] - rDelta * (c + 1))),
                (round(scrllrMngr.bgBackGroundEndColor[1] - gDelta * (c + 1))),
                (round(scrllrMngr.bgBackGroundEndColor[2] - bDelta * (c + 1))),
                200,
            )
            w = patternLength
            outline = None
            if c < 0:
                outline = (255, 0, 0, 200)
            drawRef.rectangle((xPos, 0, xPos + w, config.canvasHeight), fill=fillClr, outline=outline)
            xPos += w
            if transitionCount < scrllrMngr.patternLengthTransition - 1:
                transitionCount += 1
            else:
                patternLength = xDiv
        scrllrMngr.bgBackGroundColor = scrllrMngr.bgBackGroundEndColor

    def _draw_foreground(drawRef, rows, cols, xDiv, yDiv, steps):
        rowMultiplier = 1
        colMultiplier = 1
        if scrllrMngr.pattern == "bricks":
            rowMultiplier = 1
            colMultiplier = 1
        elif scrllrMngr.pattern == "diamonds":
            rowMultiplier = 2
            colMultiplier = 2
        elif scrllrMngr.pattern == "harlequin":
            rowMultiplier = 2
            colMultiplier = 2
        elif scrllrMngr.pattern in ["regularLines", "pluses"]:
            rowMultiplier = 2
            colMultiplier = 1

        rDelta = (scrllrMngr.patternEndColor[0] - scrllrMngr.patternColor[0]) / steps
        gDelta = (scrllrMngr.patternEndColor[1] - scrllrMngr.patternColor[1]) / steps
        bDelta = (scrllrMngr.patternEndColor[2] - scrllrMngr.patternColor[2]) / steps

        xPos = 0
        xStart = 0
        yStart = 0
        transitionCount = 0
        scrllrMngr.patternLengthTransition = 8
        lengthDelta = round((xDiv - scrllrMngr.currentPatternLength) / scrllrMngr.patternLengthTransition)

        harlequinCount = 0
        gap = 2
        _c1 = tuple(scrllrMngr.harlequinColors[0])
        _c2 = tuple(scrllrMngr.harlequinColors[1])
        _c3 = tuple(scrllrMngr.harlequinColors[2])
        _c4 = tuple(scrllrMngr.harlequinColors[3])

        # pieceLogger(_c4)

        for c in range(cols + 1):
            _c4 = tuple(scrllrMngr.harlequinColors[3])
            rCol = scrllrMngr.patternColor[0] + rDelta
            gCol = scrllrMngr.patternColor[1] + gDelta
            bCol = scrllrMngr.patternColor[2] + bDelta
            scrllrMngr.patternColor = (rCol, gCol, bCol)
            fillClr = (
                (round(scrllrMngr.patternEndColor[0] - rDelta * (c + 1))),
                (round(scrllrMngr.patternEndColor[1] - gDelta * (c + 1))),
                (round(scrllrMngr.patternEndColor[2] - bDelta * (c + 1))),
                225,
            )
            patternLength = xDiv
            for r in range(rows):
                columnOffset = 0
                rowOffset = xDiv
                _c4 = tuple(scrllrMngr.harlequinColors[3])

                if r in [0, 2, 4, 6]:
                    columnOffset = xDiv

                if r / 2 % 2 == 0:
                    columnOffset = xDiv
                    rowOffset = 0
                    _c4 = tuple(random.choice(scrllrMngr.harlequinColors))

                if random.random() < scrllrMngr.patternDrawProb or c == 0 or scrllrMngr.pattern == "harlequin":
                    if scrllrMngr.pattern == "test":
                        drawRef.rectangle((xPos, 5, xPos + 4, 55), fill=fillClr)
                    if random.random() < scrllrMngr.redGreenSwapProb:
                        fillClr = (fillClr[1], fillClr[0], fillClr[2])
                    if random.random() < scrllrMngr.redBlueSwapProb:
                        fillClr = (fillClr[2], fillClr[1], fillClr[0])
                    if random.random() < scrllrMngr.greenBlueSwapProb:
                        fillClr = (fillClr[0], fillClr[2], fillClr[1])

                    if scrllrMngr.pattern == "harlequin":
                        fillClr = scrllrMngr.harlequinColors[harlequinCount]
                        harlequinCount += 1
                        if harlequinCount >= len(scrllrMngr.harlequinColors):
                            harlequinCount = 0

                        poly = [
                            (xStart, yStart + gap),
                            (xStart + xDiv / 2 - gap, yStart + yDiv),
                            (xStart, yStart + yDiv + yDiv - gap),
                        ]
                        if random.random() < scrllrMngr.patternDrawProb:
                            drawRef.polygon(poly, fill=_c4)

                        poly = [
                            (xStart + xDiv * 2, yStart + gap),
                            (xStart + xDiv * 2 * 0.75 + gap, yStart + yDiv),
                            (xStart + xDiv * 2, yStart + yDiv + yDiv - gap),
                        ]
                        if random.random() < scrllrMngr.patternDrawProb:
                            drawRef.polygon(poly, fill=_c4)

                        poly = [
                            (xStart + xDiv / 2 + gap, yStart + yDiv),
                            (xStart + xDiv, yStart + gap),
                            (xStart + xDiv + xDiv / 2 - gap, yStart + yDiv),
                            (xStart + xDiv, yStart + 2 * yDiv - gap),
                        ]
                        if random.random() < scrllrMngr.patternDrawProb:
                            drawRef.polygon(poly, fill=_c3)

                        poly = [
                            (xStart + gap, yStart),
                            (xStart + xDiv / 2, yStart + yDiv - gap),
                            (xStart + xDiv - gap, yStart),
                        ]
                        if random.random() < scrllrMngr.patternDrawProb:
                            drawRef.polygon(poly, fill=_c1)

                        poly = [
                            (xStart + gap, yStart + yDiv * 2),
                            (xStart + xDiv / 2, yStart + yDiv + gap),
                            (xStart + xDiv - gap, yStart + yDiv * 2),
                        ]
                        if random.random() < scrllrMngr.patternDrawProb:
                            drawRef.polygon(poly, fill=_c1)

                        poly = [
                            (xStart + xDiv + gap, yStart),
                            (xStart + xDiv + xDiv / 2, yStart + yDiv - gap),
                            (xStart + xDiv * 2 - gap, yStart),
                        ]
                        if random.random() < scrllrMngr.patternDrawProb:
                            drawRef.polygon(poly, fill=_c2)

                        poly = [
                            (xStart + xDiv + gap, yStart + 2 * yDiv),
                            (xStart + xDiv + xDiv / 2, yStart + yDiv + gap),
                            (xStart + xDiv * 2 - gap, yStart + 2 * yDiv),
                        ]
                        if random.random() < scrllrMngr.patternDrawProb:
                            drawRef.polygon(poly, fill=_c2)

                    if scrllrMngr.pattern == "diamonds":
                        poly = [
                            (xStart, yStart + yDiv),
                            (xStart + xDiv, yStart),
                            (xStart + xDiv + xDiv, yStart + yDiv),
                            (xStart + xDiv, yStart + yDiv + yDiv),
                        ]
                        drawRef.polygon(poly, fill=fillClr)
                    if scrllrMngr.pattern == "bricks":
                        length = xDiv
                        yPos = yStart
                        drawRef.rectangle(
                            (xPos + columnOffset, yPos, xPos + columnOffset + length, yPos + yDiv),
                            fill=fillClr,
                            outline=None,
                        )
                    if scrllrMngr.pattern == "pluses":
                        length = xDiv
                        height = xDiv / 2
                        yPos = yStart
                        xPos2 = xPos + round(length / 2 - height / 2)
                        yPos2 = round(yPos - length / 2 + height / 2)
                        drawRef.rectangle(
                            (xPos + columnOffset, yPos, xPos + length + columnOffset, yPos + yDiv),
                            fill=fillClr,
                            outline=None,
                        )
                        drawRef.rectangle(
                            (xPos2, yPos2, xPos2 + height, yPos2 + length),
                            fill=fillClr,
                            outline=None,
                        )
                    if scrllrMngr.pattern == "regularLines":
                        length = patternLength
                        yPos = yStart
                        drawRef.rectangle((xPos + columnOffset, yPos, xPos + length + columnOffset, yPos + yDiv), fill=fillClr)
                    if scrllrMngr.pattern == "lines":
                        length = int(round(random.uniform(1, 2 * xDiv)))
                        offset = int(round(random.uniform(0, 4 * xDiv)))
                        if random.random() < 0.5:
                            drawRef.rectangle(
                                (xStart, yStart, xStart + 2 * xDiv, yStart + yDiv),
                                fill=fillClr,
                                outline=None,
                            )
                        else:
                            drawRef.rectangle(
                                (
                                    xStart + offset,
                                    yStart,
                                    xStart + length + offset,
                                    yStart + yDiv,
                                ),
                                fill=fillClr,
                                outline=None,
                            )
                yStart += rowMultiplier * yDiv
                if scrllrMngr.pattern == "harlequin":
                    xStart += 0

            if transitionCount < scrllrMngr.patternLengthTransition - 1:
                transitionCount += 1
            else:
                scrllrMngr.currentPatternLength = xDiv
            xStart += colMultiplier * xDiv if scrllrMngr.pattern == "lines" else xDiv * 2
            xPos += xDiv
            yStart = 0
        scrllrMngr.patternColor = scrllrMngr.patternEndColor
        scrllrMngr.currentPatternLength = xDiv

    rows = scrllrMngr.patternRows * 1
    cols = scrllrMngr.patternCols * 1
    xDiv = 2 * config.canvasWidth * scrllrMngr.displayCols / cols
    yDiv = (config.canvasHeight / rows) / scrllrMngr.displayRows
    steps = cols
    scrllrMngr.arrowBgBackGroundColor = (0, 0, 0, 20)
    colorChange = False

    _draw_background(drawRef, cols, xDiv, steps)
    _draw_foreground(drawRef, rows, cols, xDiv, yDiv, steps)

    if scrllrMngr.alwaysRandomPattern == True:
        if random.random() < 0.15:
            scrllrMngr.patternDrawProb = random.uniform(0.08, 0.8)
        if random.random() < 0.15:
            scrllrMngr.patternRows = round(random.uniform(8, config.canvasHeight))
        if random.random() < 0.15:
            scrllrMngr.patternCols = round(random.uniform(4, config.canvasWidth))
        if random.random() < 0.15:
            if random.random() < 0.5:
                scrllrMngr.pattern == "lines"
            else:
                scrllrMngr.pattern == "pluses"
    else:
        scrllrMngr.pattern == scrllrMngr.initialPattern

    scrllrMngr.patternColor = scrllrMngr.patternEndColor
    if random.random() < scrllrMngr.backgroundColorChangeProb:
        scrllrMngr.patternEndColor = colorutils.getRandomColorHSV(
            scrllrMngr.fg_minHue,
            scrllrMngr.fg_maxHue,
            scrllrMngr.fg_minSaturation,
            scrllrMngr.fg_maxSaturation,
            scrllrMngr.fg_minValue,
            scrllrMngr.fg_maxValue,
            scrllrMngr.fg_dropHueMinValue,
            scrllrMngr.fg_dropHueMaxValue,
            255,
            config.brightness,
        )

    scrllrMngr.bgBackGroundColor = scrllrMngr.bgBackGroundEndColor
    if random.random() < scrllrMngr.backgroundColorChangeProb:
        scrllrMngr.bgBackGroundEndColor = colorutils.getRandomColorHSV(
            scrllrMngr.bg_minHue,
            scrllrMngr.bg_maxHue,
            scrllrMngr.bg_minSaturation,
            scrllrMngr.bg_maxSaturation,
            scrllrMngr.bg_minValue,
            scrllrMngr.bg_maxValue,
            scrllrMngr.bg_dropHueMinValue,
            scrllrMngr.bg_dropHueMaxValue,
            255,
            config.brightness,
        )


## Layer imagery callbacks & regeneration functions
def remakePatternBlock(imageRef, direction):
    # print("remakePatternBlock")
    ## Stacking the cards ...

    """
    if config.setPatternColor == True :
        config.setPatternEndColor = colorutils.getRandomColorHSV(
                config.fg_minHue, config.fg_maxHue,
                config.fg_minSaturation, config.fg_maxSaturation,
                config.fg_minValue, config.fg_maxValue,
                config.fg_dropHueMinValue, config.fg_dropHueMaxValue, 255, config.brightness)
        config.patternEndColor = config.setPatternEndColor
        config.patternColor = config.setPatternEndColor
    """

    if scrllrMngr.alwaysRandomPattern == True:
        if random.random() < 0.15:
            scrllrMngr.patternDrawProb = random.uniform(0.08, 0.8)

        if random.random() < 0.15:
            scrllrMngr.patternRows = round(random.uniform(8, config.canvasHeight))

        if random.random() < 0.15:
            scrllrMngr.patternCols = round(random.uniform(4, config.canvasWidth))

        if random.random() < 0.15:
            if random.random() < 0.5:
                scrllrMngr.pattern == "lines"
            else:
                scrllrMngr.pattern == "pluses"
    else:
        scrllrMngr.pattern == scrllrMngr.initialPattern

    scrllrMngr.patternColor = scrllrMngr.patternEndColor
    if random.random() < scrllrMngr.backgroundColorChangeProb:
        scrllrMngr.patternEndColor = colorutils.getRandomColorHSV(
            scrllrMngr.fg_minHue,
            scrllrMngr.fg_maxHue,
            scrllrMngr.fg_minSaturation,
            scrllrMngr.fg_maxSaturation,
            scrllrMngr.fg_minValue,
            scrllrMngr.fg_maxValue,
            scrllrMngr.fg_dropHueMinValue,
            scrllrMngr.fg_dropHueMaxValue,
            255,
            config.brightness,
        )

    scrllrMngr.bgBackGroundColor = scrllrMngr.bgBackGroundEndColor
    if random.random() < scrllrMngr.backgroundColorChangeProb:
        scrllrMngr.bgBackGroundEndColor = colorutils.getRandomColorHSV(
            scrllrMngr.bg_minHue,
            scrllrMngr.bg_maxHue,
            scrllrMngr.bg_minSaturation,
            scrllrMngr.bg_maxSaturation,
            scrllrMngr.bg_minValue,
            scrllrMngr.bg_maxValue,
            scrllrMngr.bg_dropHueMinValue,
            scrllrMngr.bg_dropHueMaxValue,
            255,
            config.brightness,
        )

    overlayControls.altColor = scrllrMngr.bgBackGroundEndColor
    drawRef = ImageDraw.Draw(imageRef)
    makeBackGround(drawRef, direction)


def runWork():
    global config
    pieceLogger("RUNNING Scroller Holder scroller-holder-v2.py", 2)
    while config.isRunning == True:
        iterate()
        time.sleep(config.redrawSpeed)
        if config.standAlone == False:
            config.callBack()


def checkTime(scrollerObj):
    scrllrMngr.t2 = time.time()
    delta = scrllrMngr.t2 - scrllrMngr.t1

    if delta > scrllrMngr.timeToComplete and scrllrMngr.deltaTimeDone == False:

        scrollerObj.xSpeed -= 0.2

        if scrollerObj.xSpeed <= 0.70:
            scrllrMngr.deltaTimeDone = True
            scrllrMngr.useFadeThruAnimation = True
            scrllrMngr.f.fadingDone = True

            # print ("DELTA TIME UP")
            processImageForScrolling()
            if scrllrMngr.useUltraSlowSpeed == True:
                scrollerObj.xSpeed = 1


def processImageForScrolling():
    global overlayControls
    ## Run through each of the objects being scrolled - text, image, background etc
    for scrollerObj in scrllrMngr.scrollArray:
        scrollerObj.scroll()

        if scrollerObj.typeOfScroller != "foo":
            config.canvasImage.paste(scrollerObj.canvas, (0, 0), scrollerObj.canvas)
        else:
            config.textImage.paste(scrollerObj.canvas, (0, scrollerObj.textSlide * scrllrMngr.bandHeight), scrollerObj.canvas)

    # Chop up the scrollImage into "rows"
    for n in range(0, scrllrMngr.displayRows):
        segment = config.canvasImage.crop(
            (
                n * config.canvasWidth,
                0,
                config.canvasWidth + n * config.canvasWidth,
                scrllrMngr.bandHeight,
            )
        )
        textsegment = config.textImage.crop(
            (
                n * config.canvasWidth,
                0,
                config.canvasWidth + n * config.canvasWidth,
                scrllrMngr.bandHeight,
            )
        )

        if (n % 2 == 0) and (scrllrMngr.displayRows > 1) and scrllrMngr.altDirectionScrolling:
            segment = ImageOps.flip(segment)
            # segment = ImageOps.mirror(segment)
            segment = segment.rotate(180)


        # segment = ImageChops.add_modulo(segment, textsegment)
        # segment = ImageChops.composite(segment, textsegment, textsegment)
        # segment = ImageChops.overlay( textsegment, segment)
        config.workImage.paste(segment, (0, n * scrllrMngr.bandHeight))
        # config.workImage.paste(textsegment, (0, n * scrllrMngr.bandHeight))

        overlayControls.handleOverlayActions()

    if scrllrMngr.useOverLayImage == True:
        if random.random() < scrllrMngr.overlayGlitchRate:
            glitchBox(scrllrMngr.loadedImage, -scrllrMngr.overlayGlitchSize, scrllrMngr.overlayGlitchSize)
        if random.random() < scrllrMngr.overlayResetRate:
            scrllrMngr.loadedImage.paste(scrllrMngr.loadedImageCopy)
        config.workImage.paste(
            scrllrMngr.loadedImage,
            (scrllrMngr.overLayXPos, scrllrMngr.overLayYPos),
            scrllrMngr.loadedImage,
        )

    if scrllrMngr.overallBlur != 0:
        config.workImage = config.workImage.filter(ImageFilter.GaussianBlur(radius=scrllrMngr.overallBlur))


def iterate():
    global config, overlayControls

    # config.workImageDraw.rectangle((0,0,config.canvasWidth,config.canvasHeight), fill  = (0,0,0))
    # config.canvasImageDraw.rectangle((0,0,config.canvasWidth*10,config.canvasHeight), fill  = (0,0,0,20))

    for scrollerObj in scrllrMngr.scrollArray:
        if scrollerObj.typeOfScroller == "bg":
            if random.random() < scrllrMngr.changeProb * scrllrMngr.changeProbReleaseFactor and scrllrMngr.deltaTimeDone == True and scrllrMngr.useFadeThruAnimation == True:
                scrllrMngr.useFadeThruAnimation = False
                scrollerObj.xSpeed = random.uniform(0.6, scrollerObj.xMaxSpeed)
                scrllrMngr.deltaTimeDone = False
                scrllrMngr.t1 = time.time()
                scrllrMngr.timeToComplete = random.uniform(3, 10)
            checkTime(scrollerObj)

    if scrllrMngr.useFadeThruAnimation == True and scrllrMngr.useUltraSlowSpeed == True:
        if scrllrMngr.f.fadingDone == True:

            scrllrMngr.renderImageFullOld = config.renderImageFull.copy()
            config.renderImageFull.paste(
                config.workImage,
                (config.imageXOffset, config.imageYOffset),
                config.workImage,
            )
            scrllrMngr.f.xPos = config.imageXOffset
            scrllrMngr.f.yPos = config.imageYOffset
            # config.renderImageFull = config.renderImageFull.convert("RGBA")
            # renderImageFull = renderImageFull.convert("RGBA")
            scrllrMngr.f.setUp(
                scrllrMngr.renderImageFullOld.convert("RGBA"),
                config.workImage.convert("RGBA"),
            )
            processImageForScrolling()

        scrllrMngr.f.fadeIn()
        config.render(scrllrMngr.f.blendedImage, 0, 0)

    else:
        processImageForScrolling()
        config.renderImageFull.paste(
            config.workImage,
            (config.imageXOffset, config.imageYOffset),
            config.workImage,
        )

        # RENDERING AS A MOCKUP OR AS REAL
        if config.useDrawingPoints == True:
            config.panelDrawing.canvasToUse = config.renderImageFull
            config.panelDrawing.render()
        else:
            # config.render(config.canvasImage, 0, 0, config.canvasWidth, config.canvasHeight)
            # config.render(config.image, 0, 0)
            config.render(config.renderImageFull, 0, 0)


def main(run=True):
    global config, threads, thrd, scrllrMngr
    scrllrMngr = ScrollerManager(config)
    scrllrMngr.setUp(workConfig)

    if run:
        runWork()


### Kick off .......
if __name__ == "__main__":
    main()
