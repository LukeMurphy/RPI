import random
import threading
import time
import tkinter as tk
from PIL import (
	Image,
	ImageChops,
	ImageDraw,
	ImageEnhance,
	ImageFilter,
	ImageFont,
	ImageTk,
)

from modules.configuration import Config, bcolors
from modules.filters import *

# from Tkinter import *
# import tkMessageBox
# import PIL.Image
# import PIL.ImageTk
# import gc, os


class CanvasElement:
	def __init__(self, root, config):
		print(">> CanvasElement Initialized ** ")
		self.root = root
		self.config = config
		self.buff = 8
		self.counter = 0
		self.threadsList = []

	def setUp(self):
		self.config.renderImage = PIL.Image.new(
			"RGBA", (self.config.screenWidth * self.config.rows, 32)
		)
		self.config.renderImageFull = PIL.Image.new(
			"RGBA", (self.config.screenWidth, self.config.screenHeight)
		)
		self.config.image = PIL.Image.new(
			"RGBA", (self.config.screenWidth, self.config.screenHeight)
		)
		self.config.draw = ImageDraw.Draw(self.config.image)
		self.config.renderDraw = ImageDraw.Draw(self.config.renderImageFull)
		self.config.canvasOffsetX = 0
		self.config.canvasOffsetY = 0
		print(
			bcolors.FAIL
			+ ">> CanvasElement setting up renderImageFull: "
			+ str(self.config.renderImageFull)
			+ bcolors.ENDC
		)

	def setUpCanvas(self, root):
		print(">> CanvasElement setting up canvas ** ")
		self.config.torqueAngle = 0
		self.cnvs = tk.Canvas(
			root,
			width=self.config.screenWidth + self.buff,
			height=self.config.screenHeight + self.buff,
			border=0,
			name="main1",
		)
		# self.config.cnvs = self.cnvs
		self.cnvs.create_rectangle(
			0,
			0,
			self.config.screenWidth + self.buff,
			self.config.screenHeight + self.buff,
			fill="black",
		)
		self.cnvs.pack()
		self.cnvs.place(
			bordermode="outside",
			width=self.config.screenWidth + self.buff,
			height=self.config.screenHeight + self.buff,
			x=self.canvasXPosition,
		)

	def startWork(self):

		### Putting the animation on its own thread
		### Still throws and error when manually closed though...

		print(
			">>>>>>>>>>>>Starting" + str(self) + str(self.instanceNumber),
			"Cnvs --->",
			self.cnvs,
		)

		try:
			# self.masterConfig.t = threading.Thread.__init__(self.work.runWork())
			self.t = threading.Thread(target=self.work.runWork)
			self.t.start()

			# self.t.join()
			# self.threadsList.append(t)
		except tk.TclError as details:
			print(details)
			pass
			exit()

	def on_closing(self):
		return True

	"""""" """""" """""" """""" """""" """""" """""" """""" """""" """""" ""

	def renderCall(
		self,
		imageToRender,
		xOffset,
		yOffset,
		w=128,
		h=64,
		nocrop=False,
		overlayBottom=False,
		updateCanvasCall=True,
	):
		# print("Instance Number Render: " + str(self.config.instanceNumber), self.cnvs)
		pass

	def render(
		self,
		imageToRender,
		xOffset,
		yOffset,
		w=128,
		h=64,
		nocrop=False,
		overlayBottom=False,
		updateCanvasCall=True,
	):

		# Render to canvas
		# This needs to be optomized !!!!!!

		# print(imageToRender, self.cnvs)
		# print("Instance Number Render: " + str(self.config.instanceNumber))

		self.imageToRender = imageToRender

		xOffset = 0

		if self.config.rotation != 0:
			if self.config.fullRotation == True:
				# This rotates the image that is painted i.e. after pasting-in the image sent
				self.config.renderImageFull = self.config.renderImageFull.rotate(
					-self.config.rotation, expand=False
				)
			else:
				# This rotates the image sent to be rendered
				self.imageToRender = self.imageToRender.rotate(
					-self.config.rotation, expand=True
				)
				# imageToRender = ImageChops.offset(imageToRender, -40, 40)

		try:
			self.config.renderImageFull.paste(
				self.imageToRender, (xOffset, yOffset), self.imageToRender
			)

		except:
			self.config.renderImageFull.paste(self.imageToRender, (xOffset, yOffset))

		# config.drawBeforeConversion()

		self.config.renderImageFull = self.config.renderImageFull.convert("RGB")
		self.config.renderDraw = ImageDraw.Draw(self.config.renderImageFull)

		# config.renderImageFull = ImageChops.offset(config.renderImageFull, 40, 40)

		# For planes, only this works - has to do with transparency of repeated pasting of
		# PNG's I think
		# newimage = Image.new('RGBA', config.renderImageFull.size)
		# newimage.paste(config.renderImageFull, (0, 0))
		# config.renderImageFull =  newimage.convert("RGB")

		# enhancer = ImageEnhance.Brightness(config.renderImageFull)
		# config.renderImageFull = enhancer.enhance(.75)

		"""
		"""
		if self.config.useFilters == True:

			if self.config.filterRemap == True:
				self.config.tempImage = self.config.renderImageFull.copy()
				self.config.tempImage = ditherFilter(
					self.config.tempImage, xOffset, yOffset, self.config
				)
				crop = self.config.tempImage.crop(self.config.remapImageBlockSection)
				crop = crop.convert("RGBA")
				self.config.renderImageFull.paste(
					crop, self.config.remapImageBlockDestination, crop
				)
			else:
				self.config.renderImageFull = ditherFilter(
					self.config.renderImageFull, xOffset, yOffset, self.config
				)

		if (
			self.config.usePixelSort == True
			and self.config.pixelSortRotatesWithImage == True
		):
			if random.random() < self.config.pixelSortAppearanceProb:
				self.config.renderImageFull = pixelSort(
					self.config.renderImageFull, self.config
				)

		"""
		if self.config.rotation != 0  : 
			if(self.config.rotationTrailing or self.config.fullRotation) : 
				# This rotates the image that is painted back to where it was
				# basically same thing as rotating the image to be pasted in
				# except in some cases, more trailing is created
				self.config.renderImageFull = self.config.renderImageFull.rotate(self.config.rotation)
		"""

		# ---- Pixel Sort Type Effect ---- #
		if self.config.usePixelSort and self.config.pixelSortRotatesWithImage == False:
			if random.random() < self.config.pixelSortAppearanceProb:
				self.config.renderImageFull = pixelSort(
					self.config.renderImageFull, self.config
				)

				# crop = config.renderImageFull.crop()
				# crop = crop.convert("RGBA")
				# crop =  pixelSort(crop, config)
				# config.renderImageFull = config.renderImageFull.convert("RGBA")
				# config.renderImageFull.paste(crop)

		# ---- Remap sections of image to accommodate odd panels ---- #
		if self.config.remapImageBlock == True:
			crop = self.config.renderImageFull.crop(self.config.remapImageBlockSection)
			if self.config.remapImageBlockSectionRotation != 0:
				crop = crop.convert("RGBA")
				crop = crop.rotate(self.config.remapImageBlockSectionRotation)
			crop = crop.convert("RGBA")
			self.config.renderImageFull.paste(
				crop, self.config.remapImageBlockDestination, crop
			)

		if self.config.remapImageBlock2 == True:
			crop = self.config.renderImageFull.crop(self.config.remapImageBlockSection2)
			if self.config.remapImageBlockSection2Rotation != 0:
				crop = crop.convert("RGBA")
				crop = crop.rotate(self.config.remapImageBlockSection2Rotation)
			crop = crop.convert("RGBA")
			self.config.renderImageFull.paste(
				crop, self.config.remapImageBlockDestination2, crop
			)

		if self.config.remapImageBlock3 == True:
			crop = config.renderImageFull.crop(self.config.remapImageBlockSection3)
			if self.config.remapImageBlockSection3Rotation != 0:
				crop = crop.convert("RGBA")
				crop = crop.rotate(self.config.remapImageBlockSection3Rotation)
			crop = crop.convert("RGBA")
			self.config.renderImageFull.paste(
				crop, self.config.remapImageBlockDestination3, crop
			)

		if self.config.remapImageBlock4 == True:
			crop = self.config.renderImageFull.crop(self.config.remapImageBlockSection4)
			if self.config.remapImageBlockSection4Rotation != 0:
				crop = crop.convert("RGBA")
				crop = crop.rotate(self.config.remapImageBlockSection4Rotation)
			crop = crop.convert("RGBA")
			self.config.renderImageFull.paste(
				crop, self.config.remapImageBlockDestination4, crop
			)

		if self.config.remapImageBlock5 == True:
			crop = self.config.renderImageFull.crop(self.config.remapImageBlockSection5)
			if self.config.remapImageBlockSection5Rotation != 0:
				crop = crop.convert("RGBA")
				crop = crop.rotate(self.config.remapImageBlockSection5Rotation)
			crop = crop.convert("RGBA")
			self.config.renderImageFull.paste(
				crop, self.config.remapImageBlockDestination5, crop
			)

		if self.config.remapImageBlock6 == True:
			crop = self.config.renderImageFull.crop(self.config.remapImageBlockSection6)
			if self.config.remapImageBlockSection6Rotation != 0:
				crop = crop.convert("RGBA")
				crop = crop.rotate(self.config.remapImageBlockSection6Rotation)
			crop = crop.convert("RGBA")
			self.config.renderImageFull.paste(
				crop, self.config.remapImageBlockDestination6, crop
			)

		if self.config.useLastOverlay == True:
			self.config.renderDrawOver.rectangle(
				self.config.lastOverlayBox,
				fill=self.config.lastOverlayFill,
				outline=None,
			)
			self.config.renderImageFull.paste(
				self.config.renderImageFullOverlay,
				(0, 0),
				self.config.renderImageFullOverlay,
			)



	"""""" """""" """""" """""" """""" """""" """""" """""" """""" """""" ""
	# This is kind of screwy as it's only used by the main window .....
	def updateTheCanvas(self, players):


		xOff = 0
		self.config.renderImageFull = self.config.renderImageFull.convert("RGBA")
		for work in players:
			temp = work.config.renderImageFull.copy()
			temp = temp.convert("RGBA")
			temp2 = temp.copy()
			if work.config.canvasRotation != 0:
				temp2 = temp.rotate(-work.config.canvasRotation, expand=True)

			"""
			if work.config.useFilters == True:

				if work.config.filterRemap == True:
					work.config.tempImage = work.config.renderImageFull.copy()
					work.config.tempImage = ditherFilter(
						work.config.tempImage, 0, 0, work.config.tempImage
					)
					crop = work.config.tempImage.crop(
						work.config.remapImageBlockSection
					)
					crop = crop.convert("RGBA")
					work.config.renderImageFull.paste(
						crop, work.config.remapImageBlockDestination, crop
					)
				else:
					work.config.renderImageFull = ditherFilter(
						work.config.renderImageFull, 0, 0, work.config
					)
			"""

			if (
				work.config.usePixelSort == True
				and work.config.pixelSortRotatesWithImage == True
			):
				if random.random() < work.config.pixelSortAppearanceProb:
					work.config.renderImageFull = pixelSort(
						work.config.renderImageFull, work.config
					)

			# ---- Pixel Sort Type Effect ---- #
			if (
				work.config.usePixelSort
				and work.config.pixelSortRotatesWithImage == False
			):
				if random.random() < work.config.pixelSortAppearanceProb:
					work.config.renderImageFull = pixelSort(
						work.config.renderImageFull, work.config
					)

			'''
			if work.config.useBlur == True:
				temp = work.config.renderImageFull.copy()
				temp3 = temp.filter(
					ImageFilter.GaussianBlur(radius=work.config.sectionBlurRadius)
				)
				temp3 = temp3.convert("RGBA")
				crop = temp3.crop(work.config.blurSection)
				crop = crop.rotate(-work.config.canvasRotation, expand=True)
				destination = (work.config.blurXOffset, work.config.blurYOffset)
				self.config.renderImageFull.paste(
					temp2, (work.config.canvasOffsetX, work.config.canvasOffsetY), temp2
				)
				self.config.renderImageFull.paste(
					crop,
					(
						work.config.canvasOffsetX + work.config.blurXOffset,
						work.config.canvasOffsetY + work.config.blurYOffset,
					),
					crop,
				)
			else:
				self.config.renderImageFull.paste(
					temp2, (work.config.canvasOffsetX, work.config.canvasOffsetY), temp2
				)
			'''

			self.config.renderImageFull.paste(
				temp2, (work.config.canvasOffsetX, work.config.canvasOffsetY), temp2)

		
		if self.config.useFilters == True :
			pass
			#tempx = ditherFilter(self.config.renderImageFull, 0, 0, self.config)
			#tempx = tempx.convert("RGBA")
			#self.config.renderImageFull.paste(tempx, (0,0), tempx)

					# ---- Overall image blurring  ---- #
		if self.config.useBlur == True:
			"""
			config.renderImageFull = config.renderImageFull.filter(ImageFilter.GaussianBlur(radius=config.sectionBlurRadius))
			"""
			crop = self.config.renderImageFull.crop(self.config.blurSection)
			destination = (self.config.blurXOffset, self.config.blurYOffset)
			crop = crop.convert("RGBA")
			crop = crop.filter(ImageFilter.GaussianBlur(radius=self.config.sectionBlurRadius))
			self.config.renderImageFull.paste(crop, destination, crop)

		# UPDATES THE MAIN CANVAS -- there is only one even in the multiplayer setup
		self.cnvs.delete("main1")
		self.cnvs._image_tk = PIL.ImageTk.PhotoImage(self.config.renderImageFull)
		self.cnvs._image_id = self.cnvs.create_image(
			self.config.canvasOffsetX,
			self.config.canvasOffsetY,
			image=self.cnvs._image_tk,
			anchor="nw",
			tag="main1",
		)
		self.cnvs.update()

	def remappingFunctionTemp(self):
		for i in range(0, 4):
			## Map the one below to the next set of 4
			pix = 16
			colWidth = 128
			row = i
			cropRow = i * 2 + 1

			remapImageBlockSection = (0, cropRow * pix, colWidth, cropRow * pix + pix)
			remapImageBlockDestination = (colWidth, row * 16)
			crop = config.renderImageFull.crop(remapImageBlockSection)
			crop = crop.convert("RGBA")
			config.renderImageFull.paste(crop, remapImageBlockDestination, crop)
			## Move a row "up"

			remapImageBlockSection = (
				0,
				(cropRow - 1) * pix,
				colWidth,
				(cropRow - 1) * pix + pix,
			)
			remapImageBlockDestination = (0, (row) * pix)
			crop = config.renderImageFull.crop(remapImageBlockSection)
			crop = crop.convert("RGBA")
			config.renderImageFull.paste(crop, remapImageBlockDestination, crop)

	def drawBeforeConversion():
		return True

	"""""" """""" """""" """""" """""" """""" """""" """""" """""" """""" ""
