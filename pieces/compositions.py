import time
import random
import textwrap
import math
from PIL import ImageFont, Image, ImageDraw, ImageOps, ImageEnhance, ImageChops
from modules import colorutils, badpixels, coloroverlay




def ScaleRotateTranslate(image, angle, center = None, new_center = None, scale = None,expand=False):
	if center is None:
		return image.rotate(angle)
	angle = -angle/180.0*math.pi
	nx,ny = x,y = center
	sx=sy=1.0
	if new_center:
		(nx,ny) = new_center
	if scale:
		(sx,sy) = scale
	cosine = math.cos(angle)
	sine = math.sin(angle)
	a = cosine/sx
	b = sine/sx
	c = x-nx*a-ny*b
	d = -sine/sy
	e = cosine/sy
	f = y-nx*d-ny*e
	return image.transform(image.size, Image.AFFINE, (a,b,c,d,e,f), resample=Image.BICUBIC)

def drawCompositions():


	startx = config.imageWidth/9
	wVariance = [config.imageWidth/6, config.imageWidth/3]
	hVariance = [config.imageHeight/6, config.imageHeight/2]
	wFactor = 1
	hFactor = 2
	starty = 0

	# Choose seam x point  -- ideally about 1/3 from left
	xVariance = 100
	config.flip = False

	xSeam = int(random.uniform(config.imageWidth * 2/3 - xVariance, config.imageWidth * 2/3 + xVariance))
	tiedToBottom = 0 if random.random() < .5 else 2

	angleRotation = random.uniform(-3,3)

	for n in range(0, config.numSquarePairs):
		gray0 = int(random.uniform(0,160))
		gray1 = int(random.uniform(0,160))
		gray2 = int(random.uniform(0,160))
		fills = [
			(gray0,gray1,gray1,255),
			(gray1,gray1,gray1,255),
			(gray2,gray2,gray2,255)]

		if random.random() < .5 :
			fills[0] = (gray0,gray0,gray1,255)

		if (n == 2):
			wFactor *= 1.5

		if (n == 0) : 
			x1 = int(xSeam)
			x2 = int(random.uniform(x1 + startx, x1 + wVariance[1]))
			y1 = int(random.uniform(hVariance[0], hVariance[1]))
			y2 = int(random.uniform(y1 + hVariance[0]*hFactor, y1 + hVariance[1]*hFactor))
			if (n == tiedToBottom) : y2 = config.imageHeight
			starty = int(random.uniform(0,config.imageHeight/2))


		else :
			x1 = int(random.uniform(xSeam - startx * wFactor, xSeam - wVariance[1]* wFactor) ) 
			x2 = int(xSeam)
			y1 = starty
			y2 = int(random.uniform(y1 + hVariance[0], y1 + hVariance[1]))
			if (n == tiedToBottom) : y2 = config.imageHeight
			starty = y2

			if random.random() < config.filterPatchProb :
				choice = round(random.uniform(1,2))
				if n == choice :
					config.remapImageBlock = True
					config.remapImageBlockSection = (x1,y1,x2,y2)
					config.remapImageBlockDestination = (x1,y1)

		rectHeight = y2 - y1
		

		temp = Image.new("RGBA", (config.imageWidth, config.imageHeight))
		drawtemp = ImageDraw.Draw(temp)
		drawtemp.rectangle((x1,y1,x2,y2), fill=fills[n])
		temp = ScaleRotateTranslate(temp,angleRotation, None, None, None, True)
		config.canvasImage.paste(temp, temp)



	#config.canvasImage.paste(temp, temp)
	
	if(config.flip == True) :
		config.canvasImage = config.canvasImage.transpose(Image.FLIP_TOP_BOTTOM)
		config.canvasImage = config.canvasImage.transpose(Image.ROTATE_180)



''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

def main(run = True) :
	global config,workConfig
	print("---------------------")

	config.delay = float(workConfig.get("compositions", 'delay')) 
	config.canvasImageWidth = int(workConfig.get("compositions", 'canvasImageWidth')) 
	config.canvasImageHeight = int(workConfig.get("compositions", 'canvasImageHeight')) 
	config.refreshCount = int(workConfig.get("compositions", 'refreshCount')) 
	config.timeToComplete = float(workConfig.get("compositions", 'timeToComplete')) 
	config.cleanSlateProbability = float(workConfig.get("compositions", 'cleanSlateProbability')) 
	config.filterPatchProb = float(workConfig.get("compositions", 'filterPatchProb')) 

	config.imageWidth = config.canvasImageWidth
	config.imageHeight = config.canvasImageHeight


	print("Running")

	config.bgColor =  tuple(int(i) for i in (workConfig.get("compositions", 'bgColor').split(',')))

	config.numSquarePairs = 3

	config.t1  = time.time()
	config.t2  = time.time()

	# initial crossfade settings
	config.doingRefresh = config.refreshCount
	config.doingRefreshCount = config.refreshCount


	config.canvasImage = Image.new("RGBA", (config.canvasImageWidth  , config.canvasImageHeight))
	config.draw = ImageDraw.Draw(config.canvasImage)
	config.draw.rectangle((0,0,config.imageWidth, config.imageHeight), fill=config.bgColor)

	drawCompositions()

	setUp()

	if(run) : runWork()


''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''


def restartDrawing() :

	config.flip = True if random.random() < .5 else False
	if random.random() < config.cleanSlateProbability :
		grayLevel = round(random.uniform(20,70))
		config.bgColor = (grayLevel,grayLevel,grayLevel)

		config.bgColor = colorutils.getRandomColorHSV(0,360, .0,.15, .1,.4)

		config.draw.rectangle((0,0,config.imageWidth,config.imageHeight), fill=config.bgColor)
	drawCompositions()

	config.t1  = time.time()
	config.t2  = time.time()
	# initialize crossfade - in this case 100 steps ...
	config.doingRefresh = 0
	config.doingRefreshCount = config.refreshCount

def setUp():
	global config
	pass



''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

def runWork():
	global blocks, config, XOs
	#gc.enable()
	while True:
		iterate()
		time.sleep(config.delay)  

''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

def iterate() :
	global config

	config.t2  = time.time()
	delta = config.t2  - config.t1

	if delta > config.timeToComplete :
		config.snapShot = config.canvasImage.copy()
		restartDrawing()

	# Need to do a crossfade 
	if config.doingRefresh < config.doingRefreshCount :			
		crossFade = Image.blend(config.snapShot, config.canvasImage, config.doingRefresh/config.doingRefreshCount)
		config.render(crossFade, 0,0)
		config.doingRefresh += 1
	else :
		temp = Image.new("RGBA", (config.canvasImageWidth, config.canvasImageHeight))
		temp.paste(config.canvasImage, (0,0), config.canvasImage)
		config.render(temp, 0,0)
	#config.render(config.canvasImage, 0,0)
		

''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

def callBack() :
	global config, XOs
	return True

''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
