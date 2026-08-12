import configparser
import itertools
import math
import random

import noise
from PIL import Image, ImageFilter

from modules.holder_director import Holder
from modules.configuration import pieceLogger
_config = None
_workConfig = None


def init(cfg, wCfg):
    global _config, _workConfig
    _config = cfg
    _workConfig = wCfg


# --------------------- WAVE DEFORMER CLASS ---------------------

class WaveDeformer:
    def transform(self, x, y):
        y = y + _config.waveAmplitude * math.sin((x + _config.waveDeformXPos) / _config.wavePeriodMod) * noise.pnoise2(math.sin(x), y / _config.pNoiseMod)
        _config.waveAmplitude += _config.waveAmplitudeSpeed

        if _config.waveAmplitude > _config.waveAmplitudeMax:
            _config.waveAmplitudeSpeed *= -1
        if _config.waveAmplitude < _config.waveAmplitudeMin:
            _config.waveAmplitudeSpeed *= -1

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
            (x, y, x + _config.wavegridspace, y + _config.wavegridspace)
            for x, y in itertools.product(
                range(0, self.w, _config.wavegridspace),
                range(0, self.h, _config.wavegridspace),
            )
        ]
        source_grid = [self.transform_rectangle(*rect) for rect in target_grid]

        return list(zip(target_grid, source_grid))


# --------------------- DISTURBANCES  ---------------------
# loads the disturbance configs and calls the disturbance
# setup functions
def setupDisturbances():
    print(f"Setting up disturbances {_config}")

    try:
        _config.transformShape = _workConfig.getboolean("movingpattern", "transformShape")
        transformTuples = _workConfig.get("movingpattern", "transformTuples").split(",")
        _config.transformTuples = tuple(float(i) for i in transformTuples)
    except Exception as e:
        print(f"Error: setupDisturbance: {e}")
        _config.transformShape = False
    # end try

    try:
        setWaveDistortionParams()
    except Exception as e:
        print(e)
        _config.useWaveDistortion = False

    _config.sectionDisturbance = _workConfig.getboolean("movingpattern", "sectionDisturbance")
    _config.doSectionDisturbance = False
    _config.disturbanceConfigSets = (_workConfig.get("movingpattern", "disturbanceConfigSets")).split(",")
    _config.changeDisturbanceSetProb = float(_workConfig.get("movingpattern", "changeDisturbanceSetProb"))
    workingDisturbanceSet = _config.disturbanceConfigSets[0]
    _config.skipFrames = 0
    _config.skipFramesCount = 0
    setUpDisturbanceConfigs(workingDisturbanceSet)

    _config.stableSectionsMin = int(_workConfig.get("movingpattern", "stableSectionsMin"))
    _config.stableSectionsMax = int(_workConfig.get("movingpattern", "stableSectionsMax"))
    _config.stableSectionsMinWidth = int(_workConfig.get("movingpattern", "stableSectionsMinWidth"))
    _config.stableSectionsMinHeight = int(_workConfig.get("movingpattern", "stableSectionsMinHeight"))
    setupStableSections()

    _config.movingSections = []
    for _ in range(_config.numberOfSections):
        section = Holder()
        _config.movingSections.append(section)
    rebuildSections()



def setWaveDistortionParams():
    _config.useWaveDistortion = _workConfig.getboolean("movingpattern", "useWaveDistortion")
    _config.waveAmplitude = float(_workConfig.get("movingpattern", "waveAmplitude"))
    _config.waveAmplitudeMax = float(_workConfig.get("movingpattern", "waveAmplitudeMax", fallback=_config.waveAmplitude * 2))
    _config.waveAmplitudeMin = float(_workConfig.get("movingpattern", "waveAmplitudeMin", fallback=0))
    _config.waveAmplitudeSpeed = float(_workConfig.get("movingpattern", "waveAmplitudeSpeed", fallback="0.0"))
    _config.wavePeriodMod = float(_workConfig.get("movingpattern", "wavePeriodMod"))
    _config.wavegridspace = int(_workConfig.get("movingpattern", "wavegridspace"))
    _config.pNoiseMod = float(_workConfig.get("movingpattern", "pNoiseMod"))
    _config.waveDeformXPosRate = float(_workConfig.get("movingpattern", "waveDeformXPosRate"))
    _config.waveDeformXPos = 0


# loads the disturbance configs
def setUpDisturbanceConfigs(configSet):

    _config.disturbanceConfigFile = _workConfig.get("movingpattern", "disturbancesConfigs")
    _config.disturbanceConfig = configparser.ConfigParser()
    argument = f"{_config.path}/configs/{_config.disturbanceConfigFile}"
    _config.disturbanceConfig.read(argument)

    _config.baseSectionSpeed = float(_config.disturbanceConfig.get(configSet, "baseSectionSpeed"))

    sectionPlacementXRange = _config.disturbanceConfig.get(configSet, "sectionPlacementXRange").split(",")
    _config.sectionPlacementXRange = tuple(map(lambda x: int(x), sectionPlacementXRange))

    sectionPlacementYRange = _config.disturbanceConfig.get(configSet, "sectionPlacementYRange").split(",")
    _config.sectionPlacementYRange = tuple(map(lambda x: int(x), sectionPlacementYRange))

    sectionWidthRange = _config.disturbanceConfig.get(configSet, "sectionWidthRange").split(",")
    _config.sectionWidthRange = tuple(map(lambda x: int(x), sectionWidthRange))

    sectionHeightRange = _config.disturbanceConfig.get(configSet, "sectionHeightRange").split(",")
    _config.sectionHeightRange = tuple(map(lambda x: int(x), sectionHeightRange))

    _config.numberOfSections = int(_config.disturbanceConfig.get(configSet, "numberOfSections"))
    _config.sectionMovementCountMax = int(_config.disturbanceConfig.get(configSet, "sectionMovementCountMax"))

    _config.redoSectionDisturbance = float(_config.disturbanceConfig.get(configSet, "redoSectionDisturbance"))
    _config.rebuildImmediatelyAfterDone = _config.disturbanceConfig.getboolean(configSet, "rebuildImmediatelyAfterDone")

    _config.disturbanceScaleX = float(_config.disturbanceConfig.get(configSet, "disturbanceScaleX", fallback=5.0))
    _config.disturbanceScaleY = float(_config.disturbanceConfig.get(configSet, "disturbanceScaleY", fallback=5.0))


def setupStableSections():
    # print("New stable sections")
    _config.stableSegments = []
    n = round(random.uniform(_config.stableSectionsMin, _config.stableSectionsMax))
    minWidth = _config.stableSectionsMinWidth
    minHeight = _config.stableSectionsMinHeight
    for _ in range(n):
        xPos = round(random.uniform(0, _config.pictureWidth))
        xPos2 = round(random.uniform(xPos + minWidth, _config.pictureWidth))
        yPos = round(random.uniform(0, _config.pictureHeight))
        yPos2 = round(random.uniform(yPos + minHeight, _config.pictureHeight))
        _config.stableSegments.append([xPos, yPos, xPos2, yPos2])


# changes what disturbance sections are doing
def rebuildSections():
    global _config

    if random.random() < _config.changeDisturbanceSetProb:
        setNumber = math.floor(random.uniform(0, len(_config.disturbanceConfigSets)))
        setUpDisturbanceConfigs(_config.disturbanceConfigSets[setNumber])

    baseSpeed = _config.baseSectionSpeed

    for i in range(_config.numberOfSections):
        if i < len(_config.movingSections):
            section = _config.movingSections[i]
            section.sectionPlacementInit = [
                round(random.uniform(_config.sectionPlacementXRange[0], _config.sectionPlacementXRange[1])),
                round(random.uniform(_config.sectionPlacementYRange[0], _config.sectionPlacementYRange[1])),
            ]
            section.sectionSize = [
                round(random.uniform(_config.sectionWidthRange[0], _config.sectionWidthRange[1])),
                round(random.uniform(_config.sectionHeightRange[0], _config.sectionHeightRange[1])),
            ]
            section.actionCount = 0
            section.actionCountLimit = round(random.uniform(10, _config.sectionMovementCountMax))
            section.sectionMaxOffset = [
                random.uniform(-baseSpeed, baseSpeed) * _config.disturbanceScaleX,
                random.uniform(-baseSpeed, baseSpeed) * _config.disturbanceScaleY,
            ]

    _config.drawingPrinted = False


# performs the disturbances
def disturber():
    """Applies disturbances to the canvas image based on configuration."""
    """This function applies "disturbances" to a canvas image, either by
    disturbing specific sections or (in commented code) by repeating a pattern image.
    It also pastes stable (undisturbed) sections back onto the canvas. Thanks AI!"""
    _config.doneCount = 0

    if _config.doSectionDisturbance:
        disturbSections()

        # Paste stable sections onto the canvas
        for s in _config.stableSegments:
            tempCrop = _config.patternImage.crop((s[0], s[1], s[2], s[3]))
            # pieceLogger(f"{_config.canvasImage} {_config.config.canvasImage}")
            _config.canvasImage.paste(tempCrop, (s[0], s[1]), tempCrop)

    # else:
    #     drawRepeatedPatternImage(_config, _config.patternImage)
    # _config.canvasImage.paste(_config.patternImage, (0, 0), _config.patternImage)


def disturbSections():
    """Disturbs individual sections of the canvas image."""
    if _config.skipFramesCount >= _config.skipFrames:
        _config.skipFramesCount = 0
        # pieceLogger(f"[disturbance.disturbSections] {_config.numberOfSections}")

        for i in range(_config.numberOfSections):
            sectionParams = _config.movingSections[i]
            if sectionParams.actionCount >= sectionParams.actionCountLimit:
                _config.doneCount += 1
            else:
                disturbSingleSection(sectionParams)
    else:
        _config.skipFramesCount += 1


def disturbSingleSection(sectionParams):
    xPos = round(sectionParams.sectionPlacementInit[0])
    yPos = round(sectionParams.sectionPlacementInit[1])

    section = _config.canvasImage.crop((xPos, yPos, xPos + sectionParams.sectionSize[0], yPos + sectionParams.sectionSize[1]))

    t = sectionParams.actionCount / sectionParams.actionCountLimit
    # ease-out: fast start, gradual stop
    ease = 1 - math.pow(t, 3)

    dx = sectionParams.sectionMaxOffset[0] * ease
    dy = sectionParams.sectionMaxOffset[1] * ease

    _config.canvasImage.paste(section, (round(xPos + dx), round(yPos + dy)), section)

    sectionParams.actionCount += 1


# --------------------- LOOP HANDLERS ---------------------

def handleDisturbances():
    """Handles various image disturbances and effects."""
    # pieceLogger(_config.ySpeed)

    if _config.randomizeSpeed:
        if random.random() < 0.03:
            _config.ySpeed = _config.ySpeedInit
        if random.random() < 0.1:
            _config.ySpeed = 0

    if random.random() < 0.0005:
        _config.triangles = True

    if random.random() < 0.01:
        _config.triangles = False

    if _config.sectionDisturbance and _config.fader.fadingDone:
        disturber()

    if _config.useBlurSection:
        cp = _config.canvasImage.copy()
        mask_blur = _config.mask.filter(ImageFilter.GaussianBlur(_config.mask_blur_amt))
        cp_blur = cp.filter(ImageFilter.GaussianBlur(_config.cp_blur_amt))
        _config.canvasImage = Image.composite(cp_blur, _config.canvasImage, mask_blur)


def handleSectionDisturbances():
    """Handles random overlay repetition disturbance."""
    if random.random() < _config.redoSectionDisturbance and _config.sectionDisturbance and _config.fader.fadingDone:
        _config.doSectionDisturbance = True
        # this causes a jump!!!!
        # _config.canvasImage.paste(_config.patternImage, (0, 0), _config.patternImage)
        rebuildSections()


def handleShingleVariation():
    """Handles shingle variation if enabled."""
    if _config.shingleVariation and random.random() < _config.redoSectionDisturbance:
        _config.shingleVariationAmount = round(random.uniform(0, _config.shingleVariationRange))
        rebuildSections()
