# ################################################### #
import argparse
import math
import random
import time
import types
from modules.configuration import bcolors
from modules.movieClip import movieClip
from modules import badpixels, coloroverlay, colorutils, panelDrawing, pattern_blocks
from PIL import Image, ImageDraw, ImageEnhance, ImageFont, ImageOps, ImageFilter
import numpy as np

# This version substitutes the overlay disturbance with a slide-repeating of a section

###############################################


class Fader:
    def __init__(self):
        self.doingRefresh = 0
        self.doingRefreshCount = 20
        self.fadingDone = False
        self.testing = True

    def setUp(self):
        self.blankImage = Image.new("RGBA", (self.width, self.height))
        self.image = Image.new("RGBA", (self.width, self.height))
        self.crossFade = Image.new("RGBA", (self.width, self.height))

    def test(self):
        print("test")
        # self.blankImage = Image.new("RGBA", (self.width, self.height))
        draw = ImageDraw.Draw(self.crossFade)
        draw.rectangle((0, 0, 100, 100), fill=(0, 0, 255, 255))
        config.image.paste(
            self.crossFade, (self.xPos, self.yPos), self.crossFade
        )

    def fadeIn(self, config):
        config.fadeThruBlack = False
        if self.fadingDone == False:

            if self.testing == True:
                self.testing = False
                # print(self.fadingDone, self.doingRefresh)

            if self.doingRefresh < self.doingRefreshCount:

                if config.fadeThruBlack == True:
                    self.blankImage = Image.new(
                        "RGBA", (self.width, self.height))
                percent = self.doingRefresh / self.doingRefreshCount
                self.crossFade = Image.blend(
                    self.blankImage,
                    self.image,
                    percent,
                )
                config.image.paste(
                    self.crossFade, (self.xPos, self.yPos), self.crossFade
                )
                self.doingRefresh += 1
            else:
                config.image.paste(
                    self.image, (self.xPos, self.yPos), self.image)
                self.fadingDone = True
                self.doingRefresh = 0
                self.blankImage = self.image.copy()
                self.testing = True


def redraw(config):

    if config.patternModel == "wavePattern":
        pattern_blocks.wavePattern(config)

    if config.patternModel == "reMove":
        pattern_blocks.reMove(config)

    if config.patternModel == "diagonalMove":
        pattern_blocks.diagonalMove(config)

    if config.patternModel == "randomizer":
        pattern_blocks.randomizer(config)

    if config.patternModel == "runningSpiral":
        pattern_blocks.runningSpiral(config)

    if config.patternModel == "concentricBoxes":
        pattern_blocks.concentricBoxes(config)

    if config.patternModel == "diamond":
        pattern_blocks.diamond(config)

    if config.patternModel == "shingles":
        pattern_blocks.shingles(config)

    if config.patternModel == "balls":
        pattern_blocks.balls(config)

    if config.patternModel == "bars":
        pattern_blocks.bars(config)
        
    if config.patternModel == "circles":
        pattern_blocks.circles(config)
        
    if config.patternModel == "circlesPacked":
        pattern_blocks.circlesPacked(config)
        
    if config.patternModel == "decoBoxes":
        pattern_blocks.decoBoxes(config)


def repeatImage(config, canvasImage):
    cntr = 0
    # 2021-06-28 Opted to build the repetition/tiling vertically instead of horizontally
    # to suit the graph piece better and upwards or downwards is better than sideways sometimes
    # so reversed the order of "for c in ..." with "for r in range(..." so builds rows vertically

    # 2022-07-12 Changed my mind because the graph piece is not going to get this code - going for a
    # tower configuration

    # config.transitionImage = Image.new("RGBA", (config.canvasWidth, config.canvasHeight))

    extraOverlapx = 0
    extraOverlapy = 0

    for c in range(0, config.cols):
        for r in range(0, config.rows):
            if cntr in config.skipBlocks:
                config.canvasDraw.rectangle((c * config.blockWidth, r * config.blockHeight, c * config.blockWidth + config.blockWidth,
                                             r * config.blockHeight + config.blockHeight), fill=config.bgColor, outline=config.bgColor)
            else:
                temp = config.blockImage.copy()
                # disabling for a moment 2023-04-01
                temp = temp.rotate(90)
                if config.patternModel == "circlesPacked" :
                    extraOverlapx = round(config.blockWidth / 8 )
                    
                if config.patternModel == "waveScales" :
                    temp = temp.rotate(-180)
                    
                if c % 2 != 0 and config.rotateAltBlock == 1:
                    temp = temp.rotate(-90)

                canvasImage.paste(
                    temp, (c * config.blockWidth - c*extraOverlapx, r * config.blockHeight - r*extraOverlapy), temp)
                # config.transitionImage.paste(temp, (c * config.blockWidth-c, r * config.blockHeight-r), temp)

            if config.patternModelVariations == True:
                for s in config.patternSequence:
                    if cntr == s[1]:
                        config.patternModel = s[0]
                        config.rotateAltBlock = s[2]
                        func = eval("pattern_blocks." + s[0])
                        func(config)

            cntr += 1

    config.patternImage = canvasImage.copy()
    # config.patternImage = transformImage(config.patternImage)


def rebuildPatternSequence(config):

    config.patternSequence = []
    numberOfPatterns = round(random.uniform(2, 5))
    config.numConcentricBoxes = round(random.uniform(8, 18))
    lastPosition = 0
    totalSlots = config.rows * config.cols

    if random.random() < .75:
        config.altLineColoring = True
    else:
        config.altLineColoring = False

    # for i in range(0,numberOfPatterns) :
    i = 0
    iterateCount = 0
    usedPatterns = []
    
    # print(numberOfPatterns)
    # Had to add an iterate couter because sometimes things
    # just ran away and it all froze ....
    
    while i < numberOfPatterns:
        
        # print(str("iterateCount count: {}").format(iterateCount))
        pattern = config.patterns[math.floor(
            random.uniform(0, len(config.patterns)))]

        if pattern not in usedPatterns or iterateCount >= 256:
            if pattern not in (["shingles", "fishScales", "balls"]):
                rotate = round(random.uniform(0, 1))
            else:
                rotate = 0
            slotsLeft = totalSlots - lastPosition
            position = round(random.uniform(lastPosition, slotsLeft-1))
            config.patternSequence.append([pattern, position, rotate])
            usedPatterns.append(pattern)
            lastPosition = position
            i += 1
        iterateCount += 1


def loadImageForBase():
    # image = Image.open("./assets/imgs/drawings/P1060494.jpg", "r")
    # image = Image.open("./assets/imgs/miscl/comp-384.jpg", "r")
    # image = Image.open("./assets/imgs/miscl/lm_a.png", "r")

    i = math.floor(random.random() * len(config.imageSources))
    imagePath = config.imageSources[i]
    print(imagePath)
    image = Image.open(imagePath)
    image.load()
    config.canvasImage.paste(image, (0, 0))


def getConfigOverlay(tLimitBase, minHue, maxHue, minSaturation, maxSaturation, minValue, maxValue):
    colOverlay = coloroverlay.ColorOverlay()
    colOverlay.randomSteps = False
    colOverlay.timeTrigger = True
    colOverlay.tLimitBase = tLimitBase
    colOverlay.maxBrightness = 1
    colOverlay.steps = 50
    colOverlay.minHue = minHue
    colOverlay.maxHue = maxHue
    colOverlay.minSaturation = minSaturation
    colOverlay.maxSaturation = maxSaturation
    colOverlay.minValue = minValue
    colOverlay.maxValue = maxValue
    colOverlay.colorTransitionSetup()
    return colOverlay


def buildPalette(config, index=0):
    global workConfig
    palette = config.palettes[index]

    print(str("New palette {}").format(palette))

    tLimitBase = int(workConfig.get(palette, "tLimitBase"))
    minHue = float(workConfig.get(palette, "minHue"))
    maxHue = float(workConfig.get(palette, "maxHue"))
    minSaturation = float(workConfig.get(palette, "minSaturation"))
    maxSaturation = float(workConfig.get(palette, "maxSaturation"))
    minValue = float(workConfig.get(palette, "minValue"))
    maxValue = float(workConfig.get(palette, "maxValue"))
    # config.colOverlay = getConfigOverlay(tLimitBase, minHue, maxHue, minSaturation, maxSaturation, minValue, maxValue)
    config.colOverlay = Holder()
    config.colOverlay.currentColor = [10, 10, 10, 100]
    config.colOverlay.currentColor = colorutils.getRandomColorHSV(minHue, maxHue, minSaturation, maxSaturation, minValue, maxValue, 0, 0,
                                                                  round(random.uniform(config.bgColorAlpha[0], config.bgColorAlpha[1])))
    config.colOverlay.bgColor = colorutils.getRandomColorHSV(
        minHue, maxHue, minSaturation, maxSaturation, minValue, maxValue)

    tLimitBase = int(workConfig.get(palette, "line_tLimitBase"))
    minHue = float(workConfig.get(palette, "line_minHue"))
    maxHue = float(workConfig.get(palette, "line_maxHue"))
    minSaturation = float(workConfig.get(palette, "line_minSaturation"))
    maxSaturation = float(workConfig.get(palette, "line_maxSaturation"))
    minValue = float(workConfig.get(palette, "line_minValue"))
    maxValue = float(workConfig.get(palette, "line_maxValue"))
    # config.linecolOverlay = getConfigOverlay(tLimitBase, minHue, maxHue, minSaturation, maxSaturation, minValue, maxValue)
    config.linecolOverlay = Holder()
    config.linecolOverlay.currentColor = [200, 10, 10]
    config.linecolOverlay.currentColor = colorutils.getRandomColorHSV(
        minHue, maxHue, minSaturation, maxSaturation, minValue, maxValue)

    tLimitBase = int(workConfig.get(palette, "line2_tLimitBase"))
    minHue = float(workConfig.get(palette, "line2_minHue"))
    maxHue = float(workConfig.get(palette, "line2_maxHue"))
    minSaturation = float(workConfig.get(palette, "line2_minSaturation"))
    maxSaturation = float(workConfig.get(palette, "line2_maxSaturation"))
    minValue = float(workConfig.get(palette, "line2_minValue"))
    maxValue = float(workConfig.get(palette, "line2_maxValue"))
    # config.linecolOverlay2 = getConfigOverlay(tLimitBase, minHue, maxHue, minSaturation, maxSaturation, minValue, maxValue)
    config.linecolOverlay2 = Holder()
    config.linecolOverlay2.currentColor = [10, 100, 10]
    config.linecolOverlay2.currentColor = colorutils.getRandomColorHSV(
        minHue, maxHue, minSaturation, maxSaturation, minValue, maxValue)

    # config.colOverlay.currentColor = colorutils.getRandomColorHSV(minHue, maxHue, minSaturation, maxSaturation, minValue, maxValue,0,0,200)
    # config.canvasDraw.rectangle((0,0,config.canvasWidth, config.canvasHeight), fill = config.colOverlay.currentColor)
    # config.colOverlay.currentColor = colorutils.getRandomColorHSV(minHue, maxHue, minSaturation, maxSaturation, minValue, maxValue,0,0,10)


def writeImage(baseName, renderImage):
    # baseName = "outputquad3/comp2_"
    if config.saveImages == True:
        fn = baseName+".png"
        renderImage.save(fn)


def rebuildPatterns(arg=0):

    c = round(random.uniform(1, 4))

    if c == 1:
        if config.numRowsRandomize == True:
            # refresh pattern parameters
            config.numRows = round(random.uniform(1, 2))
            config.numShingleRows = round(random.uniform(1, 2))
            config.numScaleRows = round(random.uniform(1, 2))
            dotRows = [1, 2, 4]
            config.numDotRows = dotRows[round(random.uniform(0, 2))]
            config.waveScaleRings = round(random.uniform(config.ringsRange[0], config.ringsRange[1]))
            config.waveScaleSteps = round(random.uniform(config.stepsRange[0], config.stepsRange[1]))
            
            print( config.waveScaleRings, config.waveScaleSteps)

    if c == 2:
        newPalette = math.floor(random.uniform(0, len(config.palettes)))
        if newPalette == len(config.palettes):
            newPalette = 0
        buildPalette(config, newPalette)

    if c >= 3:
        rebuildPatternSequence(config)

    config.repeatDrawingMode = 1
    config.fader.doingRefreshCount = 20
    rebuildSections()

###############################################


def rebuildSections():
    global config

    if random.random() < config.changeDisturbanceSetProb:
        setNumber = math.floor(random.uniform(
            0, len(config.disturbanceConfigSets)))
        setUpDisturbanceConfigs(config.disturbanceConfigSets[setNumber])
        # print("REBUILDSECTIONS RUNNING NOW: " + config.disturbanceConfigSets[setNumber])

    if random.random() < .5:
        config.speedDeAcceleration = config.speedDeAccelerationUpperLimit
    else:
        speedDeAcceleration = config.speedDeAccelerationBase

    if config.diagonalMovement == False :
        sectionDisturbanceDirection = 1 if random.random() < .5 else 0
        
    baseSpeed = config.baseSectionSpeed
    
    for i in range(0, config.numberOfSections):
        section = config.movingSections[i]
        section.sectionRotation = random.uniform(
            -config.sectionRotationRange, config.sectionRotationRange)
        section.sectionPlacement = [round(random.uniform(config.sectionPlacementXRange[0], config.sectionPlacementXRange[1])), round(
            random.uniform(config.sectionPlacementYRange[0], config.sectionPlacementYRange[1]))]
        section.sectionPlacementInit = [
            section.sectionPlacement[0], section.sectionPlacement[1]]
        section.sectionSize = [round(random.uniform(config.sectionWidthRange[0], config.sectionWidthRange[1])), round(
            random.uniform(config.sectionHeightRange[0], config.sectionHeightRange[1]))]
        section.sectionSpeed = [random.uniform(-baseSpeed, baseSpeed)/config.sectionSpeedFactorHorizontal,
                                random.uniform(-baseSpeed, baseSpeed)/config.sectionSpeedFactorVertical]
        
        if config.diagonalMovement == False :
            if sectionDisturbanceDirection == 1 :
                section.sectionSpeed = [random.uniform(-baseSpeed, baseSpeed)/config.sectionSpeedFactorHorizontal,0]
            else :
                section.sectionSpeed = [0,random.uniform(-baseSpeed, baseSpeed)/config.sectionSpeedFactorVertical]
                
        if config.randomDiagonal == False :
            speed = random.uniform(-baseSpeed, baseSpeed)/config.sectionSpeedFactorHorizontal
            
            hComponent = math.cos(config.diagonalFixedAngle) * speed
            vComponent = math.sin(config.diagonalFixedAngle) * speed
            section.sectionSpeed = [hComponent,vComponent]

            
        section.rotationSpeed = random.uniform(-baseSpeed, baseSpeed)
        section.actionCount = 0
        section.actionCountLimit = round(
            random.uniform(10, config.sectionMovementCountMax))
        section.done = False
        section.stopProb = random.uniform(0, config.stopProb)
    config.drawingPrinted = False


#############################################


class Holder:
    def __init__(self):
        pass


class Director:
    """docstring for Director"""

    slotRate = .5

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


def disturber():
    config.doneCount = 0

    if config.doSectionDisturbance == True:
        if config.skipFramesCount >= config.skipFrames:
            config.skipFramesCount = 0

            for i in range(0, config.numberOfSections):
                sectionParams = config.movingSections[i]
                if sectionParams.actionCount >= sectionParams.actionCountLimit:
                    # sectionParams.rotationSpeed = 0
                    # sectionParams.sectionSpeed[0] = 0
                    # sectionParams.sectionSpeed[1] = 0
                    config.doneCount += 1

                if sectionParams.actionCount < sectionParams.actionCountLimit:

                    xPos = round(sectionParams.sectionPlacementInit[0])
                    yPos = round(sectionParams.sectionPlacementInit[1])
                    section = config.canvasImage.crop(
                        (xPos, yPos, xPos + sectionParams.sectionSize[0], yPos + sectionParams.sectionSize[1]))
                    '''
					section = section.rotate(sectionParams.sectionRotation, Image.NEAREST, True)
					sectionParams.sectionRotation += sectionParams.rotationSpeed
					'''

                    config.canvasImage.paste(section, (round(sectionParams.sectionPlacement[0]), round(
                        sectionParams.sectionPlacement[1])), section)

                    delta = (sectionParams.actionCountLimit -
                             sectionParams.actionCount)/sectionParams.actionCountLimit
                    # rads = (math.pi / 2) / sectionParams.actionCountLimit
                    # d = 1.0 - math.sin(sectionParams.actionCount * rads)
                    # d = 1.0 - math.pow(3, -.9 * delta)

                    d = math.pow(delta, 8)
                    d = 1

                    sectionParams.sectionPlacement[0] += sectionParams.sectionSpeed[0] * d
                    sectionParams.sectionPlacement[1] += sectionParams.sectionSpeed[1] * d
                    sectionParams.sectionSpeed[0] *= config.speedDeAcceleration
                    sectionParams.sectionSpeed[1] *= config.speedDeAcceleration

                    '''
					if sectionParams.sectionSpeed[0] != 0:
						sectionParams.sectionSpeed[0] = delta/sectionParams.sectionSpeed[0] 
					if sectionParams.sectionSpeed[1] != 0:
						sectionParams.sectionSpeed[1] = delta/sectionParams.sectionSpeed[1] 
					'''

                    # add some better easing

                    sectionParams.actionCount += 1

                    if random.random() < sectionParams.stopProb:
                        sectionParams.rotationSpeed = 0
                    if random.random() < sectionParams.stopProb:
                        sectionParams.sectionSpeed[0] = 0
                    if random.random() < sectionParams.stopProb:
                        sectionParams.sectionSpeed[1] = 0

        else:
            config.skipFramesCount += 1

        for s in config.stableSegments:

            tempCrop = config.patternImage.crop((s[0], s[1], s[2], s[3]))
            config.canvasImage.paste(tempCrop, (s[0], s[1]), tempCrop)

    '''
	tempCrop = config.patternImage.crop((0,0,256,32))

	tempCrop = config.patternImage.crop((0,160,256,184))
	config.canvasImage.paste(tempCrop, (0,160), tempCrop)	

	tempCrop = config.patternImage.crop((50,54,256,176))
	config.canvasImage.paste(tempCrop, (50,54), tempCrop)	
	'''


def runWork():
    global config
    print(bcolors.OKGREEN + "** " + bcolors.BOLD)
    print("Running repeatblocks.py")
    print(bcolors.ENDC)
    while config.isRunning == True:
        config.directorController.checkTime()
        if config.directorController.advance == True:
            iterate()
        time.sleep(config.redrawSpeed)
        if config.standAlone == False:
            config.callBack()


def iterate():
    global config
    # config.colOverlay.stepTransition()
    # config.linecolOverlay.stepTransition()
    # config.linecolOverlay2.stepTransition()
    # print(str("running  {}"))

    config.bgColor = tuple(
        round(a * config.brightness) for a in (config.colOverlay.currentColor)
    )

    # redraw(config)
    
    
    if config.useClipPlayer == True :
        config.clipMain.loadFrame()
        temp = config.clipMain.canvasImage.resize((config.clipMain.clipWidth,config.clipMain.clipHeight))
        temp = temp.rotate(config.clipRotate,expand=True)
        config.image.paste(temp, (config.clipXPos, config.clipYPos), mask =config.clipMain.removalMask )
        # config.image.paste(temp, (config.clipXPos, config.clipYPos), mask = temp )
        

    repeatImage(config, config.patternImage)

    if config.repeatDrawingMode == 1:
        redraw(config)

        if random.random() < config.loadAnImageProb:
            loadImageForBase()
        else:
            repeatImage(config, config.canvasImage)

        config.repeatDrawingMode = 0

    if random.random() < .005 and config.usePixelSortRandomize == True:
        config.usePixelSort = False

    if random.random() < .005 and config.usePixelSortRandomize == True:
        config.usePixelSort = True

    if config.randomizeSpeed == True:

        if random.random() < .03:
            config.ySpeed = config.ySpeedInit

        if random.random() < .1:
            config.ySpeed = 0

    if random.random() < .0005:
        config.triangles = True

    if random.random() < .01:
        config.triangles = False

    if random.random() < config.stableSectionsChangeProb:
        setupStableSections()

    # paste over a section of the image on to itself and rotate
    if config.sectionDisturbance == True and config.fader.fadingDone == True:
        disturber()

        
    # a blurred section distrubance
    if config.useBlurSection == True:
        cp = config.canvasImage.copy()
        mask_blur = config.mask.filter(
            ImageFilter.GaussianBlur(config.mask_blur_amt))
        cp_blur = cp.filter(ImageFilter.GaussianBlur(config.cp_blur_amt))
        config.canvasImage = Image.composite(
            cp_blur, config.canvasImage, mask_blur)

    if config.fader.fadingDone == True:
        config.fader.fadingDone = False
        config.fader.image = config.canvasImage
        config.fader.doingRefreshCount = 0
        # Rebuild the main pattern, halt any disturbances immediately - i.e. don't wait
        if config.doneCount >= (config.numberOfSections) and config.rebuildImmediatelyAfterDone == True:
            config.doSectionDisturbance = False
            rebuildPatterns()

    if config.doneCount >= config.numberOfSections and config.drawingPrinted == False and config.saveImages == True:
        config.fader.doingRefreshCount = 40
        config.drawingPrinted = True
        currentTime = time.time()
        baseName = config.outPutPath + str(currentTime)
        writeImage(baseName, renderImage=config.canvasImage)

    if random.random() < .01 :
        config.doSectionDisturbance = False
    if random.random() < .01 :
        config.doSectionDisturbance = True
    
    # Rebuild the main pattern, halt any disturbances
    if random.random() < config.rebuildPatternProbability:
        config.doSectionDisturbance = False
        rebuildPatterns()

    # RANDOM OVERLAY REPETITION DISTURBANCE
    if random.random() < config.redoSectionDisturbance and config.sectionDisturbance == True:
        config.doSectionDisturbance = True
        rebuildSections()

    if config.shingleVariation == True:
        if random.random() < config.redoSectionDisturbance:
            config.shingleVariationAmount = round(
                random.uniform(0, config.shingleVariationRange))
            config.doSectionDisturbance == True
            rebuildSections()

    config.fader.fadeIn(config)


        
    temp1 = Image.new("RGBA", (config.canvasWidth, config.canvasHeight))
    temp1Draw = ImageDraw.Draw(temp1)
    temp1Draw.rectangle((0, 0, config.canvasWidth,
                        config.canvasHeight), fill=config.colOverlay.bgColor)
    temp1.paste(config.image, (0, 0), config.image)
    
    if config.transformShape == True :
        temp1 = transformImage(temp1)
    
    if config.canvasRotation != 0 :
        temp1 = temp1.rotate(config.canvasRotation,3,True)
        temp1 = ImageEnhance.Contrast(temp1).enhance(1.20)
        # temp1 = temp1.transform()
    
    config.render(temp1, config.imgcanvasOffsetX, config.imgcanvasOffsetY, config.canvasWidth, config.canvasHeight)
    # Done


def transformImage(img):
	width, height = img.size
	m = -0.0
	xshift = abs(m) * 420
	new_width = width + int(round(xshift))

	# img = img.transform(
	# 	(new_width, height), Image.AFFINE, (1, -0.1, 0.0, -0.5, 1, 1), Image.BICUBIC
	# )
	img = img.transform(
		(new_width, height), Image.PERSPECTIVE, config.transformTuples, Image.BICUBIC
	)
	return img


def setUpDisturbanceConfigs(configSet):
    config.baseSectionSpeed = float(
        workConfig.get(configSet, "baseSectionSpeed"))
    config.sectionRotationRange = float(
        workConfig.get(configSet, "sectionRotationRange"))

    sectionPlacementXRange = workConfig.get(
        configSet, "sectionPlacementXRange").split(",")
    config.sectionPlacementXRange = tuple(
        map(lambda x: int(int(x)), sectionPlacementXRange))

    sectionPlacementYRange = workConfig.get(
        configSet, "sectionPlacementYRange").split(",")
    config.sectionPlacementYRange = tuple(
        map(lambda x: int(int(x)), sectionPlacementYRange))

    sectionWidthRange = workConfig.get(
        configSet, "sectionWidthRange").split(",")
    config.sectionWidthRange = tuple(
        map(lambda x: int(int(x)), sectionWidthRange))

    sectionHeightRange = workConfig.get(
        configSet, "sectionHeightRange").split(",")
    config.sectionHeightRange = tuple(
        map(lambda x: int(int(x)), sectionHeightRange))

    config.numberOfSections = int(
        workConfig.get(configSet, "numberOfSections"))
    config.sectionMovementCountMax = int(
        workConfig.get(configSet, "sectionMovementCountMax"))

    config.stopProb = float(workConfig.get(configSet, "stopProbMax"))
    config.sectionSpeedFactorHorizontal = float(
        workConfig.get(configSet, "sectionSpeedFactorHorizontal"))
    config.sectionSpeedFactorVertical = float(
        workConfig.get(configSet, "sectionSpeedFactorVertical"))
    config.speedDeAcceleration = float(
        workConfig.get(configSet, "speedDeAcceleration"))
    config.speedDeAccelerationBase = float(
        workConfig.get(configSet, "speedDeAcceleration"))
    config.redoSectionDisturbance = float(
        workConfig.get(configSet, "redoSectionDisturbance"))
    config.speedDeAccelerationUpperLimit = float(
        workConfig.get(configSet, "speedDeAccelerationUpperLimit"))
    config.rebuildImmediatelyAfterDone = (
        workConfig.getboolean(configSet, "rebuildImmediatelyAfterDone"))
    
    try:
        # comment: 
        config.diagonalMovement = (
        workConfig.getboolean(configSet, "diagonalMovement"))
        config.randomDiagonal = (
        workConfig.getboolean(configSet, "randomDiagonal"))
        config.diagonalFixedAngle = float(
        workConfig.get(configSet, "diagonalFixedAngle"))
    except Exception as e:
        print(str(e))
        config.diagonalMovement = False
    # end try


def setupStableSections():
    config.stableSegments = []
    n = round(random.uniform(config.stableSectionsMin, config.stableSectionsMax))
    minWidth = config.stableSectionsMinWidth
    minHeight = config.stableSectionsMinHeight
    for i in range(0, n):
        xPos = round(random.uniform(0, config.canvasWidth))
        xPos2 = round(random.uniform(xPos + minWidth, config.canvasWidth))
        yPos = round(random.uniform(0, config.canvasHeight))
        yPos2 = round(random.uniform(yPos + minHeight, config.canvasHeight))
        config.stableSegments.append([xPos, yPos, xPos2, yPos2])


def main(run=True):
    global config
    config.redrawSpeed = float(workConfig.get("movingpattern", "redrawSpeed"))
    config.blockWidth = int(workConfig.get("movingpattern", "blockWidth"))
    config.blockHeight = int(workConfig.get("movingpattern", "blockHeight"))
    config.rows = int(workConfig.get("movingpattern", "rows"))
    config.cols = int(workConfig.get("movingpattern", "cols"))
    config.lineDiff = int(workConfig.get("movingpattern", "lineDiff"))

    config.useDoubleLine = (workConfig.getboolean(
        "movingpattern", "useDoubleLine"))

    config.randomizeSpeed = (workConfig.getboolean(
        "movingpattern", "randomizeSpeed"))

    config.patternModel = (workConfig.get("movingpattern", "patternModel"))
    config.steps = int(workConfig.get("movingpattern", "steps"))
    config.steps2 = int(workConfig.get("movingpattern", "steps2"))
    config.amplitude = int(workConfig.get("movingpattern", "amplitude"))
    config.amplitude2 = int(workConfig.get("movingpattern", "amplitude2"))
    config.yOffset = int(workConfig.get("movingpattern", "yOffset"))
    config.yOffset2 = int(workConfig.get("movingpattern", "yOffset2"))

    config.speedFactor = float(workConfig.get("movingpattern", "speedFactor"))
    config.phaseFactor = float(workConfig.get("movingpattern", "phaseFactor"))
    config.xSpeed = float(workConfig.get("movingpattern", "xSpeed"))
    config.ySpeed = float(workConfig.get("movingpattern", "ySpeed"))
    config.ySpeedInit = float(workConfig.get("movingpattern", "ySpeed"))

    skipBlocks = (workConfig.get("movingpattern", "skipBlocks")).split(",")
    config.skipBlocks = tuple(map(lambda x: int(int(x)), skipBlocks))

    config.diamondUseTriangles = False
    config.diamondStep = int(workConfig.get("movingpattern", "diamondStep"))
    

    config.numConcentricBoxes = int(workConfig.get(
        "movingpattern", "numConcentricBoxes"))
    
    
    config.numShingleRows = int(workConfig.get(
        "movingpattern", "numShingleRows"))
    
    try:
        config.canvasRotation = float(workConfig.get("movingpattern", "canvasRotation"))
        config.imgcanvasOffsetX = int(workConfig.get("movingpattern", "canvasOffsetX"))
        config.imgcanvasOffsetY = int(workConfig.get("movingpattern", "canvasOffsetY"))
    except Exception as e:
        print(str(e))
        config.canvasRotation = 0
        config.imgcanvasOffsetX = 0
        config.imgcanvasOffsetY = 0
    # end try
    try:
        ringsRange = workConfig.get("movingpattern","ringsRange").split(",")
        stepsRange = workConfig.get("movingpattern","stepsRange").split(",")
        config.numScaleRows = int(workConfig.get("movingpattern","numScaleRows"))
        config.stepsRange = tuple(map(lambda x: int(int(x)), stepsRange))
        config.ringsRange = tuple(map(lambda x: int(int(x)), ringsRange))
    except Exception as e:
        print(str(e))
        config.stepsRange = (1,1)
        config.ringsRange = (1,1)
        config.numScaleRows = config.numShingleRows
        
        
    try:
        config.transformShape = workConfig.getboolean("movingpattern", "transformShape")
        transformTuples = workConfig.get("movingpattern", "transformTuples").split(",")
        config.transformTuples = tuple([float(i) for i in transformTuples])
    except Exception as e:
        print(str(e))
    # end try
    
    config.waveScaleRings = round(random.uniform(config.ringsRange[0], config.ringsRange[1]))
    config.waveScaleSteps = round(random.uniform(config.stepsRange[0], config.stepsRange[1]))
    print( config.waveScaleRings, config.waveScaleSteps)
    # end try

    config.randomBlockProb = float(
        workConfig.get("movingpattern", "randomBlockProb"))
    config.randomBlockWidth = int(workConfig.get(
        "movingpattern", "randomBlockWidth"))
    config.randomBlockHeight = int(workConfig.get(
        "movingpattern", "randomBlockHeight"))
    
    
    config.decoBoxBandWidth = int(workConfig.get(
        "movingpattern", "decoBoxBandWidth"))

    config.repeatProb = .99

    config.xIncrementer = 0
    config.yIncrementer = 0

    config.altLineColoring = True

    ########################################################################
    # CREATE THE IMAGE HOLDERS
    # canvasImage will get the drawing
    # disturbanceImage will get the disturbance / glitching
    # image will be the final output

    config.image = Image.new("RGBA", (config.canvasWidth, config.canvasHeight))
    config.patternImage = Image.new(
        "RGBA", (config.canvasWidth, config.canvasHeight))

    config.canvasImage = Image.new(
        "RGBA", (config.canvasWidth, config.canvasHeight))
    config.canvasDraw = ImageDraw.Draw(config.canvasImage)

    config.blockImage = Image.new(
        "RGBA", (config.blockWidth, config.blockHeight))
    config.blockDraw = ImageDraw.Draw(config.blockImage)

    ########################################################################

    config.destinationImage = Image.new(
        "RGBA", (config.canvasWidth, config.canvasHeight))
    config.transitionImage = Image.new(
        "RGBA", (config.canvasWidth, config.canvasHeight))

    config.rotateAltBlock = 0

    config.numRows = int(workConfig.get("movingpattern", "numRows"))
    config.numRowsRandomize = (workConfig.getboolean(
        "movingpattern", "numRowsRandomize"))

    config.numDotRows = int(workConfig.get("movingpattern", "numDotRows"))

    config.rebuildPatternProbability = float(
        workConfig.get("movingpattern", "rebuildPatternProbability"))
    config.patterns = workConfig.get("movingpattern", "patterns").split(",")

    config.patternModelVariations = workConfig.getboolean(
        "movingpattern", "patternModelVariations")
    patternSequence = workConfig.get(
        "movingpattern", "patternSequence").split(",")
    config.patternSequence = []
    for i in range(0, len(patternSequence), 3):
        config.patternSequence.append([patternSequence[i], int(
            patternSequence[i+1]), int(patternSequence[i+2])])

    config.usePixelSortRandomize = (workConfig.getboolean(
        "movingpattern", "usePixelSortRandomize"))

    config.shingleVariation = (workConfig.getboolean(
        "movingpattern", "shingleVariation"))
    config.shingleVariationRange = int(workConfig.get(
        "movingpattern", "shingleVariationRange"))
    config.shingleVariationAmount = config.shingleVariationRange

    config.useBlurSection = (workConfig.getboolean(
        "movingpattern", "useBlurSection"))
    config.blurSectionWidth = int(workConfig.get(
        "movingpattern", "blurSectionWidth"))
    config.blurSectionHeight = int(workConfig.get(
        "movingpattern", "blurSectionHeight"))
    config.blurSectionXPos = int(workConfig.get(
        "movingpattern", "blurSectionXPos"))
    config.blurSectionYPos = int(workConfig.get(
        "movingpattern", "blurSectionYPos"))
    config.mask_blur_amt = int(workConfig.get(
        "movingpattern", "mask_blur_amt"))
    config.cp_blur_amt = int(workConfig.get("movingpattern", "cp_blur_amt"))

    config.mask = Image.new("L", config.canvasImage.size, 0)
    config.mask_draw = ImageDraw.Draw(config.mask)

    config.mask_draw.ellipse((config.blurSectionXPos, config.blurSectionYPos, config.blurSectionXPos +
                              config.blurSectionWidth, config.blurSectionYPos + config.blurSectionHeight), fill=255)
    config.mask_blur_amt = config.mask_blur_amt
    config.cp_blur_amt = config.cp_blur_amt

    config.palettes = workConfig.get("movingpattern", "palettes").split(",")
    bgColorAlpha = (workConfig.get("movingpattern", "bgColorAlpha")).split(",")
    config.bgColorAlpha = list(map(lambda x: (int(x)), bgColorAlpha))
    buildPalette(config, 0)


    config.sectionDisturbance = (workConfig.getboolean(
        "movingpattern", "sectionDisturbance"))
    config.doSectionDisturbance = False
    config.disturbanceConfigSets = (workConfig.get(
        "movingpattern", "disturbanceConfigSets")).split(",")
    config.changeDisturbanceSetProb = float(
        workConfig.get("movingpattern", "changeDisturbanceSetProb"))
    workingDisturbanceSet = config.disturbanceConfigSets[0]
    config.skipFrames = 1
    config.skipFramesCount = 0
    setUpDisturbanceConfigs(workingDisturbanceSet)

    config.stableSectionsMin = int(workConfig.get(
        "movingpattern", "stableSectionsMin"))
    config.stableSectionsMax = int(workConfig.get(
        "movingpattern", "stableSectionsMax"))
    config.stableSectionsMinWidth = int(workConfig.get(
        "movingpattern", "stableSectionsMinWidth"))
    config.stableSectionsMinHeight = int(workConfig.get(
        "movingpattern", "stableSectionsMinHeight"))
    config.stableSectionsChangeProb = float(
        workConfig.get("movingpattern", "stableSectionsChangeProb"))
    setupStableSections()

    config.movingSections = []
    for i in range(0, config.numberOfSections):
        section = Holder()
        config.movingSections.append(section)
    rebuildSections()

    config.repeatDrawingMode = 1
    config.drawingPrinted = True
    config.saveImages = (workConfig.getboolean("movingpattern", "saveImages"))
    config.outPutPath = workConfig.get("movingpattern", "outPutPath")
    config.loadAnImageProb = float(
        workConfig.get("movingpattern", "loadAnImageProb"))
    config.imageSources = workConfig.get(
        "movingpattern", "imageSources").split(',')
    
    # ###########################################################################
    # ####################### clip player instert ################################
    try:
        config.useClipPlayer = workConfig.getboolean("imageSequencePlayer", "useClipPlayer")
        config.clipXPos = int(workConfig.get("imageSequencePlayer", "clipXPos"))
        config.clipYPos = int(workConfig.get("imageSequencePlayer", "clipYPos"))
        config.clipRotate = float(workConfig.get("imageSequencePlayer", "clipRotate"))
        config.clipMain = movieClip(config)
        config.clipMain.clipRotate = config.clipRotate
        config.clipMain.setUp(workConfig)
        
        
    except Exception as e:
        print(str(e))
        config.useClipPlayer = False
    # ###########################################################################

    config.doneCount = 0

    config.fader = Fader()
    config.fader.height = config.canvasHeight
    config.fader.width = config.canvasWidth
    config.fader.xPos = 0
    config.fader.yPos = 0
    config.fader.setUp()
    config.fader.image = config.canvasImage
    
    rebuildPatternSequence(config)

    config.directorController = Director(config)
    config.directorController.slotRate = .03

    # THIS IS USED AS WAY TO MOCKUP A CONFIGURATION OF RECTANGULAR PANELS
    panelDrawing.mockupBlock(config, workConfig)

    ''' 
		########### Need to add something like this at final render call  as well
			
		########### RENDERING AS A MOCKUP OR AS REAL ###########
		if config.useDrawingPoints == True :
			config.panelDrawing.canvasToUse = config.renderImageFull
			config.panelDrawing.render()
		else :
			#config.render(config.canvasImage, 0, 0, config.canvasWidth, config.canvasHeight)
			#config.render(config.image, 0, 0)
			config.render(config.renderImageFull, 0, 0)
	'''

    if run:
        runWork()


###############################################
