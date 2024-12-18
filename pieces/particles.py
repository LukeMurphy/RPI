import datetime
import math
import random
import textwrap
import time
from modules.configuration import bcolors
from modules import coloroverlay, colorutils, panelDrawing
from modules.particleobjects.particle import Particle
from modules.particleobjects.particlesystem import ParticleSystem
from PIL import (
    Image,
    ImageChops,
    ImageDraw,
    ImageEnhance,
    ImageFilter,
    ImageFont,
    ImageOps,
)
import noise
from noise import *
from modules.holder_director import Holder 
from modules.holder_director import Director 

"""""" """""" """""" """""" """""" """""" """""" """""" """""" """""" ""


class WaveDeformer:
    def transform(self, x, y):
        y = y + config.waveAmplitude * math.sin(
            (x + config.xPos) / config.wavePeriodMod
        ) * noise.pnoise2(math.sin(x), y / config.pNoiseMod)
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

        target_grid = []
        for x in range(0, self.w, config.wavegridspace):
            for y in range(0, self.h, config.wavegridspace):
                target_grid.append(
                    (x, y, x + config.wavegridspace, y + config.wavegridspace)
                )

        source_grid = [self.transform_rectangle(*rect) for rect in target_grid]

        return [t for t in zip(target_grid, source_grid)]


def main(run=True):
    global config, directionOrder, ps
    global workConfig
    print("---------------------")
    print("Particles Loaded")
    colorutils.brightness = config.brightness
    config.canvasImageWidth = config.canvasWidth
    config.canvasImageHeight = config.canvasHeight
    config.canvasImageWidth -= 4
    config.canvasImageHeight -= 4
    config.numUnits = 60

    """
	config.fontColorVals = ((workConfig.get("diag", 'fontColor')).split(','))
	config.fontColor = tuple(map(lambda x: int(int(x)  * config.brightness), config.fontColorVals))
	config.outlineColorVals = ((workConfig.get("diag", 'outlineColor')).split(','))
	config.outlineColor = tuple(map(lambda x: int(int(x) * config.brightness) , config.outlineColorVals))
	"""

    """""" """""" """""" """""" """""" """""" """""" """""" """""" """"""

    config.canvasImage = Image.new(
        "RGBA", (config.canvasImageWidth, config.canvasImageHeight)
    )
    config.fontSize = 14
    config.font = ImageFont.truetype(
        config.path + "/assets/fonts/freefont/FreeSansBold.ttf", config.fontSize
    )

    """""" """""" """""" """""" """""" """""" """""" """""" """""" """"""

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
        ps.changechangeCohesionProb = float(
            workConfig.get("particleSystem", "changechangeCohesionProb")
        )
    except Exception as e:
        print(str(e))
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
    config.bgColorVals = (workConfig.get("particleSystem", "bgColor")).split(",")
    config.bgColor = tuple(
        map(lambda x: int(int(x) * config.brightness), config.bgColorVals)
    )

    ps.centerRangeXMin = int(workConfig.get("particleSystem", "centerRangeXMin"))
    ps.centerRangeYMin = int(workConfig.get("particleSystem", "centerRangeYMin"))
    ps.centerRangeXMax = int(workConfig.get("particleSystem", "centerRangeXMax"))
    ps.centerRangeYMax = int(workConfig.get("particleSystem", "centerRangeYMax"))

    ps.objType = workConfig.get("particleSystem", "objType")

    if ps.objType == "image":
        ps.objImage = workConfig.get("particleSystem", "objImage")
        ps.objImageColorize = workConfig.getboolean(
            "particleSystem", "objImageColorize"
        )
        ps.objImageFlipRate = float(
            workConfig.get("particleSystem", "objImageFlipRate")
        )
        ps.objImageRotateRate = float(
            workConfig.get("particleSystem", "objImageRotateRate")
        )
        ps.objImageAlphaBlend = float(
            workConfig.get("particleSystem", "objImageAlphaBlend")
        )
        arg = config.path + "assets/" + ps.objImage
        ps.loadedImage = Image.open(arg, "r")
        ps.loadedImage.load()
        ps.loadedImageCopy = ps.loadedImage.copy()

    try:
        config.renderDiagnostics = workConfig.getboolean(
            "particleSystem", "renderDiagnostics"
        )
        config.renderDiagnosticsCall = renderDiagnosticsCall
    except Exception as e:
        print(str(e))
        config.renderDiagnostics = False

    # managing speed of animation and framerate
    config.directorController = Director(config)

    try:
        config.delay = float(workConfig.get("particleSystem", "delay"))
    except Exception as e:
        print(str(e))
        config.delay = 0.01
        ps.delay = 0.01
    try:
        config.directorController.slotRate = float(
            workConfig.get("particleSystem", "slotRate")
        )
    except Exception as e:
        print(str(e))
        print("SHOULD ADJUST TO USE slotRate AS FRAMERATE ")
        config.directorController.slotRate = 0.03

    try:
        ps.meanderFactor = float(workConfig.get("particleSystem", "meanderFactor"))
    except Exception as e:
        print(str(e))
        ps.meanderFactor = 1.0

    try:
        ps.meanderFactor2 = float(workConfig.get("particleSystem", "meanderFactor2"))
    except Exception as e:
        print(str(e))
        ps.meanderFactor2 = 90.0

    try:
        ps.meanderDirection = int(workConfig.get("particleSystem", "meanderDirection"))
    except Exception as e:
        print(str(e))
        ps.meanderDirection = 0

    try:
        ps.objTrails = workConfig.getboolean("particleSystem", "objTrails")
    except Exception as e:
        print(str(e))
        ps.objTrails = True

    try:
        config.bgTransitions = workConfig.getboolean("particleSystem", "bgTransitions")
        config.colOverlayA = coloroverlay.ColorOverlay()
        config.bgRangeA = int(workConfig.get("particleSystem", "bgRangeA"))
        config.bgRangeB = int(workConfig.get("particleSystem", "bgRangeB"))
        config.colOverlayA.randomRange = (config.bgRangeA, config.bgRangeB)
        # config.colOverlayA.colorA = tuple(int(a*config.brightness) for a in (colorutils.getRandomColor()))
        config.colOverlayA.minHue = int(workConfig.get("particleSystem", "minHue"))
        config.colOverlayA.maxHue = int(workConfig.get("particleSystem", "maxHue"))

        config.colOverlayA.minValue = float(
            workConfig.get("particleSystem", "minValue")
        )
        config.colOverlayA.maxValue = float(
            workConfig.get("particleSystem", "maxValue")
        )

        config.colOverlayA.maxBrightness = float(
            workConfig.get("particleSystem", "maxBrightness")
        )
        config.colOverlayA.bgTransparency = float(
            workConfig.get("particleSystem", "bgTransparency")
        )
        config.colOverlayA.randomSteps = True
        config.colOverlayA.timeTrigger = True
        config.colOverlayA.tLimitBase = int(
            workConfig.get("particleSystem", "tLimitBase")
        )
        config.colOverlayA.setStartColor()
        config.colOverlayA.getNewColor()
        config.colOverlayA.colorTransitionSetup()

    except Exception as e:
        print(str(e))
        config.bgTransitions = False

    try:
        ps.linearMotionAlsoHorizontal = workConfig.getboolean(
            "particleSystem", "linearMotionAlsoHorizontal"
        )
    except Exception as e:
        print(str(e))
        ps.linearMotionAlsoHorizontal = True

    try:
        ps.oneDirection = workConfig.getboolean("particleSystem", "oneDirection")
    except Exception as e:
        print(str(e))
        ps.oneDirection = False

    try:
        ps.reEmitNumber = int(workConfig.get("particleSystem", "reEmitNumber"))
    except Exception as e:
        print(str(e))
        ps.reEmitNumber = 2

    try:
        ps.fixedUnitArray = workConfig.getboolean("particleSystem", "fixedUnitArray")
    except Exception as e:
        print(str(e))
        ps.fixedUnitArray = False

    try:
        ps.transparencyRange = workConfig.get(
            "particleSystem", "transparencyRange"
        ).split(",")
        ps.transparencyRange = tuple(map(lambda x: int(int(x)), ps.transparencyRange))
    except Exception as e:
        print(str(e))
        ps.transparencyRange = (10, 200)

    try:
        config.transformShape = workConfig.getboolean(
            "particleSystem", "transformShape"
        )
        transformTuples = workConfig.get("particleSystem", "transformTuples").split(",")
        config.transformTuples = tuple([float(i) for i in transformTuples])
    except Exception as e:
        print(str(e))
        config.transformShape = False

    try:
        config.torqueDelta = int(workConfig.get("particleSystem", "torqueDelta"))
        config.torqueRate = float(workConfig.get("particleSystem", "torqueRate"))
    except Exception as e:
        print(str(e))
        config.torqueDelta = 0
        config.torqueRate = 0

    try:
        config.xWind = float(workConfig.get("particleSystem", "xWind"))
    except Exception as e:
        print(str(e))
        config.xWind = 0

    try:
        config.particleWinkOutXMin = float(
            workConfig.get("particleSystem", "particleWinkOutXMin")
        )
        config.particleWinkOutYMin = float(
            workConfig.get("particleSystem", "particleWinkOutYMin")
        )
    except Exception as e:
        print(str(e))
        config.particleWinkOutXMin = 5
        config.particleWinkOutYMin = 5

    try:
        config.pixelSortProbChange = float(
            workConfig.get("displayconfig", "pixelSortProbChange")
        )
        config.pixelSortProbChangeMin = float(
            workConfig.get("displayconfig", "pixelSortProbChangeMin")
        )
        config.pixelSortProbChangeMax = float(
            workConfig.get("displayconfig", "pixelSortProbChangeMax")
        )
    except Exception as e:
        print(str(e))
        config.pixelSortProbChange = 0

    try:
        config.restartProb = float(workConfig.get("particleSystem", "restartProb"))
    except Exception as e:
        print(str(e))
        config.restartProb = 0

    try:
        config.filterRemapping = workConfig.getboolean(
            "particleSystem", "filterRemapping"
        )
        config.filterRemappingProb = float(
            workConfig.get("particleSystem", "filterRemappingProb")
        )
        config.filterRemapminHoriSize = int(
            workConfig.get("particleSystem", "filterRemapminHoriSize")
        )
        config.filterRemapminVertSize = int(
            workConfig.get("particleSystem", "filterRemapminVertSize")
        )
    except Exception as e:
        print(str(e))
        config.filterRemapping = False
        config.filterRemappingProb = 0.0
        config.filterRemapminHoriSize = 24
        config.filterRemapminVertSize = 24

    try:
        config.filterRemapRangeX = int(
            workConfig.get("particleSystem", "filterRemapRangeX")
        )
        config.filterRemapRangeY = int(
            workConfig.get("particleSystem", "filterRemapRangeY")
        )
    except Exception as e:
        print(str(e))
        config.filterRemapRangeX = config.canvasWidth
        config.filterRemapRangeY = config.canvasHeight
    """
	Why this? because desaturation transitions are not always expected, because Phil and Sarah suggested it
	Because colors are more interesting against gray, because everything goes gray

	Rate of desaturation is set as greyRate

	Sorry about schitzoid spelling of grey-gray

	"""

    try:
        config.pixelsGoGray = workConfig.getboolean("particleSystem", "pixelsGoGray")
        config.greyRate = float(workConfig.get("particleSystem", "greyRate"))
    except Exception as e:
        print(str(e))
        config.pixelsGoGray = False

    # ok this may seem screwy, but because I made an error a while ago, the jumpToGray
    # effect is actually default ... so if you want gradual turn to gray, it must be set
    # actively. blurp. ugh.
    try:
        config.jumpToGray = workConfig.getboolean("particleSystem", "jumpToGray")
    except Exception as e:
        print(str(e))
        config.jumpToGray = True

    try:
        config.pixelsGoGrayModel = int(
            workConfig.get("particleSystem", "pixelsGoGrayModel")
        )
    except Exception as e:
        print(str(e))
        config.pixelsGoGrayModel = 3

    ps.movement = workConfig.get("particleSystem", "movement")
    ps.objColor = workConfig.get("particleSystem", "objColor")
    ps.objWidth = int(workConfig.get("particleSystem", "objWidth"))
    ps.objHeight = int(workConfig.get("particleSystem", "objHeight"))
    ps.widthRate = float(workConfig.get("particleSystem", "widthRate"))
    ps.heightRate = float(workConfig.get("particleSystem", "heightRate"))
    config.variance = float(workConfig.get("particleSystem", "variance"))

    try:
        ps.objWidthMax = int(workConfig.get("particleSystem", "objWidthMax"))
        ps.objHeightMax = int(workConfig.get("particleSystem", "objHeightMax"))

        ps.objWidthMin = int(workConfig.get("particleSystem", "objWidthMin"))
        ps.objHeightMin = int(workConfig.get("particleSystem", "objHeightMin"))
    except Exception as e:
        print(str(e))
        ps.objWidthMax = ps.objWidth
        ps.objHeightMax = ps.objHeight
        ps.objWidthMin = ps.objWidth
        ps.objHeightMin = ps.objHeight

    try:
        ps.rndSizeFactorMin = float(
            workConfig.get("particleSystem", "rndSizeFactorMin")
        )
        ps.rndSizeFactorMax = float(
            workConfig.get("particleSystem", "rndSizeFactorMax")
        )
    except Exception as e:
        print(str(e))
        ps.rndSizeFactorMin = 0.5
        ps.rndSizeFactorMax = 1.5

    config.fillColorVals = (workConfig.get("particleSystem", "fillColor")).split(",")
    config.fillColor = tuple(
        map(lambda x: int(int(x) * config.brightness), config.fillColorVals)
    )

    config.outlineColorVals = (workConfig.get("particleSystem", "outlineColor")).split(
        ","
    )
    config.outlineColor = tuple(
        map(lambda x: int(int(x) * config.brightness), config.outlineColorVals)
    )

    try:
        config.extraOutlineColorVals = (
            workConfig.get("particleSystem", "extraOutlineColor")
        ).split(",")
        config.extraOutlineColor = tuple(
            map(
                lambda x: round(int(x) * config.brightness),
                config.extraOutlineColorVals,
            )
        )
    except Exception as e:
        print(str(e))
        config.extraOutlineColor = None

    try:
        config.pUseHSV = workConfig.getboolean("particleSystem", "pUseHSV")
        pFillRange = (workConfig.get("particleSystem", "pFillRange")).split(",")
        config.pFillRange = tuple(
            map(lambda x: (float(x) * config.brightness), pFillRange)
        )
        pOutlineRange = (workConfig.get("particleSystem", "pOutlineRange")).split(",")
        config.pOutlineRange = tuple(
            map(lambda x: (float(x) * config.brightness), pOutlineRange)
        )
    except Exception as e:
        config.pUseHSV = False
        print(str(e))

    # second color for some particles
    try:
        config.useSecondColorProb = float(
            workConfig.get("particleSystem", "useSecondColorProb")
        )
        config.fillColorVals2 = (workConfig.get("particleSystem", "fillColor2")).split(
            ","
        )
        config.fillColor2 = tuple(
            map(lambda x: int(int(x) * config.brightness), config.fillColorVals2)
        )

        config.outlineColorVals2 = (
            workConfig.get("particleSystem", "outlineColor2")
        ).split(",")
        config.outlineColor2 = tuple(
            map(lambda x: int(int(x) * config.brightness), config.outlineColorVals2)
        )

        try:
            config.extraOutlineColorVals2 = (
                workConfig.get("particleSystem", "extraOutlineColor2")
            ).split(",")
            config.extraOutlineColor2 = tuple(
                map(
                    lambda x: round(int(x) * config.brightness),
                    config.extraOutlineColorVals2,
                )
            )
        except Exception as e:
            print(str(e))
            config.extraOutlineColor2 = None
    except Exception as e:
        print(str(e))
        config.useSecondColorProb = 0
        config.extraOutlineColor2 = config.extraOutlineColor
        config.fillColor2 = config.fillColor
        config.outlineColor2 = config.outlineColor
        config.extraOutlineColor2 = config.extraOutlineColor

    ps.unitBlur = int(workConfig.get("particleSystem", "unitBlur"))
    config.overallBlur = int(workConfig.get("particleSystem", "overallBlur"))

    try:
        config.legacyUnsharpMask = workConfig.getboolean(
            "particleSystem", "legacyUnsharpMask"
        )
        config.optionallegacyToggleProb = float(
            workConfig.get("particleSystem", "optionallegacyToggleProb")
        )
    except Exception as e:
        print(str(e))
        config.legacyUnsharpMask = True
        config.optionallegacyToggleProb = 0

    try:
        config.useWaveDistortion = workConfig.getboolean(
            "particleSystem", "useWaveDistortion"
        )
        config.waveAmplitude = float(workConfig.get("particleSystem", "waveAmplitude"))
        config.wavePeriodMod = float(workConfig.get("particleSystem", "wavePeriodMod"))
        config.wavegridspace = int(workConfig.get("particleSystem", "wavegridspace"))
        config.pNoiseMod = float(workConfig.get("particleSystem", "pNoiseMod"))
    except Exception as e:
        print(str(e))
        config.useWaveDistortion = False

    config.useOverLay = workConfig.getboolean("particleSystem", "useOverLay")
    config.overlayColorVals = (workConfig.get("particleSystem", "overlayColor")).split(
        ","
    )
    config.overlayColor = tuple(
        map(lambda x: int(int(x) * config.brightness), config.overlayColorVals)
    )
    config.clrBlkWidth = int(workConfig.get("particleSystem", "clrBlkWidth"))
    config.clrBlkHeight = int(workConfig.get("particleSystem", "clrBlkHeight"))
    config.overlayxPos = int(workConfig.get("particleSystem", "overlayxPos"))
    config.overlayyPos = int(workConfig.get("particleSystem", "overlayyPos"))

    try:
        config.useOverLayEnhanced = workConfig.getboolean(
            "particleSystem", "useOverLayEnhanced"
        )
        config.useOverOnBG = workConfig.getboolean("particleSystem", "useOverOnBG")
    except Exception as e:
        print(str(e))
        config.useOverLayEnhanced = False
        config.useOverOnBG = False

    # THIS IS USED AS WAY TO MOCKUP A CONFIGURATION OF RECTANGULAR PANELS
    panelDrawing.mockupBlock(config, workConfig)
    # Need to add something like this at final render call  as well
    """
		########### RENDERING AS A MOCKUP OR AS REAL ###########
		if config.useDrawingPoints == True :
			config.panelDrawing.canvasToUse = config.renderImageFull
			config.panelDrawing.render()
		else :
			# config.render(config.canvasImage, 0, 0, config.canvasWidth, config.canvasHeight)
			# config.render(config.image, 0, 0)
			config.render(config.renderImageFull, 0, 0)
	"""

    config.xPos = 0

    for i in range(0, ps.numUnits):
        emitParticle()

    setUp()

    if run:
        runWork()


"""""" """""" """""" """""" """""" """""" """""" """""" """""" """""" ""


def emitParticle(i=None):
    global config, ps
    p = Particle(ps)
    p.objWidth = round(random.uniform(ps.objWidthMin, ps.objWidthMax))
    p.objHeight = round(random.uniform(ps.objHeightMin, ps.objHeightMax))

    p.particleWinkOutXMin = config.particleWinkOutXMin
    p.particleWinkOutYMin = config.particleWinkOutYMin

    p.setUpParticle()

    p.xPosR = (
        config.canvasWidth / 2
        - ps.centerRangeXMin
        + round(random.random() * ps.centerRangeXMax)
        - p.objWidth
    )
    p.yPosR = (
        config.canvasHeight / 2
        - ps.centerRangeYMin
        + round(random.random() * ps.centerRangeYMax)
        - p.objHeight
    )

    # variance = math.pi/3

    if ps.movement == "fire":
        p.direction = random.uniform(0, 180) * math.pi / 180
        if ps.oneDirection == True:
            p.direction = 1

    if ps.movement == "travel":
        p.direction = random.uniform(0, 360) * math.pi / 180
        if ps.oneDirection == True:
            p.direction = 1

    """
	p.direction = random.uniform(
		math.pi + math.pi / 2 - config.variance,
		math.pi + math.pi / 2 + config.variance
	)

	p.direction = random.uniform(-math.pi,math.pi)

	p.direction = random.uniform(0,360) * math.pi/180
	"""

    p.v = random.uniform(ps.speedMin, ps.speedMax)
    p.xWind = config.xWind

    p.pixelsGoGray = config.pixelsGoGray
    p.jumpToGray = config.jumpToGray

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

        p.fillColor = config.fillColor  # (240,150,0,100)
        p.outlineColor = config.outlineColor  # (100,0,0,100)
        p.extraOutlineColor = config.extraOutlineColor

        if config.pUseHSV == True:
            p.fillColor = colorutils.getRandomColorHSV(
                config.pFillRange[0], config.pFillRange[1], 
                config.pFillRange[2], config.pFillRange[3], 
                config.pFillRange[4], config.pFillRange[5], 
                0, 0, 
                int(config.pFillRange[6]), ps.config.brightness)
            p.outlineColor = colorutils.getRandomColorHSV(
                config.pOutlineRange[0], config.pOutlineRange[1], 
                config.pOutlineRange[2], config.pOutlineRange[3], 
                config.pOutlineRange[4], config.pOutlineRange[5], 
                0, 0, 
                int(config.pOutlineRange[6]), ps.config.brightness)

        if random.random() < config.useSecondColorProb:
            p.fillColor = config.fillColor2  # (240,150,0,100)
            p.outlineColor = config.outlineColor2  # (100,0,0,100)
            p.extraOutlineColor = config.extraOutlineColor2

        if config.pixelsGoGray == True:
            p.greyRate = random.uniform(config.greyRate / 4, config.greyRate)
            # p.greyRate = config.greyRate

            """
			0.2989, 0.5870, 0.1140
			from BT.601 : Studio encoding parameters of digital television for standard 4:3 and wide screen 16:9 aspect ratios

			others are
			0.21 R + 0.72 G + 0.07 B

			or 1/3 each channel

			Turns out, in this context, it does not change things that much - probably has to do with what the
			dominant color that is being transitioned to gray -

			"""

            if config.pixelsGoGrayModel == 3:
                # BT.601
                rRatio = 0.2989
                gRatio = 0.5870
                bRatio = 0.1140
            elif config.pixelsGoGrayModel == 2:
                # Luminosity
                rRatio = 0.21
                gRatio = 0.72
                bRatio = 0.07
            else:
                # Average
                rRatio = 0.33
                gRatio = 0.33
                bRatio = 0.33

            p.outlineGrey = (
                rRatio * p.outlineColor[0]
                + gRatio * p.outlineColor[1]
                + bRatio * p.outlineColor[2]
            )
            p.outlineGreyRate = [
                (p.outlineGrey - p.outlineColor[0]) / p.greyRate,
                (p.outlineGrey - p.outlineColor[1]) / p.greyRate,
                (p.outlineGrey - p.outlineColor[2]) / p.greyRate,
            ]

            p.fillGrey = (
                rRatio * p.fillColor[0]
                + gRatio * p.fillColor[1]
                + bRatio * p.fillColor[2]
            )

            p.fillGreyRate = [
                (p.fillGrey - p.fillColor[0]) / p.greyRate,
                (p.fillGrey - p.fillColor[1]) / p.greyRate,
                (p.fillGrey - p.fillColor[2]) / p.greyRate,
            ]

            # print("Fill", p.fillColor)
            # print("Fill Grey, GreayRate",p.fillGrey, p.fillGreyRate )

            p.fillColorRawValues = tuple(float(i) for i in p.fillColor)
            p.outlineColorRawValues = tuple(float(i) for i in p.outlineColor)

    if ps.movement == "linearMotion":

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

        if ps.linearMotionAlsoHorizontal == True:
            dirVal = round(random.uniform(0, 3))

        p.direction = directions[dirVal]
        p.xPosR = origins[dirVal][0]
        p.yPosR = origins[dirVal][1]

    if i != None:
        ps.unitArray[i] = p
    else:
        ps.unitArray.append(p)


"""""" """""" """""" """""" """""" """""" """""" """""" """""" """""" ""


def transformImage(img):
    width, height = img.size
    m = -0.5
    xshift = abs(m) * 420
    new_width = width + int(round(xshift))

    img = img.transform(
        (new_width, height), Image.AFFINE, (1, m, 0, 0, 1, 0), Image.BICUBIC
    )
    img = img.transform(
        (new_width, height), Image.PERSPECTIVE, config.transformTuples, Image.BICUBIC
    )
    return img


"""""" """""" """""" """""" """""" """""" """""" """""" """""" """""" ""


def colorize():

    # Colorize via overlay etc
    config.clrBlock = Image.new("RGBA", (config.clrBlkWidth, config.clrBlkHeight))
    clrBlockDraw = ImageDraw.Draw(config.clrBlock)

    # Color overlay on b/w PNG sprite
    # clrBlockDraw.rectangle((0,0, w, h), fill=(255,255,255))
    clrBlockDraw.rectangle(
        (0, 0, config.canvasWidth, config.clrBlkHeight), fill=(0, 0, 0, 255)
    )

    clrBlockDraw.rectangle(
        (0, 0, config.clrBlkWidth, config.clrBlkHeight), fill=config.overlayColor
    )

    """
		try :
			config.image = ImageChops.multiply(config.clrBlock, config.image)
			# pass
		except Exception as e:
			print(e, config.image.mode)
			pass
		"""


"""""" """""" """""" """""" """""" """""" """""" """""" """""" """""" ""


def brightnessChanger():
    global config, ps
    if config.brightnessVariation == True:
        if config.brightnessVariationTransition == False:
            if random.random() < config.brightnessVariationProb:
                config.destinationBrightness = random.uniform(
                    0.1, config.baseBrightness
                )
                config.destinationBrightness = 0.1
                config.brightnessDelta = (
                    config.destinationBrightness - config.brightness
                ) / 100
                config.brightnessVariationTransition = True
                print(
                    "New brightness:",
                    config.brightness,
                    config.destinationBrightness,
                    config.brightnessDelta,
                )

        else:
            config.brightness += config.brightnessDelta
            ps.config.brightness = config.brightness
            if (
                config.brightness > config.destinationBrightness
                and config.brightnessDelta > 0
            ) or (
                config.brightness < config.destinationBrightness
                and config.brightnessDelta < 0
            ):
                config.brightnessVariationTransition = False
                print(config.brightness)


"""""" """""" """""" """""" """""" """""" """""" """""" """""" """""" ""


def setUp():
    global config
    colorize()
    pass


"""""" """""" """""" """""" """""" """""" """""" """""" """""" """""" ""


def runWork():
    global config
    print(bcolors.OKGREEN + "** " + bcolors.BOLD)
    print("RUNNING Particle System pieces/singletons/particles.py")
    print(bcolors.ENDC)

    while config.isRunning == True:
        config.directorController.checkTime()
        if config.directorController.advance == True:
            iterate()
        time.sleep(config.delay)
        if config.standAlone == False:
            config.callBack()


"""""" """""" """""" """""" """""" """""" """""" """""" """""" """""" ""


def iterate():
    global config, ps

    brightnessChanger()

    if config.bgTransitions == True:
        config.colOverlayA.stepTransition(alpha=config.colOverlayA.bgTransparency)
        config.bgColor = tuple(
            int(a * config.brightness) for a in config.colOverlayA.currentColor
        )

    # Fade trails or not...
    config.draw.rectangle(
        (0, 0, config.canvasWidth - 1, config.canvasHeight - 1),
        fill=config.bgColor,
        outline=None,
    )

    if config.useOverOnBG == True:
        config.image.paste(
            config.clrBlock, (config.overlayxPos, config.overlayyPos), config.clrBlock
        )

    """
	# ORIG PLACEMENT
	if config.useOverLay == True:
		# config.image = ImageChops.multiply(config.clrBlock, config.image)
		config.image.paste(
			config.clrBlock, (config.overlayxPos, config.overlayyPos), config.clrBlock
		)


	"""
    for p in ps.unitArray:
        p.update()
        p.render()

        if p.objHeight > 200:
            p.remove = True

        if p.remove == True:
            # print("REMOVING",ps.unitArray.index(p),len(ps.unitArray))

            if ps.fixedUnitArray == False:
                ps.unitArray.remove(p)

                if len(ps.unitArray) < config.numUnits + 0:
                    for i in range(0, ps.reEmitNumber):
                        emitParticle()
            else:
                emitParticle(i=ps.unitArray.index(p))

    if random.random() < config.restartProb:
        for p in ps.unitArray:
            p.remove = True
        config.draw.rectangle(
            (0, 0, config.canvasWidth, config.canvasHeight), fill=(0, 0, 0, 200)
        )
        config.renderImageFull.paste(config.image)

    # This was added for the stair steps fire line
    # to move the dithered sparkle around a bit to
    # disturb the eveness of things ..

    if random.random() < config.optionallegacyToggleProb:
        if config.legacyUnsharpMask == True:
            config.legacyUnsharpMask = False
        else:
            config.legacyUnsharpMask = True

    if random.random() < config.filterRemappingProb:
        if config.useFilters == True and config.filterRemapping == True:
            config.filterRemap = True

            # startX = round(random.uniform(0,config.canvasWidth - config.filterRemapminHoriSize) )
            # startY = round(random.uniform(0,config.canvasHeight - config.filterRemapminVertSize) )
            # endX = round(random.uniform(startX+config.filterRemapminHoriSize,config.canvasWidth) )
            # endY = round(random.uniform(startY+config.filterRemapminVertSize,config.canvasHeight) )
            # new version  more control but may require previous pieces to be re-worked
            startX = round(random.uniform(0, config.filterRemapRangeX))
            startY = round(random.uniform(0, config.filterRemapRangeY))
            endX = round(random.uniform(4, config.filterRemapminHoriSize))
            endY = round(random.uniform(4, config.filterRemapminVertSize))
            config.remapImageBlockSection = [
                startX,
                startY,
                startX + endX,
                startY + endY,
            ]
            config.remapImageBlockDestination = [startX, startY]

    if (
        random.random() < ps.changechangeCohesionProb
        and ps.changeCohesion == True
        and ps.movement == "travel"
    ):
        if random.random() > 0.5:
            ps.cohesionDistance = random.uniform(10, 150)

            # ps.repelDistance = random.uniform(1, ps.cohesionDistance )
        else:
            ps.repelDistance = random.uniform(0, 10)
            # ps.cohesionDistance = random.uniform(ps.repelDistance * 2 ,200 )
            # ps.repelFactor = random.uniform(0,10)

        # print(ps.cohesionDistance, ps.repelDistance)

    if config.overallBlur > 0:
        config.image = config.image.filter(
            ImageFilter.GaussianBlur(radius=config.overallBlur)
        )
        # This needs to be reset
        if config.legacyUnsharpMask == True:
            config.image = config.image.filter(
                ImageFilter.UnsharpMask(radius=80, percent=250, threshold=1)
            )
        config.draw = ImageDraw.Draw(config.image)

    if config.transformShape == True:
        config.image = transformImage(config.image)

    if config.pixelSortProbChange != 0:
        if random.random() < config.pixelSortProbChange:
            config.pixSortprobDraw = random.uniform(
                config.pixelSortProbChangeMin, config.pixelSortProbChangeMax
            )

    if config.torqueRate != 0:
        xDist = 0
        rows = round(config.canvasHeight / config.torqueDelta)

        for i in range(0, rows):
            # counter speed - i.e. faster at top
            # xDist = 1 + (rows -i)/config.torqueRate
            xDist = 1 + (i) / config.torqueRate

            box = (
                0,
                i * config.torqueDelta,
                448,
                i * config.torqueDelta + config.torqueDelta,
            )
            crop = config.renderImageFull.crop(box)
            crop = crop.convert("RGBA")
            config.renderImageFull.paste(
                crop, (round(xDist), i * config.torqueDelta), crop
            )

    # print("particles ",config.render, config.instanceNumber)

    if config.useOverLayEnhanced == True:
        # config.image = ImageChops.multiply(config.clrBlock, config.image)
        # config.image = ImageChops.invert(config.image)

        # config.image.paste(config.clrBlock, (config.overlayxPos, config.overlayyPos), config.clrBlock)

        # temp = ImageChops.lighter(config.clrBlock, config.image)
        # temp = temp.crop((config.overlayxPos, config.overlayyPos,config.clrBlkWidth,config.clrBlkHeight))

        temp = config.image.crop(
            (
                config.overlayxPos,
                config.overlayyPos,
                config.clrBlkWidth,
                config.clrBlkHeight,
            )
        )
        temp = ImageChops.invert(temp)
        temp = ImageChops.multiply(temp, config.clrBlock)

        config.image.paste(
            temp, (config.overlayxPos, config.overlayyPos), config.clrBlock
        )

    elif config.useOverLay == True:
        config.image.paste(
            config.clrBlock, (config.overlayxPos, config.overlayyPos), config.clrBlock
        )

    # RENDERING AS A MOCKUP OR AS REAL
    if config.useDrawingPoints == True:
        config.panelDrawing.canvasToUse = config.image
        config.panelDrawing.render()
    else:

        if config.useWaveDistortion == False:
            config.render(config.image, 0, 0, config.canvasWidth, config.canvasHeight)
        else:
            config.xPos += 1
            config.workImage = ImageOps.deform(config.image, WaveDeformer())
            config.render(config.workImage, 0, 0)


"""""" """""" """""" """""" """""" """""" """""" """""" """""" """""" ""


def renderDiagnosticsCall():
    config.renderImageFullOverlay = Image.new(
        "RGBA", (config.screenWidth, config.screenHeight)
    )
    config.renderDrawOver = ImageDraw.Draw(config.renderImageFullOverlay)

    config.lastOverlayBox1 = (0, 0, 192, 128)
    config.lastOverlayBox2 = (0, 128, 192, 256)
    config.lastOverlayBox3 = (192, 0, 384, 128)
    config.lastOverlayBox4 = (192, 128, 384, 256)

    config.renderDrawOver.rectangle(
        config.lastOverlayBox1, fill=(255, 0, 0, 0), outline=(255, 255, 0, 255)
    )
    config.renderDrawOver.rectangle(
        config.lastOverlayBox2, fill=(255, 0, 0, 0), outline=(255, 255, 0, 255)
    )
    config.renderDrawOver.rectangle(
        config.lastOverlayBox3, fill=(255, 0, 0, 0), outline=(255, 255, 0, 255)
    )
    config.renderDrawOver.rectangle(
        config.lastOverlayBox4, fill=(255, 0, 0, 0), outline=(255, 255, 0, 255)
    )
    config.renderImageFull.paste(
        config.renderImageFullOverlay, (0, 0), config.renderImageFullOverlay
    )


"""""" """""" """""" """""" """""" """""" """""" """""" """""" """""" ""


def callBack():
    global config
    return True


"""""" """""" """""" """""" """""" """""" """""" """""" """""" """""" ""
