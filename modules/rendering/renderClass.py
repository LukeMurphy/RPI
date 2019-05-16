import tkinter as tk
from PIL import Image, ImageTk, ImageDraw, ImageFont
from PIL import ImageFilter, ImageChops, ImageEnhance
import random
import time
import threading

from modules.filters import *

#from Tkinter import *
#import tkMessageBox
#import PIL.Image
#import PIL.ImageTk
#import gc, os



class CanvasElement:

	def __init__(self, root, config):
		print("** CanvasElement Initialized ** ")
		self.root = root
		self.config = config
		self.buff = 8
		self.counter = 0
		self.threadsList = []


	def setUp(self):
		self.config.renderImage = PIL.Image.new("RGBA", (self.config.screenWidth*self.config.rows, 32))
		self.config.renderImageFull = PIL.Image.new("RGBA", (self.config.screenWidth, self.config.screenHeight))
		self.config.image = PIL.Image.new("RGBA", (self.config.screenWidth, self.config.screenHeight))
		self.config.draw = ImageDraw.Draw(self.config.image)
		self.config.renderDraw = ImageDraw.Draw(self.config.renderImageFull)
		self.config.canvasOffsetX = 0
		self.config.canvasOffsetY = 0


	def setUpCanvas(self, root):
		self.config.torqueAngle = 0
		self.cnvs = tk.Canvas(root, width=self.config.screenWidth + self.buff, height=self.config.screenHeight + self.buff, border=0, name='main1')
		#self.config.cnvs = self.cnvs
		self.cnvs.create_rectangle(0, 0, self.config.screenWidth + self.buff, self.config.screenHeight + self.buff, fill="black")
		self.cnvs.pack()
		self.cnvs.place(bordermode='outside', width=self.config.screenWidth + self.buff, height=self.config.screenHeight + self.buff, x = self.canvasXPosition)


	def startWork(self) :

		### Putting the animation on its own thread
		### Still throws and error when manually closed though...

		print("Starting" + str(self) + str(self.instanceNumber), "Cnvs --->" , self.cnvs)
		
		try:
			#self.masterConfig.t = threading.Thread.__init__(self.work.runWork())
			self.t = threading.Thread(target=self.work.runWork)
			self.t.start()

			#self.t.join()
			#self.threadsList.append(t)
		except tk.TclError as details:
			print(details)
			pass
			exit()


	def on_closing(self):
		return True


	def updateCanvas(self) :

		## For testing ...
		#draw1  = ImageDraw.Draw(config.renderImageFull)
		#draw1.rectangle((xOffset+32,yOffset,xOffset + 32 + 32, yOffset +32), fill=(255,100,0))
		self.counter +=1
		if(self.counter > 1000) :
			#print(gc.get_count())
			# I don't know if this really really helps
			gc.collect()
			self.counter = 0

		#print("Instance Number Render: " + str(self.config.instanceNumber))
		#print(self.instanceNumber, self.cnvs)

		# This significantly helped performance !!
		'''
		self.cnvs.delete("main1")
		self.cnvs._image_tk = PIL.ImageTk.PhotoImage(self.config.renderImageFull)
		self.cnvs._image_id = self.cnvs.create_image(self.config.canvasOffsetX, self.config.canvasOffsetY, image=self.cnvs._image_tk, anchor='nw', tag="main1")
		self.cnvs.update()
		'''
		
		# This *should* be more efficient 
		#config.cnvs.update_idletasks()
		#root.update()

		############################################################
		######  Check if config file has changed and reload    #####
		############################################################

		if(self.config.checkForConfigChanges == True) :
			self.currentTime = time.time()
			f = os.path.getmtime(self.config.fileName )
			self.config.delta = ((self.currentTime - f ))

			if(self.config.delta <= 1) : 
				if(self.config.reloadConfig == False) :
					print ("LAST MODIFIED DELTA: ", self.config.delta)
					self.config.doingReload = True
					self.config.loadFromArguments(True)
				self.config.reloadConfig = True
			else :
				self.config.reloadConfig = False


	''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

	def renderCall(self, imageToRender, xOffset, yOffset, w=128, h=64, nocrop=False, overlayBottom=False, updateCanvasCall=True) :
		#print("Instance Number Render: " + str(self.config.instanceNumber), self.cnvs)
		pass


	def render(self, imageToRender, xOffset, yOffset, w=128, h=64, nocrop=False, overlayBottom=False, updateCanvasCall=True) :

		# Render to canvas
		# This needs to be optomized !!!!!!

		#print(imageToRender, self.cnvs)
		#print("Instance Number Render: " + str(self.config.instanceNumber))

		self.imageToRender = imageToRender

		xOffset = 0


		if(self.config.rotation != 0) : 
			if(self.config.fullRotation == True) :
				# This rotates the image that is painted i.e. after pasting-in the image sent
				self.config.renderImageFull = self.config.renderImageFull.rotate(-self.config.rotation, expand=False)
			else :
				# This rotates the image sent to be rendered
				self.imageToRender = self.imageToRender.rotate(-self.config.rotation, expand=True )
				#imageToRender = ImageChops.offset(imageToRender, -40, 40) 

		try :
			self.config.renderImageFull.paste(self.imageToRender, (xOffset, yOffset), self.imageToRender)

		except  :
			self.config.renderImageFull.paste(self.imageToRender, (xOffset, yOffset))

		#config.drawBeforeConversion()

		self.config.renderImageFull = self.config.renderImageFull.convert("RGB")
		self.config.renderDraw = ImageDraw.Draw(self.config.renderImageFull)

		#config.renderImageFull = ImageChops.offset(config.renderImageFull, 40, 40) 

		# For planes, only this works - has to do with transparency of repeated pasting of
		# PNG's I think
		#newimage = Image.new('RGBA', config.renderImageFull.size)
		#newimage.paste(config.renderImageFull, (0, 0))
		#config.renderImageFull =  newimage.convert("RGB")
		
		#enhancer = ImageEnhance.Brightness(config.renderImageFull)
		#config.renderImageFull = enhancer.enhance(.75)


		if self.config.useFilters == True :

			if self.config.filterRemap == True :
				self.config.tempImage = self.config.renderImageFull.copy()
				self.config.tempImage = ditherFilter(config.tempImage,xOffset, yOffset, config)
				crop = self.config.tempImage.crop(self.config.remapImageBlockSection)
				crop = crop.convert("RGBA")
				self.config.renderImageFull.paste(crop, self.config.remapImageBlockDestination, crop)
			else:
				self.config.renderImageFull = ditherFilter(self.config.renderImageFull,xOffset, yOffset, self.config)

		if self.config.usePixelSort == True and self.config.pixelSortRotatesWithImage == True :
			if(random.random()< self.config.pixelSortAppearanceProb) :
				self.config.renderImageFull =  pixelSort(self.config.renderImageFull, self.config)

		if self.config.rotation != 0  : 
			if(self.config.rotationTrailing or self.config.fullRotation) : 
				# This rotates the image that is painted back to where it was
				# basically same thing as rotating the image to be pasted in
				# except in some cases, more trailing is created
				self.config.renderImageFull = self.config.renderImageFull.rotate(self.config.rotation)


		# ---- Pixel Sort Type Effect ---- #
		if self.config.usePixelSort and self.config.pixelSortRotatesWithImage == False  :
			if(random.random()< self.config.pixelSortAppearanceProb) :
				self.config.renderImageFull =  pixelSort(self.config.renderImageFull, self.config)

				
				#crop = config.renderImageFull.crop()
				#crop = crop.convert("RGBA")
				#crop =  pixelSort(crop, config)
				#config.renderImageFull = config.renderImageFull.convert("RGBA")
				#config.renderImageFull.paste(crop)


		# ---- Remap sections of image to accommodate odd panels ---- #
		if self.config.remapImageBlock == True :
			crop = self.config.renderImageFull.crop(self.config.remapImageBlockSection)
			if self.config.remapImageBlockSectionRotation != 0 :
				crop = crop.convert("RGBA")
				crop = crop.rotate(self.config.remapImageBlockSectionRotation)
			crop = crop.convert("RGBA")
			self.config.renderImageFull.paste(crop, self.config.remapImageBlockDestination, crop)


		if self.config.remapImageBlock2 == True :
			crop = self.config.renderImageFull.crop(config.remapImageBlockSection2)
			if self.config.remapImageBlockSection2Rotation != 0 :
				crop = crop.convert("RGBA")
				crop = crop.rotate(self.config.remapImageBlockSection2Rotation)
			crop = crop.convert("RGBA")
			self.config.renderImageFull.paste(crop, self.config.remapImageBlockDestination2, crop)	


		if self.config.remapImageBlock3 == True :
			crop = config.renderImageFull.crop(self.config.remapImageBlockSection3)
			if self.config.remapImageBlockSection3Rotation != 0 :
				crop = crop.convert("RGBA")
				crop = crop.rotate(self.config.remapImageBlockSection3Rotation)
			crop = crop.convert("RGBA")
			self.config.renderImageFull.paste(crop, self.config.remapImageBlockDestination3, crop)
			

		if self.config.remapImageBlock4 == True :
			crop = self.config.renderImageFull.crop(self.config.remapImageBlockSection4)
			if self.config.remapImageBlockSection4Rotation != 0 :
				crop = crop.convert("RGBA")
				crop = crop.rotate(self.config.remapImageBlockSection4Rotation)
			crop = crop.convert("RGBA")
			self.config.renderImageFull.paste(crop, self.config.remapImageBlockDestination4, crop)
			


		# ---- Overall image blurring  ---- #
		if self.config.useBlur == True :
			'''
			config.renderImageFull = config.renderImageFull.filter(ImageFilter.GaussianBlur(radius=config.sectionBlurRadius))
			'''
			crop = self.config.renderImageFull.crop(self.config.blurSection)
			destination = (self.config.blurXOffset, self.config.blurYOffset)
			crop = crop.convert("RGBA")
			crop = crop.filter(ImageFilter.GaussianBlur(radius=self.onfig.sectionBlurRadius))
			self.config.renderImageFull.paste(crop, destination, crop)
			
		if self.config.useLastOverlay == True :
			self.config.renderDrawOver.rectangle(self.config.lastOverlayBox, fill = self.config.lastOverlayFill, outline = None)
			self.config.renderImageFull.paste(self.config.renderImageFullOverlay, (0,0), self.config.renderImageFullOverlay)


		'''
		for i in range(0,40) :
			delta = 16
			box = (0,i*delta,448,i*delta+delta)
			crop = config.renderImageFull.crop(box)
			crop = crop.convert("RGBA")
			config.renderImageFull.paste(crop, (i*2 + config.angle, i*delta), crop)

		config.torqueAngle += 1
		
		if config.torqueAngle > 1000064 :
			config.torqueAngle = 0
		'''

		#if(updateCanvasCall ) : self.updateCanvas() 

		#mem = int(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)/1024/1024
		#if mem > memoryUsage and debug :
		#	memoryUsage = mem 
		#	print 'Memory usage: %s (mb)' % str(memoryUsage)


	''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
	# This is kind of screwy as it's only used by the main window .....
	def updateTheCanvas(self, players):

		xOff = 0
		for player in players :
			#self.config.renderImageFull = self.config.renderImageFull.convert("RGBA")
			#player.config.renderImageFull = player.config.renderImageFull.convert("RGBA")
			temp = player.config.renderImageFull.copy()
			temp = player.config.renderImageFull.rotate(-player.config.canvasRotation, expand=False)
			self.config.renderImageFull.paste(temp, (player.config.canvasOffsetX,player.config.canvasOffsetY))


		self.cnvs.delete("main1")
		self.cnvs._image_tk = PIL.ImageTk.PhotoImage(self.config.renderImageFull)
		self.cnvs._image_id = self.cnvs.create_image(self.config.canvasOffsetX, self.config.canvasOffsetY, image=self.cnvs._image_tk, anchor='nw', tag="main1")
		self.cnvs.update()



	def remappingFunctionTemp(self) :
		for i in range (0,4) :
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

			remapImageBlockSection = (0, (cropRow-1) * pix, colWidth, (cropRow-1) * pix + pix)
			remapImageBlockDestination = (0, (row) * pix)
			crop = config.renderImageFull.crop(remapImageBlockSection)
			crop = crop.convert("RGBA")
			config.renderImageFull.paste(crop, remapImageBlockDestination, crop)


	def drawBeforeConversion() :
		return True

	''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''



