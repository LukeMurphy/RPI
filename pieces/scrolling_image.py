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

from modules.holder_director import Holder 
from modules.holder_director import Director 


lastRate = 0
colorutils.brightness = 1

def calculateNewSpeed() :
    if config.speedMPH != 0 :
        timeToComlete = 1 / config.speedMPH * (60 * 60) 
        desiredTimeToComplete =  1 / config.speedMPH * (60 * 60)  
        
        rate = config.directorController.slotRate
        numberOfCycles = timeToComlete  / rate
        newSpeed = round(config.maxX / numberOfCycles)
        config.speedX = newSpeed
        
        print(str("Cycles of drawing / second = {} repeat/second").format(1/config.directorController.slotRate))
        print(str("Time to complete one full turn = {} seconds").format(timeToComlete))
        print(str("Number of cycles it will take to complete = {}").format(numberOfCycles))
        print(str("Speed in pixels (the amount the drawing moves accross the total screen each cyle) = {} pixels/second").format(newSpeed))
        print(str("Physical speed accross lights = {} pixel-mm/second").format(newSpeed * config.mmPerPixel))
        
        # print(str("desired = {} seconds").format(round(desiredTimeToComplete,4)))
        if config.cycleCount > 0 :
            print(str("Desired Time per cycle = {}").format(round(desiredTimeToComplete/config.cycleCount, 6)))
        # print("----")
            
        # this changes the speed by changing the rate of change
        '''
        config.directorController.slotRate = desiredTimeToComplete/config.cycleCount
        '''


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
    
    config.cycleCount += 1
    
    # print(width, config.maxX,deltaX)
    if width >= config.maxX and deltaX >= (-config.scrollX)  :
        
        if deltaX < 0 : deltaX = 0
        print(str("deltaX = {}").format(deltaX))
        print(str("config.speedX = {}").format(config.speedX))
        
        crop1 = config.bufferImage.crop((xPos, yPos, deltaX + config.scrollX, height)).convert('RGBA')
        crop2 = config.bufferImage.crop((0, yPos, config.segmentWidth - deltaX, height)).convert('RGBA')
        config.canvasImage.paste(crop1, (config.xOffSet, config.yOffSet), crop1)
        config.canvasImage.paste(crop2, (deltaX + config.xOffSet, config.yOffSet), crop2)
        
        # config.speedX = 1
        # if deltaX <= config.speedX :
        config.t2 = time.time()
        delta = config.t2 - config.t1
        mph = 3600 * (config.maxX * config.mmPerPixel) / 1609344 / delta
        kmph = 3600 * (config.maxX * config.mmPerPixel) / 1000000 / delta
        
        print("\n")
        print(str("Time to complete 1 circuit = {}").format(round(delta, 4)))
        print(str("MPH = {}").format(round(mph,4)))
        print(str("KMPH = {}").format(round(kmph,4)))
        print(str("config.cycleCount = {}").format(config.cycleCount))
        print(str("Time per cycle = {}").format(round(delta/config.cycleCount, 6)))
        
        # if the rate of change is held the same, to change the speed, need to increase or decrease
        # the pixels traveled per cycle
        calculateNewSpeed()
        
        config.t1 = time.time()
        config.scrollX = 0
        xPos = 0
        config.cycleCount = 0
                    

                    
                    
    else:
        crop1 = config.bufferImage.crop((xPos, yPos, width, height)).convert('RGBA')
        config.canvasImage.paste(crop1, (config.xOffSet, config.yOffSet), crop1)
        crop1 = config.bufferImage2.crop((xPos, yPos, width, height)).convert('RGBA')
        crop1 = crop1.rotate(180)
        # config.canvasImage.paste(crop1, (0, 0), crop1)
        
        # cropt1Temp = crop1.copy()
        # cropt1Temp = cropt1Temp.rotate(180)
        # config.canvasImage.paste(cropt1Temp, (0, 0), cropt1Temp)
        # print(str("xPos = {}").format(xPos))
        
    # crop2 = config.bufferImage.crop((0, config.scrollStep, config.colStop, config.rowStop)).convert('RGBA')
    # config.canvasImage.paste(crop2, (0, 0), crop2)
    
    config.scrollX += config.speedX
    


def runWork():
    global config
    print(bcolors.OKGREEN + "** " + bcolors.BOLD)
    print("Running scrolling_image.py")
    print(bcolors.ENDC)
    
    while config.isRunning == True:
        config.directorController.checkTime()
        if config.directorController.advance == True:
            iterate()
            time.sleep(config.directorController.delay)
        if config.standAlone == False:
            config.callBack()



def iterate():
    global config
    redraw()
    
    
    if random.random() < config.filterRemappingProb:
        if config.useFilters == True and config.filterRemapping == True:
            config.filterRemap = True
            # new version  more control but may require previous pieces to be re-worked
            startX = round(random.uniform(0, config.filterRemapRangeX))
            startY = round(random.uniform(0, config.filterRemapRangeY))
            endX = round(random.uniform(config.filterRemapMinHorizSize, config.filterRemapHorizSize))
            endY = round(random.uniform(config.filterRemapMinVertiSize, config.filterRemapVertSize))
            
            # print(startX,endX,startY,endY)
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
    config.segmentWidth = int(workConfig.get("scrollingImage", "segmentWidth"))
    config.segmentHeight = int(workConfig.get("scrollingImage", "segmentHeight"))
    
    try:
        # comment: 
        config.speedMPH = float(workConfig.get("scrollingImage", "speedMPH"))
    except Exception as e:
        print(str(e))
        config.speedMPH = 0.0
    try:
        # comment: 
        config.speedKmPH = float(workConfig.get("scrollingImage", "speedKmPH"))
    except Exception as e:
        print(str(e))
        config.speedKmPH = 0.0
    # end try
    
    
    config.t1 = time.time()
    config.t2 = time.time()
    
    config.canvasImage = Image.new( "RGBA", (config.canvasWidth, config.canvasHeight))
    config.finalImage = Image.new("RGBA", (config.canvasWidth, config.canvasHeight))
    config.bufferImage = Image.new("RGBA", (config.canvasWidth, config.canvasHeight))
    config.image = Image.new("RGBA", (config.canvasWidth, config.canvasHeight))
    config.draw = ImageDraw.Draw(config.image)
    config.canvasDraw = ImageDraw.Draw(config.canvasImage)
    config.destinationImage = Image.new("RGBA", (config.canvasWidth, config.canvasHeight))
    config.xOffSet = int(workConfig.get("scrollingImage", "xOffSet"))
    config.yOffSet = int(workConfig.get("scrollingImage", "yOffSet"))

    config.redrawSpeed = float(workConfig.get("scrollingImage", "redrawSpeed"))
    config.baseImage = (workConfig.get("scrollingImage", "baseImage"))

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
    config.colOverlay.tLimitBase = 20
    config.colOverlay.steps = 50

    config.colOverlay.maxBrightness = config.brightness
    config.colOverlay.minSaturation = config.bg_minSaturation
    config.colOverlay.maxSaturation = config.bg_maxSaturation
    config.colOverlay.minValue = config.bg_minValue
    config.colOverlay.maxValue = config.bg_maxValue
    config.colOverlay.minHue = config.bg_minHue
    config.colOverlay.maxHue = config.bg_maxHue
    config.colOverlay.dropHueMin = config.bg_dropHueMinValue
    config.colOverlay.dropHueMax = config.bg_dropHueMaxValue

    config.colOverlay.colorTransitionSetup()

    config.backgroundColorChangeProb = float(workConfig.get("scrollingImage", "backgroundColorChangeProb"))
    config.filterRemapping = (workConfig.getboolean("scrollingImage", "filterRemapping"))
    config.filterRemappingProb = float(workConfig.get("scrollingImage", "filterRemappingProb"))
    config.filterRemapHorizSize = int(workConfig.get("scrollingImage", "filterRemapHorizSize"))
    config.filterRemapVertSize = int(workConfig.get("scrollingImage", "filterRemapVertSize"))
    config.filterRemapMinVertiSize = int(workConfig.get("scrollingImage", "filterRemapMinVertiSize"))
    config.filterRemapMinHorizSize = int(workConfig.get("scrollingImage", "filterRemapMinHorizSize"))
    config.filterRemapRangeX = int(workConfig.get("scrollingImage", "filterRemapRangeX"))
    config.filterRemapRangeY = int(workConfig.get("scrollingImage", "filterRemapRangeY"))
    
    config.directorController = Director(config)
    config.directorController.slotRate = float(workConfig.get("scrollingImage", "slotRate"))
    config.directorController.delay = float(workConfig.get("scrollingImage", "redrawSpeed"))
    config.mmPerPixel = int(workConfig.get("scrollingImage", "mmPerPixel"))
    config.mmSizeOfDrawing = int(workConfig.get("scrollingImage", "mmSizeOfDrawing"))
    
    config.resizeHeight = int(workConfig.get("scrollingImage", "resizeHeight"))
    
    im = Image.open(config.path + config.baseImage)
    config.bufferImage = im.copy()
    config.bufferImage2 = im.copy()
    config.bufferImage2 = config.bufferImage2.rotate(180)
    config.maxX = im.size[0]
    config.maxY = im.size[1]
    
    config.runCount = 0
    config.cycleCount = 0
    
    print(bcolors.OKGREEN + "** " + bcolors.BOLD)
    #  e.g in p4 mm panels, width of panel = 256 mm at 4mm per pixel = 64 pixels
    #  one mile = 16099344mm
    # 1,609,344 mm/mile  /  4 pixels/mm  pixels (at 4mm apart) = 402,336 pixels 
    # so an image that is 402,336 pixels in length or width, 
    # when displayed on a p4mm panel would stretch 1 mile
    
    # mph is 60s * 60m / time to travel length of image in pixels 
    # where image length = mm / mile  / width of panel in mm / distance in pixels
    
    # make it 1 mile in mm / pixels per mm
    config.newSize = round(config.mmSizeOfDrawing / config.mmPerPixel)
    config.maxX = config.newSize
    
    print(str("Total mm distance = {} mm").format(config.mmSizeOfDrawing ))
    print(str("Physcial scale of pixels {} mm/pixel").format(config.mmPerPixel ))
    print(str("Doing image resize to {} pixels to match the dots/mm of the panels").format(config.newSize ))
    print(str("Travel speed aiming for = {} MPH").format(config.speedMPH ))
    # config.bufferImage = config.bufferImage.resize((config.newSize,im.size[1]))
    
    if config.resizeHeight > 1 :
        config.bufferImage = config.bufferImage.resize((config.newSize,config.resizeHeight))
    else:
        config.bufferImage = config.bufferImage.resize((config.newSize,config.maxY))
        
    
    
    if config.speedMPH != 0 :
        # try to calculate the distance/s speed to match MPH
        #config.speedX = (config.maxX * config.mmPerPixel/ 16099344  /config.directorController.slotRate)
        calculateNewSpeed()
        # print(str("Length of Image in Pixels = {}").format(config.maxX ))
        # print(str("Speed Calculated = {}").format(config.speedX))
        print("***\n")
    
    
    if run:
        runWork()
