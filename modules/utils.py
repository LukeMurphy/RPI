import time
import random
import math
import sys
import messenger
import ImageChops, ImageOps

screenWidth =  128
screenHeight = 64

tileSize = (32,64)
rows = 2
cols = 1
imageRows = [] * rows
actualScreenWidth = tileSize[1]*cols*rows
path = "/home/pi/rpimain"
useMassager = False
brightness = 1

colorWheel = ["RED","VERMILLION","ORANGE","AMBER","YELLOW","CHARTREUSE","GREEN","TEAL","BLUE","VIOLET","PURPLE","MAGENTA"]
wheel = [(255,2,2),(253,83,8),(255,153,1),(250,188,2),(255,255,0),(0,125,0),(146,206,0),(0,255,255),(0,0,255),(65,0,165),(135,0,175),(167,25,75)]

rgbColorWheel = ["RED","GREEN","BLUE","YELLOW","MAGENTA","CYAN"]
rgbWheel = [(255,0,0),(0,255,0),(0,0,255),(255,255,0),(255,0,255),(0,255,255)]

global imageTop,imageBottom,image,config,transWiring

transWiring = True

def getRandomRGB(brtns=1) :
	global brightness, rgbColorWheel, rgbWheel
	if(brtns == 1) : brtns = brightness
	indx = int(random.uniform(0,len(rgbWheel)))
	clr = rgbWheel[indx]
	r = int(clr[0] * brtns)
	g = int(clr[1] * brtns)
	b = int(clr[2] * brtns)
	return (r,g,b)

def getRandomColorWheel(brtns=1) :
	global brightness, colorWheel, wheel
	if(brtns == 1) : brtns = brightness
	indx = int(random.uniform(0,len(colorWheel)))
	clr = wheel[indx]
	r = int(clr[0] * brtns)
	g = int(clr[1] * brtns)
	b = int(clr[2] * brtns)
	return (r,g,b) 

def randomColor(brtns=1) :
	global brightness
	if(brtns == 1) : brtns = brightness
	r = int((random.uniform(0,255)) * brtns)
	g = int((random.uniform(0,255)) * brtns)
	b = int((random.uniform(0,255)) * brtns)
	return (r,g,b) 

def colorCompliment((r,g,b), brtns=1) :
	global brightness
	if(brtns == 1) : brtns = brightness
	minRGB = min(r,min(g,b))
	maxRGB = max(r,max(g,b))
	minmax = minRGB + maxRGB
	r = int((minmax - r) * brtns)
	g = int((minmax - g) * brtns)
	b = int((minmax - b) * brtns)
	return (r,g,b)     

# Find the closest point 
def closestRBYfromRGB((r,g,b)) :
	global brightness, wheel
	# d = sqrt( x2-x1 ^ 2 ....)
	dMax = 0
	dArray = []
	for n in range (0, len(wheel)) :
		d = int(math.sqrt( (r-wheel[n][0])**2 + (g-wheel[n][1])**2 + (b-wheel[n][2])**2 ))
		dArray.append([n,d])
	dArray = sorted(dArray, key=lambda n:n[1], reverse=False)
	return wheel[dArray[0][0]]


def subtractiveColors(arg) :
	color = (0,0,0)
	if(arg == "RED") : color = tuple(int(a*brightness) for a in ((255,2,2)))
	if(arg == "VERMILLION") : color = tuple(int(a*brightness) for a in ((253,83,8)))
	if(arg == "ORANGE") : color = tuple(int(a*brightness) for a in ((255,153,1)))
	if(arg == "AMBER") : color = tuple(int(a*brightness) for a in ((250,188,2)))
	if(arg == "YELLOW") : color = tuple(int(a*brightness) for a in ((255,255,0)))
	if(arg == "CHARTREUSE") : color = tuple(int(a*brightness) for a in ((0,255,0)))
	if(arg == "GREEN") : color = tuple(int(a*brightness) for a in ((0,125,0)))
	if(arg == "TEAL") : color = tuple(int(a*brightness) for a in ((146,206,0)))
	if(arg == "BLUE") : color = tuple(int(a*brightness) for a in ((0,0,255)))
	if(arg == "VIOLET") : color = tuple(int(a*brightness) for a in ((65,0,165)))    
	if(arg == "PURPLE") : color = tuple(int(a*brightness) for a in ((135,0,175)))    
	if(arg == "MAGENTA") : color = tuple(int(a*brightness) for a in ((167,25,75)))    
	return color
	
def colorComplimentRBY(arg) :
	global colorWheel
	l = len(colorWheel) / 2
	indx = colorWheel.index(arg)
	oppIndx  =  indx + l 
	if(oppIndx > 11) : oppIndx -= (l*2)
	return subtractiveColors(colorWheel[oppIndx])

def changeColor(rnd = False) :
	global brightness           
	if (rnd == False) :
					if(r == 255) :
									r = 0
									g = 255
									b = 0
					else :
									g = 0
									r = 255
									b = 0
	else :
					r = int(random.uniform(0,255) * brightness)
					g = int(random.uniform(0,255) * brightness)
					b = int(random.uniform(0,255) * brightness)

def soliloquy(override = False,arg = "") :
	global useMassager
	if (useMassager) : messenger.soliloquy(override,arg)

def render(imageToRender,xOffset,yOffset,w=128,h=64,nocrop=False, overlayBottom=False):

	global imageTop, imageBottom, screenHeight, screenWidth, panels, matrix, image, renderImage, tileSize, rows, cols, transWiring

	#w = screenWidth
	#h = screenHeight

	segmentImage = []

	# the rendered image is the screen size
	#renderImage = Image.new("RGBA", (screenWidth , 32))

	if(nocrop == True) :
		for n in range(0,rows) :
			segmentWidth = tileSize[1] * cols
			segmentHeight = 32
			xPos = n * segmentWidth - xOffset
			yPos = n * 32 #- yOffset
			segment =  imageToRender.crop((0, yPos, segmentWidth, segmentHeight + yPos))
			renderImage.paste(segment, (xPos,0,segmentWidth + xPos,segmentHeight))

	elif (nocrop == False) :
		segmentWidth = tileSize[1] * cols
		segmentHeight = 32

		#yOffset = 10
		#xOffset = 100
		# Must crop exactly the overlap and position of the to-be-rendered image with each segment
		#           ________________
		#           |               |
		#           |               |
		#           |    |||||||||  |
		#           -----|||||||||---
		#           |    |||||||||  |
		#           |    |||||||||  |

		
		cropP1 = [0,0]
		cropP2 = [0,0]

		for n in range(0,rows) :

			# Crop PLACEMENTS\
			a = max(0, xOffset) + segmentWidth * n
			b = max(0, yOffset - segmentHeight * n)
			c = min(segmentWidth, xOffset + w) + segmentWidth * n
			d = min(segmentHeight, yOffset + h - segmentHeight * n)

			# Cropping
			cropP2 = [  cropP1[0] + c - xOffset, 
						cropP1[1] + min(32, d - yOffset + n * segmentHeight)]

			cropP1 = [max(0 , 0 - xOffset),     max(0, n * segmentHeight - yOffset)]
			cropP2 = [min(w , segmentWidth - xOffset),   min(h, n * segmentHeight + 32 - yOffset)]

			pCrop  = cropP1 + cropP2

			if ((n==0 or n == 2 or n == 4) and (transWiring == False) ) : pCrop[1] = 0
			segmentImage.append(imageToRender.crop(pCrop))

			#print(a,b,c,d,cropP1,cropP2)


			# Depending on the cabling, either copy segment laterally - which I think
			# is faster, or transform the segment each time to flip and mirror because
			# the panels are upside down wrt the ones below them
			# Wiring from BACK  **** = ribbon jumper cables
			#           ________________
			#           |               |
			#           |        <--  * |
			#           |           | * |
			#           --------------*--
			#           |             * |
			#           |        ^    * |
			#           |        |-->   |
			#           ________________

			#           ________________
			#           |        ^      |
			#           | *      |-->   |
			#           |    *          |
			#           --------*--------
			#           |          *    |
			#           |        ^    * |
			#           |        |-->   |
			#           ________________


			# Only render if needs be
			if(pCrop[3] - pCrop[1] > 0 ) : 
				if ( pCrop[2] - pCrop[0] > 0) :
					segImg = segmentImage[n]
					if ((n==0 or n == 2 or n == 4) and (transWiring == False) ) : 
						# This flips, reveses and places the segment when the row is "upside down" wrt
						# the previous row of panels - this is when transWiring == False - i.e no long transverse cable
						segImg = ImageOps.flip(segImg)
						segImg = ImageOps.mirror(segImg)

						an = segmentWidth - xOffset - w
						if(an < 0) : an = 0

						bn = segmentHeight - yOffset - h
						if(bn < 0) : bn = 0

						renderImage.paste( segImg, (an, bn, an + pCrop[2] - pCrop[0], bn + pCrop[3] - pCrop[1]))
					else:
						renderImage.paste( segImg, (a, b, a + pCrop[2] - pCrop[0], b + pCrop[3] - pCrop[1]))

	 
			cropP1[1] = cropP2[1]


	if(overlayBottom) :
		renderImage = Image.new("RGBA", (w , h))
		renderImage.paste(imageToRender, (0,0))
		iid = renderImage.im.id
		idtemp = image.im.id
		matrix.SetImage(iid, xOffset + screenWidth, 0)
	else :
		iid = renderImage.im.id
		idtemp = image.im.id
		matrix.SetImage(iid, 0, 0)


	# DEBUG .....
	#time.sleep(10)
	#exit()
	# ************************************ #

	#print(">>")
	#if(random.random() > .95) : soliloquy()

