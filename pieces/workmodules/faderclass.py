import math
import random
import time

from PIL import Image, ImageDraw, ImageEnhance, ImageFont, ImageOps


class FaderObj:
	def __init__(self):
		print("FADER CLASS LOADED")
		self.doingRefreshCount = 100

	def setUp(self, startImage, endImage):
		self.doingRefresh = 0
		self.fadingDone = False
		self.startImage = startImage
		self.endImage = endImage
		self.blendedImage = endImage
		self.xPos = 0
		self.yPos = 0

		# targetImage = config.image

	def fadeIn(self):
		if self.fadingDone == False:
			if self.doingRefresh < self.doingRefreshCount:
				# print(self.doingRefresh)
				# self.blendImage = Image.new("RGBA", (self.width, self.height))
				self.blendedImage = Image.blend(
					self.startImage,
					self.endImage,
					self.doingRefresh / self.doingRefreshCount,
				)
				# self.targetImage.paste(self.crossFade, (self.xPos, self.yPos), self.crossFade)
				self.doingRefresh += 1
			else:
				# self.blendedImage.paste(self.endImage.convert("RGBA"), (self.xPos, self.yPos), self.endImage.convert("RGBA"))
				self.fadingDone = True
				# print("Fading done")
