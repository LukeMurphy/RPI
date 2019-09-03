# ################################################### #
import math
import random
import sys
import time

from PIL import Image

r=g=b=125
pulseSpeed = .01

# defaults
boxWidth = 74
boxHeight = 32

theta = 0
radius = 100
PI = math.pi
flashRate = 6
probabilityOfAlternateResolution = .25
probabilityOfAlternateResolutionHold = .5

global rectangles, overLap, overLapColor,overLapInit, solidOverLapColor

def clrAdjust(clr) :
		clrr = int(clr[0] * config.brightness)
		clrg = int(clr[1] * config.brightness)
		clrb = int(clr[2] * config.brightness)
		return (clrr,clrg,clrb)


def drawRects() :
		# Draw blocks of color on each panel
		# increace the lumens on each as if flashing lights - so 
		# increase is probably something like relates to a rate of
		# 2 Pi r or 

		global config
		global theta, radius, PI
		global colorSwitch
		global boxWidth,boxHeight

		rLevel = int((math.cos(theta) * 255))
		bLevel = int((math.sin(theta) * 255))
		clr = [(rLevel,0,0),(0,0,bLevel)]
		theta += PI/12
		if(theta >= 2*PI) : theta = 0

		for n in range(0,2) :
				xStart = n * boxWidth
				xEnd = xStart + boxWidth
				yStart = 0
				yEnd = boxHeight
				config.draw.rectangle((xStart, yStart, xEnd, yEnd ),  fill=clrAdjust(clr[n]) )

def moveRects() :
		# Move each rectangle to create a pseudo blend
		global config
		global theta, radius, PI, flashRate
		global colorSwitch, overLapInit, overLapInit, overLapColor, solidOverLapColor
		global boxWidth, boxHeight, rectangles, probabilityOfAlternateResolution

		rLevel = int((math.cos(theta) * 255))
		bLevel = int((math.sin(theta) * 255))
		clr = [(rLevel,0,0),(0,0,bLevel)]
		#clr = [(255,0,0),(0,0,255)]
		theta += PI/flashRate
		if(theta >= 2*PI) : theta = 0

		config.draw.rectangle((0, 0, config.screenWidth, config.screenHeight ),  fill=0 )

		for n in range(0,2) :
				xStart = rectangles[n][0]
				xEnd = xStart + rectangles[n][4]
				yStart = 0
				yEnd = boxHeight

				#use set colors
				fillColor = clrAdjust(rectangles[n][2])

				#use Flashing colors
				fillColor = clrAdjust(clr[n])

				config.draw.rectangle((xStart, yStart, xEnd, yEnd ),  fill=fillColor)

				### Movement ###
				rectangles[n][0] += rectangles[n][3]
				if ((rectangles[n][0] >= (config.screenWidth - rectangles[n][4]/2)) 
						or (rectangles[n][0] <= (0 - rectangles[n][4]/2))) : 
								rectangles[n][3] = rectangles[n][3] * -1


		a = max(rectangles[0][0], rectangles[1][0])
		b = 0
		c = min(rectangles[0][0] + rectangles[n][4], rectangles[1][0] + rectangles[n][4])
		d = boxHeight/1

		#print (a,c)

		if(a < c ) : 
				overLap = True

				if (overLapInit == True) :
						overLapInit = False
						if(random.random() > probabilityOfAlternateResolution) : 
								overLapColor = True
						else :
								overLapColor = False
								solidOverLapColor = clrAdjust(rectangles[2][2])
								solidOverLapColor = "VIOLET"
								clrToUse = config.colorWheel[int(random.uniform(0, len(config.colorWheel)))]
								solidOverLapColor = config.subtractiveColors(clrToUse)

				vlines = c - a
				hlines = d - b

				if(overLapColor):
						for n in range(0, hlines, 2) :
								# h lines
								#use set colors
								fillColor = clrAdjust(rectangles[0][2])

								#use Flashing colors
								fillColor = clrAdjust(clr[0])

								config.draw.line((a, b + n , c  , b + n), fillColor)
								config.draw.line((a  , b + n + 1 , c  , b + n + 1), fillColor)
						for n in range(-d, vlines, 2) :        
								# diagonal lines
								p1 = ( max( a, a + n ) , max (b, - n))
								p2 = ( min( a+n + d, c ),  min (d, c - (a + n) ) )
								config.draw.line((p1,p2), clrAdjust( rectangles[1][2] ))
				else :
						config.draw.rectangle((a, b, c , d ), fill=solidOverLapColor)

				# PAUSER
				if (vlines >= boxWidth-2) : 
						if(random.random() > probabilityOfAlternateResolutionHold and overLapColor==False) : 
								config.draw.rectangle((0, 0, config.screenWidth, config.screenHeight ),  fill=(0) )
								config.draw.rectangle((0, 0, config.screenWidth, config.screenHeight ),  fill=(0,0,255) )
				config.draw.rectangle((0, 0, config.screenWidth, config.screenHeight ),  fill=(0) )
				config.draw.rectangle((a, b, c , d ), fill=solidOverLapColor)
								config.render(config.image,0,0,config.screenWidth,config.screenHeight, False)
								time.sleep(random.uniform(1,4))
								# Flash of one color - red is most disturbing for some reason
								config.draw.rectangle((0, 0, config.screenWidth, config.screenHeight ),  fill=(255,0,0) )
		else :
				overLap = False
				overLapInit = True

def redraw():
		global config
		#drawRects()
		moveRects() 
		if(random.random() > .9) : config.brightness = random.random()
		config.render(config.image,0,0,config.screenWidth,config.screenHeight, False)

		
# adapted to show Soliloguy of The Point
def animator(arg) :
		global rHeight,rWidth, numSquares, colorSwitch, pulseSpeed, msg
		global columnLimit, rectangles , boxWidth, boxHeight, overLap, overLapColor, overLapInit, solidOverLapColor

		overLap =  False
		overLapInit = False
		overLapColor = False
		solidOverLapColor = "VIOLET"
		
	boxHeight = config.screenHeight

		# reseting render image size
		config.renderImage = Image.new("RGBA", (config.actualScreenWidth , 32))
		config.image = config.Image.new("RGBA", (config.screenWidth, config.screenHeight))
		config.draw  = config.ImageDraw.Draw(config.image)
		config.id = config.image.im.id
		#config.matrix.Clear()

		config.brightness = .165

		count = 0
		countLimit = arg * 160 + 1
		interval = 4

		i = 0

		rectangles = [  [0,0,(255,0,0),2, boxWidth+1],
						[config.screenWidth - boxWidth,0,(0,0,255),-2, boxWidth],
						[0,0,(255,0,255),0,0]
						]

		while (count < countLimit) :
				redraw()
				count += 1
				# ----  if arg = 0 assume endless ---
				if(arg == 0) : count = 0
				#i += 1
				time.sleep(pulseSpeed)

		config.matrix.Clear()
		config.matrix.Fill(0)
