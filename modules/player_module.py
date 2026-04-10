#!/usr/bin/python
# import modules
import configparser
import datetime
import getopt
import importlib
import math
import os
import random
import sys
import textwrap
import time
import threading

import PIL.Image
from modules import configuration, panelDrawing
from modules.configuration import bcolors
from modules.configuration import pieceLogger
from PIL import Image, ImageChops, ImageDraw, ImageFont

"""
import gc
import io
import threading
import resource
from subprocess import call
"""


global thrd, config
global imageTop, imageBottom, image, transWiring

threads = []


class TopDirector:
    """docstring for TopDirector"""

    slotRate = 0.5

    def __init__(self, config):
        super(TopDirector, self).__init__()
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


def _configure_ReMapping(config, workconfig):
    """Configures image remapping settings."""

    

    try:
        _initialBlockSectionRemapping(workconfig, config)
    except Exception as e:
        pieceLogger(f" ** {e}", 1)
        config.remapImageBlock = False
        config.filterRemap = False
    try:
        config.remapImageBlockRotation = float(workconfig.get("displayconfig", "remapImageBlockSectionRotation"))
    except Exception as e:
        pieceLogger(f" ** {e}", 1)
        config.remapImageBlockRotation = 0

    try:
        config.remapImageBlockSectionRotation = float(workconfig.get("displayconfig", "remapImageBlockSectionRotation"))
    except Exception as e:
        pieceLogger(f" ** {e}", 1)
        config.remapImageBlockSectionRotation = 0

    try:
        config.remapImageBlock2 = workconfig.getboolean("displayconfig", "remapImageBlock2")
        config.remapImageBlockSection2 = workconfig.get("displayconfig", "remapImageBlockSection2").split(",")
        config.remapImageBlockSection2 = tuple(int(i) for i in config.remapImageBlockSection2)
        config.remapImageBlockDestination2 = workconfig.get("displayconfig", "remapImageBlockDestination2").split(",")
        config.remapImageBlockDestination2 = tuple(int(i) for i in config.remapImageBlockDestination2)
    except Exception as e:
        pieceLogger(f" ** {e}", 1)
        config.remapImageBlock2 = False

    try:
        config.remapImageBlockSection2Rotation = float(workconfig.get("displayconfig", "remapImageBlockSection2Rotation"))
    except Exception as e:
        pieceLogger(f" ** {e}", 1)
        config.remapImageBlockSection2Rotation = 0

    try:
        config.remapImageBlock3 = workconfig.getboolean("displayconfig", "remapImageBlock3")
        config.remapImageBlockSection3 = workconfig.get("displayconfig", "remapImageBlockSection3").split(",")
        config.remapImageBlockSection3 = tuple(int(i) for i in config.remapImageBlockSection3)
        config.remapImageBlockDestination3 = workconfig.get("displayconfig", "remapImageBlockDestination3").split(",")
        config.remapImageBlockDestination3 = tuple(int(i) for i in config.remapImageBlockDestination3)
    except Exception as e:
        pieceLogger(f" ** {e}", 1)
        config.remapImageBlock3 = False

    try:
        config.remapImageBlockSection3Rotation = float(workconfig.get("displayconfig", "remapImageBlockSection3Rotation"))
    except Exception as e:
        pieceLogger(f" ** {e}", 1)
        config.remapImageBlockSection3Rotation = 0

    try:
        config.remapImageBlock4 = workconfig.getboolean("displayconfig", "remapImageBlock4")
        config.remapImageBlockSection4 = workconfig.get("displayconfig", "remapImageBlockSection4").split(",")
        config.remapImageBlockSection4 = tuple(int(i) for i in config.remapImageBlockSection4)
        config.remapImageBlockDestination4 = workconfig.get("displayconfig", "remapImageBlockDestination4").split(",")
        config.remapImageBlockDestination4 = tuple(int(i) for i in config.remapImageBlockDestination4)
    except Exception as e:
        pieceLogger(f" ** {e}", 1)
        config.remapImageBlock4 = False

    try:
        config.remapImageBlockSection4Rotation = float(workconfig.get("displayconfig", "remapImageBlockSection4Rotation"))
    except Exception as e:
        pieceLogger(f" ** {e}", 1)
        config.remapImageBlockSection4Rotation = 0

    try:
        config.remapImageBlock5 = workconfig.getboolean("displayconfig", "remapImageBlock5")
        config.remapImageBlockSection5 = workconfig.get("displayconfig", "remapImageBlockSection5").split(",")
        config.remapImageBlockSection5 = tuple(int(i) for i in config.remapImageBlockSection5)
        config.remapImageBlockDestination5 = workconfig.get("displayconfig", "remapImageBlockDestination5").split(",")
        config.remapImageBlockDestination5 = tuple(int(i) for i in config.remapImageBlockDestination5)
    except Exception as e:
        pieceLogger(f" ** {e}", 1)
        config.remapImageBlock5 = False

    try:
        config.remapImageBlockSection5Rotation = float(workconfig.get("displayconfig", "remapImageBlockSection5Rotation"))
    except Exception as e:
        pieceLogger(f" ** {e}", 1)
        config.remapImageBlockSection5Rotation = 0

    try:
        config.remapImageBlock6 = workconfig.getboolean("displayconfig", "remapImageBlock6")
        config.remapImageBlockSection6 = workconfig.get("displayconfig", "remapImageBlockSection6").split(",")
        config.remapImageBlockSection6 = tuple(int(i) for i in config.remapImageBlockSection6)
        config.remapImageBlockDestination6 = workconfig.get("displayconfig", "remapImageBlockDestination6").split(",")
        config.remapImageBlockDestination6 = tuple(int(i) for i in config.remapImageBlockDestination6)
    except Exception as e:
        pieceLogger(f" ** {e}", 1)
        config.remapImageBlock6 = False

    try:
        config.remapImageBlockSection6Rotation = float(workconfig.get("displayconfig", "remapImageBlockSection6Rotation"))
    except Exception as e:
        pieceLogger(f" ** {e}", 1)
        config.remapImageBlockSection6Rotation = 0

    try:
        config.remapImageBlock7 = workconfig.getboolean("displayconfig", "remapImageBlock7")
        config.remapImageBlockSection7 = workconfig.get("displayconfig", "remapImageBlockSection7").split(",")
        config.remapImageBlockSection7 = tuple(int(i) for i in config.remapImageBlockSection7)
        config.remapImageBlockDestination7 = workconfig.get("displayconfig", "remapImageBlockDestination7").split(",")
        config.remapImageBlockDestination7 = tuple(int(i) for i in config.remapImageBlockDestination7)
    except Exception as e:
        pieceLogger(f" ** {e}", 1)
        config.remapImageBlock7 = False

    try:
        config.remapImageBlockSection7Rotation = float(workconfig.get("displayconfig", "remapImageBlockSection7Rotation"))
    except Exception as e:
        pieceLogger(f" ** {e}", 1)
        config.remapImageBlockSection7Rotation = 0


    _specialShiftBlockRemapping(workconfig, config)


def _specialShiftBlockRemapping(workconfig, config):
    # remapImageBlockShift
    for i in range(1,6) :
        _suff= ""
        if i > 1:
            _suff = str(i)
        _remapImageBlockShift = workconfig.getboolean("displayconfig", f"remapImageBlockShift{_suff}", fallback = False)
        setattr(config, f"remapImageBlockShift{_suff}", _remapImageBlockShift)
        pieceLogger(f"**> remapImageBlockShift{_suff} {_remapImageBlockShift}", 3)

        if _remapImageBlockShift :
            _remapImageBlockShiftSection = workconfig.get("displayconfig", f"remapImageBlockShiftSection{_suff}", fallback = "").split(",")
            _remapImageBlockShiftSection = tuple(int(i) for i in _remapImageBlockShiftSection)
            _remapImageBlockShiftDestination = workconfig.get("displayconfig", f"remapImageBlockShiftDestination{_suff}", fallback = "").split(",")
            _remapImageBlockShiftDestination = tuple(int(i) for i in _remapImageBlockShiftDestination)
            _remapImageBlockShiftStableSection = workconfig.get("displayconfig", f"remapImageBlockShiftStableSection{_suff}", fallback = "").split(",")
            _remapImageBlockShiftStableSection = tuple(int(i) for i in _remapImageBlockShiftStableSection)
            setattr(config, f"remapImageBlockShift{_suff}Section", _remapImageBlockShiftSection)
            setattr(config, f"remapImageBlockShift{_suff}Destination", _remapImageBlockShiftDestination)
            setattr(config, f"remapImageBlockShift{_suff}StableSection", _remapImageBlockShiftStableSection)



def _initialBlockSectionRemapping(workconfig, config):
    config.remapImageBlock = workconfig.getboolean("displayconfig", "remapImageBlock")
    config.remapImageBlockSection = workconfig.get("displayconfig", "remapImageBlockSection").split(",")
    config.remapImageBlockSection = tuple(int(i) for i in config.remapImageBlockSection)
    config.remapImageBlockDestination = workconfig.get("displayconfig", "remapImageBlockDestination").split(",")
    config.remapImageBlockDestination = tuple(int(i) for i in config.remapImageBlockDestination)
    config.filterRemap = True
    
    

def configure(config, workconfig):
    """Configures the player based on the provided configuration."""
    global path, tempImage, threads, thrd
    # gc.enable()
    pieceLogger(".......................................................................................",3)
    pieceLogger(f"** Setting PLAYER config values **", 3)
    _configure_base(config, workconfig)
    _configure_pixelsort(config, workconfig)
    _configure_ReMapping(config, workconfig)
    _configure_image_offsets(config, workconfig)
    _configure_blur(config, workconfig)
    _configure_color_boost(config, workconfig)
    _configure_brightness_variation(config, workconfig)
    _configure_force_bg_swap(config, workconfig)
    _configure_display(config, workconfig)
    _configure_tiles(config, workconfig)
    _configure_saving(config, workconfig)
    _load_work_module(config, workconfig)
    pieceLogger(f"{bcolors.ENDC}")


def _configure_base(config, workconfig):
    """Configures base settings."""
    config.checkForConfigChanges = workconfig.getboolean("displayconfig", "checkForConfigChanges", fallback=False)
    config.doFullReloadOnChange = workconfig.getboolean("displayconfig", "doFullReloadOnChange", fallback=False)
    config.outputMode = workconfig.get("displayconfig", "outputMode", fallback="")


def _configure_pixelsort(config, workconfig):
    """Configures pixelsort settings."""
    config.usePixelSort = workconfig.getboolean("displayconfig", "usePixelSort", fallback=False)
    config.pixelSortRotatesWithImage = workconfig.getboolean("displayconfig", "pixelSortRotatesWithImage", fallback=True)
    config.unsharpMaskPercent = int(workconfig.get("displayconfig", "unsharpMaskPercent", fallback=50))
    config.blurRadius = int(workconfig.get("displayconfig", "blurRadius", fallback=0))
    config.pixSortXOffset = int(workconfig.get("displayconfig", "pixSortXOffset", fallback=0))
    config.pixSortYOffset = int(workconfig.get("displayconfig", "pixSortYOffset", fallback=0))
    config.pixSortboxHeight = int(workconfig.get("displayconfig", "pixSortboxHeight", fallback=40))
    config.pixSortboxWidth = int(workconfig.get("displayconfig", "pixSortboxWidth", fallback=96))
    config.pixSortgap = int(workconfig.get("displayconfig", "pixSortgap", fallback=2))
    config.pixSortprobDraw = float(workconfig.get("displayconfig", "pixSortprobDraw", fallback=0.5))
    config.pixSortprobGetNextColor = float(workconfig.get("displayconfig", "pixSortprobGetNextColor", fallback=0.2))
    config.pixSortProbDecriment = float(workconfig.get("displayconfig", "pixSortProbDecriment", fallback=0.5))
    config.pixSortSizeDecriment = float(workconfig.get("displayconfig", "pixSortSizeDecriment", fallback=0.5))
    config.pixSortSampleVariance = int(workconfig.get("displayconfig", "pixSortSampleVariance", fallback=10))
    config.pixSortDrawVariance = int(workconfig.get("displayconfig", "pixSortDrawVariance", fallback=10))
    config.pixSortDirection = workconfig.get("displayconfig", "pixSortDirection", fallback="lateral")
    config.randomColorProbabilty = float(workconfig.get("displayconfig", "randomColorProbabilty", fallback=0.002))
    config.brightnessVarLow = float(workconfig.get("displayconfig", "brightnessVarLow", fallback=0.8))
    config.brightnessVarHi = float(workconfig.get("displayconfig", "brightnessVarHi", fallback=1.0))
    config.pixelSortAppearanceProb = float(workconfig.get("displayconfig", "pixelSortAppearanceProb", fallback=1.0))



def _configure_image_offsets(config, workconfig):
    """Configures image offset settings."""
    config.imageXOffset = int(workconfig.get("displayconfig", "imageXOffset", fallback=0))
    config.imageYOffset = int(workconfig.get("displayconfig", "imageYOffset", fallback=0))


def _configure_blur(config, workconfig):
    """Configures blur settings."""
    config.useBlur = workconfig.getboolean("displayconfig", "useBlur", fallback=False)
    config.blurXOffset = int(workconfig.get("displayconfig", "blurXOffset", fallback=0))
    config.blurYOffset = int(workconfig.get("displayconfig", "blurYOffset", fallback=0))
    config.blurSectionWidth = int(workconfig.get("displayconfig", "blurSectionWidth", fallback=0))
    config.blurSectionHeight = int(workconfig.get("displayconfig", "blurSectionHeight", fallback=0))
    config.sectionBlurRadius = int(workconfig.get("displayconfig", "sectionBlurRadius", fallback=0))

    if config.useBlur:
        config.blurSection = (
            config.blurXOffset,
            config.blurYOffset,
            config.blurXOffset + config.blurSectionWidth,
            config.blurYOffset + config.blurSectionHeight,
        )


def _configure_color_boost(config, workconfig):
    """Configures color boost settings."""
    config.redBoost = float(workconfig.get("displayconfig", "redBoost", fallback=1.0))
    config.greenBoost = float(workconfig.get("displayconfig", "greenBoost", fallback=1.0))
    config.blueBoost = float(workconfig.get("displayconfig", "blueBoost", fallback=1.0))


def _configure_brightness_variation(config, workconfig):
    """Configures brightness variation settings."""
    config.brightnessVariation = workconfig.getboolean("displayconfig", "brightnessVariation", fallback=False)
    config.brightnessVariationProb = float(workconfig.get("displayconfig", "brightnessVariationProb", fallback=0.0))

    if config.brightnessVariation:
        config.destinationBrightness = random.uniform(0.1, config.brightness)
        config.baseBrightness = config.brightness
        config.brightnessVariationTransition = False

    config.brightness = float(workconfig.get("displayconfig", "brightness", fallback=1.0))
    if config.brightnessOverride is not None:
        config.brightness = config.brightnessOverride
    config.minBrightness = float(workconfig.get("displayconfig", "minBrightness", fallback=1.0))


def _configure_force_bg_swap(config, workconfig):
    """Configures force background swap settings."""
    config.forceBGSwap = workconfig.getboolean("displayconfig", "forceBGSwap", fallback=False)


def _configure_display(config, workconfig):
    """Configures display settings."""
    config.screenHeight = int(workconfig.get("displayconfig", "screenHeight"))
    config.screenWidth = int(workconfig.get("displayconfig", "screenWidth"))
    config.windowWidth = int(workconfig.get("displayconfig", "windowWidth", fallback=config.screenWidth))
    config.windowHeight = int(workconfig.get("displayconfig", "windowHeight", fallback=config.screenHeight))


def _configure_tiles(config, workconfig):
    """Configures tile settings."""
    config.tileSizeWidth = int(workconfig.get("displayconfig", "tileSizeWidth", fallback=0))
    config.tileSizeHeight = int(workconfig.get("displayconfig", "tileSizeHeight", fallback=0))
    config.tileSize = (config.tileSizeWidth, config.tileSizeHeight)
    config.rows = int(workconfig.get("displayconfig", "rows"))
    config.cols = int(workconfig.get("displayconfig", "cols"))


def _configure_saving(config, workconfig):
    """Configures saving settings."""
    config.saveToFile = workconfig.getboolean("displayconfig", "saveToFile", fallback=False)

    if config.saveToFile:
        config.outPutPath = workconfig.get("displayconfig", "outPutPath")
        config.timeToTakeInterval = float(workconfig.get("displayconfig", "timeToTakeInterval"))
        config.saveFileCropFromLeft = workconfig.getint("displayconfig", "saveFileCropFromLeft", fallback=0)
        config.saveFileCropFromTop = workconfig.getint("displayconfig", "saveFileCropFromTop", fallback=0)
        config.topDirector = TopDirector(config)
        config.topDirector.slotRate = config.timeToTakeInterval


def _load_work_module(config, workconfig):
    """Loads the work module."""
    config.work = workconfig.get("displayconfig", "work")
    config.rendering = workconfig.get("displayconfig", "rendering", fallback ="hub")
    config.overallResize = workconfig.getboolean("displayconfig", "overallResize", fallback=False)

    pieceLogger(f"\n** modules.player.py is Loading: {config.work}\n", 3)
    pieceLogger("")

    try:
        work = importlib.import_module(f"pieces.{config.work}")
    except Exception as e:
        pieceLogger(f" ** {e}", 1)
        work = importlib.import_module(f"pieces.{config.work}")  # Try again without the pieces prefix

    work.config = config
    work.workConfig = workconfig
    config.workRefForSequencer = work

    if config.rendering == "hat":
        work.config.isRPI = True
        renderUsingIDAFruitHat(work)
    elif config.rendering == "hub":
        renderAsAnimationWindow(work)
    elif config.rendering == "out":
        renderUsingFFMPEG(work)


def renderUsingIDAFruitHat(work):

    # The AdaFruit specific LED matrix HAT
    from modules.rendering import rendertohat

    # this tests for the power-down RPI switch
    from cntrlscripts import stest

    thrd = threading.Thread(target=stest.__main__)
    threads.append(thrd)
    thrd.start()

    r = rendertohat
    # work.config.matrixTiles = int(work.workConfig.get("displayconfig", "matrixTiles"))
    work.config.transWiring = work.workConfig.getboolean("displayconfig", "transWiring")
    work.config.actualScreenWidth = int(work.workConfig.get("displayconfig", "actualScreenWidth"))
    work.config.canvasWidth = int(work.workConfig.get("displayconfig", "canvasWidth"))
    work.config.canvasHeight = int(work.workConfig.get("displayconfig", "canvasHeight"))
    work.config.rotation = float(work.workConfig.get("displayconfig", "rotation"))
    work.config.rotationTrailing = work.workConfig.getboolean("displayconfig", "rotationTrailing")
    work.config.fullRotation = work.workConfig.getboolean("displayconfig", "fullRotation")
    work.config.useFilters = work.workConfig.getboolean("displayconfig", "useFilters")

    try:
        work.config.isRPI = work.workConfig.getboolean("displayconfig", "isRPI")
    except Exception as e:
        pieceLogger(f"{bcolors.FAIL} ** {e}", 1)
        work.config.useFilters = False
        work.config.isRPI = True

    r.config = work.config
    r.work = work
    r.canvasOffsetX = int(work.workConfig.get("displayconfig", "canvasOffsetX"))
    r.canvasOffsetY = int(work.workConfig.get("displayconfig", "canvasOffsetY"))
    work.config.windowXOffset = int(work.workConfig.get("displayconfig", "windowXOffset"))
    work.config.windowYOffset = int(work.workConfig.get("displayconfig", "windowYOffset"))
    r.setUp()
    work.config.render = r.render
    work.config.updateCanvas = r.updateCanvas
    work.main()


def renderAsAnimationWindow(work):

    from modules.rendering import render
    import threading

    work.config.useFilters = work.workConfig.getboolean("displayconfig", "useFilters")
    work.config.rotation = float(work.workConfig.get("displayconfig", "rotation"))
    work.config.rotationTrailing = work.workConfig.getboolean("displayconfig", "rotationTrailing", fallback=True)
    work.config.fullRotation = work.workConfig.getboolean("displayconfig", "fullRotation", fallback=True)
    work.config.canvasWidth = int(work.workConfig.get("displayconfig", "canvasWidth"))
    work.config.canvasHeight = int(work.workConfig.get("displayconfig", "canvasHeight"))    
    # This is a special override for certain pieces where the dither mapping interacts with the 
    # remapping of sections of the image
    work.config.applyDitherBeforeRemapping = False

    try:
        work.config.ditherFilterBrightness = float(work.workConfig.get("displayconfig", "ditherFilterBrightness"))
    except Exception as e:
        pieceLogger(f"{bcolors.FAIL} ** {e}", 1)
        work.config.ditherFilterBrightness = 1.0

    try:
        work.config.ditherBlurRadius = int(work.workConfig.get("displayconfig", "ditherBlurRadius"))
        work.config.ditherUnsharpMaskPercent = int(work.workConfig.get("displayconfig", "ditherUnsharpMaskPercent"))
    except Exception as e:
        work.config.ditherBlurRadius = 0
        work.config.ditherUnsharpMaskPercent = 30
        pieceLogger(f"{bcolors.FAIL} ** {e}", 1)

    try:
        work.config.isRPI = work.workConfig.getboolean("displayconfig", "isRPI")
    except Exception as e:
        work.config.usePixSort = False
        work.config.isRPI = False
        pieceLogger(f"{bcolors.FAIL} ** {e}", 1)

    try:
        work.config.renderDiagnostics = work.workConfig.getboolean("displayconfig", "renderDiagnostics")
    except Exception as e:
        work.config.renderDiagnostics = False
        pieceLogger(f"{bcolors.FAIL} ** {e}", 1)

    if work.config.isRPI:
        from cntrlscripts import stest

        thrd = threading.Thread(target=stest.__main__)
        threads.append(thrd)
        thrd.start()

    try:
        work.config.filterRemapping = work.workConfig.getboolean("displayconfig", "filterRemapping")
        work.config.filterRemappingProb = float(work.workConfig.get("displayconfig", "filterRemappingProb"))
        work.config.filterRemapminHoriSize = int(work.workConfig.get("displayconfig", "filterRemapminHoriSize"))
        work.config.filterRemapminVertSize = int(work.workConfig.get("displayconfig", "filterRemapminVertSize"))
        work.config.filterRemapRangeX = int(work.workConfig.get("displayconfig", "filterRemapRangeX"))
        work.config.filterRemapRangeY = int(work.workConfig.get("displayconfig", "filterRemapRangeY"))
    except Exception as e:
        pieceLogger(f"{bcolors.FAIL} ** {e}", 1)
        work.config.filterRemapping = False
        work.config.filterRemappingProb = 0.0
        work.config.filterRemapminHoriSize = 128
        work.config.filterRemapminVertSize = 128
        work.config.filterRemapRangeX = work.config.canvasWidth
        work.config.filterRemapRangeY = work.config.canvasHeight

    # Create the image-canvas for the work
    # Because rotation is an option, recreate accordingly
    # And to be sure, make the renderImageFull bigger than necessary -
    work.config.renderImage = PIL.Image.new("RGBA", (work.config.canvasWidth * work.config.rows, 32))
    work.config.renderImageFull = PIL.Image.new("RGBA", (work.config.canvasWidth, work.config.canvasHeight))
    work.config.renderImageFull = PIL.Image.new("RGBA", (work.config.screenWidth, work.config.screenHeight))

    work.config.renderDraw = ImageDraw.Draw(work.config.renderImageFull)
    work.config.image = PIL.Image.new("RGBA", (work.config.canvasWidth, work.config.canvasHeight))
    work.config.draw = ImageDraw.Draw(work.config.image)

    renderer = render
    renderer.config = work.config
    renderer.work = work

    try:
        work.config.useLastOverlay = work.workConfig.getboolean("displayconfig", "useLastOverlay")
        work.config.useLastOverlayProb = float(work.workConfig.get("displayconfig", "useLastOverlayProb"))
        work.config.renderImageFullOverlay = Image.new("RGBA", (work.config.canvasWidth, work.config.canvasHeight))
        work.config.renderDrawOver = ImageDraw.Draw(work.config.renderImageFullOverlay)
    except Exception as e:
        pieceLogger(f"{bcolors.FAIL} ** {e}", 1)
        work.config.useLastOverlay = False

    renderer.canvasOffsetX = int(work.workConfig.get("displayconfig", "canvasOffsetX"))
    renderer.canvasOffsetY = int(work.workConfig.get("displayconfig", "canvasOffsetY"))
    work.config.windowXOffset = int(work.workConfig.get("displayconfig", "windowXOffset"))
    work.config.windowYOffset = int(work.workConfig.get("displayconfig", "windowYOffset"))

    work.config.drawBeforeConversion = renderer.drawBeforeConversion
    work.config.render = renderer.render
    work.config.updateCanvas = renderer.updateCanvas
    work.main(False)

    pieceLogger(f"** Player setting up: doing reload? {str(work.config.doingReload)}", 3)
    if work.config.doingReload == False and work.config.standAlone == True:
        renderer.setUp(work.config)


def renderUsingFFMPEG(work):

    from modules.rendering import rendertofile

    work.config.useFilters = work.workConfig.getboolean("displayconfig", "useFilters")
    work.config.rotation = float(work.workConfig.get("displayconfig", "rotation"))
    work.config.rotationTrailing = work.workConfig.getboolean("displayconfig", "rotationTrailing")
    work.config.fullRotation = work.workConfig.getboolean("displayconfig", "fullRotation")
    # work.config.matrixTiles = int(work.workConfig.get("displayconfig", "matrixTiles"))
    work.config.transWiring = work.workConfig.getboolean("displayconfig", "transWiring")
    work.config.actualScreenWidth = int(work.workConfig.get("displayconfig", "actualScreenWidth"))
    work.config.canvasWidth = int(work.workConfig.get("displayconfig", "canvasWidth"))
    work.config.canvasHeight = int(work.workConfig.get("displayconfig", "canvasHeight"))
    

    r = rendertofile
    r.config = work.config
    r.work = work
    r.work.x = r.work.y = 0
    r.fps = int(work.workConfig.get("output", "fps"))
    r.duration = int(work.workConfig.get("output", "duration"))
    r.mode = work.workConfig.get("output", "mode")

    # Test white rectangle on main rendering image
    # config.renderDraw.rectangle((0,0,400,300), fill=(255,255,255))

    work.config.render = r.render
    work.config.updateCanvas = r.updateCanvas
    work.main(False)

    r.setUp(r.mode)



