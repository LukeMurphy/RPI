# Sprite
class Sprite:

	config = type("config", (object,), {})()

	def __init__(self, args):
		print("init Sprite")
		(
			self.x,
			self.y,
			self.wd,
			self.ht,
			self.dx,
			self.dx,
			self.start,
			self.end,
			self.steps,
			self.count,
		) = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

	def callBack(self):
		# Empty function to be overridden
		return False

	def iterate(self, n=0):
		# global config, x, y, wd, ht, dx, dx, start, end, steps, count
		self.config.sendToRender(self.config.image, self.x, self.y, self.wd, self.ht)
		self.x += self.dx
		self.y += self.dy

		self.count += self.steps

		if self.count > abs(self.end):
			self.callBack()
			count = 0
			# Done

	def sendToRender(self, img, xP, yP, wD, hT, c=False):
		# global config, x, y, wd, ht
		self.x, self.y, self.wd, self.ht = xP, yP, wD, hT
		config.render(img, xP, yP, wD, hT)
