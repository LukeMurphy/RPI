import math
import random
import textwrap
import time
import noise
from noise import *
from modules.configuration import bcolors
from modules import badpixels, coloroverlay, colorutils, panelDrawing
from PIL import Image, ImageChops, ImageDraw, ImageEnhance, ImageFont, ImageOps


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


class WaveDeformer:
    def __init__(self, config):
        self.config = config
        
    def transform(self, x, y):
        y = y + self.config.waveAmplitude * math.sin(
            (x + self.config.waveDeformXPos) / self.config.wavePeriodMod
        ) * noise.pnoise2(math.sin(x), y / self.config.pNoiseMod)
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
        for x in range(0, self.w, self.config.wavegridspace):
            for y in range(0, self.h, self.config.wavegridspace):
                target_grid.append(
                    (x, y, x + self.config.wavegridspace, y + self.config.wavegridspace)
                )

        source_grid = [self.transform_rectangle(*rect) for rect in target_grid]

        return [t for t in zip(target_grid, source_grid)]
    

def setUpDisturbanceConfigs(configSet, config, workConfig):
    config.baseSectionSpeed = float(workConfig.get(configSet, "baseSectionSpeed"))
    config.sectionRotationRange = float(workConfig.get(configSet, "sectionRotationRange"))

    sectionPlacementXRange = workConfig.get(configSet, "sectionPlacementXRange").split(",")
    config.sectionPlacementXRange = tuple(map(lambda x: int(int(x)), sectionPlacementXRange))

    sectionPlacementYRange = workConfig.get(configSet, "sectionPlacementYRange").split(",")
    config.sectionPlacementYRange = tuple(map(lambda x: int(int(x)), sectionPlacementYRange))

    sectionWidthRange = workConfig.get(configSet, "sectionWidthRange").split(",")
    config.sectionWidthRange = tuple(map(lambda x: int(int(x)), sectionWidthRange))

    sectionHeightRange = workConfig.get(configSet, "sectionHeightRange").split(",")
    config.sectionHeightRange = tuple(map(lambda x: int(int(x)), sectionHeightRange))

    config.numberOfSections = int(workConfig.get(configSet, "numberOfSections"))
    config.sectionMovementCountMax = int(workConfig.get(configSet, "sectionMovementCountMax"))

    config.stopProb = float(workConfig.get(configSet, "stopProbMax"))
    config.sectionSpeedFactorHorizontal = float(workConfig.get(configSet, "sectionSpeedFactorHorizontal"))
    config.sectionSpeedFactorVertical = float(workConfig.get(configSet, "sectionSpeedFactorVertical"))
    config.speedDeAcceleration = float(workConfig.get(configSet, "speedDeAcceleration"))
    config.speedDeAccelerationBase = float(workConfig.get(configSet, "speedDeAcceleration"))
    config.redoSectionDisturbance = float(workConfig.get(configSet, "redoSectionDisturbance"))
    config.speedDeAccelerationUpperLimit = float(workConfig.get(configSet, "speedDeAccelerationUpperLimit"))
    config.rebuildImmediatelyAfterDone = (workConfig.getboolean(configSet, "rebuildImmediatelyAfterDone"))
    
    try:
        # comment: 
        config.diagonalMovement = (
        workConfig.getboolean(configSet, "diagonalMovement"))
    except Exception as e:
        print(str(e))
        config.diagonalMovement = False
    # end try

    try:
        config.randomDiagonal = (
        workConfig.getboolean(configSet, "randomDiagonal"))
        config.diagonalFixedAngle = float(
        workConfig.get(configSet, "diagonalFixedAngle"))
    except Exception as e:
        print(str(e))
        config.randomDiagonal = True


def setupStableSections(config):
    # print("setupStableSections RUNNING NOW")
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
    

def rebuildSections(config):
    # global config

    # print("REBUILDSECTIONS RUNNING NOW")
    if random.random() < config.changeDisturbanceSetProb:
        setNumber = math.floor(random.uniform(0, len(config.disturbanceConfigSets)))
        setUpDisturbanceConfigs(config.disturbanceConfigSets[setNumber],config.distortionConfigRef, config.distortionworkConfigRef)
        # print("REBUILDSECTIONS NEW RUNNING NOW: " + config.disturbanceConfigSets[setNumber])

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
                
        if config.randomDiagonal == False and config.diagonalMovement == True :
            speed = random.uniform(-baseSpeed, baseSpeed)/config.sectionSpeedFactorHorizontal
            
            hComponent = math.cos(config.diagonalFixedAngle) * speed
            vComponent = math.sin(config.diagonalFixedAngle) * speed
            section.sectionSpeed = [hComponent,vComponent]

            
        section.rotationSpeed = random.uniform(-baseSpeed, baseSpeed)
        section.actionCount = 0
        section.actionCountLimit = round(random.uniform(10, config.sectionMovementCountMax))
        section.done = False
        section.stopProb = random.uniform(0, config.stopProb)
        
    config.drawingPrinted = False


def disturber(config):

    if config.doSectionDisturbance == True:

        for i in range(0, config.numberOfSections):
            sectionParams = config.movingSections[i]

            if sectionParams.actionCount < sectionParams.actionCountLimit:
                
                # print("RUNNING disturb " + str(random.random()))

                xPos = round(sectionParams.sectionPlacementInit[0])
                yPos = round(sectionParams.sectionPlacementInit[1])
                section = config.canvasImage.crop(
                    (xPos, yPos, xPos + sectionParams.sectionSize[0], yPos + sectionParams.sectionSize[1]))


                config.canvasImage.paste(section, (round(sectionParams.sectionPlacement[0]), round(
                    sectionParams.sectionPlacement[1])), section)

                # delta = (sectionParams.actionCountLimit - sectionParams.actionCount)/sectionParams.actionCountLimit
                # d = math.pow(delta, 8)
                d = 1
                
                # print(sectionParams.sectionSpeed[0], sectionParams.sectionSpeed[1])

                sectionParams.sectionPlacement[0] += sectionParams.sectionSpeed[0] * d
                sectionParams.sectionPlacement[1] += sectionParams.sectionSpeed[1] * d
                sectionParams.sectionSpeed[0] *= config.speedDeAcceleration
                sectionParams.sectionSpeed[1] *= config.speedDeAcceleration

                sectionParams.actionCount += 1

                if random.random() < sectionParams.stopProb:
                    sectionParams.rotationSpeed = 0
                if random.random() < sectionParams.stopProb:
                    sectionParams.sectionSpeed[0] = 0
                if random.random() < sectionParams.stopProb:
                    sectionParams.sectionSpeed[1] = 0
                    
                # config.canvasDraw.rectangle((round(sectionParams.sectionPlacement[0]), 
                #                              round(sectionParams.sectionPlacement[1]), 
                #                              round(sectionParams.sectionPlacement[0]) +  sectionParams.sectionSize[0], 
                #                              round(sectionParams.sectionPlacement[1]) + + sectionParams.sectionSize[1] ), 
                #                             fill=(0,0,255,150))
                    
                # if sectionParams.rotationSpeed == 0 and sectionParams.sectionSpeed[0] == 0 and sectionParams.sectionSpeed[1] == 0 :
                #     config.doSectionDisturbance = False
                #     print("Turned off disturb - distrub done")


        # these are the sections that do not get smeared
        
        
        if config.doingRefresh < config.doingRefreshCount:
            tempCanvasImage  = Image.new("RGBA", (config.canvasWidth, config.canvasHeight))
            for s in config.stableSegments:
                tempCrop = config.image.crop((s[0], s[1], s[2], s[3]))
                # config.canvasImage.paste(tempCrop, (s[0], s[1]), tempCrop)
                tempCanvasImage.paste(tempCrop, (s[0], s[1]), tempCrop)
            
            # print("Crossfadings: " +  str(config.doingRefresh))
            # new blend in over a couple steps
            crossFade = Image.blend(
                config.canvasImage,
                tempCanvasImage,
                config.doingRefresh / config.doingRefreshCount,
            )
            config.doingRefresh +=1
            config.canvasImage.paste(crossFade, (0,0), crossFade)

        else :
            # print("pasting")
            for s in config.stableSegments:
                tempCrop = config.image.crop((s[0], s[1], s[2], s[3]))
                config.canvasImage.paste(tempCrop, (s[0], s[1]), tempCrop)
            
            
        


def additonalSetup(config, workConfig):
    
    config.distortionConfigRef = config
    config.distortionworkConfigRef = workConfig
    
    config.directorController = Director(config)
    config.redrawSpeed = float(workConfig.get("additonalSetup", "redrawSpeed"))
    config.directorController.slotRate = float(workConfig.get("additonalSetup", "slotRate"))

    config.dblockWidth = int(workConfig.get("additonalSetup", "blockWidth"))
    config.dblockHeight = int(workConfig.get("additonalSetup", "blockHeight"))

    config.imgcanvasOffsetX = int(workConfig.get("additonalSetup", "canvasOffsetX"))
    config.imgcanvasOffsetY = int(workConfig.get("additonalSetup", "canvasOffsetY"))
    
    config.useWaveDistortion = workConfig.getboolean("additonalSetup", "useWaveDistortion")
    config.waveAmplitude = float(workConfig.get("additonalSetup", "waveAmplitude"))
    config.wavePeriodMod = float(workConfig.get("additonalSetup", "wavePeriodMod"))
    config.wavegridspace = int(workConfig.get("additonalSetup", "wavegridspace"))
    config.pNoiseMod = float(workConfig.get("additonalSetup", "pNoiseMod"))
    config.waveDeformXPosRate = float(workConfig.get("additonalSetup", "waveDeformXPosRate"))
    config.waveDeformXPos = 0
        
    config.sectionDisturbance = (workConfig.getboolean("additonalSetup", "sectionDisturbance"))
    config.doSectionDisturbance = False
    config.disturbanceConfigSets = (workConfig.get("additonalSetup", "disturbanceConfigSets")).split(",")
    config.changeDisturbanceSetProb = float(workConfig.get("additonalSetup", "changeDisturbanceSetProb"))
    config.rebuildPatternProbability = float(workConfig.get("additonalSetup", "rebuildPatternProbability"))
    workingDisturbanceSet = config.disturbanceConfigSets[0]
    config.skipFrames = 1
    config.skipFramesCount = 0
    setUpDisturbanceConfigs(workingDisturbanceSet, config, workConfig)

    config.stableSectionsMin = int(workConfig.get("additonalSetup", "stableSectionsMin"))
    config.stableSectionsMax = int(workConfig.get("additonalSetup", "stableSectionsMax"))
    config.stableSectionsMinWidth = int(workConfig.get("additonalSetup", "stableSectionsMinWidth"))
    config.stableSectionsMinHeight = int(workConfig.get("additonalSetup", "stableSectionsMinHeight"))
    config.stableSectionsChangeProb = float(workConfig.get("additonalSetup", "stableSectionsChangeProb"))
    setupStableSections(config)

    config.movingSections = []
    for i in range(0, config.numberOfSections):
        section = Holder()
        config.movingSections.append(section)
        
    rebuildSections(config)


def iterationFunction(config):
    if random.random() < config.stableSectionsChangeProb:
        # print("resetting stable sections IN ITERATE")
        rebuildSections(config)
        setupStableSections(config)

    # paste over a section of the image on to itself and rotate
    if config.doSectionDisturbance == True:
        # print("Calling disturb " + str(random.random()))
        disturber(config)
    else :
        config.canvasImage.paste(config.image,(0,0),config.image)

    # print("quilts ",config.render, config.instanceNumber)
    # Rebuild the main pattern, halt any disturbances
    if random.random() < config.rebuildPatternProbability and config.doSectionDisturbance == True:
        # print("Setting disturb to off")
        config.doSectionDisturbance = False
        rebuildSections(config)

    # RANDOM OVERLAY REPETITION DISTURBANCE
    if random.random() < config.redoSectionDisturbance :
        # print("rebuilding disturb sections, truning disturb on")
        rebuildSections(config)
        config.doSectionDisturbance = True
        
def resetFunction(config):
    
        # config.doingRefresh = 1
        rebuildSections(config)
        setupStableSections(config)
        disturber(config)