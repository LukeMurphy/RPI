
"Just a handy object to hold ranges for hue, saturation and value"
class ColorSet:

	hueRange = []
	saturationRange = []
	valueRange = []

	def __init__(self,h,s,v):
		self.hueRange = h
		self.saturationRange = s
		self.valueRange = v