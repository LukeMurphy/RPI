[displayconfig]

work = particles
#--------------------------#

rendering = hub
rotation = 90
fullRotation = True
rotationTrailing = False
checkForConfigChanges = True
isRPI = False
useFilters = False

tileSizeHeight = 32
tileSizeWidth = 64
matrixTiles = 48
cols = 5
rows = 6

# ---  Also determines the window geometry
screenWidth = 320
screenHeight = 320

# ---  preparing for rotation
windowWidth = 320
windowHeight = 320

canvasWidth = 320
canvasHeight = 320

# - for small adjustments when sending to 
# - matrix panels & cards
canvasOffsetX = 4
canvasOffsetY = 3

# Window Offset
#windowXOffset = 1700
#windowXOffset = 2812
windowXOffset = 2684
windowYOffset = 201

brightness =  .8
minBrightness = 0

imageXOffset = 0
imageYOffset = 0

remapImageBlock = False
remapImageBlockSection = 0,0,64,160
remapImageBlockDestination = 0,-25


usePixelSort = True
pixelSortRotatesWithImage = False
unsharpMaskPercent = 30
blurRadius = 0
pixSortXOffset = 1
pixSortYOffset = 0
pixSortboxHeight = 51
pixSortboxWidth = 319
pixSortgap = 4
pixSortprobDraw = .99
pixSortprobGetNextColor = 1
pixSortSizeDecriment =  0
pixSortProbDecriment = 0
pixSortSampleVariance = 10
pixSortDrawVariance = 0
pixSortDirection = lateral
randomColorProbabilty = 0.00001
brightnessVarLow = .9
brightnessVarHi = .9
pixelSortAppearanceProb = 1.0

useBlur  = False
blurXOffset = 0
blurYOffset = 0
blurSectionWidth = 270
blurSectionHeight = 170
sectionBlurRadius = 2



[diag]
#--------------------------#
fontColor = 255,255,0
outlineColor = 255,0,0
fontColor2 = 0,0,100
bgColor = 0,0,254
showGrid = True
fontSize = 14

brightness =  .8
outerColor = 10,0,100
innerColor = 230,40,0
borderColor = 10,0,0


[particleSystemBAK]
#--------------------------#
objColor = fixed
fillColor = 10,1,140,80
outlineColor = 184,100,1,225 
bgColor = 180,100,0,50


[particleSystem]
#--------------------------#
numUnits = 290
delay = .02

xGravity = 0
yGravity = 0

ignoreBottom = False

speedMin = .1
speedMax = 1

meandorfactor = .35

#initial direction 3.14/2
variance = 1

objWidth = 50
objHeight = 60
objType = rect
objTrails = False

widthRate = .998
heightRate = .999

overallBlur = 1
unitBlur = 0

objColor = fixed
fillColor = 180,100,0,30
outlineColor = 184,80,1,105 
#bgColor = 80,10,0,20
bgColor = 80,10,30,20

bgTransitions = True
bgRangeA =  100
bgRangeB = 300
hueMin = 0
hueMax = 360
maxBrightness = .955
bgTransparency = 10

transparencyRange = 10,30

#*****
centerRangeXMin = 10
centerRangeYMin = -170

centerRangeXMax = 320
centerRangeYMax = -110

damping = 1
collisionDamping = 1

borderCollisions = True
expireOnExit = True
reEmitNumber = 2
### If this is True, always creating just
### one unit when one goes off screen vs.
### bursting -- prevents flickering of the
### units when one gets removed and the
### drawing order changes mid-stream
fixedUnitArray = True

# travel fire linearMotion
movement = fire
linearMotionAlsoHorizontal = False
useFlocking = False
cohesionDistance = 40
repelDistance = 3
repelFactor = 2
clumpingFactor = 1
distanceFactor = 1
cohesionDegrades = .99
changeCohesion = False

trailingFade = 200

## This color should have a little red in it
## but my current card configs paint pure blue 
## more like 10,0,50,200 -- should have a slight
## purple cast

useOverLay = False
overlayColor = 100,0,200,1
clrBlkWidth = 32
clrBlkHeight = 32
overlayxPos = 60
overlayyPos = 60
#overlayColor = 88,40,0,190


