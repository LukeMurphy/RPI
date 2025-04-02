import math
import random
import time

from matplotlib.pylab import rand
import numpy as np
from PIL import Image, ImageDraw
from scipy.spatial import Voronoi
from scipy.interpolate import splprep, splev  # For spline interpolation
from modules.holder_director import Director
from modules import badpixels, colorutils, coloroverlay

"""""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" ""

# ----------------------------------------------------##----------------------------------------------------#
class Pen:
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


def resetSystem(fullReset=False):
    global config
    _create_image_layers(config)
    config.totalResetTime = random.randint(101,287)


def changeDrawingMode():
    config.drawingMode = random.randint(1,4)
    config.startNewLineProb = .005
    config.changeTimeController.slotRate = random.randint(20,33)

    if config.drawingMode in {2, 3}:
        config.startNewLineProb = .1
        config.changeTimeController.slotRate = random.randint(33,63)



    print(f" => New Drawing Mode: {config.drawingMode}")


def changePalettes():
    config.bgColor = random.choice(config.bgColorSets)
    # print(f" New bg Color : {config.bgColor}")
    _create_image_layers(config)
    config.underLayerDraw.rectangle((0, 0, config.canvasWidth, config.canvasHeight), fill=(config.bgColor[0], config.bgColor[1], config.bgColor[2], config.bgColorAlpha))
    config.changeColorSetTime = random.randint(123,287)


# ------------------------------------------- PEN ACTIONS ---------------------------------------------------#

def startNewLine(_pen):
    setPenProperties(_pen)
    setPenColor(_pen)
    # _pen._w = round(random.uniform(1, 6))
    # _n = round(random.uniform(_pen.minNumPoints, _pen.maxNumPoints))
    # _ran = random.uniform(_pen.minRandom, _pen.maxRandom)
    # _centerVariationX = random.randint(0, _pen.centerVariationXMax)
    # _centerVariationY = random.randint(0, _pen.centerVariationYMax)
    # _img = generateSmoothLinePoints(_pen, config.canvasWidth, config.canvasHeight, _n, _centerVariationX, _centerVariationY)
    _img = generateSmoothLinePoints(_pen)
    _pen._p = 1
    # config.image = config.image.rotate(random.uniform(-10,10))
    config.image = Image.new("RGBA", (config.canvasWidth, config.canvasHeight))
    config.draw = ImageDraw.Draw(config.image)


def setPenProperties(pen) :
        pen.drawingSize = [config.canvasWidth , config.canvasHeight ]
        pen.lastPoint = [config.canvasWidth / 2, config.canvasHeight / 2]
        pen._p = 0
        pen.smooth_points = []
        pen.speed = random.randint(1, 5)
        pen.centerVariationXMax = random.randint(10, 100)
        pen.centerVariationYMax = random.randint(0, 0)

        # genral size of drawing
        pen.drawingSkip = random.uniform(0.0,.01)
        
        # shape of scribbles
        if config.drawingMode == 1 :
            markType  =  random.randint(1,3) 
            if markType == 1 :
                _scratchyLong(pen)
            elif markType == 2 :
                _shortMarks(pen)
            elif markType == 3 :
                _longOvalSweeps(pen)
        elif config.drawingMode == 2 :
            if random.random() < .5 :
                _scratchyLong(pen)
            else :
                _shortMarks(pen)
        elif config.drawingMode == 3 :
            _scratchyLong(pen)
        elif config.drawingMode == 4 :
            _longOvalSweeps(pen)

        setPenColor(pen)


def _scratchyLong(pen):
    # tight scratch angry linear
    pen.minNumPoints = 4
    pen.maxNumPoints = 10
    pen.num_points = random.randint(pen.minNumPoints, pen.maxNumPoints)
    pen.turns = round(random.uniform(8, 12))
    pen.minInterpolatedPoints = 80
    pen.maxInterpolatedPoints = 200
    
    pen.baseRadiusFactor = random.uniform(1.8,3)
    pen.yRadiusFactor = random.uniform(0.001,.05)
    pen.xRadiusFactor = random.uniform(1.8, 2.5)

    pen.xRadiusFactorNoiseFactor = 10.10
    pen.yRadiusFactorNoiseFactor = 10.0
    pen.yRandom = random.randint(-10, 10)
    pen.xRandom = random.randint(-10, 140)
    
    pen.rotationFactor = 12
    pen.rotationAngle = random.uniform(-math.pi/2/pen.rotationFactor,math.pi/2/pen.rotationFactor)
    
    pen.xOffset = random.randint(-100,100)
    pen.yOffset = random.randint(-100,100)
    pen._w = 1
    pen.mode = 1


def _shortMarks(pen):
    pen.minNumPoints = 4
    pen.maxNumPoints = 10
    pen.num_points = random.randint(pen.minNumPoints, pen.maxNumPoints)
    pen.turns = round(random.uniform(3, 4))
    pen.minInterpolatedPoints = 80
    pen.maxInterpolatedPoints = 100
    
    pen.baseRadiusFactor = random.uniform(1.0,1.1)
    pen.xRadiusFactor = random.uniform(0.001,.01)
    pen.yRadiusFactor = random.uniform(.45, .6)

    pen.xRadiusFactorNoiseFactor = 1.1
    pen.yRadiusFactorNoiseFactor = .0
    pen.yRandom = random.randint(-50, 50)
    pen.xRandom = random.randint(-10, 10)
    
    pen.rotationFactor = 4
    pen.rotationAngle = random.uniform(-math.pi/2/pen.rotationFactor,math.pi/2/pen.rotationFactor)
    
    pen.xOffset = random.randint(-200,200)
    pen.yOffset = random.randint(-100,100)
    pen._w = 1
    pen.mode = 1


def _longOvalSweeps(pen):
    # winding scribbles
    pen.num_points = 8
    pen.turns = random.randint(3,7)
    pen.minInterpolatedPoints = 190
    pen.maxInterpolatedPoints = 220

    pen.baseRadiusFactor = 1.8
    pen.xRadiusFactor = 1.2
    pen.yRadiusFactor = random.uniform(.80,.2)

    pen.xRadiusFactorNoiseFactor = 1.0
    pen.yRadiusFactorNoiseFactor = 1.0
    pen.xRandom = random.randint(-10, 100)
    pen.yRandom = random.randint(-10, 10)

    pen.rotationFactor = 8
    pen.rotationAngle = random.uniform(-math.pi/2/pen.rotationFactor,math.pi/2/pen.rotationFactor)

    pen.xOffset = random.randint(-10,10)
    pen.yOffset = random.randint(-10,10)
    pen._w = round(random.uniform(1, 6))
    pen.mode = 2


def _canvasCircumscribes(pen) :
    # For ref -- this makes an oval at center
    pen.num_points = 6
    pen.baseRadiusFactor = 1.8
    pen.xRadiusFactor = 1.2
    pen.yRadiusFactor = .80
    pen.rotationAngle = 0
    pen.xOffset = random.randint(-1,1)
    pen.yOffset = random.randint(-1,1)
    pen.xRandom = random.randint(-1, 1)
    pen.yRandom = random.randint(-1, 1)
    pen.turns = 5
    pen.minInterpolatedPoints = 190
    pen.maxInterpolatedPoints = 220

# ----------------------------------------------------##----------------------------------------------------#

def setPenColor(_pen):
    _pen.lineColor = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 225),200)

    if random.random() <  .7 :
        if random.random() <  .1 :
            _pen.lineColor = (random.randint(170, 190), random.randint(170, 190), random.randint(170, 190), 200)
        else :
            _pen.lineColor = (random.randint(0, 10), random.randint(0, 10), random.randint(0, 10),200)

    if _pen.mode ==2 and random.random() < .4:
        _pen.lineColor = (random.randint(120, 200), random.randint(0, 10), random.randint(0, 10),200)


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
    
    center_x = width // 2 #+ _pen.xOffset  # + round(centerVariationX - random.random() * centerVariationX * 2)
    center_y = height // 2 #+ _pen.yOffset  # + round(centerVariationY - random.random() * centerVariationY * 2)

    
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
            points.append([x, y])
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
    for pt in smooth_points_c :
        ptx = pt[0] * np.cos(_pen.rotationAngle) - pt[1] * np.sin(_pen.rotationAngle)
        pty = pt[1] * np.cos(_pen.rotationAngle) + pt[0] * np.sin(_pen.rotationAngle)
        _pen.rotationAngle += _pen.rotationAngle/500
        smooth_points_r.append((ptx + _pen.xOffset,pty + _pen.yOffset))

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


def drawLine(_pen):
    # Draw the shape
    _penSkip = random.random() <= _pen.drawingSkip
    for _ in range(_pen.speed):
        if _pen._p < len(_pen.smooth_points) and _pen._p > 0:
            _p1 = _pen.smooth_points[_pen._p - 1]
            _p2 = _pen.smooth_points[_pen._p]
            # if abs(_p1[0] - _p2[0])<10 and abs(_p1[1] - _p2[1]) < 30 :
            if not _penSkip :
                config.draw.line((_p1, _p2), fill=_pen.lineColor, width=_pen._w)
            _pen._p += 1
            config.doingDrawing = True
        if _pen._p == len(_pen.smooth_points):
            _pen._p = 0
            config.doingDrawing = False

        if random.random() < 0.2:
                _pen._w += 1
        if random.random() < 0.2 or _pen._w > 7:
                _pen._w -= 1
        if _pen._w <= 0 :
            _pen._w = 1    


def _pen_functions():
    for _pen in config.penArray:
        if random.random() < 0.01:
            setPenColor((_pen))

        if random.random() < config.startNewLineProb and _pen._p == 0:
            startNewLine(_pen)

        drawLine(_pen)


# ----------------------------------------------------##----------------------------------------------------#


def _do_drawing_glitch():
    glitchIterations = round(random.uniform(1, 10))
    for _ in range(glitchIterations):
        glitchBox(
            config.image,
            config.canvasWidth,
            config.canvasHeight,
            2,
            2,
        )


def _bg_colors_filling(config):

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
        cR = config.bgBoxColorRange
        # print(cR)
        bgBoxFill = colorutils.getRandomColorHSV(cR[0], cR[1], cR[2], cR[3], cR[4], cR[5], cR[6], cR[7])
        # print(bgBoxFill)
        config.bgBoxFill = (
            round(config.brightness * bgBoxFill[0]),
            round(config.brightness * bgBoxFill[1]),
            round(config.brightness * bgBoxFill[2]),
            round(random.uniform(config.bgBoxAlphaRange[0], config.bgBoxAlphaRange[1])),
        )

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
def animationBackGroundFadeIn():
    currentAnimation = config.animations[config.currentAnimationIndex]
    if currentAnimation.bg_alpha <= currentAnimation.bg_alpha_max:
        currentAnimation.bg_alpha += 2

# ----------------------------------------------------##----------------------------------------------------#

def runWork():
    while True:
        config.directorController.checkTime()
        if config.directorController.advance:
            iterate()

        time.sleep(config.redrawSpeed)


def iterate():
    global config

    if config.changeColorSetTime > 0:
        config.paletteController.checkTime()
        if config.paletteController.advance:
            changePalettes()

    if config.changeTime > 0:
        config.changeTimeController.checkTime()
        if config.changeTimeController.advance:
            changeDrawingMode()

    if config.totalResetTime > 0:
        config.systemController.checkTime()
        if config.systemController.advance:
            resetSystem(True)


    config.fadeRate += config.fadeRateDelta

    if config.fadeRate > 255:
        config.fadeRate = 30
        config.fadeRateDelta = random.uniform(0.1, 2)

        if config.fadeRateDelta <= config.fadeRateNewSystemThreshold:
            config.bgColor = random.choice(config.bgColorSets)

    if random.SystemRandom().random() < config.usebgBoxProb and not config.doingDrawing:
        _do_drawing_glitch()
        _bg_colors_filling(config)

    # dithering movement
    if random.random() < config.filterRemappingProb:
        filterRemapImage(config)

    if not config.doingDrawing and random.random() < 0.1:
        _do_drawing_glitch()


    _pen_functions()

    renderImage()


def renderImage() :

    config.underLayer.paste(config.image, (0, 0), config.image)
    config.canvasImage.paste(config.underLayer, (0, 0), config.underLayer)
    config.render(config.canvasImage, 0, 0, config.canvasWidth, config.canvasHeight)

# ----------------------------------------------------##----------------------------------------------------#

def main(run=True):
    global config, workConfig
    _load_background_color_config(config)
    _create_image_layers(config)
    _load_filter_config(config)
    _load_color_config(config)
    _initialize_system(config)
    if run:
        runWork()


def _load_background_color_config(config):
    """Loads background-related configuration parameters."""
    bgColorSets = workConfig.get("drawingField", "bgColorSets").split(",")
    config.bgColorSets = []
    for bg in bgColorSets:
        bgColor = workConfig.get(bg, "bgColor").split(",")
        bgColors = [int(x) for x in bgColor]
        config.bgColorSets.append(bgColors)
    config.bgColor = config.bgColorSets[0]
    config.bgColorAlpha = int(workConfig.get("drawingField", "bgColorAlpha"))


def _create_image_layers(config):
    config.image = Image.new("RGBA", (config.canvasWidth, config.canvasHeight))
    config.draw = ImageDraw.Draw(config.image)

    config.canvasImage = Image.new("RGBA", (config.canvasWidth, config.canvasHeight))
    config.canvasDraw = ImageDraw.Draw(config.canvasImage)

    config.underLayer = Image.new("RGBA", (config.canvasWidth, config.canvasHeight))
    config.underLayerDraw = ImageDraw.Draw(config.underLayer)

    # config.underLayerDraw.rectangle((0, 0, config.canvasWidth, config.canvasHeight), fill=(100, 0, 80, 100))
    config.underLayerDraw.rectangle((0, 0, config.canvasWidth, config.canvasHeight), fill=(config.bgColor[0], config.bgColor[1], config.bgColor[2], config.bgColorAlpha))



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


def _load_color_config(config):
    """Loads color-related configuration parameters."""
    config.changeColorSetTime = float(workConfig.get("drawingField", "changeColorSetTime", fallback=0))

    if config.changeColorSetTime > 0:
        config.paletteController = Director(config)
        config.paletteController.slotRate = config.changeColorSetTime

    config.bgBoxColorRange = list(
        map(
            lambda x: float(x),
            workConfig.get("drawingField", "bgBoxColorRange").split(","),
        )
    )
    config.bgBoxAlphaRange = tuple(
        map(
            lambda x: int(x),
            workConfig.get("drawingField", "bgBoxAlphaRange").split(","),
        )
    )
    config.usebgBox = workConfig.getboolean("drawingField", "forcebgBox")
    config.usebgBoxProb = float(workConfig.get("drawingField", "usebgBoxProb"))
    config.bgBoxBox = tuple(map(lambda x: int(x), workConfig.get("drawingField", "bgBoxBox").split(",")))
    config.renderImageFullOverlay = Image.new("RGBA", (config.canvasWidth, config.canvasHeight))
    config.renderDrawOver = ImageDraw.Draw(config.renderImageFullOverlay)
    config.bgBoxFill = (100, 0, 80, 100)

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


def _initialize_system(config):
    """Initializes the system and related parameters."""
    """Loads rendering-related configuration parameters."""
    config.fadeRate = float(workConfig.get("drawingField", "fadeRate"))
    config.fadeRateDelta = float(workConfig.get("drawingField", "fadeRateDelta"))
    config.fadeRateNewSystemThreshold = float(workConfig.get("drawingField", "fadeRateNewSystemThreshold"))

    config.totalResetTime = float(workConfig.get("drawingField", "totalResetTime", fallback=33))
    config.changeTime = float(workConfig.get("drawingField", "changeTime", fallback=10))

    if config.totalResetTime > 0:
        config.systemController = Director(config)
        config.systemController.slotRate = config.totalResetTime

    if config.changeTime > 0:
        config.changeTimeController = Director(config)
        config.changeTimeController.slotRate = config.changeTime

    config.slotRate = float(workConfig.get("drawingField", "slotRate", fallback=0.03))
    config.redrawSpeed = float(workConfig.get("drawingField", "redrawSpeed", fallback=0.03))
    config.startNewLineProb = float(workConfig.get("drawingField", "startNewLineProb", fallback=0.03))
    config.directorController = Director(config)
    config.directorController.slotRate = config.slotRate

    config.doingDrawing = False
    config.penArray = []
    config.drawingMode = 1
    
    for i in range(1):
        pen = Pen()
        pen.number = i
        setPenProperties(pen)
        config.penArray.append(pen)

