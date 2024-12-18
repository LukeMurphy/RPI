# System
import math

"Movement types are linearMotion fire and travel"


class ParticleSystem(object):

	unitArray = []
	boundries = ()

	xGravity = +0.0
	yGravity = +0
	damping = 1
	borderCollisions = False
	cohesionDistance = 10
	repelDistance = 1
	repelFactor = 1
	distanceFactor = 1
	clumpingFactor = 8
	cohesionFactor = 1
	cohesionDegrades = 1
	useFlocking = False

	centerRangeXMin = 0
	centerRangeXMax = 0
	centerRangeYMin = 0
	centerRangeYMax = 0

	ignoreBottom = False

	movement = "travel"
	meanderDirection = 0.0

	meanderFactor2 = 90.0
	meanderFactor = 1.0

	minDx = 2
	minDy = 2

	numUnits = 2

	def __init__(self, arg):
		super(ParticleSystem, self).__init__()
		self.config = arg

		w = self.config.screenWidth
		h = self.config.screenHeight
		self.boundries = (0, 0, self.config.screenWidth, self.config.screenHeight)

		self.maxDistance = math.sqrt(w * w + h * h)
