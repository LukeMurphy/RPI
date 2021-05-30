import math
import random
import time
from operator import sub

from modules import colorutils
from PIL import Image, ImageChops, ImageDraw, ImageEnhance, ImageFont, ImageOps

"""""" """""" """""" """""" """""" """""" """""" """""" """""" """"""

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


class PanelPathDrawing:
	def __init__(self, config):

		self.config = config
		self.canvas = Image.new("RGBA", (config.screenWidth, config.screenHeight))
		self.canvasDraw = ImageDraw.Draw(self.canvas)
		self.panelHeight = config.tileSizeHeight
		self.panelWidth = config.tileSizeWidth
		self.drawingPath = []
		self.canvasToUse = config.canvasImage
		self.drawMarkers = True

		self.a = 100
		self.b = 120
		self.panels = 14
		self.xOffset = 0
		self.yOffset = 0 
		self.orientation = 0
		self.fillColor = (0,0,0,255)

	def generateSpiral(self):

		self.drawingPath = []
		angle = 2 * math.pi/self.panels

		orientationAngle = 90
		if self.orientation == 1 :
			orientationAngle = 0

		self.a = self.b = self.panelWidth

		for i in range(0,self.panels) :
			theta = i * angle
			a1 = self.a * math.sin(theta)
			b1 = self.b * math.cos(theta)
			r = self.a * self.b / math.sqrt(a1*a1 + b1*b1)
			x = r * math.cos(theta) + self.xOffset
			y = r * math.sin(theta) + self.yOffset
			rTheta = 180 - theta * 180 / math.pi + orientationAngle + (random.uniform(-5,5))
			self.drawingPath.append((round(x), round(y), round(rTheta)))
			self.a += 10
			self.b += 10

	def generateOval(self):

		self.drawingPath = []
		angle = 2 * math.pi/self.panels

		orientationAngle = 90
		if self.orientation == 1 :
			orientationAngle = 0

		for i in range(0,self.panels) :
			theta = i * angle
			a1 = self.a * math.sin(theta)
			b1 = self.b * math.cos(theta)
			r = self.a * self.b / math.sqrt(a1*a1 + b1*b1)
			x = r * math.cos(theta) + self.xOffset
			y = r * math.sin(theta) + self.yOffset
			rTheta = 180 - theta * 180 / math.pi + orientationAngle + (random.uniform(-5,5))
			self.drawingPath.append((round(x), round(y), round(rTheta)))



	def render(self) :

		self.canvasDraw.rectangle((0,0,self.config.screenWidth, self.config.screenHeight), fill = self.fillColor)
		row = 0
		col = 0
		rowBuffer = 0
		colBuffer = 0
		colOffset = 0
		rowOffset = 0
		prevX = 0
		prevY = 0


		for i in range(0, len(self.drawingPath)):

			x = col * self.panelWidth
			y = row * self.panelHeight

			w = round(x + self.panelWidth)
			h = round(y + self.panelHeight)
			section = self.canvasToUse.crop((x,y,w,h))

			section = section.convert("RGBA")
			sectionImage = Image.new("RGBA", (self.panelWidth+4, self.panelHeight+4), (0,0,0,255))
			sectionImage.paste(section,(2,2),section)


			sectionDraw = ImageDraw.Draw(sectionImage)
			#sectionDraw.rectangle((0,0,w+1,h+1), outline=(255,0,0,255))
			#sectionDraw.rectangle((-1,-1,w+2,h+2), outline=(255,0,0,255))

			if x >=self.config.canvasWidth - self.panelWidth :
				row += 1
				col = 0
			else :
				col += 1
			xPos = round(self.drawingPath[i][0])
			yPos = round(self.drawingPath[i][1])
			angle = self.drawingPath[i][2]
			# seem to need to convert to RGBA before doing rotation
			sectionImage = sectionImage.rotate(angle, Image.NEAREST , 1)
			sectionSize = sectionImage.size
			self.canvas.paste(sectionImage,(xPos + colOffset - round(sectionSize[0]/2),yPos + rowOffset - round(sectionSize[1]/2) ),sectionImage)
			if self.drawMarkers ==True: 
				self.canvasDraw.rectangle((xPos,yPos,xPos+2,yPos+2), fill=(0,255,255))

			prevX = xPos
			prevY = yPos

		self.finalRender()


	def finalRender(self):
		self.config.render(self.canvas, 0, 0)


def mockupBlock(config, workConfig) :
	### THIS IS USED AS WAY TO MOCKUP A CONFIGURATION OF RECTANGULAR PANELS
	try:
		config.useDrawingPoints = workConfig.getboolean("mockup", "useDrawingPoints")
		xOffset = int(workConfig.get("mockup", "xOffset"))
		yOffset = int(workConfig.get("mockup", "yOffset"))
		a = int(workConfig.get("mockup", "a"))
		b = int(workConfig.get("mockup", "b"))
		orientation = int(workConfig.get("mockup", "orientation"))
		panels = int(workConfig.get("mockup", "panels"))
		programmedPath = (workConfig.get("mockup", "programmedPath"))
		drawMarkers = workConfig.getboolean("mockup", "drawMarkers")

		try:
			bgColorVals = workConfig.get("mockup", "bgColor").split(",")
			fillColor = tuple(int(a) for a in bgColorVals)
		except Exception as e:
			print(str(e))

		config.panelDrawing = PanelPathDrawing(config)
		config.panelDrawing.canvasToUse = config.image
		config.panelDrawing.xOffset = xOffset
		config.panelDrawing.yOffset = yOffset
		config.panelDrawing.a = a
		config.panelDrawing.b = b
		config.panelDrawing.orientation = orientation
		config.panelDrawing.panels = panels
		config.panelDrawing.drawMarkers = drawMarkers
		config.panelDrawing.fillColor = fillColor


		if programmedPath == "ellipse" :
			config.panelDrawing.generateOval()
		elif programmedPath == "spiral" :
			config.panelDrawing.generateSpiral()
		else:
			drawingPathPoints = workConfig.get("mockup", "drawingPathPoints").split("|")
			config.panelDrawing.drawingPath = []

			for i in range(0, len(drawingPathPoints)) :
				p = drawingPathPoints[i].split(",")
				config.panelDrawing.drawingPath.append((int(p[0]) + xOffset, int(p[1]) + yOffset, int(p[2])))
	except Exception as e:
		print(str(e))
		config.useDrawingPoints = False




