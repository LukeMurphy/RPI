# ################################################### #
import math
import random
import time
from modules.configuration import bcolors
from modules import coloroverlay, colorutils
from PIL import Image, ImageDraw, ImageEnhance, ImageFont, ImageOps

#############################################


class ColorPalette:

    def __init__(self):
        pass


class Cell:
    n = s = e = w = 1

    def __init__(self):
        pass


class Director:
    """docstring for Director"""

    slotRate = .5

    def __init__(self, config):
        super(Director, self).__init__()
        self.config = config
        self.tT = time.time()

    def checkTime(self):
        if (time.time() - self.tT) >= self.slotRate:
            self.tT = time.time()
            self.advance = True
        else:
            self.advance = False

    def next(self):
        self.checkTime()


def newColor(arg=0):

    cp = config.colorPalettes[arg]
    return colorutils.getRandomColorHSV(
        cp.bg_minHue,
        cp.bg_maxHue,
        cp.bg_minSaturation,
        cp.bg_maxSaturation,
        cp.bg_minValue,
        cp.bg_maxValue,
        cp.bg_dropHueMinValue,
        cp.bg_dropHueMaxValue,
        round(random.uniform(cp.bg_minAlpha, cp.bg_maxAlpha))
    )


def newColorAlt(arg=0):
    cp = config.colorPalettes[arg]
    return colorutils.getRandomColorHSV(
        cp.lines_minHue,
        cp.lines_maxHue,
        cp.lines_minSaturation,
        cp.lines_maxSaturation,
        cp.lines_minValue,
        cp.lines_maxValue,
        cp.lines_dropHueMinValue,
        cp.lines_dropHueMaxValue,
        round(random.uniform(cp.lines_minAlpha, cp.lines_maxAlpha))
    )


def main(run=True):
    global config
    global expandingRingss

    expandingRingss = []
    config.image = Image.new("RGBA", (config.canvasWidth, config.canvasHeight))
    config.draw = ImageDraw.Draw(config.image)

    config.redrawSpeed = float(workConfig.get("forms", "redrawSpeed"))

    config.colorPaletteSets = workConfig.get("forms", "sets").split(",")

    config.colorPalettes = []

    for s in config.colorPaletteSets:

        colorSet = ColorPalette()

        colorSet.bg_minHue = float(workConfig.get(s, "bg_minHue"))
        colorSet.bg_maxHue = float(workConfig.get(s, "bg_maxHue"))
        colorSet.bg_minSaturation = float(workConfig.get(s, "bg_minSaturation"))
        colorSet.bg_maxSaturation = float(workConfig.get(s, "bg_maxSaturation"))
        colorSet.bg_minValue = float(workConfig.get(s, "bg_minValue"))
        colorSet.bg_maxValue = float(workConfig.get(s, "bg_maxValue"))
        colorSet.bg_dropHueMinValue = float(workConfig.get(s, "bg_dropHueMinValue"))
        colorSet.bg_dropHueMaxValue = float(workConfig.get(s, "bg_dropHueMaxValue"))
        colorSet.bg_minAlpha = float(workConfig.get(s, "bg_minAlpha"))
        colorSet.bg_maxAlpha = float(workConfig.get(s, "bg_maxAlpha"))

        colorSet.lines_minHue = float(workConfig.get(s, "lines_minHue"))
        colorSet.lines_maxHue = float(workConfig.get(s, "lines_maxHue"))
        colorSet.lines_minSaturation = float(workConfig.get(s, "lines_minSaturation"))
        colorSet.lines_maxSaturation = float(workConfig.get(s, "lines_maxSaturation"))
        colorSet.lines_minValue = float(workConfig.get(s, "lines_minValue"))
        colorSet.lines_maxValue = float(workConfig.get(s, "lines_maxValue"))
        colorSet.lines_dropHueMinValue = float(workConfig.get(s, "lines_dropHueMinValue"))
        colorSet.lines_dropHueMaxValue = float(workConfig.get(s, "lines_dropHueMaxValue"))
        colorSet.lines_minAlpha = float(workConfig.get(s, "lines_minAlpha"))
        colorSet.lines_maxAlpha = float(workConfig.get(s, "lines_maxAlpha"))

        config.colorPalettes.append(colorSet)

    config.activeColorPalette = 0

    # background color - higher the
    # alpha = less persistent images
    backgroundColor = (workConfig.get("forms", "backgroundColor")).split(",")
    config.backgroundColor = tuple(int(x) for x in backgroundColor)

    backgroundFlashcolor = (workConfig.get("forms", "backgroundFlashcolor")).split(",")
    config.backgroundFlashcolor = tuple(int(x) for x in backgroundFlashcolor)

    config.filterPatchProb = float(workConfig.get("forms", "filterPatchProb"))
    config.filterPatchProbOff = float(workConfig.get("forms", "filterPatchProbOff"))

    config.directorController = Director(config)
    config.directorController.slotRate = float(workConfig.get("forms", "slotRate"))

    config.progressive = (workConfig.getboolean("forms", "progressive"))
    config.cellSize = int(workConfig.get("forms", "cellSize"))

    # col, row

    obstacleIndexVals = (workConfig.get("forms", "obstacleIndex")).split(",")
    config.obstacleIndex = list(int(i) for i in obstacleIndexVals)
    config.reDoDelay = float(workConfig.get("forms", "reDoDelay"))
    config.pWalls = int(workConfig.get("forms", "pWalls"))
    config.pLines = int(workConfig.get("forms", "pLines"))
    config.wallColor_s = (workConfig.get("forms", "wallColor_s")).split(",")
    config.wallColor_w = (workConfig.get("forms", "wallColor_w")).split(",")
    config.wallColor_n = (workConfig.get("forms", "wallColor_n")).split(",")
    config.wallColor_e = (workConfig.get("forms", "wallColor_e")).split(",")
    config.lineColor_s = (workConfig.get("forms", "lineColor_s")).split(",")
    config.lineColor_w = (workConfig.get("forms", "lineColor_w")).split(",")
    config.lineColor_n = (workConfig.get("forms", "lineColor_n")).split(",")
    config.lineColor_e = (workConfig.get("forms", "lineColor_e")).split(",")
    setupMaze()


def setupMaze():

    config.cellsCleared = []
    config.cells = []

    config.rows = round(config.canvasHeight / config.cellSize)
    config.cols = round(config.canvasWidth / config.cellSize)
    config.grid = []


    print(("Rows {}  Cols {}  ").format(config.rows, config.cols))

    # config.cellSize = round(config.canvasWidth / config.cols)

    for row in range(0, config.rows):
        for col in range(0, config.cols):
            _c = Cell()
            _c.row = row
            _c.col = col
            _c.n = 1
            _c.s = 1
            _c.w = 1
            _c.e = 1
            _c.i = row * config.cols + col
            _c.cleared = False
            _c.skip = False
            if _c.i == 0:
                _c.skip = True

            config.cells.append(_c)

    numCells = len(config.cells)
    config.leadCell = round(random.uniform(0, numCells-1))
    while config.leadCell in config.obstacleIndex :
        config.leadCell = round(random.uniform(0, numCells-1))
    config.cellsCleared.append([config.leadCell, "n"])

    print(("Initial Cell is {}").format(config.leadCell))


    randomWalk()


def getAdjacentCells(n):
    cell = config.cells[n]
    adjacentCells = []
    rowPosition = cell.row
    colPosition = cell.col

    # get south cell
    if rowPosition < config.rows - 1:
        cellIndex = (cell.row + 1) * config.cols + cell.col
        if config.cells[cellIndex].cleared == False and cellIndex not in config.obstacleIndex :
            adjacentCells.append([config.cells[cellIndex], "s"])

    # get north cell
    if rowPosition > 0:
        cellIndex = (cell.row - 1) * config.cols + cell.col
        if config.cells[cellIndex].cleared == False and cellIndex not in config.obstacleIndex:
            adjacentCells.append([config.cells[cellIndex], "n"])

    # get east cell
    if colPosition < config.cols - 1:
        cellIndex = cell.row * config.cols + cell.col + 1
        if config.cells[cellIndex].cleared == False and cellIndex not in config.obstacleIndex:
            adjacentCells.append([config.cells[cellIndex], "e"])

    # get west cell
    if colPosition < config.cols and colPosition > 0:
        cellIndex = cell.row * config.cols + cell.col - 1
        if config.cells[cellIndex].cleared == False and cellIndex not in config.obstacleIndex:
            adjacentCells.append([config.cells[cellIndex], "w"])

    return adjacentCells


def walkBack():
    # for each previously cleared cell, if there are open
    # adjacent cells, restart with that one
    found = False
    for i in range(len(config.cellsCleared)-1, 0, -1):
        adjCells = getAdjacentCells(config.cellsCleared[i][0])
        if len(adjCells) > 0:
            config.leadCell = config.cellsCleared[i][0]
            found = True
            break
    if found == True and config.progressive == False:
        randomWalk()


def randomWalk():
    cell = config.cells[config.leadCell]
    cell.cleared = True
    adjCells = getAdjacentCells(config.leadCell)

    if len(adjCells) > 0:
        nextCell = round(random.uniform(0, len(adjCells)-1))
        cellRef = adjCells[nextCell][0]
        # need to figure the direction to clear the walls ...
        direction = adjCells[nextCell][1]

        config.leadCell = cellRef.i
        config.cellsCleared.append([config.leadCell, direction])

        if direction == "s":
            cell.s = 0
            cellRef.n = 0

        if direction == "n":
            cell.n = 0
            cellRef.s = 0

        if direction == "e":
            cell.e = 0
            cellRef.w = 0

        if direction == "w":
            cell.w = 0
            cellRef.e = 0

    if len(adjCells) == 0:
        if len(config.cellsCleared) < config.rows * config.cols - len(config.obstacleIndex):
            walkBack()
        elif config.progressive == True:
             time.sleep( config.reDoDelay)
             setupMaze()
    elif config.progressive == False:
        randomWalk()


def reDraw(config):

    config.draw.rectangle((0, 0, config.canvasWidth, config.canvasHeight), fill=config.backgroundFlashcolor)
    n = 0
    w = 0


    wallColor_s = tuple(config.wallColor_s)
    wallColor_n = tuple(config.wallColor_n)
    wallColor_e = tuple(config.wallColor_e)
    wallColor_w = tuple(config.wallColor_w)
    wallColor = tuple(int(i) for i in config.wallColor_w)


    for row in range(0, config.rows):
        for col in range(0, config.cols):

            n = row * config.cols + col

            if n < config.rows * config.cols :
                cell = config.cells[n]
                xPos = cell.col * config.cellSize
                yPos = cell.row * config.cellSize
                # n north
                if cell.n == 1:
                    for l in range(-config.pLines,config.pWalls):
                        config.draw.rectangle((xPos, yPos+l, xPos + config.cellSize, yPos + w + l), fill=wallColor)
                        #config.draw.rectangle((xPos, yPos, xPos + config.cellSize, yPos + w), fill=wallColor)
                # s south
                if cell.s == 1:
                    config.draw.rectangle((xPos, yPos + config.cellSize, xPos + config.cellSize,
                                           yPos + config.cellSize + w), fill=wallColor)
                # w west
                if cell.w == 1:
                    for l in range(-config.pLines,config.pLines):
                        config.draw.rectangle((xPos+l, yPos, xPos + w + l, yPos + config.cellSize), fill=wallColor)
                        #config.draw.rectangle((xPos, yPos, xPos + w, yPos + config.cellSize), fill=wallColor)
                # e east
                if cell.e == 1:
                    config.draw.rectangle((xPos + config.cellSize, yPos, xPos + config.cellSize +
                                           w, yPos + config.cellSize), fill=wallColor)

            if n in config.obstacleIndex:
                config.draw.rectangle((xPos, yPos, xPos + config.cellSize, yPos + config.cellSize), fill=wallColor)

def drawPathsAfter(config):
    xPos = 0
    yPos = 0
    lastRow = 0
    lastCol = 0
    numCells = len(config.cellsCleared)
    subCell = config.cellSize/2/4

    lines = 3

    xPoints = []
    yPoints = []
    xPoints2 = []
    yPoints2 = []


    lineColor_n = (255, 0, 255, 10)
    lineColor_s = (255, 0, 255, 10)
    lineColor_e = (100, 10, 255, 10)
    lineColor_w = (255, 0, 255, 10)

    lineColor_n = (255, 0, 0, 10)
    lineColor_e = (255, 0, 180, 10)
    lineColor_w = (2, 255, 100, 10)
    lineColor_s = (255, 180, 0, 10)

    lineColor_w = tuple(int(i) for i in config.lineColor_w)
    lineColor_s = tuple(int(i) for i in config.lineColor_s)
    lineColor_n = tuple(int(i) for i in config.lineColor_n)
    lineColor_e = tuple(int(i) for i in config.lineColor_e)

    pLines = 1
    for l in range(0, lines):
        xPoints.append(0)
        yPoints.append(0)
        xPoints2.append(0)
        yPoints2.append(0)

    for n in range(0, numCells):
        c = config.cells[config.cellsCleared[n][0]]
        if n == 0:
            xPos = c.col * config.cellSize + config.cellSize/2
            yPos = c.row * config.cellSize + config.cellSize/2
            for p in range(0, lines):
                xPoints[p] = (c.col * config.cellSize + config.cellSize/2 * p)
                yPoints[p] = (c.row * config.cellSize + config.cellSize/2 * p)

        for p in range(0, lines):
            xPoints2[p] = (c.col * config.cellSize + config.cellSize/2 * p)
            yPoints2[p] = (c.row * config.cellSize + config.cellSize/2 * p)

        xPos2 = c.col * config.cellSize + config.cellSize/2
        yPos2 = c.row * config.cellSize + config.cellSize/2

        rowDiff = abs(lastRow - c.row)
        colDiff = abs(lastCol - c.col)

        if (rowDiff > 1 or colDiff > 1) or (rowDiff == colDiff):
            # config.draw.line((xPos, yPos, xPos2, yPos2), fill=(0, 100, 0, 100))
            # config.draw.rectangle((xPos2-2, yPos2-2, xPos2+2, yPos2+2), fill=(0, 255, 0, 100))
            # config.draw.rectangle((xPos-2, yPos-2, xPos+2, yPos+2), fill=(0, 255, 0, 100))
            pass
        else:
            # config.draw.ellipse((xPos - config.cellSize/2, yPos- config.cellSize/2, xPos + config.cellSize/2, yPos + config.cellSize/2), fill=None, outline=(0, 100, 0, 100))
            # config.draw.ellipse((xPos - config.cellSize/4, yPos- config.cellSize/4, xPos + config.cellSize/4, yPos + config.cellSize/4), fill=None, outline=(0, 100, 0, 100))
            # for p in range(0, lines):
            # config.draw.line((xPoints[p], yPoints[p], xPoints2[p], yPoints2[p]), fill=(0, 200, 20, 100))
            if config.cellsCleared[n][1] == "n":
                for l in range(-config.pLines,config.pLines):
                    config.draw.line((xPos+l, yPos, xPos2+l, yPos2), fill=lineColor_n)
                if config.pLines == 0 :
                    l = 0
                    config.draw.line((xPos+l, yPos, xPos2+l, yPos2), fill=lineColor_n)


            if config.cellsCleared[n][1] == "s" :
                for l in range(-config.pLines,config.pLines):
                    config.draw.line((xPos+l, yPos, xPos2+l, yPos2), fill=lineColor_s)
                if config.pLines == 0 :
                    l = 0
                    config.draw.line((xPos+l, yPos, xPos2+l, yPos2), fill=lineColor_s)


            if config.cellsCleared[n][1] == "e" :
                for l in range(-config.pLines,config.pLines):
                    config.draw.line((xPos, yPos+l, xPos2, yPos2+l), fill=lineColor_e)
                if config.pLines == 0 :
                    l = 0
                    config.draw.line((xPos, yPos+l, xPos2, yPos2+l), fill=lineColor_e)


            if config.cellsCleared[n][1] == "w" :
                for l in range(-config.pLines,config.pLines):
                    config.draw.line((xPos, yPos+l, xPos2, yPos2+l), fill=lineColor_w)
                if config.pLines == 0 :
                    l = 0
                    config.draw.line((xPos, yPos+l, xPos2, yPos2+l), fill=lineColor_w)


        xPos = xPos2
        yPos = yPos2
        for p in range(0, lines):
            xPoints[p] = xPoints2[p]
            yPoints[p] = yPoints2[p]

        lastRow = c.row
        lastCol = c.col



def drawPaths(config):
    xPos = 0
    yPos = 0
    lastRow = 0
    lastCol = 0
    numCells = len(config.cellsCleared)

    lines = 3

    xPoints = []
    yPoints = []
    xPoints2 = []
    yPoints2 = []
    for l in range(0, lines):
        xPoints.append(0)
        yPoints.append(0)
        xPoints2.append(0)
        yPoints2.append(0)

    for n in range(0, numCells):
        c = config.cells[config.cellsCleared[n][0]]
        if n == 0:
            xPos = c.col * config.cellSize + config.cellSize/2
            yPos = c.row * config.cellSize + config.cellSize/2
            for p in range(0, lines):
                xPoints[p] = (c.col * config.cellSize + config.cellSize/2 * p)
                yPoints[p] = (c.row * config.cellSize + config.cellSize/2 * p)

        for p in range(0, lines):
            xPoints2[p] = (c.col * config.cellSize + config.cellSize/2 * p)
            yPoints2[p] = (c.row * config.cellSize + config.cellSize/2 * p)

        xPos2 = c.col * config.cellSize + config.cellSize/2
        yPos2 = c.row * config.cellSize + config.cellSize/2

        rowDiff = abs(lastRow - c.row)
        colDiff = abs(lastCol - c.col)

        if (rowDiff > 1 or colDiff > 1) or (rowDiff == colDiff):
            config.draw.line((xPos, yPos, xPos2, yPos2), fill=(0, 100, 0, 100))
        else:
            # for p in range(0, lines):
                # config.draw.line((xPoints[p], yPoints[p], xPoints2[p], yPoints2[p]), fill=(0, 200, 20, 100))
            if config.cellsCleared[n][1] == "n" :
                config.draw.line((xPos, yPos, xPos2, yPos2), fill=(255, 0, 0, 100))
            if config.cellsCleared[n][1] == "s" :
                config.draw.line((xPos, yPos, xPos2, yPos2), fill=(255, 255, 0, 100))
            if config.cellsCleared[n][1] == "e" :
                config.draw.line((xPos, yPos, xPos2, yPos2), fill=(255, 0, 255, 100))
            if config.cellsCleared[n][1] == "w" :
                config.draw.line((xPos, yPos, xPos2, yPos2), fill=(2, 255, 255, 100))


        xPos = xPos2
        yPos = yPos2
        for p in range(0, lines):
            xPoints[p] = xPoints2[p]
            yPoints[p] = yPoints2[p]

        lastRow = c.row
        lastCol = c.col


def iterate():
    global config
    config.draw.rectangle((0, 0, config.canvasWidth, config.canvasHeight), fill=config.backgroundColor)

    if config.progressive == True :
        randomWalk()
    reDraw(config)
    drawPathsAfter(config)
    #drawPaths(config)

    # Do the final rendering of the composited image
    config.render(config.image, 0, 0, config.canvasWidth, config.canvasHeight)


def runWork():
    global config
    print(bcolors.OKGREEN + "** " + bcolors.BOLD)
    print("Running maze.py")
    print(bcolors.ENDC)
    while config.isRunning == True:
        config.directorController.checkTime()
        if config.directorController.advance == True:
            iterate()
        time.sleep(config.redrawSpeed)
        if config.standAlone == False:
            config.callBack()
