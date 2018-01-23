#System
import math
class ParticleSystem(object):

	xGravity = +.0
	yGravity = +0
	damping = 1
	unitArray = []

	boundries = ()

	borderCollisions = True

	cohesionDistance = 20
	repelDistance = 1
	repelFactor = 1
	distanceFactor = 1
	clumpingFactor = 8

	minDx  = 2
	minDy  = 2

	

	def __init__(self, arg):
		super(ParticleSystem, self).__init__()
		self.config = arg

		w = self.config.screenWidth
		h = self.config.screenHeight
		self.boundries = (0,0,self.config.screenWidth, self.config.screenHeight)

		self.maxDistance = math.sqrt(w*w + h*h)



