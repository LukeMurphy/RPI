import math
import random
import textwrap
import time
from modules.configuration import bcolors
from modules import badpixels, coloroverlay, colorutils, panelDrawing
from PIL import Image, ImageChops, ImageDraw, ImageEnhance, ImageFont, ImageOps
from modules.holder_director import Holder 
from modules.holder_director import Director 


def ScaleRotateTranslate(image, angle, center=None, new_center=None, scale=None, expand=False):
    if center is None:
        return image.rotate(angle)
    angle = -angle / 180.0 * math.pi
    nx, ny = x, y = center
    sx = sy = 1.0
    if new_center:
        (nx, ny) = new_center
    if scale:
        (sx, sy) = scale
    cosine = math.cos(angle)
    sine = math.sin(angle)
    a = cosine / sx
    b = sine / sx
    c = x - nx * a - ny * b
    d = -sine / sy
    e = cosine / sy
    f = y - nx * d - ny * e
    return image.transform(
        image.size, Image.AFFINE, (a, b, c, d, e, f), resample=Image.BICUBIC
    )


"""""" """""" """""" """""" """""" """""" """""" """""" """""" """""" ""


def drawCompositions():

    startx = config.imageWidth / 9
    wVariance = [config.imageWidth / 6, config.imageWidth / 3]
    hVariance = [config.imageHeight / 6, config.imageHeight / 2]
    wFactor = 1
    hFactor = 2
    starty = 0

    # Choose seam x point  -- ideally about 1/3 from left
    # the 100 px spread around the 1/3 width should really be proportional to the overall size
    # xVariance = round(random.uniform(config.canvasWidth - 50, config.canvasWidth + 50) / 3) 
    xVarianceSpread = round(config.canvasWidth/6)
    xVariance = round(random.uniform(config.canvasWidth - xVarianceSpread, config.canvasWidth + xVarianceSpread) / 3) 
    config.flip = False

    xSeam = int(
        random.uniform(
            config.imageWidth * 2 / 3 - xVariance, config.imageWidth * 2 / 3 + xVariance
        )
    )
    tiedToBottom = 0 if random.random() < 0.5 else 2

    angleRotation = random.uniform(-3, 3)

    fillsIn =(0,0,0,round(random.uniform(0,130)))

    insetPoly = []
    for p in config.inset_coords:
        xPos = config.inset_varX + round(p[0] + random.uniform(-config.inset_varX, config.inset_varX))
        yPos = config.inset_varY + round(p[1] + random.uniform(-config.inset_varY, config.inset_varY))
        insetPoly.append((xPos, yPos))

    temp = Image.new("RGBA", (config.imageWidth, config.imageHeight))
    drawtemp = ImageDraw.Draw(temp)
    drawtemp.polygon(insetPoly, fill=fillsIn)
 
    # previous interations did this
    if config.insetRotate == True :
        temp = ScaleRotateTranslate(temp, angleRotation, None, None, None, True)
  
    config.canvasImage.paste(temp, temp)
    fills = []
 
    for n in range(0, config.numSquarePairs):
        if config.useInsetColorControls == True :
            fills.append([0])
            fills[n] = colorutils.getRandomColorHSVSaturated(
                                            config.inset_minHue,
                                           config.inset_maxHue,
                                           config.inset_minSaturation,
                                           config.inset_maxSaturation,
                                            config.inset_minValue,
                                            config.inset_maxValue,
                                            config.inset_dropHueMin,
                                            config.inset_dropHueMax,
                                            config.inset_transparency
                                           )
        else :
            gray0 = round(random.uniform(0, 160) * config.brightness)
            gray1 = round(random.uniform(0, 160) * config.brightness)
            gray2 = round(random.uniform(0, 160) * config.brightness)
            fills = [
                (gray0, gray1, gray1, 255),
                (gray1, gray1, gray1, 255),
                (gray2, gray2, gray2, 255),
            ]

            if random.random() < 0.5:
                fills[0] = (gray0, gray0, gray1, 255)
   
   
            
        if n == 2:
            wFactor *= 1.5

        if n == 0:
            x1 = round(xSeam)
            x2 = round(random.uniform(x1 + startx, x1 + wVariance[1]))
            y1 = round(random.uniform(hVariance[0], hVariance[1]))
            y2 = round(
                random.uniform(y1 + hVariance[0] * hFactor, y1 + hVariance[1] * hFactor)
            )
            if n == tiedToBottom:
                y2 = config.imageHeight
            starty = round(random.uniform(0, config.imageHeight / 2))

        else:
            x1 = round(
                random.uniform(xSeam - startx * wFactor, xSeam - wVariance[1] * wFactor)
            )
            x2 = round(xSeam)
            y1 = starty - config.bottomOffsetModifier
            y2 = round(random.uniform(y1 + hVariance[0], y1 + hVariance[1]))
            if n == tiedToBottom:
                y2 = config.imageHeight
            starty = y2

            if random.random() < config.filterPatchProb:
                choice = round(random.uniform(1, 2))
                if n == choice:
                    config.remapImageBlock = True
                    config.remapImageBlockSection = (x1, y1, x2, y2)
                    config.remapImageBlockDestination = (x1, y1)

        rectHeight = y2 - y1

        temp = Image.new("RGBA", (config.imageWidth, config.imageHeight))
        drawtemp = ImageDraw.Draw(temp)
        if y2<y1 :
            y2=y1+5
        if x2<x1 :
            x2=x1+5
        drawtemp.rectangle((x1, y1, x2, y2), fill=fills[n])
  
        temp = ScaleRotateTranslate(temp, angleRotation, None, None, None, True)
        config.canvasImage.paste(temp, temp)

    # config.canvasImage.paste(temp, temp)

    if config.flip == True:
        config.canvasImage = config.canvasImage.transpose(Image.FLIP_TOP_BOTTOM)
        config.canvasImage = config.canvasImage.transpose(Image.ROTATE_180)


"""""" """""" """""" """""" """""" """""" """""" """""" """""" """""" ""


def main(run=True):
    global config, workConfig
    print("---------------------")
    print(bcolors.OKGREEN + "** " + bcolors.BOLD)
    print("STARTING compositions2.py")
    print(bcolors.OKGREEN + "** " + bcolors.BOLD)
    print(bcolors.ENDC)

    config.delay = float(workConfig.get("compositions", "delay"))
    config.canvasImageWidth = int(workConfig.get("compositions", "canvasImageWidth"))
    config.canvasImageHeight = int(workConfig.get("compositions", "canvasImageHeight"))
    config.refreshCount = int(workConfig.get("compositions", "refreshCount"))
    config.timeToComplete = float(workConfig.get("compositions", "timeToComplete"))
    config.cleanSlateProbability = float(workConfig.get("compositions", "cleanSlateProbability"))
    config.filterPatchProb = float(workConfig.get("compositions", "filterPatchProb"))

    config.imageWidth = config.canvasImageWidth
    config.imageHeight = config.canvasImageHeight

    config.minHue = float(workConfig.get("compositions", "minHue"))
    config.maxHue = float(workConfig.get("compositions", "maxHue"))
    config.minSaturation = float(workConfig.get("compositions", "minSaturation"))
    config.maxSaturation = float(workConfig.get("compositions", "maxSaturation"))
    config.minValue = float(workConfig.get("compositions", "minValue"))
    config.maxValue = float(workConfig.get("compositions", "maxValue"))
    try:
        config.dropHueMin = float(workConfig.get("compositions", "dropHueMin"))
        config.dropHueMax = float(workConfig.get("compositions", "dropHueMax"))
        # comment: 
    except Exception as e:
        print(str(e))
        config.dropHueMin = 0
        config.dropHueMax = 0
    # end try
 
    try:
        config.bgColorTransparency = int(workConfig.get("compositions", "bgColorTransparency"))
    except Exception as e:
        print(str(e))
        config.bgColorTransparency = 255
    # end try
    try:
        config.bottomOffsetModifier = int(workConfig.get("compositions", "bottomOffsetModifier"))
    except Exception as e:
        print(str(e))
        config.bottomOffsetModifier = 0
    # end try


    shapeCoords = list(
        map(lambda x: int(x), workConfig.get("compositions", "inset_coords").split(","))
    )
    config.inset_coords = []

    for c in range(0, len(shapeCoords), 2):
        config.inset_coords.append((shapeCoords[c], shapeCoords[c + 1]))


    try:
        config.insetRotate = (workConfig.getboolean("compositions", "insetRotate"))
        # comment: 
    except Exception as e:
        print(str(e))
        config.insetRotate = True
  
    try:
        config.useInsetColorControls = (workConfig.getboolean("compositions", "useInsetColorControls"))
        # comment: 
    except Exception as e:
        print(str(e))
        config.useInsetColorControls = False

  
    config.inset_varX = int(workConfig.get("compositions", "inset_varX"))
    config.inset_varY = int(workConfig.get("compositions", "inset_varY"))
    config.inset_minHue = float(workConfig.get("compositions", "inset_minHue"))
    config.inset_maxHue = float(workConfig.get("compositions", "inset_maxHue"))
    config.inset_maxSaturation = float(workConfig.get("compositions", "inset_maxSaturation"))
    config.inset_minSaturation = float(workConfig.get("compositions", "inset_minSaturation"))
    config.inset_maxValue = float(workConfig.get("compositions", "inset_maxValue"))
    config.inset_minValue = float(workConfig.get("compositions", "inset_minValue"))

    try:
        config.inset_dropHueMin = float(workConfig.get("compositions", "inset_dropHueMin"))
        config.inset_dropHueMax = float(workConfig.get("compositions", "inset_dropHueMax"))
        # comment: 
    except Exception as e:
        print(str(e))
        config.inset_dropHueMin = 0
        config.inset_dropHueMax = 0

    try:
        config.inset_transparency = int(workConfig.get("compositions", "insetMaxTransparency"))
        # comment: 
    except Exception as e:
        print(str(e))
        inset_transparency = 255
    # end try

    print("Running")

    try:
        config.bgColor = tuple(
            int(i) for i in (workConfig.get("compositions", "bgColor").split(","))
        )
        # comment: 
    except Exception as e:
        print(str(e))
        config.bgColor = colorutils.getRandomColorHSVSaturated(
            config.minHue,
            config.maxHue,
            config.minSaturation,
            config.maxSaturation,
            config.minValue,
            config.maxValue,
            config.dropHueMin,
            config.dropHueMax,
            config.bgColorTransparency,
        )
    # end try


    try:
        config.numSquarePairs = int(workConfig.get("compositions", "numSquarePairs"))
        # comment: 
    except Exception as e:
        print(str(e))
        config.numSquarePairs = 3
 
 
    config.t1 = time.time()
    config.t2 = time.time()

    # initial crossfade settings
    config.doingRefresh = config.refreshCount
    config.doingRefreshCount = config.refreshCount

    config.canvasImage = Image.new(
        "RGBA", (config.canvasImageWidth, config.canvasImageHeight)
    )
    config.draw = ImageDraw.Draw(config.canvasImage)
 
    config.draw.rectangle(
        (0, 0, config.imageWidth, config.imageHeight), fill=config.bgColor
    )

    config.firstRun = True
    config.flip = False
 
 
    config.directorController = Director(config)
 
    try :
        config.directorController.slotRate = float(workConfig.get("compositions", "slotRate"))
        config.directorController.delay = float(workConfig.get("compositions", "redrawSpeed"))
    except Exception as e:
        print(str(e))
        config.directorController.slotRate = .02
        config.directorController.delay = .02

    ### THIS IS USED AS WAY TO MOCKUP A CONFIGURATION OF RECTANGULAR PANELS
    panelDrawing.mockupBlock(config, workConfig)
    #### Need to add something like this at final render call  as well
    ''' 
        ########### RENDERING AS A MOCKUP OR AS REAL ###########
        if config.useDrawingPoints == True :
            config.panelDrawing.canvasToUse = config.renderImageFull
            config.panelDrawing.render()
        else :
            #config.render(config.canvasImage, 0, 0, config.canvasWidth, config.canvasHeight)
            #config.render(config.image, 0, 0)
            config.render(config.renderImageFull, 0, 0)
    '''

    drawCompositions()

    setUp()

    if run:
        runWork()


"""""" """""" """""" """""" """""" """""" """""" """""" """""" """""" ""


def restartDrawing():

    config.flip = True if random.random() < 0.5 else False
    if random.random() < config.cleanSlateProbability or config.firstRun == True:
        # grayLevel = round(random.uniform(20,70))
        # config.bgColor = (grayLevel,grayLevel,grayLevel)
        config.bgColor = colorutils.getRandomColorHSVSaturated(
            config.minHue,
            config.maxHue,
            config.minSaturation,
            config.maxSaturation,
            config.minValue,
            config.maxValue,
            config.dropHueMin,
            config.dropHueMax,
        )

        # print(config.bgColor)
        # config.bgColor = colorutils.getRandomColorHSV(0,360, .3,.95, .1,.94)
        config.draw.rectangle(
            (0, 0, config.imageWidth, config.imageHeight), fill=config.bgColor
        )
        config.firstRun = False
    drawCompositions()

    config.t1 = time.time()
    config.t2 = time.time()
    # initialize crossfade - in this case 100 steps ...
    config.doingRefresh = 0
    config.doingRefreshCount = config.refreshCount


"""""" """""" """""" """""" """""" """""" """""" """""" """""" """""" ""


def setUp():
    global config
    pass


"""""" """""" """""" """""" """""" """""" """""" """""" """""" """""" ""

def runWork():
    global config
    print(bcolors.OKGREEN + "** " + bcolors.BOLD)
    print("RUNNING compositions2.py")
    print(bcolors.OKGREEN + "** " + bcolors.BOLD)
    print(bcolors.ENDC)
    while config.isRunning == True:
        config.directorController.checkTime()
        if config.directorController.advance == True:
            iterate()
            time.sleep(config.directorController.delay)
        if config.standAlone == False :
            config.callBack()


"""""" """""" """""" """""" """""" """""" """""" """""" """""" """""" ""


def iterate():
    global config

    config.t2 = time.time()
    delta = config.t2 - config.t1

    if delta > config.timeToComplete:
        config.snapShot = config.canvasImage.copy()
        restartDrawing()

    # Need to do a crossfade
    if config.doingRefresh < config.doingRefreshCount:
        crossFade = Image.blend(
            config.snapShot,
            config.canvasImage,
            config.doingRefresh / config.doingRefreshCount,
        )
        #config.render(crossFade, 0, 0)
        ########### RENDERING AS A MOCKUP OR AS REAL ###########
        if config.useDrawingPoints == True :
            config.panelDrawing.canvasToUse = crossFade
            config.panelDrawing.render()
        else :
            config.render(crossFade, 0, 0)
        config.doingRefresh += 1
    else:
        temp = Image.new("RGBA", (config.canvasImageWidth, config.canvasImageHeight))
        temp.paste(config.canvasImage, (0, 0), config.canvasImage)
        #config.render(temp, 0, 0)
        ########### RENDERING AS A MOCKUP OR AS REAL ###########
        if config.useDrawingPoints == True :
            config.panelDrawing.canvasToUse = temp
            config.panelDrawing.render()
        else :
            config.render(temp, 0, 0)
    # config.render(config.canvasImage, 0,0)


"""""" """""" """""" """""" """""" """""" """""" """""" """""" """""" ""


def callBack():
    global config, XOs
    return True


"""""" """""" """""" """""" """""" """""" """""" """""" """""" """""" ""
