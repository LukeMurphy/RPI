import math
import random
import time

from matplotlib.pylab import rand
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageChops
# from scipy.spatial import Voronoi
from scipy.interpolate import splprep, splev  # For spline interpolation
from modules.holder_director import Director
from modules import colorutils

"""""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" ""
# ----------------------------------------------------##----------------------------------------------------#
class Palette:
    def __init__(self):
        pass

class Pen:
    def __init__(self):
        pass

class Mark:
    def __init__(self):
        pass

class Texture:
    def __init__(self):
        pass

# ----------------------------------------------------##----------------------------------------------------#
def filterRemapImage(config):
    config.useFilters = True
    config.remapImageBlock = False
    startX = round(random.uniform(0, config.filterRemapRangeX))
    startY = round(random.uniform(0, config.filterRemapRangeY))
    endX = round(random.uniform(config.filterRemapMinHorzSize, config.filterRemapMaxHorzSize))
    endY = round(random.uniform(config.filterRemapMinVertSize, config.filterRemapMaxVertSize))
    config.remapImageBlockSection = [startX, startY, startX + endX, startY + endY]
    config.remapImageBlockDestination = [startX, startY]


def changeDrawing(args):
    global config
    print("\nCHANGE DRAWING/PAINTING")
    createImageLayers()
    changePalettes()
    initDrawings()

    config.systemController = Director(config)
    _newTime = random.randint(config.totalResetTime, round(float(config.totalResetTime)*config.totalResetTimeMaxMultiplier))
    config.systemController.slotRate = _newTime

    # config.underLayerDraw.rectangle((0, 0, config.canvasWidth, config.canvasHeight), fill=config.bgColor)
    # config.finalCompositeLayerDraw.rectangle((0, 0, config.canvasWidth, config.canvasHeight), fill=config.bgColor)
    config.fadeThruToNew = 0


def changeDrawingMode():
    config.drawingMode = random.randint(1, 4)
    # config.startNewLineProb = 0.005
    config.changeTimeController.slotRate = random.randint(20, 33)

    if config.drawingMode in {2, 3}:
        # config.startNewLineProb = 0.1
        config.changeTimeController.slotRate = random.randint(33, 63)

    # print(f" => New Drawing Mode: {config.drawingMode}")


def changePalettes():
    config.activePalette = random.choice(config.paletteSets)
    print(f"New Palette : {config.activePalette.name}")
    setBGColor()
    config.canvasDraw.rectangle((0,0,config.canvasWidth,config.canvasHeight), fill = (config.bgColor))
    config.canvasDraw.rectangle((0,0,config.canvasWidth,config.canvasHeight), fill = (config.bgColor))
    config.underLayerDraw.rectangle((0,0,config.canvasWidth,config.canvasHeight), fill = (config.bgColor))
    config.underLayerDraw.rectangle((0,0,config.canvasWidth,config.canvasHeight), fill = (config.bgColor))
    primeCanvas()
    # print(f" New bg Color : {config.bgColor}")
    # print(f"brightness calculated = {colorutils.brightness(config.bgColor[0],config.bgColor[1],config.bgColor[2])}")
    config.changeColorSetTimeToUse = random.randint(config.changeColorSetTime, round(config.changeColorSetTime*config.changeColorSetTimeMaxMultiplier))
    config.paletteController.slotRate = config.changeColorSetTimeToUse



# ------------------------------------------- PEN ACTIONS ---------------------------------------------------#

def startNewLine(_pen):
    # print(f"=========>   startNewLine _pen ==> {_pen.name} {config.activePalette.pens}")
    setPenProperties(_pen)
    setPenColor(_pen)
    _img = generateSmoothLinePoints(_pen)
    _pen._p = 1
    config.image = Image.new("RGBA", (config.canvasWidth, config.canvasHeight))
    config.draw = ImageDraw.Draw(config.image)


def setPenProperties(pen):
    # print(f"setting {pen} {pen.name}")
    setPenPropsByName(pen.name, pen)
    setPenColor(pen)


def setPenPropsByName(_name, pen):

    # TODO Add some specific pen based rules for shapes based on where
    # the center may end up and how much we want the pen to exit the edges
    # or stay close to the edge - i.e. like Jerry, close to the edge but
    # not over the edge
    _penProps = None

    for _p in config.marksPalette:
        _penProps = _p
        if _p.name == _name:
            _penProps = _p
            break

    # print(f"config.drawingMode {config.drawingMode}")
    # print(f"Asking to set the pen instance {_name} ==> ")
    # print(f"Setting the pen instance <=== {_penProps.name} ")

    pen.name = _name
    pen.minNumPoints = _penProps.minNumPoints
    pen.maxNumPoints = _penProps.maxNumPoints
    pen.num_points = random.randint(pen.minNumPoints, pen.maxNumPoints)
    pen.turns = round(random.uniform(_penProps.turnsRange[0], _penProps.turnsRange[1]))
    pen.minInterpolatedPoints = _penProps.minInterpolatedPoints
    pen.maxInterpolatedPoints = _penProps.maxInterpolatedPoints

    pen.baseRadiusFactor = random.uniform(_penProps.baseRadiusFactorRange[0], _penProps.baseRadiusFactorRange[1])
    pen.yRadiusFactor = random.uniform(_penProps.yRadiusFactorRange[0], _penProps.yRadiusFactorRange[1])
    pen.xRadiusFactor = random.uniform(_penProps.xRadiusFactorRange[0], _penProps.xRadiusFactorRange[1])

    pen.xRadiusFactorNoiseFactor = _penProps.xRadiusFactorNoiseFactor
    pen.yRadiusFactorNoiseFactor = _penProps.yRadiusFactorNoiseFactor
    pen.yRandom = random.randint(_penProps.yRandomRange[0], _penProps.yRandomRange[1])
    pen.xRandom = random.randint(_penProps.xRandomRange[0], _penProps.xRandomRange[1])

    pen.rotationFactor = _penProps.rotationFactor
    pen.rotationAngle = random.uniform(-math.pi / 2 / pen.rotationFactor, math.pi / 2 / pen.rotationFactor)

    pen.xOffset = random.randint(_penProps.xOffsetRange[0], _penProps.xOffsetRange[1])
    pen.yOffset = random.randint(_penProps.yOffsetRange[0], _penProps.yOffsetRange[1])
    
    pen._w = _penProps.w
    pen.maxMarkWidth = _penProps.maxMarkWidth
    pen.changeMarkWidthProb = _penProps.changeMarkWidthProb
    pen.mode = _penProps.mode

    pen.xTravelRange = _penProps.xTravelRange
    pen.yTravelRange = _penProps.yTravelRange
    pen.xTravelIncr = _penProps.xTravelIncrRange
    pen.yTravelIncr = _penProps.yTravelIncrRange
    pen.xtravelMode = 1 if random.random() < _penProps.xtravelProb else 0
    pen.ytravelMode = 1 if random.random() < _penProps.ytravelProb else 0

    pen.radiusChangePerRound = _penProps.radiusChangePerRound

    pen.drawingSize = [config.canvasWidth, config.canvasHeight]
    pen.lastPoint = [config.canvasWidth / 2, config.canvasHeight / 2]
    pen.centerVariationXMax = random.randint(config.pen_centerVariationXMin, config.pen_centerVariationXMin)
    pen.centerVariationYMax = random.randint(config.pen_centerVariationYMin, config.pen_centerVariationYMax)

    # genral size of drawing
    pen.drawingSkip = random.uniform(0.0, 0.01)
    pen._p = 0
    pen.smooth_points = []
    pen.speed = random.randint(1, 5)

    # print(f"setting pen props pen.name {pen.name}")
    # print(f"pen.drawingSkip {pen.drawingSkip}")
    # print("--")


def setPenColor(_pen):
    cR = config.activePalette.penColor
    _pen.lineColor = colorutils.getRandomColorHSV(cR[0], cR[1], cR[2], cR[3], cR[4], cR[5], cR[6], cR[7], config.penAlpha, config.brightness)
    if random.random() < config.totalRandomBGBoxColorProb :
        _pen.lineColor = colorutils.getRandomColorHSV(0,360,.1,1.0,.1,1.0,0,0, config.penAlpha, config.brightness) 


def choosePenMark() :
    _penName = random.choice(config.activePalette.pens)
    for _pen in config.marksPalette:
        # print(f"{_pen.name} {config.activePalette.pens}")
        if _pen.name == _penName :
            # print(f"we chose {_pen.name}")
            return _pen


def generateSmoothLinePoints(_pen):

    width = _pen.drawingSize[0]
    height = _pen.drawingSize[1]
    num_points = _pen.num_points

    # Generate initial points in a circle
    base_radius = min(width, height) // _pen.baseRadiusFactor
    # Generate random points around a circle
    angles = np.linspace(0, 2 * np.pi, num_points, endpoint=False)
    points = [_pen.lastPoint]
    points = []

    center_x = width // 2  # + _pen.xOffset  # + round(centerVariationX - random.random() * centerVariationX * 2)
    center_y = height // 2  # + _pen.yOffset  # + round(centerVariationY - random.random() * centerVariationY * 2)

    _xTravel = random.uniform(_pen.xTravelRange[0], _pen.xTravelRange[1])
    _yTravel = random.uniform(_pen.yTravelRange[0], _pen.yTravelRange[1])

    _xTravelIncr = random.uniform(_pen.xTravelIncr[0], _pen.xTravelIncr[1])
    _yTravelIncr = random.uniform(_pen.yTravelIncr[0], _pen.yTravelIncr[1])

    for _ in range(_pen.turns):
        for angle in angles:
            # Add random variation to the radius
            radius_x = base_radius * _pen.xRadiusFactor + (_pen.xRadiusFactorNoiseFactor - 2 * _pen.xRadiusFactorNoiseFactor * (random.random()))
            radius_y = base_radius * _pen.yRadiusFactor + (_pen.yRadiusFactorNoiseFactor - 2 * _pen.yRadiusFactorNoiseFactor * (random.random()))
            x = center_x + radius_x * np.cos(angle)
            y = center_y + radius_y * np.sin(angle)

            if random.random() < 0.1:
                x += _pen.xRandom
            if random.random() < 0.1:
                y += _pen.yRandom
            base_radius += random.uniform(-5, 5)

            base_radius += _pen.radiusChangePerRound

            points.append([x, y])

            if _pen.xtravelMode == 1:
                center_x += _xTravel
                _xTravel *= _xTravelIncr
            else:
                center_x += random.uniform(_pen.xTravelRange[0], _pen.xTravelRange[1])

            if _pen.ytravelMode == 1:
                center_y += _yTravel
                _yTravel *= _yTravelIncr
            else:
                center_y += random.uniform(_pen.yTravelRange[0], _pen.yTravelRange[1])
        _pen.lastPoint = [x, y]

    # Close the shape by repeating the first point
    points.append(points[0])
    points = np.array(points)

    # Fit a B-spline to the points
    tck, u = splprep([points[:, 0], points[:, 1]], s=0, k=3, per=1)
    # tck, u = splprep([points[:, 0], points[:, 1]], s=0, k=3, per=1)

    # Generate more points along the spline for smoothness
    _mp = random.randint(_pen.minInterpolatedPoints, _pen.maxInterpolatedPoints)
    u_new = np.linspace(0, 1, _mp)
    smooth_points = splev(u_new, tck)

    # Convert to list of tuples for PIL
    smooth_points_c = list(zip(smooth_points[0], smooth_points[1]))

    smooth_points_r = []
    for pt in smooth_points_c:
        ptx = pt[0] * np.cos(_pen.rotationAngle) - pt[1] * np.sin(_pen.rotationAngle)
        pty = pt[1] * np.cos(_pen.rotationAngle) + pt[0] * np.sin(_pen.rotationAngle)
        _pen.rotationAngle += _pen.rotationAngle / 500
        smooth_points_r.append((ptx + _pen.xOffset, pty + _pen.yOffset))

    _pen.smooth_points = smooth_points_r

    # either clockwise or counter
    if random.random() < 0.5:
        _pen.smooth_points.reverse()

    # print(f"line: {_mp} {_n} {noise_factor} ")

    # # Draw the shape
    # color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

    # for _p in range(1,len(smooth_points)) :
    #     _p1 = smooth_points[_p - 1]
    #     _p2 = smooth_points[_p]
    #     config.draw.line((_p1,_p2), fill = color, width=3)

    # config.draw.polygon(smooth_points, fill=None, outline=color, width=4)

    # return image
    return True


def pauseDrawing():
    config.stoppedAndWaitingToDraw = True
    config.canDraw = False
    config.drawingController.slotRate = random.uniform(config.activePalette.startNewLineDelayRange[0],config.activePalette.startNewLineDelayRange[1])
    # print(f"paused for {config.drawingController.slotRate}")

def releaseDrawing():
    # print("released")
    config.stoppedAndWaitingToDraw = False
    config.canDraw = True


def penLoopActions():
    if random.random() < config.changePenColorWhileDrawingProb:
        setPenColor((config.activePalette.activePen))

    if random.random() < config.startNewLineProb and config.activePalette.activePen._p == 0 and config.canDraw:
        _pen = choosePenMark()
        config.activePalette.activePen = _pen
        startNewLine(_pen)

    drawLine(config.activePalette.activePen)

    # if not config.doingDrawing and config.canDraw and not config.stoppedAndWaitingToDraw:
    #     print(f"config.activePalette.activePen._p {config.activePalette.activePen._p}")
    #     print(f"config.canDraw {config.canDraw}")
    #     pauseDrawing()

    


def drawLine(_pen):
    # Draw the shape
    # print(f"pen {_pen.name}")
    _penSkip = random.random() <= _pen.drawingSkip
    for _ in range(_pen.speed):
        if _pen._p < len(_pen.smooth_points) and _pen._p > 0:
            _p1 = _pen.smooth_points[_pen._p - 1]
            _p2 = _pen.smooth_points[_pen._p]
            # if abs(_p1[0] - _p2[0])<10 and abs(_p1[1] - _p2[1]) < 30 :
            if not _penSkip:
                config.draw.line((_p1, _p2), fill=_pen.lineColor, width=_pen._w)
            _pen._p += 1
            config.doingDrawing = True
        if _pen._p == len(_pen.smooth_points):
            _pen._p = 0
            config.doingDrawing = False
            pauseDrawing()

        if random.random() < _pen.changeMarkWidthProb:
            _pen._w += 1

        if random.random() < _pen.changeMarkWidthProb or _pen._w > _pen.maxMarkWidth:
            _pen._w -= 1

        if _pen._w <= 0:
            _pen._w = 1


# ----------------------------------------------------##----------------------------------------------------#


def doDrawingJitter():
    jitterIterations = round(random.uniform(config.jitterIterationsMin, config.jitterIterationsMin))
    for _ in range(jitterIterations):
        glitchBox(
            config.image,
            config.canvasWidth,
            config.canvasHeight,
            config.jitterIterationsHoriz,
            config.jitterIterationsVert,
        )


def bgColorBlocksFilling(arg):
    global config

    if not arg : print(f"drawing a bg box {config.blendLevel}")
    config.blendLevelRate = config.blendLevelRateBase
    config.blendLevel = 0.0

    xPos = math.floor(random.uniform(0, config.canvasWidth))
    yPos = math.floor(random.uniform(0, config.canvasHeight))

    config.tileSizeWidth = round(random.uniform(config.bgTileSizeWidthMin, config.bgTileSizeWidthMax))
    config.tileSizeHeight = round(random.uniform(config.bgTileSizeHeightMin, config.bgTileSizeHeightMax))

    if random.SystemRandom().random() < config.clearbgBoxProb:
        xPos = yPos = 0
        config.bgBoxBox = (
            xPos,
            yPos,
            xPos + config.canvasWidth,
            yPos + config.canvasHeight,
        )
        config.bgBoxFill = (0, 0, 0, 0)
    else:

       
        config.bgBoxBox = (
            xPos,
            yPos,
            xPos + config.tileSizeWidth,
            yPos + config.tileSizeHeight,
        )
        cR = config.activePalette.bgBoxColorRange
        # print(cR)
        config.bgBoxFill = colorutils.getRandomColorHSV(
            cR[0], cR[1], cR[2], cR[3], cR[4], cR[5], cR[6], cR[7], round(random.uniform(config.activePalette.bgBoxAlphaRange[0], config.activePalette.bgBoxAlphaRange[1])), config.brightness
        )

        if random.random() < config.totalRandomBGBoxColorProb :
           config.bgBoxFill = colorutils.getRandomColorHSV(0,360,.1,1.0,.1,1.0,0,0, round(random.uniform(config.activePalette.bgBoxAlphaRange[0], config.activePalette.bgBoxAlphaRange[1])), config.brightness) 

    config.underLayerDraw.rectangle(config.bgBoxBox, fill=config.bgBoxFill)

    glitchIterations = round(random.uniform(config.bgGlitchCyclesMin, config.bgGlitchCyclesMax))
    for _ in range(glitchIterations):
        glitchBox(
            config.underLayer,
            config.canvasWidth,
            config.canvasHeight,
            config.bgGlitchDisplacementHorizontal,
            config.bgGlitchDisplacementVertical,
        )


def glitchBox(
    imageRef,
    apparentWidth,
    apparentHeight,
    imageGlitchDisplacementHorizontal,
    imageGlitchDisplacementVertical,
):

    global config

    apparentWidth = config.canvasImage.size[0]
    apparentHeight = config.canvasImage.size[1]

    dx = round(random.uniform(-imageGlitchDisplacementHorizontal, imageGlitchDisplacementHorizontal))
    dy = round(random.uniform(-imageGlitchDisplacementVertical, imageGlitchDisplacementVertical))

    sectionWidth = round(random.uniform(2, apparentWidth - dx))
    sectionHeight = round(random.uniform(2, apparentHeight - dy))

    # 95% of the time they dance together as mirrors
    try:
        if random.SystemRandom().random() < 0.97:
            cx = dx + sectionWidth
            cy = dy + sectionHeight

            if cx < 0:
                cx = 32
            if cy < 0:
                cy = 32
            cp1 = imageRef.crop((0, 0, cx, cy))
            imageRef.paste(cp1, (round(dx), round(dy)))
        # comment:
    except Exception as e:
        print(e)
        print(dx + sectionWidth, dy + sectionHeight)
    # end try


# ----------------------------------------------------##----------------------------------------------------#

def setBGColor():
    config.bgColor = colorutils.getRandomColorHSV(*config.activePalette.bgColor)
    # print(f"config.activePalette.bgColor {config.activePalette.bgColor}")
    # print(f"config.bgColor {config.bgColor}")


def primeCanvas(_i = 3):
    global config
    for _ in range(_i):
        bgColorBlocksFilling(True)


def chooseTexture() :
    _textureName = config.activePalette.textureName
    for _t in config.textureSets:
        # print(f"{_pen.name} {config.activePalette.pens}")
        if _t.name == _textureName :
            # print(f"we chose {_pen.name}")
            return _t
        
# ----------------------------------------------------##----------------------------------------------------#

def createImageLayers(arg=None):
    global config

    print("Setting up all layers")
    config.image = Image.new("RGBA", (config.canvasWidth, config.canvasHeight))
    config.draw = ImageDraw.Draw(config.image)

    config.underLayer = Image.new("RGBA", (config.canvasWidth, config.canvasHeight))
    config.underLayerDraw = ImageDraw.Draw(config.underLayer)

    config.canvasImage = Image.new("RGBA", (config.canvasWidth, config.canvasHeight))
    config.canvasDraw = ImageDraw.Draw(config.canvasImage)

    config.textureLayer = Image.new("RGBA", (config.canvasWidth, config.canvasHeight))
    config.textureLayerDraw = ImageDraw.Draw(config.textureLayer)

    config.finalCompositeLayer = Image.new("RGBA", (config.screenWidth, config.screenHeight))
    config.finalCompositeLayerDraw = ImageDraw.Draw(config.finalCompositeLayer)

    config.renderImageFullOverlay = Image.new("RGBA", (config.canvasWidth, config.canvasHeight))
    config.renderDrawOver = ImageDraw.Draw(config.renderImageFullOverlay)


def createTextureLayer(tex):
    config.useTextureLayer = tex.useTextureLayer
    for _row in range(tex.blockRows):
        for _col in range(tex.blockCols):
            if random.random() > tex.skipProb:
                for _r in range(0, tex.rows, tex.step):
                    for _c in range(0, tex.cols, tex.step):
                        x1 = _c + _col * tex.cols
                        y1 = _r + _row * tex.rows
                        x2 = x1 + tex.px
                        y2 = y1 + tex.px
                        _rate = random.uniform(1, 3)
                        _a = 2 + round(tex.base / tex.base * _r / ((tex.rows - _r) * tex.rate) * _c / ((tex.cols - _c) * tex.rate))

                        if tex.base == 255:
                            _a = tex.base
                        if random.random() < tex.drawMark:
                            if tex.usedots:
                                config.textureLayerDraw.ellipse((x1, y1, x2, y2), fill=(tex.clr_r, tex.clr_g, tex.clr_b, _a), outline=None)
                            else:
                                config.textureLayerDraw.rectangle((x1, y1, x2 + tex.xtick, y2 + tex.ytick), fill=(tex.clr_r, tex.clr_g, tex.clr_b, _a), outline=None)
                                # config.textureLayerDraw.line((x1, y1, x2+_xtick, y2+_ytick), fill=(_clr_r, _clr_g, _clr_b, 255), width=0)
    if tex.blur > 0:
        config.textureLayer = config.textureLayer.filter(ImageFilter.GaussianBlur(radius=tex.blur))


def initDrawings():
    global config
    print(f"Init drawings {config.activePalette.pens}")

    createTextureLayer(chooseTexture())
    config.underLayerDraw.rectangle((0, 0, config.canvasWidth, config.canvasHeight), fill=config.bgColor)

    primeCanvas()

    _pen = choosePenMark()
    config.activePalette.activePen = _pen
    config.startNewLineProb = config.activePalette.startNewLineProb
    config.usebgBoxProb = config.activePalette.usebgBoxProb
    config.clearCurrentDrawingProb = config.activePalette.clearCurrentDrawingProb
    startNewLine(_pen)
    doDrawingJitter()


# ----------------------------------------------------##----------------------------------------------------#


def runWork():
    while True:
        config.directorController.checkTime()
        if config.directorController.advance:
            iterate()

        time.sleep(config.redrawSpeed)


def iterate():
    global config

    if config.changeDrawingModeTime > 0:
        config.changeTimeController.checkTime()
        if config.changeTimeController.advance:
            changeDrawingMode()

    if config.changeColorSetTime > 0:
        config.paletteController.checkTime()
        if config.paletteController.advance:
            changeDrawing(True)

    if config.stoppedAndWaitingToDraw :
        config.drawingController.checkTime()
        if config.drawingController.advance:
            releaseDrawing()  

    if random.SystemRandom().random() < config.changeBGColorProb :
        setBGColor()


    if random.random() < config.clearCurrentDrawingProb:
        clearCurrentDrawing()


    if random.SystemRandom().random() < config.usebgBoxProb and not config.doingDrawing:
        if config.doJitterWhenAddingBG :
            # print("doing jitter while adding bg filling")
            doDrawingJitter()
        bgColorBlocksFilling(config)

    # dithering movement
    if random.random() < config.filterRemappingProb:
        filterRemapImage(config)

    if not config.doingDrawing and random.random() < config.doJitterProb:
        doDrawingJitter()

    penLoopActions()

    renderImage()


def renderImage():
    global config
    config.underLayer.paste(config.image, (0, 0), config.image)
    if config.useTextureLayer:
        config.underLayer.paste(config.textureLayer, (0, 0), config.textureLayer)

    _tempImage = ImageChops.blend(config.canvasImage, config.underLayer, config.blendLevel)

    config.blendLevel += config.blendLevelRate

    if config.blendLevel >= 1.0:
        config.blendLevelRate = 0.0
        config.blendLevel = 1.0

    if config.fadeThruToNew < 255 :
        config.fadeThruToNew += 10
        config.canvasDraw.rectangle((0, 0, config.canvasWidth, config.canvasHeight), fill=(config.bgColor[0],config.bgColor[1],config.bgColor[2],config.fadeThruToNew))
    elif not config.fadeThruToNewDone :
        config.fadeThruToNewDone = True
        initDrawings()
        
    config.canvasImage.paste(_tempImage, (0, 0), _tempImage)

    if not config.debugMode :
        config.finalCompositeLayerDraw.rectangle((0,0,config.canvasWidth,config.canvasHeight), fill = (config.bgColor))
        config.finalCompositeLayer.paste(config.canvasImage,(0,0),config.canvasImage)
        config.render(config.finalCompositeLayer, 0, 0, config.finalCompositeLayer, config.finalCompositeLayer)
    else :
        config.finalCompositeLayerDraw.rectangle((0,0,config.screenWidth,config.screenHeight), fill = (125,125,125))
        config.finalCompositeLayerDraw.rectangle((0,550,config.canvasWidth, 550 + config.canvasHeight), fill = (config.bgColor))

        config.finalCompositeLayer.paste(config.textureLayer,(0,0),config.textureLayer)      
        config.finalCompositeLayer.paste(config.image,(280,0),config.image)
        config.finalCompositeLayer.paste(config.underLayer,(0,280),config.underLayer)

        config.finalCompositeLayerDraw.rectangle((280,280,config.canvasWidth  + 280, 280 + config.canvasHeight), fill = (config.bgColor))
        config.finalCompositeLayer.paste(config.canvasImage,(280,280),config.canvasImage)

        config.render(config.finalCompositeLayer, 0, 0, config.finalCompositeLayer, config.finalCompositeLayer)


def clearCurrentDrawing():
    config.underLayerDraw.rectangle((0, 0, config.canvasWidth, config.canvasHeight), fill=(config.bgColor[0],config.bgColor[1],config.bgColor[2],200))

    config.image = Image.new("RGBA", (config.canvasWidth, config.canvasHeight))
    config.draw = ImageDraw.Draw(config.image)

    config.underLayer = Image.new("RGBA", (config.canvasWidth, config.canvasHeight))
    config.underLayerDraw = ImageDraw.Draw(config.underLayer)
    primeCanvas(2)
    config.canvasDraw.rectangle((0, 0, config.canvasWidth, config.canvasHeight), fill=(config.bgColor[0],config.bgColor[1],config.bgColor[2],225))


# ----------------------------------------------------##----------------------------------------------------#


def main(run=True):
    global config, workConfig
    _load_texture_models(config)
    createImageLayers(config)
    _load_filter_config(config)
    _load_drawing_configs(config)
    _load_pen_config(config)
    _initialize_system(config)
    if run:
        runWork()


def _load_texture_models(config):
    config.useTextureLayer = True
    config.textureSetNames = workConfig.get("drawingField", "textureSets", fallback='texture1').split(',')
    config.textureSets = []
    for _t in config.textureSetNames:
        _tex = _load_texture_values(_t)
        config.textureSets.append(_tex)


def _load_texture_values(_tName):
    tex = Texture()
    tex.name = _tName
    tex.useTextureLayer = workConfig.getboolean(_tName, "useTextureLayer", fallback=False)
    tex.step = workConfig.getint(_tName, "texture_step", fallback=7)
    tex.px = workConfig.getint(_tName, "texture_px", fallback=2)
    tex.blockRows = workConfig.getint(_tName, "texture_blockRows", fallback=8)
    tex.blockCols = workConfig.getint(_tName, "texture_blockCols", fallback=8)
    tex.rows = workConfig.getint(_tName, "texture_rows", fallback=64)
    tex.cols = workConfig.getint(_tName, "texture_cols", fallback=32)
    tex.rate = workConfig.getint(_tName, "texture_rate", fallback=2)
    tex.base = workConfig.getint(_tName, "texture_base", fallback=125)
    tex.clr_r = workConfig.getint(_tName, "texture_clr_r", fallback=40)
    tex.clr_g = workConfig.getint(_tName, "texture_clr_g", fallback=40)
    tex.clr_b = workConfig.getint(_tName, "texture_clr_b", fallback=240)
    tex.skipProb = workConfig.getfloat(_tName, "texture_skipProb", fallback=0.7)
    tex.blur = workConfig.getint(_tName, "texture_blur", fallback=1)
    tex.xtick = workConfig.getint(_tName, "texture_xtick", fallback=0)
    tex.ytick = workConfig.getint(_tName, "texture_ytick", fallback=0)
    tex.drawMark = workConfig.getfloat(_tName, "texture_drawMark", fallback=0.9)
    tex.usedots = workConfig.getboolean(_tName, "texture_usedots", fallback=True)
    return tex


def _load_filter_config(config):
    """Loads filter-related configuration parameters."""
    config.filterRemapping = workConfig.getboolean("particles", "filterRemapping", fallback=False)
    config.filterRemappingProb = float(workConfig.get("drawingField", "filterRemappingProb", fallback=0.0))
    config.filterRemapMinHorzSize = int(workConfig.get("drawingField", "filterRemapMinHorzSize", fallback=24))
    config.filterRemapMinVertSize = int(workConfig.get("drawingField", "filterRemapMinVertSize", fallback=24))
    config.filterRemapMaxHorzSize = int(workConfig.get("drawingField", "filterRemapMaxHorzSize", fallback=24))
    config.filterRemapMaxVertSize = int(workConfig.get("drawingField", "filterRemapMaxVertSize", fallback=24))
    config.filterRemapRangeX = int(workConfig.get("drawingField", "filterRemapRangeX", fallback=config.canvasWidth))
    config.filterRemapRangeY = int(workConfig.get("drawingField", "filterRemapRangeY", fallback=config.canvasHeight))


def _load_drawing_configs(config):
    """Loads color-related configuration parameters."""

    config.usebgBox = workConfig.getboolean("drawingField", "forcebgBox")
    config.bgTileSizeWidthMin = float(workConfig.get("drawingField", "bgTileSizeWidthMin"))
    config.bgTileSizeWidthMax = float(workConfig.get("drawingField", "bgTileSizeWidthMax"))
    config.bgTileSizeHeightMin = float(workConfig.get("drawingField", "bgTileSizeHeightMin"))
    config.bgTileSizeHeightMax = float(workConfig.get("drawingField", "bgTileSizeHeightMax"))
    # config.bgBoxFill = tuple(	map(lambda x: int(x), workConfig.get("drawingField", "bgBoxFill").split(",")))

    config.clearbgBoxProb = float(workConfig.get("drawingField", "clearbgBoxProb"))
    config.bgGlitchCyclesMin = float(workConfig.get("drawingField", "bgGlitchCyclesMin"))
    config.bgGlitchCyclesMax = float(workConfig.get("drawingField", "bgGlitchCyclesMax"))
    config.bgGlitchDisplacementHorizontal = float(workConfig.get("drawingField", "bgGlitchDisplacementHorizontal"))
    config.bgGlitchDisplacementVertical = float(workConfig.get("drawingField", "bgGlitchDisplacementVertical"))

    config.penAlpha = int(workConfig.get("drawingField", "penAlpha", fallback=200))
    config.bgColorAlpha = int(workConfig.get("drawingField", "bgColorAlpha", fallback=2))

    config.paletteSets = []
    paletteSets = workConfig.get("drawingField", "paletteSets").split(",")

    for _p in paletteSets:
        palette = Palette()
        palette.bgColor = list(
            map(
                lambda x: float(x),
                workConfig.get(_p, "bgColor").split(","),
            )
        )
        palette.bgColor.extend([config.bgColorAlpha,config.brightness])
        palette.bgBoxColorRange = list(
            map(
                lambda x: float(x),
                workConfig.get(_p, "bgBoxColorRange").split(","),
            )
        )
        palette.bgBoxAlphaRange = tuple(
            map(
                lambda x: int(x),
                workConfig.get(_p, "bgBoxAlphaRange").split(","),
            )
        )
        palette.penColor = tuple(
            map(
                lambda x: float(x),
                workConfig.get(_p, "penColor").split(","),
            )
        )

        palette.pens = workConfig.get(_p, "penNames").split(",")
        palette.name = _p
        palette.textureName = workConfig.get(_p, "texture")
        palette.usebgBoxProb = float(workConfig.get(_p, "usebgBoxProb", fallback=".01"))
        palette.blendLevelRateBase = float(workConfig.get(_p, "blendLevelRateBase", fallback=".01"))
        palette.clearCurrentDrawingProb = float(workConfig.get(_p, "clearCurrentDrawingProb", fallback=".0001"))

        # when set to 1.0 and startNewLineDelayRange is set
        # then the new line starts as soon as the random delay
        # ends - since drawing is a major event and changes the
        # attention of the viewer, controlling when it happens
        # is probably better left to timing than just cycle-based
        # probability
        palette.startNewLineProb = float(workConfig.get(_p, "startNewLineProb", fallback=".01"))
        palette.startNewLineDelayRange = list(map(lambda x: float(x), workConfig.get(_p, "startNewLineDelayRange", fallback="1,10").split(",")))


        config.paletteSets.append(palette)

    config.activePalette = random.choice(config.paletteSets)
    print(f"New Palette : {config.activePalette.name}")
    setBGColor()
        

def _load_pen_config(config):
    config.pen_centerVariationXMin = int(workConfig.get("drawingField", "pen_centerVariationXMin", fallback=0))
    config.pen_centerVariationXMax = int(workConfig.get("drawingField", "pen_centerVariationXMax", fallback=0))
    config.pen_centerVariationYMin = int(workConfig.get("drawingField", "pen_centerVariationYMin", fallback=0))
    config.pen_centerVariationYMax = int(workConfig.get("drawingField", "pen_centerVariationYMax", fallback=0))
    config.changePenColorWhileDrawingProb = float(workConfig.get("drawingField", "changePenColorWhileDrawingProb", fallback=0.01))

    config.penNames = workConfig.get("drawingField", "penNames").split(",")
    # config.marksPalette = {}
    config.marksPalette = []

    for _penConfigName in config.penNames:
        _mark = Mark()
        _mark.name = _penConfigName
        print(f" => Getting the config for the pen {_penConfigName}")

        _mark.minNumPoints = int(workConfig.get(_penConfigName, "minNumPoints", fallback=8))
        _mark.maxNumPoints = int(workConfig.get(_penConfigName, "maxNumPoints", fallback=8))
        _mark.turnsRange = list(map(lambda x: int(x), workConfig.get(_penConfigName, "turnsRange", fallback="2,2").split(",")))

        _mark.minInterpolatedPoints = int(workConfig.get(_penConfigName, "minInterpolatedPoints", fallback=200))
        _mark.maxInterpolatedPoints = int(workConfig.get(_penConfigName, "maxInterpolatedPoints", fallback=200))

        _mark.baseRadiusFactorRange = list(map(lambda x: float(x), workConfig.get(_penConfigName, "baseRadiusFactorRange", fallback="1.0,1.0").split(",")))
        _mark.xRadiusFactorRange = list(map(lambda x: float(x), workConfig.get(_penConfigName, "xRadiusFactorRange", fallback=".2,.2").split(",")))
        _mark.yRadiusFactorRange = list(map(lambda x: float(x), workConfig.get(_penConfigName, "yRadiusFactorRange", fallback=".2,.2").split(",")))

        _mark.xRadiusFactorNoiseFactor = float(workConfig.get(_penConfigName, "xRadiusFactorNoiseFactor", fallback=1.0))
        _mark.yRadiusFactorNoiseFactor = float(workConfig.get(_penConfigName, "yRadiusFactorNoiseFactor", fallback=1.0))
        _mark.xRandomRange = list(map(lambda x: int(x), workConfig.get(_penConfigName, "xRandomRange", fallback="-1,1").split(",")))
        _mark.yRandomRange = list(map(lambda x: int(x), workConfig.get(_penConfigName, "yRandomRange", fallback="-1,1").split(",")))

        _mark.rotationFactor = float(workConfig.get(_penConfigName, "rotationFactor", fallback=8.0))

        _mark.xOffsetRange = list(map(lambda x: int(x), workConfig.get(_penConfigName, "xOffsetRange", fallback="-1,1").split(",")))
        _mark.yOffsetRange = list(map(lambda x: int(x), workConfig.get(_penConfigName, "yOffsetRange", fallback="-1,1").split(",")))

        _mark.w = int(workConfig.get(_penConfigName, "w", fallback=1))
        _mark.maxMarkWidth = int(workConfig.get(_penConfigName, "maxMarkWidth", fallback=7))
        _mark.changeMarkWidthProb = float(workConfig.get(_penConfigName, "changeMarkWidthProb", fallback=".02"))
        _mark.mode = int(workConfig.get(_penConfigName, "mode", fallback=1))

        """
        adding parameters to enable geometric progression in x and y in addition to random arithmetic travel in x and y - in general the arithmetic is more nuanced
        """
        _mark.xTravelRange = list(map(lambda x: int(x), workConfig.get(_penConfigName, "xTravelRange", fallback="-1,1").split(",")))
        _mark.yTravelRange = list(map(lambda x: int(x), workConfig.get(_penConfigName, "yTravelRange", fallback="-1,1").split(",")))
        _mark.xTravelIncrRange = list(map(lambda x: float(x), workConfig.get(_penConfigName, "xTravelIncrRange", fallback="-1,1").split(",")))
        _mark.yTravelIncrRange = list(map(lambda x: float(x), workConfig.get(_penConfigName, "yTravelIncrRange", fallback="-1,1").split(",")))       
        _mark.xtravelProb = float(workConfig.get(_penConfigName, "xtravelProb", fallback=0.1))
        _mark.ytravelProb = float(workConfig.get(_penConfigName, "ytravelProb", fallback=0.1))
        _mark.radiusChangePerRound = float(workConfig.get(_penConfigName, "radiusChangePerRound", fallback=0))
        config.marksPalette.append(_mark)

    # print(config.marksPalette)


def _initialize_system(config):
    """Initializes the system and related parameters."""
    """Loads rendering-related configuration parameters."""
    
    config.changeBGColorProb = float(workConfig.get("drawingField", "changeBGColorProb", fallback=.01))
    config.totalResetTime = (workConfig.getint("drawingField", "totalResetTime", fallback=33))
    config.totalResetTimeMaxMultiplier = float(workConfig.get("drawingField", "totalResetTimeMaxMultiplier", fallback=1.0))
    config.changeDrawingModeTime = float(workConfig.get("drawingField", "changeDrawingModeTime", fallback=100.0))
    config.doJitterProb = float(workConfig.get("drawingField", "doJitterProb", fallback=0.1))
    config.jitterIterationsMin = (workConfig.getint("drawingField", "jitterIterationsMin", fallback=1))
    config.jitterIterationsMax = (workConfig.getint("drawingField", "jitterIterationsMax", fallback=10))
    config.jitterIterationsHoriz = (workConfig.getint("drawingField", "jitterIterationsHoriz", fallback=2))
    config.jitterIterationsVert = (workConfig.getint("drawingField", "jitterIterationsVert", fallback=2))
    config.doJitterWhenAddingBG = (workConfig.getboolean("drawingField", "doJitterWhenAddingBG", fallback=True))
    config.blendLevelRateBase = float(workConfig.get("drawingField", "blendLevelRateBase", fallback=0.01))
    config.totalRandomPenColorProb = float(workConfig.get("drawingField", "totalRandomPenColorProb", fallback=0.0))
    config.totalRandomBGBoxColorProb = float(workConfig.get("drawingField", "totalRandomBGBoxColorProb", fallback=0.0))
    config.debugMode = (workConfig.getboolean("drawingField", "debugMode", fallback=False))

    config.changeColorSetTime = float(workConfig.get("drawingField", "changeColorSetTime", fallback=0))
    config.changeColorSetTimeMaxMultiplier = float(workConfig.get("drawingField", "changeColorSetTimeMaxMultiplier", fallback=1))

    if config.changeColorSetTime > 0:
        config.paletteController = Director(config)
        config.paletteController.slotRate = config.changeColorSetTime
        config.changeColorSetTimeToUse = config.changeColorSetTime

    if config.changeDrawingModeTime > 0:
        config.changeTimeController = Director(config)
        config.changeTimeController.slotRate = config.changeDrawingModeTime

    config.slotRate = float(workConfig.get("drawingField", "slotRate", fallback=0.03))
    config.redrawSpeed = float(workConfig.get("drawingField", "redrawSpeed", fallback=0.03))
    
    config.directorController = Director(config)
    config.directorController.slotRate = config.slotRate

    config.drawingController = Director(config)
    config.drawingController.slotRate = 10

    config.canDraw = True
    config.doingDrawing = False
    config.stoppedAndWaitingToDraw = False


    config.penArray = []
    config.drawingMode = 1

    initDrawings()
    config.blendLevel = 0.0
    config.blendLevelRate = .1
    config.fadeThruToNew = 255
    config.fadeThruToNewDone = True

    # config.underLayerDraw.rectangle((0, 0, config.canvasWidth, config.canvasHeight), fill=(100, 0, 80, 100))

