import  random, time


class Proc:

	def __init__(self, drawRef, xpos=0, delay=.2, clr='green'):
		print("init")
		self.clr = clr
		self.xpos = xpos
		self.drawRef = drawRef
		self.delay = delay

	def proc1(self):
		while True:
			self.drawRef.rectangle( (self.xpos, 0, 250, 500 ), fill = 'red')
			self.drawRef.rectangle( (self.xpos, 0, self.xpos + round(random.uniform(10,100)), round(random.uniform(10,200) )), fill = self.clr)
			time.sleep(self.delay)
