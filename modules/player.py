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

    slotRate = .5

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


def configure(config, workconfig):
    global path, tempImage, threads, thrd
    # gc.enable()
    print(bcolors.WARNING + "** Setting PLAYER config values **" + bcolors.ENDC)


    ### Sets up for testing live config chages
    try:
        config.checkForConfigChanges = workconfig.getboolean(
            "displayconfig", "checkForConfigChanges"
        )
    except Exception as e:
        print(bcolors.FAIL + "** " +  str(e))
        config.checkForConfigChanges = False	
    ### Sets up for testing live config chages DOING FULL RELOAD
    try:
        config.doFullReloadOnChange = workconfig.getboolean(
            "displayconfig", "doFullReloadOnChange"
        )
    except Exception as e:
        print(bcolors.FAIL + "** " +  str(e))
        config.doFullReloadOnChange = False

    try:
        config.usePixelSort = workconfig.getboolean("displayconfig", "usePixelSort")
        config.pixelSortRotatesWithImage = workconfig.getboolean(
            "displayconfig", "pixelSortRotatesWithImage"
        )
        config.unsharpMaskPercent = int(
            workconfig.get("displayconfig", "unsharpMaskPercent")
        )
        config.blurRadius = int(workconfig.get("displayconfig", "blurRadius"))
        config.pixSortXOffset = int(workconfig.get("displayconfig", "pixSortXOffset"))
        config.pixSortYOffset = int(workconfig.get("displayconfig", "pixSortYOffset"))
        config.pixSortboxHeight = int(
            workconfig.get("displayconfig", "pixSortboxHeight")
        )
        config.pixSortboxWidth = int(workconfig.get("displayconfig", "pixSortboxWidth"))
        config.pixSortgap = int(workconfig.get("displayconfig", "pixSortgap"))
        config.pixSortprobDraw = float(
            workconfig.get("displayconfig", "pixSortprobDraw")
        )
        config.pixSortprobGetNextColor = float(
            workconfig.get("displayconfig", "pixSortprobGetNextColor")
        )
        config.pixSortProbDecriment = float(
            workconfig.get("displayconfig", "pixSortProbDecriment")
        )
        config.pixSortSizeDecriment = float(
            workconfig.get("displayconfig", "pixSortSizeDecriment")
        )
        config.pixSortSampleVariance = int(
            workconfig.get("displayconfig", "pixSortSampleVariance")
        )
        config.pixSortDrawVariance = int(
            workconfig.get("displayconfig", "pixSortDrawVariance")
        )
        config.pixSortDirection = str(
            workconfig.get("displayconfig", "pixSortDirection")
        )
        config.randomColorProbabilty = float(
            workconfig.get("displayconfig", "randomColorProbabilty")
        )
        config.brightnessVarLow = float(
            workconfig.get("displayconfig", "brightnessVarLow")
        )
        config.brightnessVarHi = float(
            workconfig.get("displayconfig", "brightnessVarHi")
        )
        config.pixelSortAppearanceProb = float(
            workconfig.get("displayconfig", "pixelSortAppearanceProb")
        )

    except Exception as e:
        print(bcolors.FAIL + "** " +  str(e))
        config.usePixelSort = False
        config.pixelSortRotatesWithImage = True
        config.unsharpMaskPercent = 50
        config.blurRadius = 0
        config.pixSortXOffset = 0
        config.pixSortYOffset = 0
        config.pixSortboxHeight = 40
        config.pixSortboxWidth = 96
        config.pixSortgap = 2
        config.pixSortprobDraw = 0.5
        config.pixSortprobGetNextColor = 0.2
        config.pixSortSizeDecriment = 0.5
        config.pixSortProbDecriment = 0.5
        config.pixSortSampleVariance = 10
        config.pixSortDrawVariance = 10
        config.pixSortDirection = "lateral"
        config.randomColorProbabilty = 0.002
        config.pixelSortAppearanceProb = 1

        config.brightnessVarLow = 0.8
        config.brightnessVarHi = 1

    ## used when repositioning a block of an image -- sculptural pieces when
    ## card configurations can't handle simple set up




    try:
        config.outputMode = workconfig.getboolean(
            "displayconfig", "outputMode"
        )
    except Exception as e:
        print(bcolors.FAIL + "** " +  str(e))
        config.outputMode = ""


    try:
        config.remapImageBlock = workconfig.getboolean(
            "displayconfig", "remapImageBlock"
        )
        config.remapImageBlockSection = workconfig.get(
            "displayconfig", "remapImageBlockSection"
        ).split(",")
        config.remapImageBlockSection = tuple(
            [int(i) for i in config.remapImageBlockSection]
        )
        config.remapImageBlockDestination = workconfig.get(
            "displayconfig", "remapImageBlockDestination"
        ).split(",")
        config.remapImageBlockDestination = tuple(
            [int(i) for i in config.remapImageBlockDestination]
        )
        config.filterRemap = True
    except Exception as e:
        print(bcolors.FAIL + "** " +  str(e))
        config.remapImageBlock = False
        config.filterRemap = False

    try:
        config.remapImageBlockSectionRotation = float(
            workconfig.get("displayconfig", "remapImageBlockSectionRotation")
        )
    except Exception as e:
        print(bcolors.FAIL + "** " +  str(e))
        config.remapImageBlockSectionRotation = 0

    try:
        config.remapImageBlock2 = workconfig.getboolean(
            "displayconfig", "remapImageBlock2"
        )
        config.remapImageBlockSection2 = workconfig.get(
            "displayconfig", "remapImageBlockSection2"
        ).split(",")
        config.remapImageBlockSection2 = tuple(
            [int(i) for i in config.remapImageBlockSection2]
        )
        config.remapImageBlockDestination2 = workconfig.get(
            "displayconfig", "remapImageBlockDestination2"
        ).split(",")
        config.remapImageBlockDestination2 = tuple(
            [int(i) for i in config.remapImageBlockDestination2]
        )
    except Exception as e:
        print(bcolors.FAIL + "** " +  str(e))
        config.remapImageBlock2 = False

    try:
        config.remapImageBlockSection2Rotation = float(
            workconfig.get("displayconfig", "remapImageBlockSection2Rotation")
        )
    except Exception as e:
        print(bcolors.FAIL + "** " +  str(e))
        config.remapImageBlockSection2Rotation = 0

    try:
        config.remapImageBlock3 = workconfig.getboolean(
            "displayconfig", "remapImageBlock3"
        )
        config.remapImageBlockSection3 = workconfig.get(
            "displayconfig", "remapImageBlockSection3"
        ).split(",")
        config.remapImageBlockSection3 = tuple(
            [int(i) for i in config.remapImageBlockSection3]
        )
        config.remapImageBlockDestination3 = workconfig.get(
            "displayconfig", "remapImageBlockDestination3"
        ).split(",")
        config.remapImageBlockDestination3 = tuple(
            [int(i) for i in config.remapImageBlockDestination3]
        )
    except Exception as e:
        print(bcolors.FAIL + "** " +  str(e))
        config.remapImageBlock3 = False

    try:
        config.remapImageBlockSection3Rotation = float(
            workconfig.get("displayconfig", "remapImageBlockSection3Rotation")
        )
    except Exception as e:
        print(bcolors.FAIL + "** " +  str(e))
        config.remapImageBlockSection3Rotation = 0

    try:
        config.remapImageBlock4 = workconfig.getboolean(
            "displayconfig", "remapImageBlock4"
        )
        config.remapImageBlockSection4 = workconfig.get(
            "displayconfig", "remapImageBlockSection4"
        ).split(",")
        config.remapImageBlockSection4 = tuple(
            [int(i) for i in config.remapImageBlockSection4]
        )
        config.remapImageBlockDestination4 = workconfig.get(
            "displayconfig", "remapImageBlockDestination4"
        ).split(",")
        config.remapImageBlockDestination4 = tuple(
            [int(i) for i in config.remapImageBlockDestination4]
        )
    except Exception as e:
        print(bcolors.FAIL + "** " +  str(e))
        config.remapImageBlock4 = False

    try:
        config.remapImageBlockSection4Rotation = float(
            workconfig.get("displayconfig", "remapImageBlockSection4Rotation")
        )
    except Exception as e:
        print(bcolors.FAIL + "** " +  str(e))
        config.remapImageBlockSection4Rotation = 0


    try:
        config.remapImageBlock5 = workconfig.getboolean(
            "displayconfig", "remapImageBlock5"
        )
        config.remapImageBlockSection5 = workconfig.get(
            "displayconfig", "remapImageBlockSection5"
        ).split(",")
        config.remapImageBlockSection5 = tuple(
            [int(i) for i in config.remapImageBlockSection5]
        )
        config.remapImageBlockDestination5 = workconfig.get(
            "displayconfig", "remapImageBlockDestination5"
        ).split(",")
        config.remapImageBlockDestination5 = tuple(
            [int(i) for i in config.remapImageBlockDestination5]
        )
    except Exception as e:
        print(bcolors.FAIL + "** " +  str(e))
        config.remapImageBlock5 = False

    try:
        config.remapImageBlockSection5Rotation = float(
            workconfig.get("displayconfig", "remapImageBlockSection5Rotation")
        )
    except Exception as e:
        print(bcolors.FAIL + "** " +  str(e))
        config.remapImageBlockSection5Rotation = 0


    try:
        config.remapImageBlock6 = workconfig.getboolean(
            "displayconfig", "remapImageBlock6"
        )
        config.remapImageBlockSection6 = workconfig.get(
            "displayconfig", "remapImageBlockSection6"
        ).split(",")
        config.remapImageBlockSection6 = tuple(
            [int(i) for i in config.remapImageBlockSection6]
        )
        config.remapImageBlockDestination6 = workconfig.get(
            "displayconfig", "remapImageBlockDestination6"
        ).split(",")
        config.remapImageBlockDestination6 = tuple(
            [int(i) for i in config.remapImageBlockDestination6]
        )
    except Exception as e:
        print(bcolors.FAIL + "** " +  str(e))
        config.remapImageBlock6 = False

    try:
        config.remapImageBlockSection6Rotation = float(
            workconfig.get("displayconfig", "remapImageBlockSection6Rotation")
        )
    except Exception as e:
        print(bcolors.FAIL + "** " +  str(e))
        config.remapImageBlockSection6Rotation = 0



    try:
        config.remapImageBlock7 = workconfig.getboolean(
            "displayconfig", "remapImageBlock7"
        )
        config.remapImageBlockSection7 = workconfig.get(
            "displayconfig", "remapImageBlockSection7"
        ).split(",")
        config.remapImageBlockSection7 = tuple(
            [int(i) for i in config.remapImageBlockSection7]
        )
        config.remapImageBlockDestination7 = workconfig.get(
            "displayconfig", "remapImageBlockDestination7"
        ).split(",")
        config.remapImageBlockDestination7 = tuple(
            [int(i) for i in config.remapImageBlockDestination7]
        )
    except Exception as e:
        print(bcolors.FAIL + "** " +  str(e))
        config.remapImageBlock7 = False

    try:
        config.remapImageBlockSection7Rotation = float(
            workconfig.get("displayconfig", "remapImageBlockSection7Rotation")
        )
    except Exception as e:
        print(bcolors.FAIL + "** " +  str(e))
        config.remapImageBlockSection7Rotation = 0


    try:
        config.imageXOffset = int(workconfig.get("displayconfig", "imageXOffset"))
        config.imageYOffset = int(workconfig.get("displayconfig", "imageYOffset"))
    except Exception as e:
        print(bcolors.FAIL + "** " +  str(e))
        config.imageXOffset = 0
        config.imageYOffset = 0

    try:
        config.useBlur = workconfig.getboolean("displayconfig", "useBlur")
        config.blurXOffset = int(workconfig.get("displayconfig", "blurXOffset"))
        config.blurYOffset = int(workconfig.get("displayconfig", "blurYOffset"))
        config.blurSectionWidth = int(
            workconfig.get("displayconfig", "blurSectionWidth")
        )
        config.blurSectionHeight = int(
            workconfig.get("displayconfig", "blurSectionHeight")
        )
        config.sectionBlurRadius = int(
            workconfig.get("displayconfig", "sectionBlurRadius")
        )
        config.blurSection = (
            config.blurXOffset,
            config.blurYOffset,
            config.blurXOffset + config.blurSectionWidth,
            config.blurYOffset + config.blurSectionHeight,
        )
    except Exception as e:
        print(bcolors.FAIL + "** " +  str(e))
        config.useBlur = False

    try:
        config.redBoost = float(workconfig.get("displayconfig", "redBoost"))
        config.greenBoost = float(workconfig.get("displayconfig", "greenBoost"))
        config.blueBoost = float(workconfig.get("displayconfig", "blueBoost"))
    except Exception as e:
        print(bcolors.FAIL + "** " +  str(e))
        config.redBoost = 1
        config.greenBoost = 1
        config.blueBoost = 1

    try:
        config.brightnessVariation = workconfig.getboolean(
            "displayconfig", "brightnessVariation"
        )
        config.brightnessVariationProb = float(
            workconfig.get("displayconfig", "brightnessVariationProb")
        )
        config.destinationBrightness = random.uniform(0.1, config.brightness)
        config.baseBrightness = config.brightness
        config.brightnessVariationTransition = False
    except Exception as e:
        print(bcolors.FAIL + "** " +  str(e))
        config.brightnessVariation = False
        config.brightnessVariationProb = 0


    try:
        config.forceBGSwap = workconfig.getboolean("displayconfig","forceBGSwap")
    except Exception as e:
        print(bcolors.FAIL + "** " +  str(e))
        config.forceBGSwap = False

    config.screenHeight = int(workconfig.get("displayconfig", "screenHeight"))
    config.screenWidth = int(workconfig.get("displayconfig", "screenWidth"))

    try:
        config.windowWidth = int(workconfig.get("displayconfig", "windowWidth"))
        config.windowHeight = int(workconfig.get("displayconfig", "windowHeight"))
    except Exception as e:
        print(bcolors.FAIL + "** " +  str(e))
        config.windowHeight = config.screenHeight 
        config.windowWidth = config.screenWidth 


    #config.tileSize = (int(workconfig.get("displayconfig", 'tileSizeHeight')),int(workconfig.get("displayconfig", 'tileSizeWidth')))

    try:
        config.tileSizeWidth = int(workconfig.get("displayconfig", "tileSizeWidth"))
        config.tileSizeHeight = int(workconfig.get("displayconfig", "tileSizeHeight"))
    except Exception as e:
        print(bcolors.FAIL + "** " +  str(e))
        config.forceBGSwap = False


    config.tileSize = (
        int(workconfig.get("displayconfig", "tileSizeWidth")),
        int(workconfig.get("displayconfig", "tileSizeHeight")),
    )
    config.rows = int(workconfig.get("displayconfig", "rows"))
    config.cols = int(workconfig.get("displayconfig", "cols"))

    config.brightness = float(workconfig.get("displayconfig", "brightness"))
    if config.brightnessOverride is not None:
        config.brightness = config.brightnessOverride

    config.minBrightness = float(workconfig.get("displayconfig", "minBrightness"))
    config.work = workconfig.get("displayconfig", "work")
    config.rendering = workconfig.get("displayconfig", "rendering")
 
    try:
        config.overallResize = workconfig.getboolean("displayconfig", "overallResize")
    except Exception as e:
        print(str(e))
        config.overallResize = False
 
    try:
        config.saveToFile = workconfig.getboolean("displayconfig", "saveToFile")
        config.outPutPath = workconfig.get("displayconfig", "outPutPath")
        config.timeToTakeInterval = float(workconfig.get("displayconfig", "timeToTakeInterval"))
        config.topDirector = TopDirector(config)
        config.topDirector.slotRate = config.timeToTakeInterval
    except Exception as e:
        print(str(e))
        config.saveToFile = False
    # end try

    #############################################################################
    # Create the image-canvas for the work if this is a stand-alone player!
    
    if  config.standAlone == False :
        pass
    else :
        config.renderImage = PIL.Image.new("RGBA", (config.screenWidth * config.rows, 32))
        config.renderImageFull = PIL.Image.new(
            "RGBA", (config.screenWidth, config.screenHeight)
        )

    config.image = PIL.Image.new("RGBA", (config.screenWidth, config.screenHeight))
    config.draw = ImageDraw.Draw(config.image)
    config.renderDraw = ImageDraw.Draw(config.renderImageFull)
    
    #############################################################################

    # Setting up based on how the work is displayed
    print(bcolors.WARNING + "** modules.player.py is Loading: " + str(config.work) + bcolors.ENDC)
    print(bcolors.OKBLUE)
    try:
        work = importlib.import_module("pieces." + str(config.work))
        work.config = config
        work.workConfig = workconfig
    except Exception as e:
        print(bcolors.FAIL + "** " +  str(e))
        ## On 5-23-019 a lot of pieces were moved to a sub directory called
        ## singletons - this is here to catch any unchanged configs
        work = importlib.import_module("pieces." + str(config.work))
        work.config = config
        work.workConfig = workconfig

    config.workRefForSequencer = work

    if(config.rendering == "hat") : 
        work.config.isRPI = True
        renderUsingIDAFruitHat(work)
    if config.rendering == "hub":
        renderUsingLINSNHub(work)
    if(config.rendering == "out") : 
        renderUsingFFMPEG(work)

"""
"""
def renderUsingIDAFruitHat(work):
    
    # The AdaFruit specific LED matrix HAT
    from modules.rendering import rendertohat
    # this tests for the power-down RPI switch
    from cntrlscripts import stest
    thrd = threading.Thread(target=stest.__main__)
    threads.append(thrd)
    thrd.start()

    r = rendertohat
    work.config.matrixTiles = int(work.workConfig.get("displayconfig", 'matrixTiles'))
    work.config.transWiring = (work.workConfig.getboolean("displayconfig", 'transWiring'))
    work.config.actualScreenWidth  = int(work.workConfig.get("displayconfig", 'actualScreenWidth'))
    work.config.canvasWidth = int(work.workConfig.get("displayconfig", 'canvasWidth'))
    work.config.canvasHeight = int(work.workConfig.get("displayconfig", 'canvasHeight'))
    work.config.rotation = float(work.workConfig.get("displayconfig", 'rotation'))
    work.config.rotationTrailing = (work.workConfig.getboolean("displayconfig", 'rotationTrailing'))
    work.config.fullRotation = (work.workConfig.getboolean("displayconfig", 'fullRotation'))
    work.config.useFilters  = (work.workConfig.getboolean("displayconfig", 'useFilters'))

    try :
        work.config.isRPI = (work.workConfig.getboolean("displayconfig", 'isRPI')) 
    except Exception as e: 
        print(bcolors.FAIL + "** " +  str(e))
        work.config.useFilters = False
        work.config.isRPI = True

    
    r.config = work.config
    r.work = work
    r.canvasOffsetX = int(work.workConfig.get("displayconfig", 'canvasOffsetX'))
    r.canvasOffsetY = int(work.workConfig.get("displayconfig", 'canvasOffsetY'))
    work.config.windowXOffset = int(work.workConfig.get("displayconfig", 'windowXOffset'))
    work.config.windowYOffset = int(work.workConfig.get("displayconfig", 'windowYOffset'))
    r.setUp()
    work.config.render = r.render
    work.config.updateCanvas = r.updateCanvas
    work.main()


def renderUsingLINSNHub(work):

    from modules.rendering import rendertohub
    import threading

    work.config.useFilters = work.workConfig.getboolean("displayconfig", "useFilters")
    work.config.rotation = float(work.workConfig.get("displayconfig", "rotation"))
    work.config.rotationTrailing = work.workConfig.getboolean(
        "displayconfig", "rotationTrailing"
    )
    work.config.fullRotation = work.workConfig.getboolean(
        "displayconfig", "fullRotation"
    )
    work.config.canvasWidth = int(work.workConfig.get("displayconfig", "canvasWidth"))
    work.config.canvasHeight = int(work.workConfig.get("displayconfig", "canvasHeight"))

    try:
        work.config.ditherFilterBrightness = float(
            work.workConfig.get("displayconfig", "ditherFilterBrightness")
        )
    except Exception as e:
        print(bcolors.FAIL + "** " +  str(e))
        work.config.ditherFilterBrightness = 1.0


    try:
        work.config.ditherBlurRadius = int(
            work.workConfig.get("displayconfig", "ditherBlurRadius")
        )
        work.config.ditherUnsharpMaskPercent = int(
            work.workConfig.get("displayconfig", "ditherUnsharpMaskPercent")
        )
    except Exception as e:
        work.config.ditherBlurRadius = 0
        work.config.ditherUnsharpMaskPercent = 30
        print(bcolors.FAIL + "** " +  str(e))

    try:
        work.config.isRPI = work.workConfig.getboolean("displayconfig", "isRPI")
    except Exception as e:
        work.config.usePixSort = False
        work.config.isRPI = False
        print(bcolors.FAIL + "** " +  str(e))

    try:
        work.config.renderDiagnostics = work.workConfig.getboolean("displayconfig", "renderDiagnostics")
    except Exception as e:
        work.config.renderDiagnostics = False
        print(bcolors.FAIL + "** " +  str(e))

    if work.config.isRPI == True:
        from cntrlscripts import stest

        thrd = threading.Thread(target=stest.__main__)
        threads.append(thrd)
        thrd.start()


    try:
        work.config.filterRemapping = (work.workConfig.getboolean("displayconfig", "filterRemapping"))
        work.config.filterRemappingProb = float(work.workConfig.get("displayconfig", "filterRemappingProb"))
        work.config.filterRemapminHoriSize = int(work.workConfig.get("displayconfig", "filterRemapminHoriSize"))
        work.config.filterRemapminVertSize = int(work.workConfig.get("displayconfig", "filterRemapminVertSize"))
        work.config.filterRemapRangeX = int(work.workConfig.get("displayconfig", "filterRemapRangeX"))
        work.config.filterRemapRangeY = int(work.workConfig.get("displayconfig", "filterRemapRangeY"))
    except Exception as e:
        print(bcolors.FAIL + "** " +  str(e))
        work.config.filterRemapping = False
        work.config.filterRemappingProb = 0.0
        work.config.filterRemapminHoriSize = 128
        work.config.filterRemapminVertSize = 128
        work.config.filterRemapRangeX = work.config.canvasWidth
        work.config.filterRemapRangeY = work.config.canvasHeight

        
    # Create the image-canvas for the work
    # Because rotation is an option, recreate accordingly
    # And to be sure, make the renderImageFull bigger than necessary -
    work.config.renderImage = PIL.Image.new(
        "RGBA", (work.config.canvasWidth * work.config.rows, 32)
    )
    work.config.renderImageFull = PIL.Image.new(
        "RGBA", (work.config.canvasWidth, work.config.canvasHeight)
    )
    work.config.renderImageFull = PIL.Image.new(
        "RGBA", (work.config.screenWidth, work.config.screenHeight)
    )

    work.config.renderDraw = ImageDraw.Draw(work.config.renderImageFull)
    work.config.image = PIL.Image.new(
        "RGBA", (work.config.canvasWidth, work.config.canvasHeight)
    )
    work.config.draw = ImageDraw.Draw(work.config.image)

    renderer = rendertohub
    renderer.config = work.config
    renderer.work = work

    try:
        work.config.useLastOverlay = work.workConfig.getboolean(
            "displayconfig", "useLastOverlay"
        )
        work.config.useLastOverlayProb = float(
            work.workConfig.get("displayconfig", "useLastOverlayProb")
        )
        work.config.renderImageFullOverlay = Image.new(
            "RGBA", (work.config.canvasWidth, work.config.canvasHeight)
        )
        work.config.renderDrawOver = ImageDraw.Draw(work.config.renderImageFullOverlay)
    except Exception as e:
        print(bcolors.FAIL + "** " +  str(e))
        work.config.useLastOverlay = False

    renderer.canvasOffsetX = int(work.workConfig.get("displayconfig", "canvasOffsetX"))
    renderer.canvasOffsetY = int(work.workConfig.get("displayconfig", "canvasOffsetY"))
    work.config.windowXOffset = int(
        work.workConfig.get("displayconfig", "windowXOffset")
    )
    work.config.windowYOffset = int(
        work.workConfig.get("displayconfig", "windowYOffset")
    )

    work.config.drawBeforeConversion = renderer.drawBeforeConversion
    work.config.render = renderer.render
    work.config.updateCanvas = renderer.updateCanvas
    work.main(False)

    print("** Player setting up: doing reload? " + str(work.config.doingReload))
    if work.config.doingReload == False and work.config.standAlone == True:
        renderer.setUp(work.config)


"""
"""
def renderUsingFFMPEG(work):

    from modules.rendering import rendertofile
    work.config.useFilters = work.workConfig.getboolean("displayconfig", "useFilters")
    work.config.rotation = float(work.workConfig.get("displayconfig", 'rotation'))
    work.config.rotationTrailing = (work.workConfig.getboolean("displayconfig", 'rotationTrailing'))
    work.config.fullRotation = (work.workConfig.getboolean("displayconfig", 'fullRotation'))
    work.config.matrixTiles = int(work.workConfig.get("displayconfig", 'matrixTiles'))
    work.config.transWiring = (work.workConfig.getboolean("displayconfig", 'transWiring'))
    work.config.actualScreenWidth  = int(work.workConfig.get("displayconfig", 'actualScreenWidth'))
    work.config.canvasWidth = int(work.workConfig.get("displayconfig", 'canvasWidth'))
    work.config.canvasHeight = int(work.workConfig.get("displayconfig", 'canvasHeight'))
    work.config.rotation = float(work.workConfig.get("displayconfig", 'rotation'))
    work.config.rotationTrailing = (work.workConfig.getboolean("displayconfig", 'rotationTrailing'))
    work.config.fullRotation = (work.workConfig.getboolean("displayconfig", 'fullRotation'))
    work.config.useFilters  = (work.workConfig.getboolean("displayconfig", 'useFilters'))
    r = rendertofile
    r.config = work.config
    r.work = work
    r.work.x = r.work.y = 0
    r.fps = int(work.workConfig.get("output", 'fps'))
    r.duration = int(work.workConfig.get("output", 'duration'))
    r.mode = (work.workConfig.get("output", 'mode'))

    # Test white rectangle on main rendering image
    #config.renderDraw.rectangle((0,0,400,300), fill=(255,255,255))

    work.config.render = r.render
    work.config.updateCanvas = r.updateCanvas
    work.main(False)
    
    r.setUp(r.mode)

"""""" """""" """""" """""" """""" """""" """""" """""" """""" """""" ""
