import math
import random
import threading
import time
from modules.configuration import bcolors
from modules import colorutils
from PIL import Image, ImageDraw, ImageEnhance, ImageFont, ImageOps, ImageFilter


def reDraw():  # sourcery skip: extract-duplicate-method, use-itertools-product
    _blkWidth = 64
    clr = [(255, 0, 0, 255), (255, 0, 0, 255), (255, 0, 0, 255)]

    minHue = 60
    maxHue = 60
    minSaturation = 1.0
    maxSaturation = 1.0
    minValue = 1.0
    maxValue = 1.0


    for c in range(0, 6, 3):
        for r in range(2):
            if r == 1:
                clr[0] = colorutils.getRandomColorHSL(0, 0, 1.0, 1.0, 1.0, 1.0, 0, 0, 255, 1.0)
                clr[1] = colorutils.getRandomColorHSL(0, 0, 1.0, 1.0, .50, .50, 0, 0, 255, 1.0)
                clr[2] = colorutils.getRandomColorHSV(0, 0, 1.0, 1.0, 1.0, 1.0, 0, 0, 255, 1.0)
            if c == 3:
                clr[0] = colorutils.getRandomColorHSL(60, 60, 1.0, 1.0, 1.0, 1.0, 0, 0, 255, 1.0)
                clr[1] = colorutils.getRandomColorHSL(60, 60, 1.0, 1.0, .50, .50, 0, 0, 255, 1.0)
                clr[2] = colorutils.getRandomColorHSV(60, 60, 1.0, 1.0, 1.0, 1.0, 0, 0, 255, 1.0)
            if c == 3 and r == 1:
                clr[0] = colorutils.getRandomColorHSL(120, 120, 1.0, 1.0, 1.0, 1.0, 0, 0, 255, 1.0)
                clr[1] = colorutils.getRandomColorHSL(120, 120, 1.0, 1.0, .50, .50, 0, 0, 255, 1.0)
                clr[2] = colorutils.getRandomColorHSV(minHue, maxHue, minSaturation, maxSaturation, minValue, maxValue, 0, 0, 255, 1.0)
            for c2 in range(3):
                _x1 = c * _blkWidth + 8 * c + c2 * _blkWidth + 4 * c2
                _y1 = r * _blkWidth + 0 * r
                _x2 = _x1 + _blkWidth
                _y2 = _y1 + _blkWidth
                config.draw.rectangle((_x1, _y1, _x2, _y2), fill=clr[c2])


def runWork():
    global config
    print(f"{bcolors.OKGREEN}** {bcolors.BOLD}")
    print("RUNNING dotgrid.py")
    print(bcolors.ENDC)

    while config.isRunning == True:
        iterate()
        time.sleep(config.redrawRate)
        if config.standAlone == False:
            config.callBack()


def iterate():
    global config
    # Display bar, spinner, message or %
    reDraw()
    # Do the final rendering of the composited image
    config.render(config.image, 0, 0, config.screenWidth, config.screenHeight)


def main(run=True):
    global config
    global workConfig
    config.debug = workConfig.getboolean("gradients", "debug")

    config.image = Image.new("RGBA", (config.screenWidth, config.screenHeight))
    config.draw = ImageDraw.Draw(config.image)

    # config.vOffset = int(workConfig.get("gradients", "vOffset"))
    # config.steps = int(workConfig.get("gradients", "steps"))
    config.redrawRate = float(workConfig.get("gradients", "redrawRate"))
    # config.alpha1 = float(workConfig.get("gradients", "alpha1"))
    # config.alpha2 = float(workConfig.get("gradients", "alpha2"))

    # config.rowsShown = int(workConfig.get("gradients", "rowsShown"))
    # config.colsShown = int(workConfig.get("gradients", "colsShown"))
    # config.rowHeight = int(workConfig.get("gradients", "rowHeight"))
    # config.angle = float(workConfig.get("gradients", "angle"))
    # config.probDraw = float(workConfig.get("gradients", "probDraw"))
    # config.blackProb = float(workConfig.get("gradients", "blackProb"))
    # config.heightMin = int(workConfig.get("gradients", "heightMin"))
    # config.heightMax = int(workConfig.get("gradients", "heightMax"))
    # config.colorChoice = workConfig.get("gradients", "colorChoice")
    # config.fadeThruBlack = workConfig.getboolean("gradients", "fadeThruBlack")
    # config.grayProb = float(workConfig.get("gradients", "grayProb"))

    # config.probDrawChange = float(workConfig.get("gradients", "probDrawChange"))
    # config.probDrawEffective = 1.0

    # config.boxMax = config.screenWidth - 2
    # config.boxMaxAlt = config.boxMax + int(random.uniform(10, 30) * config.screenWidth)
    # config.boxHeight = config.screenHeight - 3

    # config.xPos = 0
    # config.yPos = 0

    # config.bgColorVals = (workConfig.get("gradients", "bgColor")).split(",")
    # config.holderColor = tuple(map(lambda x: int(x), config.bgColorVals))
    # config.grayLevelLower = int(workConfig.get("gradients", "grayLevelLower"))
    # config.grayLevelUpper = int(workConfig.get("gradients", "grayLevelUpper"))
    # config.dotBlurRadius = int(workConfig.get("gradients", "dotBlurRadius"))

    # try:
    # 	config.blockXOffset = tuple(map(lambda x: int(x), workConfig.get("gradients", "blockXOffset").split(",")))
    # 	config.blockYOffset = tuple(map(lambda x: int(x), workConfig.get("gradients", "blockYOffset").split(",")))
    # except Exception as e:
    # 	print(e)
    # 	config.blockXOffset = (0,0)
    # 	config.blockYOffset = (0,0)

    config.boxWidth = 200
    config.gradientLevel = 2

    reDraw()

    if run:
        runWork()
