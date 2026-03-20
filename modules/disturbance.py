import configparser
import itertools
import math
import random

import noise
from PIL import Image, ImageFilter

from modules.holder_director import Holder

config = None
workConfig = None


def init(cfg, wCfg):
    global config, workConfig
    config = cfg
    workConfig = wCfg


# --------------------- WAVE DEFORMER CLASS ---------------------

class WaveDeformer:
    def transform(self, x, y):
        y = y + config.waveAmplitude * math.sin((x + config.waveDeformXPos) / config.wavePeriodMod) * noise.pnoise2(math.sin(x), y / config.pNoiseMod)
        config.waveAmplitude += config.waveAmplitudeSpeed

        if config.waveAmplitude > config.waveAmplitudeMax:
            config.waveAmplitudeSpeed *= -1
        if config.waveAmplitude < config.waveAmplitudeMin:
            config.waveAmplitudeSpeed *= -1

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
            (x, y, x + config.wavegridspace, y + config.wavegridspace)
            for x, y in itertools.product(
                range(0, self.w, config.wavegridspace),
                range(0, self.h, config.wavegridspace),
            )
        ]
        source_grid = [self.transform_rectangle(*rect) for rect in target_grid]

        return list(zip(target_grid, source_grid))


# --------------------- DISTURBANCES  ---------------------
# loads the disturbance configs and calls the disturbance
# setup functions
def setupDisturbances():

    try:
        config.transformShape = workConfig.getboolean("movingpattern", "transformShape")
        transformTuples = workConfig.get("movingpattern", "transformTuples").split(",")
        config.transformTuples = tuple(float(i) for i in transformTuples)
    except Exception as e:
        print(e)
        config.transformShape = False
    # end try

    try:
        setWaveDistortionParams()
    except Exception as e:
        print(e)
        config.useWaveDistortion = False

    config.sectionDisturbance = workConfig.getboolean("movingpattern", "sectionDisturbance")
    config.doSectionDisturbance = False
    config.disturbanceConfigSets = (workConfig.get("movingpattern", "disturbanceConfigSets")).split(",")
    config.changeDisturbanceSetProb = float(workConfig.get("movingpattern", "changeDisturbanceSetProb"))
    workingDisturbanceSet = config.disturbanceConfigSets[0]
    config.skipFrames = 0
    config.skipFramesCount = 0
    setUpDisturbanceConfigs(workingDisturbanceSet)

    config.stableSectionsMin = int(workConfig.get("movingpattern", "stableSectionsMin"))
    config.stableSectionsMax = int(workConfig.get("movingpattern", "stableSectionsMax"))
    config.stableSectionsMinWidth = int(workConfig.get("movingpattern", "stableSectionsMinWidth"))
    config.stableSectionsMinHeight = int(workConfig.get("movingpattern", "stableSectionsMinHeight"))
    setupStableSections()

    config.movingSections = []
    for _ in range(config.numberOfSections):
        section = Holder()
        config.movingSections.append(section)
    rebuildSections()


def setWaveDistortionParams():
    config.useWaveDistortion = workConfig.getboolean("movingpattern", "useWaveDistortion")
    config.waveAmplitude = float(workConfig.get("movingpattern", "waveAmplitude"))
    config.waveAmplitudeMax = float(workConfig.get("movingpattern", "waveAmplitudeMax", fallback=config.waveAmplitude * 2))
    config.waveAmplitudeMin = float(workConfig.get("movingpattern", "waveAmplitudeMin", fallback=0))
    config.waveAmplitudeSpeed = float(workConfig.get("movingpattern", "waveAmplitudeSpeed", fallback="0.0"))
    config.wavePeriodMod = float(workConfig.get("movingpattern", "wavePeriodMod"))
    config.wavegridspace = int(workConfig.get("movingpattern", "wavegridspace"))
    config.pNoiseMod = float(workConfig.get("movingpattern", "pNoiseMod"))
    config.waveDeformXPosRate = float(workConfig.get("movingpattern", "waveDeformXPosRate"))
    config.waveDeformXPos = 0


# loads the disturbance configs
def setUpDisturbanceConfigs(configSet):

    config.disturbanceConfigFile = workConfig.get("movingpattern", "disturbancesConfigs")
    config.disturbanceConfig = configparser.ConfigParser()
    argument = f"{config.path}/configs/{config.disturbanceConfigFile}"
    config.disturbanceConfig.read(argument)

    config.baseSectionSpeed = float(config.disturbanceConfig.get(configSet, "baseSectionSpeed"))

    sectionPlacementXRange = config.disturbanceConfig.get(configSet, "sectionPlacementXRange").split(",")
    config.sectionPlacementXRange = tuple(map(lambda x: int(x), sectionPlacementXRange))

    sectionPlacementYRange = config.disturbanceConfig.get(configSet, "sectionPlacementYRange").split(",")
    config.sectionPlacementYRange = tuple(map(lambda x: int(x), sectionPlacementYRange))

    sectionWidthRange = config.disturbanceConfig.get(configSet, "sectionWidthRange").split(",")
    config.sectionWidthRange = tuple(map(lambda x: int(x), sectionWidthRange))

    sectionHeightRange = config.disturbanceConfig.get(configSet, "sectionHeightRange").split(",")
    config.sectionHeightRange = tuple(map(lambda x: int(x), sectionHeightRange))

    config.numberOfSections = int(config.disturbanceConfig.get(configSet, "numberOfSections"))
    config.sectionMovementCountMax = int(config.disturbanceConfig.get(configSet, "sectionMovementCountMax"))

    config.redoSectionDisturbance = float(config.disturbanceConfig.get(configSet, "redoSectionDisturbance"))
    config.rebuildImmediatelyAfterDone = config.disturbanceConfig.getboolean(configSet, "rebuildImmediatelyAfterDone")

    config.disturbanceScaleX = float(config.disturbanceConfig.get(configSet, "disturbanceScaleX", fallback=5.0))
    config.disturbanceScaleY = float(config.disturbanceConfig.get(configSet, "disturbanceScaleY", fallback=5.0))


def setupStableSections():
    # print("New stable sections")
    config.stableSegments = []
    n = round(random.uniform(config.stableSectionsMin, config.stableSectionsMax))
    minWidth = config.stableSectionsMinWidth
    minHeight = config.stableSectionsMinHeight
    for _ in range(n):
        xPos = round(random.uniform(0, config.canvasWidth))
        xPos2 = round(random.uniform(xPos + minWidth, config.canvasWidth))
        yPos = round(random.uniform(0, config.canvasHeight))
        yPos2 = round(random.uniform(yPos + minHeight, config.canvasHeight))
        config.stableSegments.append([xPos, yPos, xPos2, yPos2])


# changes what disturbance sections are doing
def rebuildSections():
    global config

    if random.random() < config.changeDisturbanceSetProb:
        setNumber = math.floor(random.uniform(0, len(config.disturbanceConfigSets)))
        setUpDisturbanceConfigs(config.disturbanceConfigSets[setNumber])

    baseSpeed = config.baseSectionSpeed

    for i in range(config.numberOfSections):
        if i < len(config.movingSections):
            section = config.movingSections[i]
            section.sectionPlacementInit = [
                round(random.uniform(config.sectionPlacementXRange[0], config.sectionPlacementXRange[1])),
                round(random.uniform(config.sectionPlacementYRange[0], config.sectionPlacementYRange[1])),
            ]
            section.sectionSize = [
                round(random.uniform(config.sectionWidthRange[0], config.sectionWidthRange[1])),
                round(random.uniform(config.sectionHeightRange[0], config.sectionHeightRange[1])),
            ]
            section.actionCount = 0
            section.actionCountLimit = round(random.uniform(10, config.sectionMovementCountMax))
            section.sectionMaxOffset = [
                random.uniform(-baseSpeed, baseSpeed) * config.disturbanceScaleX,
                random.uniform(-baseSpeed, baseSpeed) * config.disturbanceScaleY,
            ]

    config.drawingPrinted = False


# performs the disturbances
def disturber():
    """Applies disturbances to the canvas image based on configuration."""
    """This function applies "disturbances" to a canvas image, either by
    disturbing specific sections or (in commented code) by repeating a pattern image.
    It also pastes stable (undisturbed) sections back onto the canvas. Thanks AI!"""
    config.doneCount = 0

    if config.doSectionDisturbance:
        disturbSections()

        # Paste stable sections onto the canvas
        for s in config.stableSegments:
            tempCrop = config.patternImage.crop((s[0], s[1], s[2], s[3]))
            config.canvasImage.paste(tempCrop, (s[0], s[1]), tempCrop)

    # else:
    #     drawRepeatedPatternImage(config, config.patternImage)
    # config.canvasImage.paste(config.patternImage, (0, 0), config.patternImage)


def disturbSections():
    """Disturbs individual sections of the canvas image."""
    if config.skipFramesCount >= config.skipFrames:
        config.skipFramesCount = 0

        for i in range(config.numberOfSections):
            sectionParams = config.movingSections[i]

            if sectionParams.actionCount >= sectionParams.actionCountLimit:
                config.doneCount += 1
            else:
                disturbSingleSection(sectionParams)
    else:
        config.skipFramesCount += 1


def disturbSingleSection(sectionParams):
    xPos = round(sectionParams.sectionPlacementInit[0])
    yPos = round(sectionParams.sectionPlacementInit[1])
    section = config.canvasImage.crop((xPos, yPos, xPos + sectionParams.sectionSize[0], yPos + sectionParams.sectionSize[1]))

    t = sectionParams.actionCount / sectionParams.actionCountLimit
    # ease-out: fast start, gradual stop
    ease = 1 - math.pow(t, 3)

    dx = sectionParams.sectionMaxOffset[0] * ease
    dy = sectionParams.sectionMaxOffset[1] * ease

    config.canvasImage.paste(section, (round(xPos + dx), round(yPos + dy)), section)

    sectionParams.actionCount += 1


# --------------------- LOOP HANDLERS ---------------------

def handleDisturbances():
    """Handles various image disturbances and effects."""
    if config.randomizeSpeed:
        if random.random() < 0.03:
            config.ySpeed = config.ySpeedInit
        if random.random() < 0.1:
            config.ySpeed = 0

    if random.random() < 0.0005:
        config.triangles = True

    if random.random() < 0.01:
        config.triangles = False

    if config.sectionDisturbance and config.fader.fadingDone:
        disturber()

    if config.useBlurSection:
        cp = config.canvasImage.copy()
        mask_blur = config.mask.filter(ImageFilter.GaussianBlur(config.mask_blur_amt))
        cp_blur = cp.filter(ImageFilter.GaussianBlur(config.cp_blur_amt))
        config.canvasImage = Image.composite(cp_blur, config.canvasImage, mask_blur)


def handleSectionDisturbances():
    """Handles random overlay repetition disturbance."""
    if random.random() < config.redoSectionDisturbance and config.sectionDisturbance and config.fader.fadingDone:
        config.doSectionDisturbance = True
        config.canvasImage.paste(config.patternImage, (0, 0), config.patternImage)
        rebuildSections()


def handleShingleVariation():
    """Handles shingle variation if enabled."""
    if config.shingleVariation and random.random() < config.redoSectionDisturbance:
        config.shingleVariationAmount = round(random.uniform(0, config.shingleVariationRange))
        rebuildSections()
