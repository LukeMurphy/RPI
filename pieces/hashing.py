from logging import config
import random
import time
import noise
from noise import *
from modules.configuration import bcolors, pieceLogger
from modules import colorutils, panelDrawing
from PIL import Image, ImageDraw

# ################################################### #
# hatching hashing lines


def R(a, b, rounded=False):
    if not rounded:
        return random.uniform(a, b)
    else:
        return round(random.uniform(a, b))


def catmull_rom(p0, p1, p2, p3, t):
    t2 = t * t
    t3 = t2 * t

    return 0.5 * (2 * p1 + (-p0 + p2) * t + (2 * p0 - 5 * p1 + 4 * p2 - p3) * t2 + (-p0 + 3 * p1 - 3 * p2 + p3) * t3)


def generateRawLine(points=20, horiz=True):
    pts = []
    if horiz:
        pointSpacing = (config.drawingWidth - 1 * config.xOffset) / points
    else:
        pointSpacing = (config.drawingHeight - 1 * config.yOffset) / points

    for i in range(points):
        a = i * pointSpacing
        b = R(-config.noiseAmplitude, config.noiseAmplitude)
        if horiz:
            pts.append((round(a), round(b)))
        else:
            pts.append((round(b), round(a)))

    # ensures the last point at the right or bottom closes the box
    if horiz:
        pts.append([config.drawingWidth - 2 * config.xOffset, b])
    else:
        pts.append([b, config.drawingHeight - 2 * config.yOffset])
    # Extra points for smoother Bézier start/end
    # pts.insert(0, pts[0])
    return pts


def getCurvePoints(points, resolution=50):

    curve_points = []
    n = len(points)

    for i in range(n - 1):
        p0 = points[max(0, i - 1)]
        p1 = points[i]
        p2 = points[i + 1]
        p3 = points[min(n - 1, i + 2)]

        for step in range(resolution):
            t = step / float(resolution)  # 0 <= t < 1

            x = catmull_rom(p0[0], p1[0], p2[0], p3[0], t)
            y = catmull_rom(p0[1], p1[1], p2[1], p3[1], t)

            curve_points.append((x, y))

    return curve_points


def generateInformalLine(pts=20, xOffset=0, yOffset=0, horiz=True):
    points = generateRawLine(pts, horiz)
    _curvedPoints = getCurvePoints(points, config.curveResolution)
    _smoothPointsForDrawing = []
    _smoothPointsForDrawing.extend((pt[0] + xOffset, pt[1] + yOffset) for pt in _curvedPoints)
    return _smoothPointsForDrawing


def getColor(r, g, b, a):
    clr = list(round(i * config.brightness) for i in [r, g, b])
    clr.append(a)
    return tuple(clr)


def hashlines2():
    global config
    _fillColor = getColor(config.lineColor[0], config.lineColor[1], config.lineColor[2], config.line_alpha)
    _lineWidth = 1
    _ptCount = 0
    for h_pts in config.h_pts:
        if random.random() < config.horizLineChange:
            h_pts = generateInformalLine(config.pointsPerLineRow, config.xOffset, config.yOffset + config.rowSpacing * _ptCount, True)
            config.h_pts[_ptCount] = h_pts
        lastPt = [h_pts[0][0], h_pts[0][1]]
        for pt in h_pts:
            drawTheLine(lastPt[0], lastPt[1], pt[0], pt[1], _fillColor, _lineWidth)
            lastPt = [pt[0], pt[1]]
        _ptCount += 1

    _ptCount = 0
    for v_pts in config.v_pts:
        if random.random() < config.vertLineChange:
            v_pts = generateInformalLine(config.pointsPerLineCol, config.xOffset + config.colSpacing * _ptCount, config.yOffset, False)
            config.v_pts[_ptCount] = v_pts
        lastPt = [v_pts[0][0], v_pts[0][1]]
        for pt in v_pts:
            drawTheLine(lastPt[0], lastPt[1], pt[0], pt[1], _fillColor, _lineWidth)
            lastPt = [pt[0], pt[1]]
        _ptCount += 1


def drawTheLine(p1x, p1y, p2x, p2y, _fillColor, _lineWidth):
    config.draw.line((p1x, p1y, p2x, p2y), fill=_fillColor, width=_lineWidth)


def drawTheBG():
    config.bgColor = (config.bgColor[0], config.bgColor[1], config.bgColor[2], round(config.bg_alpha))
    config.draw.rectangle((0, 0, config.canvasWidth, config.canvasHeight), fill=config.bgColor)

    # if config.bg_alpha != config.bg_alpha_base :
    #     pieceLogger(f"{config.bg_alpha}  /  {config.bg_alpha_base}")


# def hashlines():
#     global config
   
#     if random.random() < 1:
#         config.noiseSeed = random.random()

#     lastx = [0, 0, 0]
#     lasty = [0, 0, 0]
#     _fillColor = getColor(config.lineColor[0], config.lineColor[1], config.lineColor[2], config.line_alpha)

#     for col in range(0, config.canvasWidth - 2 * config.xOffset, config.colInterval):
#         lasty = [0, 0, 0]
#         lineWidth = random.choice([0, 1])

#         for row in range(0, config.canvasHeight - 2 * config.yOffset, config.rowInterval):
#             y = row
#             x = round(noise.pnoise2((col + config.scroll), y / (10 * config.noiseSeed) + config.scroll, 2) * config.noiseAmplitude + col)
#             lineWidth = random.choice([0, 1])

#             config.draw.line(
#                 (lastx[0] + config.xOffset, lasty[0] + config.yOffset, x + config.xOffset, y + config.yOffset),
#                 fill=_fillColor,
#                 width=lineWidth,
#             )

#             # config.draw.line(
#             #     (col + config.xOffset, row + config.yOffset, config.canvasWidth - 2 * config.xOffset, row + config.yOffset),
#             #     fill=_fillColor,
#             #     width=lineWidth,
#             # )

#             config.draw.line(
#                 (lasty[0] + config.yOffset, lastx[0] + config.xOffset, y + config.yOffset, x + config.xOffset),
#                 fill=getColor(config.lineColor[0], config.lineColor[1], config.lineColor[2], config.line_alpha),
#                 width=lineWidth,
#             )

#             lastx = [x, x, x]
#             lasty = [y, y, y]
#         # octv += 1
#     config.scroll += config.scrollRate


def setLines():
    config.colInterval = random.randint(int(config.colIntervalRange[0]), int(config.colIntervalRange[1]))

    # if uniformRatio, the column ratio is used for the rows as well - this means even rectangles across field
    if config.uniformRatio:
        config.rowInterval = config.colInterval
    else:
        config.rowInterval = random.randint(int(config.rowIntervalRange[0]), int(config.rowIntervalRange[1]))

    config.noiseAmplitude = random.uniform(float(config.noiseAmplitudeRange[0]), float(config.noiseAmplitudeRange[1]))
    config.colSpacing = (config.drawingWidth - 2 * config.xOffset + config.colAdj) / config.colInterval
    config.rowSpacing = (config.drawingHeight - 2 * config.yOffset + config.rowAdj) / config.rowInterval

    # if squareRatio, the column ratio and spacing is used for the rows as well - this means all squares across field
    if config.squareRatio:
        config.rowSpacing = config.colSpacing

    config.h_pts = []
    for row in range(config.rowInterval + config.rowAdj):
        h_pts = generateInformalLine(config.pointsPerLine, config.xOffset, config.yOffset + config.rowSpacing * row, True)
        config.h_pts.append(h_pts)
        # testing a variable arithmetic or log distribution but really that is not the point
        # config.rowSpacing -= .02

    config.v_pts = []
    for col in range(config.colInterval + config.colAdj):
        v_pts = generateInformalLine(config.pointsPerLine, config.xOffset + config.colSpacing * col, config.yOffset, False)
        config.v_pts.append(v_pts)

    if not config.useSingleMode:
        config.vertLineChange = R(config.vertLineChangeRange[0], config.vertLineChangeRange[1])
        config.horizLineChange = R(config.horizLineChangeRange[0], config.horizLineChangeRange[1])
        config.line_alpha = R(config.line_alpha_range[0], config.line_alpha_range[1], True)
        config.bg_alpha_base = R(config.bg_alpha_range[0], config.bg_alpha_range[1], True)

    # pieceLogger("New Lines")


def runWork():
    global config
    print(bcolors.OKGREEN + "** " + bcolors.BOLD)
    print("Running hatchingmarks.py")
    print(bcolors.ENDC)

    while config.isRunning == True:
        iterate()
        time.sleep(config.redrawSpeed)
        if config.standAlone == False:
            config.callBack()


def setLineColor():
    _line_alpha = config.line_alpha
    _minVal = 0.0
    _maxVal = 0.1
    if config.lightMode:
        _minVal = 0.65
        _maxVal = 1.0

    config.lineColor = colorutils.getRandomColorHSV(
        config.line_minHue,
        config.line_maxHue,
        config.line_minSaturation,
        config.line_maxSaturation,
        _minVal,
        _maxVal,
        0,
        0,
        _line_alpha,
        config.brightness,
    )
    # pieceLogger("New Line Color")


def setBGColor():
    _bg_alpha = round(config.bg_alpha)
    _minVal = 0.5
    _maxVal = 0.70
    if config.lightMode:
        _minVal = 0.0
        _maxVal = 0.1
    config.bgColor = colorutils.getRandomColorHSV(
        config.bg_minHue, config.bg_maxHue, config.bg_minSaturation, config.bg_maxSaturation, _minVal, _maxVal, 0, 0, _bg_alpha, config.brightness
    )
    # pieceLogger("New BG")


def reDraw():
    # pieceLogger(f"{config.bg_alpha} {config.bg_alpha_base}")
    if config.bg_alpha < config.bg_alpha_base:
        config.bg_alpha += config.bg_alpha_returnrate

    if config.bg_alpha > config.bg_alpha_base:
        config.bg_alpha = config.bg_alpha_base

    drawTheBG()
    hashlines2()


    # adding check on bg alpha as index of transition state - don't want another transition
    # stomping on the one in progress

    if random.random() < config.changeBGProb and config.bg_alpha == config.bg_alpha_base :
        config.bg_alpha = 0
        setBGColor()
        setLineColor()

    if random.random() < config.changeLinesProb:
        config.lightMode = False if random.random() > config.lightModeProb else True
        config.bg_alpha = 0
        setLines()


def iterate():
    reDraw()

    ########### RENDERING AS A MOCKUP OR AS REAL ###########
    if config.useDrawingPoints == True:
        config.panelDrawing.canvasToUse = config.image
        config.panelDrawing.render()
    else:
        config.render(config.image, 0, 0, config.canvasWidth, config.canvasHeight)
    # Done


def main(run=True):
    global config
    global workConfig
    config.image = Image.new("RGBA", (config.canvasWidth, config.canvasHeight))
    config.canvasImage = Image.new("RGBA", (config.canvasWidth, config.canvasHeight))
    config.draw = ImageDraw.Draw(config.image)
    config.redrawSpeed = float(workConfig.get("hatchingmarks", "redrawSpeed"))

    # refinements for setting points per column and row so amplitude of noise can be adjusted to be more even if aspect ratio is more extreme - e.g narrow beam
    # but also, lower number makes the line more purely rectilinear so can give a greater focus to one directions linearity
    config.pointsPerLine = int(workConfig.get("hatchingmarks", "pointsPerLine"))
    config.pointsPerLineCol = int(workConfig.get("hatchingmarks", "pointsPerLineCol", fallback=config.pointsPerLine))
    config.pointsPerLineRow = int(workConfig.get("hatchingmarks", "pointsPerLineRow", fallback=config.pointsPerLine))


    # the +/- variability of the points
    config.noiseAmplitude = float(workConfig.get("hatchingmarks", "noiseAmplitude"))
    config.noiseAmplitudeRange = [float(x) for x in workConfig.get("hatchingmarks", "noiseAmplitudeRange", fallback="1,4").split(",")]

    # adjust higher for higer resolution 
    config.curveResolution = int(workConfig.get("hatchingmarks", "curveResolution", fallback=10))

    # not really used - was used in first iteration using Perlin Noise
    config.noiseSeed = random.random()

    # the edge spacing - critical to making the drawing as the edges matter more than the sum of the lines
    config.xOffset = int(workConfig.get("hatchingmarks", "xOffset"))
    config.yOffset = int(workConfig.get("hatchingmarks", "yOffset"))

    '''
    # PROBABILITIES ----------------
    # generally based on an interval rate of .03, i.e. 3/100's of a second per cycle ~ 33.33 frames/second
    # so the chance of change is .001 per frame, then the chance per second is ~ 3.33%
    config.changeLinesProb = float(workConfig.get("hatchingmarks", "changeLinesProb", fallback=0.01))
    '''

    config.changeLinesProb = float(workConfig.get("hatchingmarks", "changeLinesProb", fallback=0.01))

    config.vertLineChange = float(workConfig.get("hatchingmarks", "vertLineChange", fallback=0.01))
    config.horizLineChange = float(workConfig.get("hatchingmarks", "horizLineChange", fallback=0.01))

    config.vertLineChangeRange = [float(x) for x in workConfig.get("hatchingmarks", "vertLineChangeRange", fallback=".05,.6").split(",")]
    config.horizLineChangeRange = [float(x) for x in workConfig.get("hatchingmarks", "horizLineChangeRange", fallback=".05,.6").split(",")]

    # probablility background changes 
    config.changeBGProb = float(workConfig.get("hatchingmarks", "changeBGProb", fallback=0.001))
    config.bg_alpha_range = [int(x) for x in workConfig.get("hatchingmarks", "bg_alpha_range", fallback="10,40").split(",")]
    config.line_alpha_range = [int(x) for x in workConfig.get("hatchingmarks", "line_alpha_range", fallback="18,180").split(",")]
    config.bg_alpha_returnrate = float(workConfig.get("hatchingmarks", "bg_alpha_returnrate", fallback=2.0))

    # light lines on background - more like a drawing on a screen
    config.lightMode = workConfig.getboolean("hatchingmarks", "lightMode", fallback=False)
    config.lightModeProb = float(workConfig.get("hatchingmarks", "lightModeProb", fallback=1.0))
    
    # overrides the variable background and line alpha changes and fixes at one value the rate at which the vertical and horizontal lines
    config.useSingleMode = workConfig.getboolean("hatchingmarks", "useSingleMode", fallback=True)

    config.scroll = 0
    config.scrollRate = float(workConfig.get("hatchingmarks", "scrollRate"))

    config.rowIntervalRange = [int(x) for x in workConfig.get("hatchingmarks", "rowIntervalRange", fallback="1,1").split(",")]
    config.colIntervalRange = [int(x) for x in workConfig.get("hatchingmarks", "colIntervalRange", fallback="1,1").split(",")]
    config.rowAdj = int(workConfig.get("hatchingmarks", "rowAdj"))
    config.colAdj = int(workConfig.get("hatchingmarks", "colAdj"))
    
    # means the row interval is the same as the column interval - if they are independent then
    # there can be more extreme column or row spacing, othewise they get the same ratio
    config.uniformRatio = workConfig.getboolean("hatchingmarks", "uniformRatio", fallback=False)

    # forces grid to squares - but is not currently compensated to will get ragged and missing 
    # grids at edges of drawing
    config.squareRatio = workConfig.getboolean("hatchingmarks", "squareRatio", fallback=False)

    config.line_minHue = float(workConfig.get("hatchingmarks", "line_minHue"))
    config.line_maxHue = float(workConfig.get("hatchingmarks", "line_maxHue"))
    config.line_maxSaturation = float(workConfig.get("hatchingmarks", "line_maxSaturation"))
    config.line_minSaturation = float(workConfig.get("hatchingmarks", "line_minSaturation"))
    config.line_maxValue = float(workConfig.get("hatchingmarks", "line_maxValue"))
    config.line_minValue = float(workConfig.get("hatchingmarks", "line_minValue"))
    config.line_alpha = int(workConfig.get("hatchingmarks", "line_alpha"))

    config.bg_minHue = float(workConfig.get("hatchingmarks", "bg_minHue"))
    config.bg_maxHue = float(workConfig.get("hatchingmarks", "bg_maxHue"))
    config.bg_maxSaturation = float(workConfig.get("hatchingmarks", "bg_maxSaturation"))
    config.bg_minSaturation = float(workConfig.get("hatchingmarks", "bg_minSaturation"))
    config.bg_maxValue = float(workConfig.get("hatchingmarks", "bg_maxValue"))
    config.bg_minValue = float(workConfig.get("hatchingmarks", "bg_minValue"))
    config.bg_alpha = int(workConfig.get("hatchingmarks", "bg_alpha"))
    config.bg_alpha_base = int(workConfig.get("hatchingmarks", "bg_alpha"))

    config.drawingWidth = int(workConfig.get("hatchingmarks", "drawingWidth", fallback=f"{config.canvasWidth}"))
    config.drawingHeight = int(workConfig.get("hatchingmarks", "drawingHeight", fallback=f"{config.canvasHeight}"))

    setLines()
    setLineColor()
    setBGColor()

    ### THIS IS USED AS WAY TO MOCKUP A CONFIGURATION OF RECTANGULAR PANELS
    panelDrawing.mockupBlock(config, workConfig)
    #### Need to add something like this at final render call  as well
    """ 
        ########### RENDERING AS A MOCKUP OR AS REAL ###########
        if config.useDrawingPoints == True :
            config.panelDrawing.canvasToUse = config.renderImageFull
            config.panelDrawing.render()
        else :
            #config.render(config.canvasImage, 0, 0, config.canvasWidth, config.canvasHeight)
            #config.render(config.image, 0, 0)
            config.render(config.renderImageFull, 0, 0)
    """
    if run:
        runWork()
