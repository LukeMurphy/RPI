# ################################################### #
import argparse
import math
import random
import time
import types
import numpy as np
from modules.configuration import bcolors
from modules import badpixels, coloroverlay, colorutils
from PIL import Image, ImageDraw, ImageEnhance, ImageFont, ImageOps


lastRate = 0
colorutils.brightness = 1


def redraw():
    global config
    config.colOverlay.stepTransition()
    bgColor = config.colOverlay.currentColor
    bgColor = (round(config.brightness * bgColor[0]), round(config.brightness * bgColor[1]), round(config.brightness * bgColor[2]), config.bg_alpha)
    config.canvasDraw.rectangle((0,0,config.canvasWidth,config.canvasHeight), fill= (bgColor))

    # Scroll the image
    xPos = config.scrollX
    yPos = config.scrollY
    
    width = xPos + config.segmentWidth
    height = yPos + config.segmentHeight
    
    deltaX = config.maxX - config.scrollX
    if width >= config.maxX and deltaX >= 0  :
        
        # print(str("deltaX = {}").format(deltaX))
        
        crop1 = config.bufferImage.crop((xPos, yPos, deltaX + config.scrollX, height)).convert('RGBA')
        crop2 = config.bufferImage.crop((0, yPos, config.segmentWidth - deltaX, height)).convert('RGBA')
        config.canvasImage.paste(crop1, (0, 0), crop1)
        config.canvasImage.paste(crop2, (deltaX, 0), crop2)

        if deltaX <= config.speedX :
            config.t2 = time.time()
            print(str("Time to complete 1 circuit = {}").format(config.t2 - config.t1))
            print(str("MPH = {}").format(360/(config.t2 - config.t1)))
            config.t1 = time.time()
            config.scrollX = 0
            xPos = 0
    else:
        crop1 = config.bufferImage.crop((xPos, yPos, width, height)).convert('RGBA')
        config.canvasImage.paste(crop1, (0, 0), crop1)
        # print(str("xPos = {}").format(xPos))
        
    # crop2 = config.bufferImage.crop((0, config.scrollStep, config.colStop, config.rowStop)).convert('RGBA')
    # config.canvasImage.paste(crop2, (0, 0), crop2)
    
    config.scrollX += config.speedX
    


def runWork():
    global config
    print(bcolors.OKGREEN + "** " + bcolors.BOLD)
    print("Running moving_image.py")
    print(bcolors.ENDC)
    
    while config.isRunning == True:
        config.directorController.checkTime()
        if config.directorController.advance == True:
            iterate()
            time.sleep(config.directorController.delay)
        if config.standAlone == False:
            config.callBack()


class Director:
    """docstring for Director"""

    slotRate = .5
    delay = .5

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
        
        
def iterate():
    global config
    redraw()
    
    
    if random.random() < config.filterRemappingProb:
        if config.useFilters == True and config.filterRemapping == True:
            config.filterRemap = True
            # new version  more control but may require previous pieces to be re-worked
            startX = round(random.uniform(0, config.filterRemapRangeX))
            startY = round(random.uniform(0, config.filterRemapRangeY))
            endX = round(random.uniform(8, config.filterRemapminHoriSize))
            endY = round(random.uniform(8, config.filterRemapminVertSize))
            config.remapImageBlockSection = [
                startX, startY, startX + endX, startY + endY]
            config.remapImageBlockDestination = [startX, startY]
            # print("swapping" + str(config.remapImageBlockSection))
    
    
    config.render(config.canvasImage, 0, 0,config.screenWidth, config.screenHeight)
    # Done


def main(run=True):
    global config
    global workConfig
    
    config.scrollX = 0
    config.scrollXOffSet = 0
    config.scrollY = 0
    config.scrollYOffSet = 0
    
    config.speedX = int(workConfig.get("scrollingImage", "speedX"))
    config.segmentWidth = 256
    config.segmentHeight = 192
    
    config.t1 = time.time()
    config.t2 = time.time()
    
    config.canvasImage = Image.new( "RGBA", (config.canvasWidth, config.canvasHeight))
    config.finalImage = Image.new("RGBA", (config.canvasWidth, config.canvasHeight))
    config.bufferImage = Image.new("RGBA", (config.canvasWidth, config.canvasHeight))
    config.image = Image.new("RGBA", (config.canvasWidth, config.canvasHeight))
    config.draw = ImageDraw.Draw(config.image)
    config.canvasDraw = ImageDraw.Draw(config.canvasImage)
    config.destinationImage = Image.new("RGBA", (config.canvasWidth, config.canvasHeight))

    config.redrawSpeed = float(workConfig.get("scrollingImage", "redrawSpeed"))
    config.baseImage = (workConfig.get("scrollingImage", "baseImage"))

    im = Image.open(config.baseImage)
    config.bufferImage = im.copy()
    
    config.maxX = im.size[0]

    config.bg_minHue = int(workConfig.get("scrollingImage", "bg_minHue"))
    config.bg_maxHue = int(workConfig.get("scrollingImage", "bg_maxHue"))
    config.bg_minSaturation = float(workConfig.get("scrollingImage", "bg_minSaturation"))
    config.bg_maxSaturation = float(workConfig.get("scrollingImage", "bg_maxSaturation"))
    config.bg_minValue = float(workConfig.get("scrollingImage", "bg_minValue"))
    config.bg_maxValue = float(workConfig.get("scrollingImage", "bg_maxValue"))
    config.bg_dropHueMinValue = float(workConfig.get("scrollingImage", "bg_dropHueMinValue"))
    config.bg_dropHueMaxValue = float(workConfig.get("scrollingImage", "bg_dropHueMaxValue"))
    config.bg_alpha = int(workConfig.get("scrollingImage", "bg_alpha"))
    
    config.colOverlay = coloroverlay.ColorOverlay()
    config.colOverlay.randomSteps = True
    config.colOverlay.timeTrigger = True
    config.colOverlay.tLimitBase = 5
    config.colOverlay.steps = 10

    config.colOverlay.maxBrightness = config.brightness
    config.colOverlay.minSaturation = config.bg_minSaturation
    config.colOverlay.maxSaturation = config.bg_maxSaturation
    config.colOverlay.minValue = config.bg_minValue
    config.colOverlay.maxValue = config.bg_maxValue
    config.colOverlay.minHue = config.bg_minHue
    config.colOverlay.maxHue = config.bg_maxHue
    config.colOverlay.colorTransitionSetup()

    config.backgroundColorChangeProb = float(workConfig.get("scrollingImage", "backgroundColorChangeProb"))
    config.filterRemapping = (workConfig.getboolean("scrollingImage", "filterRemapping"))
    config.filterRemappingProb = float(workConfig.get("scrollingImage", "filterRemappingProb"))
    config.filterRemapminHoriSize = int(workConfig.get("scrollingImage", "filterRemapminHoriSize"))
    config.filterRemapminVertSize = int(workConfig.get("scrollingImage", "filterRemapminVertSize"))
    
    config.directorController = Director(config)
    config.directorController.slotRate = float(workConfig.get("scrollingImage", "slotRate"))
    config.directorController.delay = float(workConfig.get("scrollingImage", "redrawSpeed"))
    
    if run:
        runWork()
