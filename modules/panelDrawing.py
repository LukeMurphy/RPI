import math
import random
import time
from operator import sub

from modules import colorutils
from PIL import Image, ImageChops, ImageDraw, ImageEnhance, ImageFont, ImageOps

"""""" """""" """""" """""" """""" """""" """""" """""" """""" """"""



class PanelPathDrawing:
	def __init__(self, config):

		self.config = config
		self.canvas = Image.new("RGBA", (config.screenWidth, config.screenHeight))
		self.canvasDraw = ImageDraw.Draw(self.canvas)
		self.panelHeight = config.tileSizeHeight
		self.panelWidth = config.tileSizeWidth
		self.drawingPath = []
		self.canvasToUse = config.canvasImage
		

	def render(self) :

		self.canvasDraw.rectangle((0,0,self.config.screenWidth, self.config.screenHeight), fill = (0,0,0,255))
		row = 0
		col = 0
		rowBuffer = 0
		colBuffer = 0
		colOffset = 20
		rowOffset = 20
		prevX = 0
		prevY = 0


		for i in range(0, len(self.drawingPath)):

			x = col * self.panelWidth
			y = row * self.panelHeight

			w = round(x + self.panelWidth)
			h = round(y + self.panelHeight)
			section = self.canvasToUse.crop((x,y,w,h))

			if x >=self.config.canvasWidth - self.panelWidth :
				row += 1
				col = 0
			else :
				col += 1
			xPos = round(self.drawingPath[i][0])
			yPos = round(self.drawingPath[i][1])
			angle = self.drawingPath[i][2]
			section = section.rotate(angle, Image.NEAREST , 1)
			section = section.convert("RGBA")
			self.canvas.paste(section,(xPos + colOffset ,yPos + rowOffset ),section)

			prevX = xPos
			prevY = yPos

		self.finalRender()


	def finalRender(self):
		self.config.render(self.canvas, 0, 0)


def PathMaker(config) :
	return True