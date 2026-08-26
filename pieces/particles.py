import itertools
import math
import random

import time
from modules.configuration import bcolors, pieceLogger
from modules import coloroverlay, colorutils, panelDrawing
from modules.particleobjects.particle import Particle
from modules.particleobjects.particlesystem import ParticleSystem
from PIL import (
    Image,
    ImageChops,
    ImageDraw,
    ImageFilter,
    ImageFont,
    ImageOps,
)
import noise

# from noise import *
from modules.holder_director import Director


# ----------------------------------------------------------------------------------- #
class ParticleManager:
    def __init__(self, config):
        self.config = config

    def setUp(self, workConfig):
        self.canvasImageWidth = self.config.canvasWidth
        self.canvasImageHeight = self.config.canvasHeight
        self.canvasImageWidth -= 4
        self.canvasImageHeight -= 4
        self.numUnits = 60

        """
		self.fontColorVals = ((workConfig.get("diag", 'fontColor')).split(','))
		self.fontColor = tuple(map(lambda x: int(int(x)  * self.config.brightness), self.fontColorVals))
		self.outlineColorVals = ((workConfig.get("diag", 'outlineColor')).split(','))
		self.outlineColor = tuple(map(lambda x: int(int(x) * self.config.brightness) , self.outlineColorVals))
		"""

        self.fontSize = 14
        self.font = ImageFont.truetype(self.config.path + "/assets/fonts/freefont/FreeSansBold.ttf", self.fontSize)

        self.bgColorVals = (workConfig.get("particleSystem", "bgColor")).split(",")
        self.bgColor = tuple(map(lambda x: int(int(x) * self.config.brightness), self.bgColorVals))

        try:
            self.bgTransitions = workConfig.getboolean("particleSystem", "bgTransitions")
            self.colOverlayA = coloroverlay.ColorOverlay()
            self.bgRangeA = int(workConfig.get("particleSystem", "bgRangeA"))
            self.bgRangeB = int(workConfig.get("particleSystem", "bgRangeB"))
            self.colOverlayA.randomRange = (self.bgRangeA, self.bgRangeB)
            # self.colOverlayA.colorA = tuple(int(a*self.config.brightness) for a in (colorutils.getRandomColor()))
            self.colOverlayA.minHue = int(workConfig.get("particleSystem", "minHue"))
            self.colOverlayA.maxHue = int(workConfig.get("particleSystem", "maxHue"))

            self.colOverlayA.minValue = float(workConfig.get("particleSystem", "minValue"))
            self.colOverlayA.maxValue = float(workConfig.get("particleSystem", "maxValue"))

            self.colOverlayA.maxBrightness = float(workConfig.get("particleSystem", "maxBrightness"))
            self.colOverlayA.bgTransparency = float(workConfig.get("particleSystem", "bgTransparency"))
            self.colOverlayA.randomSteps = True
            self.colOverlayA.timeTrigger = True
            self.colOverlayA.tLimitBase = int(workConfig.get("particleSystem", "tLimitBase"))
            self.colOverlayA.setStartColor()
            self.colOverlayA.getNewColor()
            self.colOverlayA.colorTransitionSetup()

        except Exception as e:
            pieceLogger(e, 1)
            self.bgTransitions = False

        try:
            self.transformShape = workConfig.getboolean("particleSystem", "transformShape")
            transformTuples = workConfig.get("particleSystem", "transformTuples").split(",")
            self.transformTuples = tuple([float(i) for i in transformTuples])
        except Exception as e:
            pieceLogger(e, 1)
            self.transformShape = False

        try:
            self.torqueDelta = int(workConfig.get("particleSystem", "torqueDelta"))
            self.torqueRate = float(workConfig.get("particleSystem", "torqueRate"))
        except Exception as e:
            pieceLogger(e, 1)
            self.torqueDelta = 0
            self.torqueRate = 0

        try:
            self.xWind = float(workConfig.get("particleSystem", "xWind"))
        except Exception as e:
            pieceLogger(e, 1)
            self.xWind = 0

        try:
            self.particleWinkOutXMin = float(workConfig.get("particleSystem", "particleWinkOutXMin"))
            self.particleWinkOutYMin = float(workConfig.get("particleSystem", "particleWinkOutYMin"))
        except Exception as e:
            pieceLogger(e, 1)
            self.particleWinkOutXMin = 5
            self.particleWinkOutYMin = 5

        try:
            self.pixelSortProbChange = float(workConfig.get("displayconfig", "pixelSortProbChange"))
            self.pixelSortProbChangeMin = float(workConfig.get("displayconfig", "pixelSortProbChangeMin"))
            self.pixelSortProbChangeMax = float(workConfig.get("displayconfig", "pixelSortProbChangeMax"))
        except Exception as e:
            pieceLogger(e, 1)
            self.pixelSortProbChange = 0

        try:
            self.restartProb = float(workConfig.get("particleSystem", "restartProb"))
        except Exception as e:
            pieceLogger(e, 1)
            self.restartProb = 0

        try:
            self.filterRemapping = workConfig.getboolean("particleSystem", "filterRemapping")
            self.filterRemappingProb = float(workConfig.get("particleSystem", "filterRemappingProb"))
            self.filterRemapminHoriSize = int(workConfig.get("particleSystem", "filterRemapminHoriSize"))
            self.filterRemapminVertSize = int(workConfig.get("particleSystem", "filterRemapminVertSize"))
        except Exception as e:
            pieceLogger(e, 1)
            self.filterRemapping = False
            self.filterRemappingProb = 0.0
            self.filterRemapminHoriSize = 24
            self.filterRemapminVertSize = 24

        try:
            self.filterRemapRangeX = int(workConfig.get("particleSystem", "filterRemapRangeX"))
            self.filterRemapRangeY = int(workConfig.get("particleSystem", "filterRemapRangeY"))
        except Exception as e:
            pieceLogger(e, 1)
            self.filterRemapRangeX = self.config.canvasWidth
            self.filterRemapRangeY = self.config.canvasHeight

        """
		Why this? because desaturation transitions are not always expected, because Phil and Sarah suggested it
		Because colors are more interesting against gray, because everything goes gray

		Rate of desaturation is set as greyRate

		Sorry about schitzoid spelling of grey-gray

		"""

        try:
            self.pixelsGoGray = workConfig.getboolean("particleSystem", "pixelsGoGray")
            self.greyRate = float(workConfig.get("particleSystem", "greyRate"))
        except Exception as e:
            pieceLogger(e, 1)
            self.pixelsGoGray = False

        # ok this may seem screwy, but because I made an error a while ago, the jumpToGray
        # effect is actually default ... so if you want gradual turn to gray, it must be set
        # actively. blurp. ugh.
        try:
            self.jumpToGray = workConfig.getboolean("particleSystem", "jumpToGray")
        except Exception as e:
            pieceLogger(e, 1)
            self.jumpToGray = True

        try:
            self.pixelsGoGrayModel = int(workConfig.get("particleSystem", "pixelsGoGrayModel"))
        except Exception as e:
            pieceLogger(e, 1)
            self.pixelsGoGrayModel = 3

        self.variance = float(workConfig.get("particleSystem", "variance"))

        self.fillColorVals = (workConfig.get("particleSystem", "fillColor")).split(",")
        self.fillColor = tuple(map(lambda x: int(int(x) * self.config.brightness), self.fillColorVals))

        self.outlineColorVals = (workConfig.get("particleSystem", "outlineColor")).split(",")
        self.outlineColor = tuple(map(lambda x: int(int(x) * self.config.brightness), self.outlineColorVals))

        try:
            self.extraOutlineColorVals = (workConfig.get("particleSystem", "extraOutlineColor")).split(",")
            self.extraOutlineColor = tuple(
                map(
                    lambda x: round(int(x) * self.config.brightness),
                    self.extraOutlineColorVals,
                )
            )
        except Exception as e:
            pieceLogger(e, 1)
            self.extraOutlineColor = None

        try:
            self.pUseHSV = workConfig.getboolean("particleSystem", "pUseHSV")
            pFillRange = (workConfig.get("particleSystem", "pFillRange")).split(",")
            self.pFillRange = tuple(map(lambda x: (float(x) * self.config.brightness), pFillRange))
            pOutlineRange = (workConfig.get("particleSystem", "pOutlineRange")).split(",")
            self.pOutlineRange = tuple(map(lambda x: (float(x) * self.config.brightness), pOutlineRange))
        except Exception as e:
            pieceLogger(f"error : {str(e)} with pUseHSV", 1)
            self.pUseHSV = False

        # second color for some particles
        try:
            self.useSecondColorProb = float(workConfig.get("particleSystem", "useSecondColorProb"))
            self.fillColorVals2 = (workConfig.get("particleSystem", "fillColor2")).split(",")
            self.fillColor2 = tuple(map(lambda x: int(int(x) * self.config.brightness), self.fillColorVals2))

            self.outlineColorVals2 = (workConfig.get("particleSystem", "outlineColor2")).split(",")
            self.outlineColor2 = tuple(map(lambda x: int(int(x) * self.config.brightness), self.outlineColorVals2))

            try:
                self.extraOutlineColorVals2 = (workConfig.get("particleSystem", "extraOutlineColor2")).split(",")
                self.extraOutlineColor2 = tuple(
                    map(
                        lambda x: round(int(x) * self.config.brightness),
                        self.extraOutlineColorVals2,
                    )
                )
            except Exception as e:
                pieceLogger(e, 1)
                self.extraOutlineColor2 = None
        except Exception as e:
            pieceLogger(e, 1)
            self.useSecondColorProb = 0
            self.extraOutlineColor2 = self.extraOutlineColor
            self.fillColor2 = self.fillColor
            self.outlineColor2 = self.outlineColor
            self.extraOutlineColor2 = self.extraOutlineColor

        self.overallBlur = int(workConfig.get("particleSystem", "overallBlur"))

        try:
            self.legacyUnsharpMask = workConfig.getboolean("particleSystem", "legacyUnsharpMask")
            self.optionallegacyToggleProb = float(workConfig.get("particleSystem", "optionallegacyToggleProb"))
        except Exception as e:
            pieceLogger(e, 1)
            self.legacyUnsharpMask = True
            self.optionallegacyToggleProb = 0

        try:
            self.useWaveDistortion = workConfig.getboolean("particleSystem", "useWaveDistortion")
            self.waveAmplitude = float(workConfig.get("particleSystem", "waveAmplitude"))
            self.wavePeriodMod = float(workConfig.get("particleSystem", "wavePeriodMod"))
            self.wavegridspace = int(workConfig.get("particleSystem", "wavegridspace"))
            self.pNoiseMod = float(workConfig.get("particleSystem", "pNoiseMod"))
        except Exception as e:
            pieceLogger(e, 1)
            self.useWaveDistortion = False

        self.useOverLay = workConfig.getboolean("particleSystem", "useOverLay")
        self.overlayColorVals = (workConfig.get("particleSystem", "overlayColor")).split(",")
        self.overlayColor = tuple(map(lambda x: int(int(x) * self.config.brightness), self.overlayColorVals))
        self.clrBlkWidth = int(workConfig.get("particleSystem", "clrBlkWidth"))
        self.clrBlkHeight = int(workConfig.get("particleSystem", "clrBlkHeight"))
        self.overlayxPos = int(workConfig.get("particleSystem", "overlayxPos"))
        self.overlayyPos = int(workConfig.get("particleSystem", "overlayyPos"))

        try:
            self.useOverLayEnhanced = workConfig.getboolean("particleSystem", "useOverLayEnhanced")
            self.useOverOnBG = workConfig.getboolean("particleSystem", "useOverOnBG")
        except Exception as e:
            pieceLogger(e, 1)
            self.useOverLayEnhanced = False
            self.useOverOnBG = False

        self.xPos = 0


class WaveDeformer:
    def transform(self, x, y):
        y = y + pMngr.waveAmplitude * math.sin((x + pMngr.xPos) / pMngr.wavePeriodMod) * noise.pnoise2(math.sin(x), y / pMngr.pNoiseMod)
        return x, y

    def transform_rectangle(self, x0, y0, x1, y1):
        return (
            *self.transform(x0, y0),
            *self.transform(x0, y1),
            *self.transform(x1, y1),
            *self.transform(x1, y0),
        )

    def getmesh(self, img):
        self.w, self.h = img.size

        target_grid = [
            (x, y, x + pMngr.wavegridspace, y + pMngr.wavegridspace)
            for x, y in itertools.product(
                range(0, self.w, pMngr.wavegridspace),
                range(0, self.h, pMngr.wavegridspace),
            )
        ]
        source_grid = [self.transform_rectangle(*rect) for rect in target_grid]

        return list(zip(target_grid, source_grid))


def main(run=True):
    global config, directionOrder, ps, pMngr
    global workConfig
    pieceLogger("Particles Loaded", 2, True)
    colorutils.brightness = config.brightness

    pMngr = ParticleManager(config)
    pMngr.setUp(workConfig)

    config.canvasImage = Image.new("RGBA", (pMngr.canvasImageWidth, pMngr.canvasImageHeight))

    ps = ParticleSystem(config)
    ps.unitArray = []

    ps.xGravity = float(workConfig.get("particleSystem", "xGravity"))
    ps.yGravity = float(workConfig.get("particleSystem", "yGravity"))
    ps.damping = float(workConfig.get("particleSystem", "damping"))
    ps.collisionDamping = float(workConfig.get("particleSystem", "collisionDamping"))
    ps.borderCollisions = workConfig.getboolean("particleSystem", "borderCollisions")
    ps.ignoreBottom = workConfig.getboolean("particleSystem", "ignoreBottom")
    ps.expireOnExit = workConfig.getboolean("particleSystem", "expireOnExit")
    ps.changeCohesion = workConfig.getboolean("particleSystem", "changeCohesion")

    try:
        ps.changechangeCohesionProb = float(workConfig.get("particleSystem", "changechangeCohesionProb"))
    except Exception as e:
        pieceLogger(e, 1)
        ps.changechangeCohesionProb = 0.0005

    ps.useFlocking = workConfig.getboolean("particleSystem", "useFlocking")
    ps.cohesionDistance = float(workConfig.get("particleSystem", "cohesionDistance"))
    ps.repelDistance = float(workConfig.get("particleSystem", "repelDistance"))
    ps.distanceFactor = float(workConfig.get("particleSystem", "distanceFactor"))
    ps.clumpingFactor = float(workConfig.get("particleSystem", "clumpingFactor"))
    ps.repelFactor = float(workConfig.get("particleSystem", "repelFactor"))

    ps.cohesionDegrades = float(workConfig.get("particleSystem", "cohesionDegrades"))
    ps.speedMin = float(workConfig.get("particleSystem", "speedMin"))
    ps.speedMax = float(workConfig.get("particleSystem", "speedMax"))
    ps.numUnits = int(workConfig.get("particleSystem", "numUnits"))

    ps.centerRangeXMin = int(workConfig.get("particleSystem", "centerRangeXMin"))
    ps.centerRangeYMin = int(workConfig.get("particleSystem", "centerRangeYMin"))
    ps.centerRangeXMax = int(workConfig.get("particleSystem", "centerRangeXMax"))
    ps.centerRangeYMax = int(workConfig.get("particleSystem", "centerRangeYMax"))

    ps.objType = workConfig.get("particleSystem", "objType")

    if ps.objType == "image":
        ps.objImage = workConfig.get("particleSystem", "objImage")
        ps.objImageColorize = workConfig.getboolean("particleSystem", "objImageColorize")
        ps.objImageFlipRate = float(workConfig.get("particleSystem", "objImageFlipRate"))
        ps.objImageRotateRate = float(workConfig.get("particleSystem", "objImageRotateRate"))
        ps.objImageAlphaBlend = float(workConfig.get("particleSystem", "objImageAlphaBlend"))
        arg = config.path + "assets/" + ps.objImage
        ps.loadedImage = Image.open(arg, "r")
        ps.loadedImage.load()
        ps.loadedImageCopy = ps.loadedImage.copy()

    try:
        config.renderDiagnostics = workConfig.getboolean("particleSystem", "renderDiagnostics")
        config.renderDiagnosticsCall = renderDiagnosticsCall
    except Exception as e:
        pieceLogger(e, 1)
        config.renderDiagnostics = False

    # managing speed of animation and framerate
    config.directorController = Director(config)

    try:
        config.delay = float(workConfig.get("particleSystem", "delay"))
    except Exception as e:
        pieceLogger(e, 1)
        config.delay = 0.01
        ps.delay = 0.01
    try:
        config.directorController.slotRate = float(workConfig.get("particleSystem", "slotRate"))
    except Exception as e:
        pieceLogger(e, 1)
        pieceLogger("SHOULD ADJUST TO USE slotRate AS FRAMERATE ")
        config.directorController.slotRate = 0.03

    try:
        ps.meanderFactor = float(workConfig.get("particleSystem", "meanderFactor"))
    except Exception as e:
        pieceLogger(e, 1)
        ps.meanderFactor = 1.0

    pieceLogger(ps.meanderFactor)

    try:
        ps.meanderFactor2 = float(workConfig.get("particleSystem", "meanderFactor2"))
    except Exception as e:
        pieceLogger(e, 1)
        ps.meanderFactor2 = 90.0

    try:
        ps.meanderDirection = int(workConfig.get("particleSystem", "meanderDirection"))
    except Exception as e:
        pieceLogger(e, 1)
        ps.meanderDirection = 0

    try:
        ps.objTrails = workConfig.getboolean("particleSystem", "objTrails")
    except Exception as e:
        pieceLogger(e, 1)
        ps.objTrails = True

    try:
        ps.linearMotionAlsoHorizontal = workConfig.getboolean("particleSystem", "linearMotionAlsoHorizontal")
    except Exception as e:
        pieceLogger(e, 1)
        ps.linearMotionAlsoHorizontal = True

    try:
        ps.oneDirection = workConfig.getboolean("particleSystem", "oneDirection")
    except Exception as e:
        pieceLogger(e, 1)
        ps.oneDirection = False

    try:
        ps.reEmitNumber = int(workConfig.get("particleSystem", "reEmitNumber"))
    except Exception as e:
        pieceLogger(e, 1)
        ps.reEmitNumber = 2

    try:
        ps.fixedUnitArray = workConfig.getboolean("particleSystem", "fixedUnitArray")
    except Exception as e:
        pieceLogger(e, 1)
        ps.fixedUnitArray = False

    try:
        ps.transparencyRange = workConfig.get("particleSystem", "transparencyRange").split(",")
        ps.transparencyRange = tuple(map(lambda x: int(int(x)), ps.transparencyRange))
    except Exception as e:
        pieceLogger(e, 1)
        ps.transparencyRange = (10, 200)

    ps.movement = workConfig.get("particleSystem", "movement")
    ps.objColor = workConfig.get("particleSystem", "objColor")
    ps.objWidth = int(workConfig.get("particleSystem", "objWidth"))
    ps.objHeight = int(workConfig.get("particleSystem", "objHeight"))
    ps.widthRate = float(workConfig.get("particleSystem", "widthRate"))
    ps.heightRate = float(workConfig.get("particleSystem", "heightRate"))

    try:
        ps.objWidthMax = int(workConfig.get("particleSystem", "objWidthMax"))
        ps.objHeightMax = int(workConfig.get("particleSystem", "objHeightMax"))

        ps.objWidthMin = int(workConfig.get("particleSystem", "objWidthMin"))
        ps.objHeightMin = int(workConfig.get("particleSystem", "objHeightMin"))
    except Exception as e:
        pieceLogger(e, 1)
        ps.objWidthMax = ps.objWidth
        ps.objHeightMax = ps.objHeight
        ps.objWidthMin = ps.objWidth
        ps.objHeightMin = ps.objHeight

    try:
        ps.rndSizeFactorMin = float(workConfig.get("particleSystem", "rndSizeFactorMin"))
        ps.rndSizeFactorMax = float(workConfig.get("particleSystem", "rndSizeFactorMax"))
    except Exception as e:
        pieceLogger(e, 1)
        ps.rndSizeFactorMin = 0.5
        ps.rndSizeFactorMax = 1.5

    ps.unitBlur = int(workConfig.get("particleSystem", "unitBlur"))

    # THIS IS USED AS WAY TO MOCKUP A CONFIGURATION OF RECTANGULAR PANELS
    panelDrawing.mockupBlock(config, workConfig)
    # Need to add something like this at final render call  as well
    """
		########### RENDERING AS A MOCKUP OR AS REAL ###########
		if config.useDrawingPoints  :
			config.panelDrawing.canvasToUse = config.renderImageFull
			config.panelDrawing.render()
		else :
			# config.render(config.canvasImage, 0, 0, config.canvasWidth, config.canvasHeight)
			# config.render(config.image, 0, 0)
			config.render(config.renderImageFull, 0, 0)
	"""

    for _ in range(ps.numUnits):
        emitParticle()

    setUp()

    # config.debugSelf()

    if run:
        runWork()


# ----------------------------------------------------------------------------------- #


def emitParticle(i=None):
    global config, ps
    p = Particle(ps)
    p.objWidth = round(random.uniform(ps.objWidthMin, ps.objWidthMax))
    p.objHeight = round(random.uniform(ps.objHeightMin, ps.objHeightMax))

    p.particleWinkOutXMin = pMngr.particleWinkOutXMin
    p.particleWinkOutYMin = pMngr.particleWinkOutYMin

    p.setUpParticle()

    p.xPosR = config.canvasWidth / 2 - ps.centerRangeXMin + round(random.random() * ps.centerRangeXMax) - p.objWidth
    p.yPosR = config.canvasHeight / 2 - ps.centerRangeYMin + round(random.random() * ps.centerRangeYMax) - p.objHeight

    # variance = math.pi/3

    if ps.movement == "fire":
        p.direction = random.uniform(0, 180) * math.pi / 180
        if ps.oneDirection:
            p.direction = 1

    if ps.movement == "travel":
        p.direction = random.uniform(0, 360) * math.pi / 180
        if ps.oneDirection:
            p.direction = 1

    """
	p.direction = random.uniform(
		math.pi + math.pi / 2 - pMngr.variance,
		math.pi + math.pi / 2 + pMngr.variance
	)

	p.direction = random.uniform(-math.pi,math.pi)

	p.direction = random.uniform(0,360) * math.pi/180
	"""

    p.v = random.uniform(ps.speedMin, ps.speedMax)
    p.xWind = pMngr.xWind

    p.pixelsGoGray = pMngr.pixelsGoGray
    p.jumpToGray = pMngr.jumpToGray

    if ps.objColor == "rnd":
        p.fillColor = colorutils.randomColor(ps.config.brightness)
        p.outlineColor = colorutils.getSunsetColors(ps.config.brightness / 2)

    if ps.objColor == "alphaRandom":
        p.fillColor = colorutils.randomColorAlpha(
            ps.config.brightness,
            int(random.uniform(ps.transparencyRange[0], ps.transparencyRange[1])),
        )
        p.outlineColor = colorutils.randomColorAlpha(
            ps.config.brightness,
            int(random.uniform(ps.transparencyRange[0], ps.transparencyRange[1])),
        )

    else:

        p.fillColor = pMngr.fillColor  # (240,150,0,100)
        p.outlineColor = pMngr.outlineColor  # (100,0,0,100)
        p.extraOutlineColor = pMngr.extraOutlineColor

        if pMngr.pUseHSV:
            p.fillColor = colorutils.getRandomColorHSV(
                pMngr.pFillRange[0],
                pMngr.pFillRange[1],
                pMngr.pFillRange[2],
                pMngr.pFillRange[3],
                pMngr.pFillRange[4],
                pMngr.pFillRange[5],
                0,
                0,
                int(pMngr.pFillRange[6]),
                ps.config.brightness,
            )
            p.outlineColor = colorutils.getRandomColorHSV(
                pMngr.pOutlineRange[0],
                pMngr.pOutlineRange[1],
                pMngr.pOutlineRange[2],
                pMngr.pOutlineRange[3],
                pMngr.pOutlineRange[4],
                pMngr.pOutlineRange[5],
                0,
                0,
                int(pMngr.pOutlineRange[6]),
                ps.config.brightness,
            )

        if random.random() < pMngr.useSecondColorProb:
            p.fillColor = pMngr.fillColor2  # (240,150,0,100)
            p.outlineColor = pMngr.outlineColor2  # (100,0,0,100)
            p.extraOutlineColor = pMngr.extraOutlineColor2

        if pMngr.pixelsGoGray:
            _pixelsGoGrayFcu(pMngr, p)
    if ps.movement == "linearMotion":

        _linearMotion(config, p, ps)
    if i is not None:
        ps.unitArray[i] = p
    else:
        ps.unitArray.append(p)


def _linearMotion(config, p, ps):
    p.xPosR = int(random.uniform(0, config.canvasWidth))
    p.yPosR = int(random.uniform(0, config.canvasHeight))
    # config.canvasHeight/3 - p.objHeight/4 #

    directions = [0, math.pi, math.pi / 2, -math.pi / 2]
    origins = [
        (-p.objWidth, p.yPosR),
        (config.canvasWidth + p.objWidth, p.yPosR),
        (p.xPosR, -p.objHeight),
        (p.xPosR, config.canvasHeight + p.objHeight),
    ]
    dirVal = round(random.uniform(0, 1))

    if ps.linearMotionAlsoHorizontal:
        dirVal = round(random.uniform(0, 3))

    p.direction = directions[dirVal]
    p.xPosR = origins[dirVal][0]
    p.yPosR = origins[dirVal][1]


def _pixelsGoGrayFcu(pMngr, p):
    p.greyRate = random.uniform(pMngr.greyRate / 4, pMngr.greyRate)
    # p.greyRate = pMngr.greyRate

    """
			0.2989, 0.5870, 0.1140
			from BT.601 : Studio encoding parameters of digital television for standard 4:3 and wide screen 16:9 aspect ratios

			others are
			0.21 R + 0.72 G + 0.07 B

			or 1/3 each channel

			Turns out, in this context, it does not change things that much - probably has to do with what the
			dominant color that is being transitioned to gray -

			"""

    if pMngr.pixelsGoGrayModel == 2:
        # Luminosity
        rRatio = 0.21
        gRatio = 0.72
        bRatio = 0.07
    elif pMngr.pixelsGoGrayModel == 3:
        # BT.601
        rRatio = 0.2989
        gRatio = 0.5870
        bRatio = 0.1140
    else:
        # Average
        rRatio = 0.33
        gRatio = 0.33
        bRatio = 0.33

    p.outlineGrey = rRatio * p.outlineColor[0] + gRatio * p.outlineColor[1] + bRatio * p.outlineColor[2]
    p.outlineGreyRate = [
        (p.outlineGrey - p.outlineColor[0]) / p.greyRate,
        (p.outlineGrey - p.outlineColor[1]) / p.greyRate,
        (p.outlineGrey - p.outlineColor[2]) / p.greyRate,
    ]

    p.fillGrey = rRatio * p.fillColor[0] + gRatio * p.fillColor[1] + bRatio * p.fillColor[2]

    p.fillGreyRate = [
        (p.fillGrey - p.fillColor[0]) / p.greyRate,
        (p.fillGrey - p.fillColor[1]) / p.greyRate,
        (p.fillGrey - p.fillColor[2]) / p.greyRate,
    ]

    # pieceLogger("Fill", p.fillColor)
    # pieceLogger("Fill Grey, GreayRate",p.fillGrey, p.fillGreyRate )

    p.fillColorRawValues = tuple(float(i) for i in p.fillColor)
    p.outlineColorRawValues = tuple(float(i) for i in p.outlineColor)


# ----------------------------------------------------------------------------------- #


def transformImage(img):
    width, height = img.size
    m = -0.5
    xshift = abs(m) * 420
    new_width = width + int(round(xshift))

    img = img.transform((new_width, height), Image.AFFINE, (1, m, 0, 0, 1, 0), Image.BICUBIC)
    img = img.transform((new_width, height), Image.PERSPECTIVE, pMngr.transformTuples, Image.BICUBIC)
    return img


# ----------------------------------------------------------------------------------- #


def colorize():

    # Colorize via overlay etc
    pMngr.clrBlock = Image.new("RGBA", (pMngr.clrBlkWidth, pMngr.clrBlkHeight))
    clrBlockDraw = ImageDraw.Draw(pMngr.clrBlock)

    # Color overlay on b/w PNG sprite
    # clrBlockDraw.rectangle((0,0, w, h), fill=(255,255,255))
    clrBlockDraw.rectangle((0, 0, config.canvasWidth, pMngr.clrBlkHeight), fill=(0, 0, 0, 255))

    clrBlockDraw.rectangle((0, 0, pMngr.clrBlkWidth, pMngr.clrBlkHeight), fill=pMngr.overlayColor)

    """
		try :
			config.image = ImageChops.multiply(pMngr.clrBlock, config.image)
			# pass
		except Exception as e:
			pieceLogger(e, config.image.mode)
			pass
		"""


# ----------------------------------------------------------------------------------- #


def brightnessChanger():
    global config, ps
    if config.brightnessVariation:
        if not config.brightnessVariationTransition:
            if random.random() < config.brightnessVariationProb:
                config.destinationBrightness = random.uniform(0.1, config.baseBrightness)
                config.destinationBrightness = 0.1
                config.brightnessDelta = (config.destinationBrightness - config.brightness) / 100
                config.brightnessVariationTransition = True
                pieceLogger(f"New brightness: {config.brightness} ,{config.destinationBrightness} ,{config.brightnessDelta}")

        else:
            config.brightness += config.brightnessDelta
            ps.config.brightness = config.brightness
            if (config.brightness > config.destinationBrightness and config.brightnessDelta > 0) or (
                config.brightness < config.destinationBrightness and config.brightnessDelta < 0
            ):
                config.brightnessVariationTransition = False
                pieceLogger(f"config.brightness: {config.brightness}")


# ----------------------------------------------------------------------------------- #


def setUp():
    global config
    colorize()


# ----------------------------------------------------------------------------------- #


def runWork():
    global config
    pieceLogger("RUNNING Particle System pieces/particles.py", 2, True)

    while config.isRunning:
        config.directorController.checkTime()
        if config.directorController.advance:
            iterate()
        time.sleep(config.delay)
        if not config.standAlone:
            config.callBack()


# ----------------------------------------------------------------------------------- #


def iterate():
    global config, ps

    brightnessChanger()

    if pMngr.bgTransitions:
        pMngr.colOverlayA.stepTransition(alpha=pMngr.colOverlayA.bgTransparency)
        pMngr.bgColor = tuple(int(a * config.brightness) for a in pMngr.colOverlayA.currentColor)

    # Fade trails or not...
    config.draw.rectangle(
        (0, 0, config.canvasWidth - 1, config.canvasHeight - 1),
        fill=pMngr.bgColor,
        outline=None,
    )

    if pMngr.useOverOnBG:
        config.image.paste(pMngr.clrBlock, (pMngr.overlayxPos, pMngr.overlayyPos), pMngr.clrBlock)

    """
	# ORIG PLACEMENT
	if pMngr.useOverLay :
		# config.image = ImageChops.multiply(pMngr.clrBlock, config.image)
		config.image.paste(
			pMngr.clrBlock, (pMngr.overlayxPos, pMngr.overlayyPos), pMngr.clrBlock
		)


	"""
    for p in ps.unitArray:
        p.update()
        p.render()

        if p.objHeight > 200:
            p.remove = True

        if p.remove:
            # pieceLogger("REMOVING",ps.unitArray.index(p),len(ps.unitArray))

            if not ps.fixedUnitArray:
                ps.unitArray.remove(p)

                if len(ps.unitArray) < pMngr.numUnits + 0:
                    for _ in range(ps.reEmitNumber):
                        emitParticle()
            else:
                emitParticle(i=ps.unitArray.index(p))

    if random.random() < pMngr.restartProb:
        for p in ps.unitArray:
            p.remove = True
        config.draw.rectangle((0, 0, config.canvasWidth, config.canvasHeight), fill=(0, 0, 0, 200))
        config.renderImageFull.paste(config.image)

    # This was added for the stair steps fire line
    # to move the dithered sparkle around a bit to
    # disturb the eveness of things ..

    # if random.random() < pMngr.optionallegacyToggleProb:
    #     pMngr.legacyUnsharpMask = pMngr.legacyUnsharpMask != True

    if random.random() < pMngr.filterRemappingProb and (config.useFilters and pMngr.filterRemapping):
        remapDitherFilteredParts(config, pMngr)
    if random.random() < ps.changechangeCohesionProb and ps.changeCohesion and ps.movement == "travel":
        if random.random() > 0.5:
            ps.cohesionDistance = random.uniform(10, 150)

            # ps.repelDistance = random.uniform(1, ps.cohesionDistance )
        else:
            ps.repelDistance = random.uniform(0, 10)
            # ps.cohesionDistance = random.uniform(ps.repelDistance * 2 ,200 )
            # ps.repelFactor = random.uniform(0,10)

        # pieceLogger(ps.cohesionDistance, ps.repelDistance)

    if pMngr.overallBlur > 0:
        config.image = config.image.filter(ImageFilter.GaussianBlur(radius=pMngr.overallBlur))
        # This needs to be reset
        if pMngr.legacyUnsharpMask:
            config.image = config.image.filter(ImageFilter.UnsharpMask(radius=80, percent=250, threshold=1))
        config.draw = ImageDraw.Draw(config.image)

    if pMngr.transformShape:
        config.image = transformImage(config.image)

    if pMngr.pixelSortProbChange != 0 and random.random() < pMngr.pixelSortProbChange:
        config.pixSortprobDraw = random.uniform(pMngr.pixelSortProbChangeMin, pMngr.pixelSortProbChangeMax)

    if pMngr.torqueRate != 0:
        xDist = 0
        rows = round(config.canvasHeight / pMngr.torqueDelta)

        for i in range(rows):
            # counter speed - i.e. faster at top
            # xDist = 1 + (rows -i)/pMngr.torqueRate
            xDist = 1 + (i) / pMngr.torqueRate

            box = (
                0,
                i * pMngr.torqueDelta,
                448,
                i * pMngr.torqueDelta + pMngr.torqueDelta,
            )
            crop = config.renderImageFull.crop(box)
            crop = crop.convert("RGBA")
            config.renderImageFull.paste(crop, (round(xDist), i * pMngr.torqueDelta), crop)

    # pieceLogger("particles ",config.render, config.instanceNumber)

    if pMngr.useOverLayEnhanced:
        # config.image = ImageChops.multiply(pMngr.clrBlock, config.image)
        # config.image = ImageChops.invert(config.image)

        # config.image.paste(pMngr.clrBlock, (pMngr.overlayxPos, pMngr.overlayyPos), pMngr.clrBlock)

        # temp = ImageChops.lighter(pMngr.clrBlock, config.image)
        # temp = temp.crop((pMngr.overlayxPos, pMngr.overlayyPos,pMngr.clrBlkWidth,pMngr.clrBlkHeight))

        temp = config.image.crop(
            (
                pMngr.overlayxPos,
                pMngr.overlayyPos,
                pMngr.clrBlkWidth,
                pMngr.clrBlkHeight,
            )
        )
        temp = ImageChops.invert(temp)
        temp = ImageChops.multiply(temp, pMngr.clrBlock)

        config.image.paste(temp, (pMngr.overlayxPos, pMngr.overlayyPos), pMngr.clrBlock)

    elif pMngr.useOverLay:
        config.image.paste(pMngr.clrBlock, (pMngr.overlayxPos, pMngr.overlayyPos), pMngr.clrBlock)

    # RENDERING AS A MOCKUP OR AS REAL
    if config.useDrawingPoints:
        config.panelDrawing.canvasToUse = config.image
        config.panelDrawing.render()
    elif not pMngr.useWaveDistortion:
        config.render(config.image, 0, 0, config.canvasWidth, config.canvasHeight)
    else:
        pMngr.xPos += 1
        pMngr.workImage = ImageOps.deform(config.image, WaveDeformer())
        config.render(pMngr.workImage, 0, 0)


# TODO Rename this here and in `iterate`
def remapDitherFilteredParts(config, pMngr):
    config.filterRemap = True

    # startX = round(random.uniform(0,config.canvasWidth - pMngr.filterRemapminHoriSize) )
    # startY = round(random.uniform(0,config.canvasHeight - pMngr.filterRemapminVertSize) )
    # endX = round(random.uniform(startX+pMngr.filterRemapminHoriSize,config.canvasWidth) )
    # endY = round(random.uniform(startY+pMngr.filterRemapminVertSize,config.canvasHeight) )
    # new version  more control but may require previous pieces to be re-worked
    startX = round(random.uniform(0, pMngr.filterRemapRangeX))
    startY = round(random.uniform(0, pMngr.filterRemapRangeY))
    endX = round(random.uniform(4, pMngr.filterRemapminHoriSize))
    endY = round(random.uniform(4, pMngr.filterRemapminVertSize))
    config.remapImageBlockSection = [
        startX,
        startY,
        startX + endX,
        startY + endY,
    ]
    config.remapImageBlockDestination = [startX, startY]


# ----------------------------------------------------------------------------------- #


def renderDiagnosticsCall():
    config.renderImageFullOverlay = Image.new("RGBA", (config.screenWidth, config.screenHeight))
    config.renderDrawOver = ImageDraw.Draw(config.renderImageFullOverlay)

    pMngr.lastOverlayBox1 = (0, 0, 192, 128)
    pMngr.lastOverlayBox2 = (0, 128, 192, 256)
    pMngr.lastOverlayBox3 = (192, 0, 384, 128)
    pMngr.lastOverlayBox4 = (192, 128, 384, 256)

    config.renderDrawOver.rectangle(pMngr.lastOverlayBox1, fill=(255, 0, 0, 0), outline=(255, 255, 0, 255))
    config.renderDrawOver.rectangle(pMngr.lastOverlayBox2, fill=(255, 0, 0, 0), outline=(255, 255, 0, 255))
    config.renderDrawOver.rectangle(pMngr.lastOverlayBox3, fill=(255, 0, 0, 0), outline=(255, 255, 0, 255))
    config.renderDrawOver.rectangle(pMngr.lastOverlayBox4, fill=(255, 0, 0, 0), outline=(255, 255, 0, 255))
    config.renderImageFull.paste(config.renderImageFullOverlay, (0, 0), config.renderImageFullOverlay)


# ----------------------------------------------------------------------------------- #


def callBack():
    global config
    return True


# ----------------------------------------------------------------------------------- #
