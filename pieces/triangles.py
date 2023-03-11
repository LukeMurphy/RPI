import math
import random
import threading
import time
from modules.configuration import bcolors
from modules import colorutils
#!/usr/bin/env python3
"""
Minimal delaunay2D test
See: http://github.com/jmespadero/pyDelaunay2D
"""
import numpy as np
from libs.delaunay2D import Delaunay2D

from PIL import Image, ImageDraw, ImageEnhance, ImageFont, ImageOps


'''
				fadeIn = Fader()
				# fadeIn.blankImage = Image.new("RGBA", (height, width))
				fadeIn.crossFade = Image.new("RGBA", (height, width))
				fadeIn.image = gradientImage
				fadeIn.xPos = xPos
				fadeIn.yPos = yPos
				fadeIn.height = gradientImage.height
				fadeIn.width = gradientImage.width

				config.fadeArray.append(fadeIn)

'''


class Fader:
    def __init__(self):
        self.doingRefresh = 0
        self.doingRefreshCount = 50
        self.fadingDone = False

    def fadeIn(self, config):
        if self.fadingDone == False:
            if self.doingRefresh < self.doingRefreshCount:
                self.blankImage = Image.new("RGBA", (self.width, self.height))
                self.crossFade = Image.blend(
                    self.blankImage,
                    self.image,
                    self.doingRefresh / self.doingRefreshCount,
                )
                config.image.paste(
                    self.crossFade, (self.xPos, self.yPos), self.crossFade
                )
                self.doingRefresh += 1
            else:
                config.image.paste(
                    self.image, (self.xPos, self.yPos), self.image)
                self.fadingDone = True


class Bar:
    def __init__(self):
        self.remake()

    def remake(self):
        self.xSpeed = random.uniform(
            config.xSpeedRangeMin * config.direction, config.xSpeedRangeMax * config.direction)
        self.ySpeed = random.uniform(
            config.ySpeedRangeMin, config.ySpeedRangeMax)
        self.yPos = round(random.uniform(config.yRangeMin, config.yRangeMax))
        self.xPos = -config.barThicknessMax * 2
        if config.direction == -1:
            self.xPos = config.canvasWidth + config.barThicknessMax * 2
        self.barThickness = round(random.uniform(
            config.barThicknessMin, config.barThicknessMax))
        self.barLength = round(random.uniform(
            config.barLengthMin, config.barLengthMax))
        # self.colorVal = colorutils.randomColorAlpha()
        cset = config.colorSets[config.usingColorSet]

        colorAlpha = config.outlineColorAlpha

        self.colorVal = colorutils.getRandomColorHSV(
            cset[0], cset[1], cset[2], cset[3], cset[4], cset[5], config.dropHueMax, 0, colorAlpha, config.brightness)
        self.outlineColorVal = colorutils.getRandomColorHSV(
            cset[0], cset[1], cset[2], cset[3], cset[4], cset[5], config.dropHueMax, 0, config.outlineColorAlpha, config.brightness)
        self.outlineColorVal = self.colorVal


def transformImage(img):
    width, height = img.size
    new_width = 50
    m = 0.0
    img = img.transform(
        (new_width, height), Image.AFFINE, (1, m, 0, 0, 1, 0), Image.BICUBIC
    )
    return img


def drawBar():
    global config


def reDraw():
    global config


def runWork():
    global config
    print(bcolors.OKGREEN + "** " + bcolors.BOLD)
    print("Running moving_bars.py")
    print(bcolors.ENDC)

    # Create a random set of 2D points
    # seeds = np.random.random((12, 2))

    ###########################################################
    # Generate 'numSeeds' random seeds in a square of size 'radius'
    numSeeds = 12
    radius = 200
    seeds = radius * np.random.random((numSeeds, 2))
    print("seeds:\n", seeds)
    print("BBox Min:", np.amin(seeds, axis=0),
          "Bbox Max: ", np.amax(seeds, axis=0))

    """
	Compute our Delaunay triangulation of seeds.
	"""
    # It is recommended to build a frame taylored for our data
    # dt = D.Delaunay2D() # Default frame
    center = np.mean(seeds, axis=0)
    dt = Delaunay2D(center, 100 * radius)

    # Insert all seeds one by one
    for s in seeds:
        dt.addPoint(s)

    # Dump number of DT triangles
    print(len(dt.exportTriangles()), "Delaunay triangles")
    config.triangleSet = dt.exportVoronoiRegions()

    vc, vr = config.triangleSet

    print(vc)
    print("---------")
    print(vr)

    while config.isRunning == True:
        iterate()
        time.sleep(config.redrawRate)
        if config.standAlone == False:
            config.callBack()


def iterate():
    global config

    config.draw.rectangle((0, 0, 400, 400), fill=(0, 0, 0, 10))

    vc, vr = config.triangleSet

    for r in vr:
        polygon = [vc[i] for i in vr[r]]       # Build polygon for each region
        # plt.plot(*zip(*polygon), color="red")  # Plot polygon edges in red

        pnts = []
        for p in polygon:
            if p[0] > 320:
                p[0] = 320
            if p[0] < 0:
                p[0] = 0
            if p[1] > 320:
                p[1] = 320
            if p[1] < 0:
                p[1] = 0
            pnts.append((p[0], p[1]))

        # print(*zip(*polygon))
        if len(pnts) >= 2:
            config.draw.polygon(tuple(pnts), fill=(
                255, 0, 0), outline=(255, 255, 255))

    '''
	for i in range(0, config.numberOfBars):
		bar = config.barArray[i]
		bar.xPos += bar.xSpeed
		bar.yPos += bar.ySpeed

		w = round(math.sqrt(2) * config.barThicknessMax * 1.5)

		angle = 180/math.pi * math.tan(bar.ySpeed/abs(bar.xSpeed))

		temp = Image.new("RGBA", (w, w))
		drw = ImageDraw.Draw(temp)

		if config.tipType == 1 :
			drw.rectangle((0, 0, bar.barThickness, bar.barLength ), fill = bar.colorVal, outline = bar.outlineColorVal)
			drw.rectangle((0, 2, bar.barThickness, bar.barLength+2 ), fill = bar.colorVal, outline = bar.outlineColorVal)
		
		elif config.tipType == 0:
			drw.ellipse((0, 2, bar.barThickness, bar.barLength+2 ), fill = bar.colorVal, outline = bar.outlineColorVal)

		elif config.tipType == 2:
			drw.ellipse((0, 2, bar.barThickness, bar.barThickness), fill = bar.colorVal, outline = bar.outlineColorVal)
		temp = temp.rotate(config.tipAngle - angle)

		config.image.paste(temp,(round(bar.xPos), round(bar.yPos)), temp)

		if bar.xPos > config.canvasWidth + bar.barLength and config.direction == 1:
			bar.remake()
		if bar.xPos < 0 and config.direction == -1:
			bar.remake()


	if random.random() < .002 :
		if config.dropHueMax == 0 :
			config.dropHueMax = 255
		else :
			config.dropHueMax = 0
		#print("Winter... " + str(config.dropHueMax ))

	if random.random() < config.colorChangeProb:
		config.usingColorSet = math.floor(random.uniform(0,config.numberOfColorSets))
		# just in case ....
		if config.usingColorSet == config.numberOfColorSets : 
			config.usingColorSet = config.numberOfColorSets-1
		config.colorAlpha = round(random.uniform(config.leadEdgeAlpahMin,config.leadEdgeAlpahMax))
		config.dropHueMax = 0

		if random.random() < config.changeShapeProb  :
			config.tipType = config.tipTypeAlt
		else :
			config.tipType = config.tipTypeOrig

	'''

    config.render(config.image, 0, 0)


def main(run=True):
    global config
    global workConfig
    config.redrawRate = .02

    config.image = Image.new("RGBA", (config.screenWidth, config.screenHeight))
    config.draw = ImageDraw.Draw(config.image)
    config.canvasImage = Image.new(
        "RGBA", (config.canvasWidth, config.canvasHeight))
    config.canvasDraw = ImageDraw.Draw(config.canvasImage)

    config.xPos = 0
    config.dropHueMax = 0

    config.numberOfBars = int(workConfig.get("params", "numberOfBars"))
    config.barThicknessMin = int(workConfig.get("params", "barThicknessMin"))
    config.barThicknessMax = int(workConfig.get("params", "barThicknessMax"))

    config.barLengthMin = int(workConfig.get("params", "barLengthMin"))
    config.barLengthMax = int(workConfig.get("params", "barLengthMax"))

    config.direction = int(workConfig.get("params", "direction"))
    yRange = (workConfig.get("params", "yRange")).split(",")
    config.yRangeMin = int(yRange[0])
    config.yRangeMax = int(yRange[1])

    config.leadEdgeAlpahMin = int(workConfig.get("params", "leadEdgeAlpahMin"))
    config.leadEdgeAlpahMax = int(workConfig.get("params", "leadEdgeAlpahMax"))
    config.tipAngle = float(workConfig.get("params", "tipAngle"))

    config.xSpeedRangeMin = float(workConfig.get("params", "xSpeedRangeMin"))
    config.xSpeedRangeMax = float(workConfig.get("params", "xSpeedRangeMax"))
    config.ySpeedRangeMin = float(workConfig.get("params", "ySpeedRangeMin"))
    config.ySpeedRangeMax = float(workConfig.get("params", "ySpeedRangeMax"))

    try:
        config.colorChangeProb = float(
            workConfig.get("params", "colorChangeProb"))
    except Exception as e:
        print(str(e))
        config.colorChangeProb = .003

    try:
        config.changeShapeProb = float(
            workConfig.get("params", "changeShapeProb"))
    except Exception as e:
        print(str(e))
        config.changeShapeProb = .001

    try:
        config.tipType = int(workConfig.get("params", "tipType"))
        config.tipTypeOrig = int(workConfig.get("params", "tipType"))
        config.tipTypeAlt = int(workConfig.get("params", "tipTypeAlt"))
    except Exception as e:
        print(str(e))
        config.tipType = 1
        config.tipTypeAlt = 1
        config.tipTypeOrig = 1

    config.colorAlpha = round(random.uniform(
        config.leadEdgeAlpahMin, config.leadEdgeAlpahMax))
    config.outlineColorAlpha = round(random.uniform(
        config.leadEdgeAlpahMin, config.leadEdgeAlpahMax))
    yPos = 0
    config.barArray = []

    config.colorSets = []

    config.colorSetList = list(
        i for i in (workConfig.get("params", "colorSets").split(","))
    )

    config.numberOfColorSets = len(config.colorSetList)
    for setName in config.colorSetList:
        cset = list(
            float(i) for i in (workConfig.get("params", setName).split(","))
        )
        config.colorSets.append(cset)

    config.usingColorSet = math.floor(
        random.uniform(0, config.numberOfColorSets))
    if config.usingColorSet == config.numberOfColorSets:
        config.usingColorSet = config.numberOfColorSets - 1

    # initialize and place the first set
    for i in range(0, config.numberOfBars):
        bar = Bar()
        bar.yPos = round(random.uniform(config.yRangeMin, config.yRangeMax))
        bar.xPos = round(random.uniform(
            0, config.canvasWidth - config.barThicknessMax))
        config.barArray.append(bar)
        # yPos += bar.barThickness

    if run:
        runWork()
