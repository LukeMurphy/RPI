# ################################################### #
import math
import random
import time
from modules.configuration import bcolors
from modules import coloroverlay, colorutils
from PIL import Image, ImageDraw, ImageEnhance, ImageFont, ImageOps

#############################################
class Timeout:
    """docstring for Timeout"""
    delay = 1
    def __init__(self, config):
        super(Timeout, self).__init__()
        self.config = config
        self.advance = False
        self.tT = time.time()

    def checkTime(self):
        if (time.time() - self.tT) >= self.delay:
            self.tT = time.time()
            self.advance = True
        else:
            self.advance = False

    def next(self):
        self.checkTime()


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
    config.slotRateMaker = float(workConfig.get("forms", "slotRateMaker"))
    config.slotRateSolver = float(workConfig.get("forms", "slotRateSolver"))
    config.directorController.slotRate = float(workConfig.get("forms", "slotRateMaker"))

    config.progressive = (workConfig.getboolean("forms", "progressive"))
    config.cellSizeMin = int(workConfig.get("forms", "cellSizeMin"))
    config.cellSizeMax = int(workConfig.get("forms", "cellSizeMax"))

    # col, row

    obstacleIndexVals = (workConfig.get("forms", "obstacleIndex")).split(",")
    config.obstacleIndex = list(int(i) for i in obstacleIndexVals)
    config.reDoDelay = float(workConfig.get("forms", "reDoDelay"))
    config.pWallsMin = int(workConfig.get("forms", "pWallsMin"))
    config.pWallsMax = int(workConfig.get("forms", "pWallsMax"))
    config.pLinesMin = int(workConfig.get("forms", "pLinesMin"))
    config.pLinesMax = int(workConfig.get("forms", "pLinesMax"))
    config.wallColor_s = (workConfig.get("forms", "wallColor_s")).split(",")
    config.wallColor_w = (workConfig.get("forms", "wallColor_w")).split(",")
    config.wallColor_n = (workConfig.get("forms", "wallColor_n")).split(",")
    config.wallColor_e = (workConfig.get("forms", "wallColor_e")).split(",")
    config.lineColor_s = (workConfig.get("forms", "lineColor_s")).split(",")
    config.lineColor_w = (workConfig.get("forms", "lineColor_w")).split(",")
    config.lineColor_n = (workConfig.get("forms", "lineColor_n")).split(",")
    config.lineColor_e = (workConfig.get("forms", "lineColor_e")).split(",")

    config.saveImages = (workConfig.getboolean("forms", "saveImages"))
    config.outPutPath = workConfig.get("forms", "outPutPath")

    config.okColor = (0,150,0,150)
    config.failColor = (255,0,0,150)
    config.infoColor = (255,255,0,150)
    config.infoColor2 = (0,200,100,150)

    config.recursionCount = 0
    setupMaze()


def writeImage(renderImage, callBack):
    #baseName = "outputquad3/comp2_"
    currentTime = time.time()
    baseName = config.outPutPath + str(currentTime)
    fn = baseName+".png"
    renderImage.save(fn)
    callBack()


def setupMaze():

    config.complete = False
    config.hidePath = True
    config.done = False
    config.solved = False
    config.debug = False

    config.directorController.slotRate = config.slotRateMaker

    config.delayTimer = Director(config)
    config.slotRate = config.reDoDelay

    config.cellsCleared = []
    config.cellsWalked = []
    config.decisionCells = []
    config.bridgeCells = []
    config.cells = []

    config.cellSize = round(random.uniform(config.cellSizeMin,config.cellSizeMax))
    config.pLines = round(random.uniform(config.pLinesMin,config.pLinesMax))
    config.pWalls = round(random.uniform(config.pWallsMin,config.pWallsMax))
    config.hidePath = True if random.random() < .1 else False

    config.backgroundColor = newColor()
    config.backgroundFlashcolor = newColor()
    config.wallColor_w = newColorAlt()

    # config.cellSize = 20
    # config.pLines = 0
    # config.pWalls = 0
    # config.hidePath = True
    # config.debug = True
    config.fixedStart = True

    config.rows = round(config.canvasHeight / config.cellSize)
    config.cols = round(config.canvasWidth / config.cellSize)
    config.grid = []

    config.finalPoint = config.cols - 1


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
            _c.pathok = 0
            _c.wallColor = tuple(int(i) for i in config.wallColor_w)
            if _c.i == 0:
                _c.skip = True

            config.cells.append(_c)

    numCells = len(config.cells)

    if config.fixedStart == False :
        config.leadCell = round(random.uniform(0, numCells-1))
        config.leadCellInit = config.leadCell
        config.endCell = round(random.uniform(0, numCells-1))
        while config.leadCell in config.obstacleIndex :
            config.leadCell = round(random.uniform(0, numCells-1))
            config.leadCellInit = config.leadCell

    else :
        # set a fixed start and fixed end
        config.leadCell = config.cols * (config.rows - 1)
        config.leadCellInit = config.leadCell
        config.endCell = config.cols -1
        config.cells[config.endCell].s = 0


    config.leadSolverCell = config.leadCellInit


    # config.leadCell = 50
    print("----------")
    print(("Cell size: {}").format(config.cellSize))
    print(("Rows {}  Cols {}  ").format(config.rows, config.cols))
    print(("Initial Cell: {}").format(config.leadCell))
    print(("Finals Cell: {}").format(config.endCell))
    print(("background:  {}").format(config.backgroundColor))
    print(("wallColor_w:  {}").format(config.wallColor_w))


    randomWalk()

# Recursive backtracker: This will find a solution, but it won't necessarily find the shortest solution.
# It focuses on you, is fast for all types of Mazes, and uses stack space up to the size of the Maze.
# Very simple: If you're at a wall (or an area you've already plotted), return failure, else if you're at the finish,
# return success, else recursively try moving in the four directions. Plot a line when you try a new direction,
# and erase a line when you return failure, and a single solution will be marked out when you hit success.
# When backtracking, it's best to mark the space with a special visited value, so you don't visit it again
# from a different direction. In Computer Science terms this is basically a depth first search. This method
# will always find a solution if one exists, but it won't necessarily be the shortest solution. Note this a
# lgorithm is commonly called "recursive backtracker", although the depth first search it uses only needs
# some form of stack, and doesn't have to use actual recursion.


def solver(n=-1):

    n = config.leadSolverCell
    changeCell = 0

    if len(config.cellsWalked) < 1 :
        config.lastGoodPoint = config.leadCellInit

    if n == -1 :
        cell = config.cells[config.leadCellInit]
    elif n < len(config.cells) :
        cell = config.cells[n]


    if cell.i == config.cols - 1 and config.solved == False :
        if config.debug == True :
            print(("leadCellInit {} n={} s={} e={} w={}").format(cell.i,cell.n,cell.s,cell.e,cell.w))
            print("done")
        config.cellsWalked.append(cell.i)
        config.cellsWalked.append(config.finalPoint)
        config.cells[config.finalPoint].pathok = 3
        config.lastGoodPoint = cell.i
        config.solved = True
        rebuild()
    elif config.solved == False :
        if config.debug == True :
            print(("leadCellInit {} n={} s={} e={} w={}").format(cell.i,cell.n,cell.s,cell.e,cell.w))
        if cell.i not in config.cellsWalked :
            config.cellsWalked.append(cell.i)
            cell.wallColor = tuple(int(i) for i in config.wallColor_w)
            cell.pathok = 0
            availables = (getAdjacentOpenCells(cell.i))

            # at least one choice
            if len(availables) > 0 :
                choice = random.choice(availables)
                config.leadSolverCell = choice[0]
                # shows more than one choice avail
                if len(availables) > 1 :
                    cell.pathok = 2
                    config.decisionCells.append(cell.i)

                config.bridgeCells.append([cell.i,choice[0]])

                # not doeing a recursive solution...
                #solver(choice[0])
            else :
                cell.pathok = 1
                changeCell = config.cellsWalked.index(cell.i)

                if config.debug == True :
                    print(("Some kind of end {}").format(changeCell))
                # print("")
                walkBackCount = 0
                for x in range(len(config.cellsWalked)-1, 0, -1) :
                    # mark the cells as bad paths
                    if walkBackCount != 0 :
                        config.cells[config.cellsWalked[x]].pathok = 1
                    else:
                        config.cells[config.cellsWalked[x]].pathok = 2
                    availables = (getAdjacentOpenCells(config.cellsWalked[x]))
                    walkBackCount +=1

                    if len(availables) > 0 :
                        choice = random.choice(availables)
                        config.leadSolverCell = choice[0]
                        config.cells[config.cellsWalked[x]].pathok = 1
                        config.bridgeCells.append([config.cellsWalked[x],choice[0]])

                        if config.debug == True :
                            test = getAdjacentOpenCells(config.leadSolverCell)

                            if len(test) == 0 :
                                print(("LAST end {} (cell index:{})  new lead = {}").format(x,config.cellsWalked[x],config.leadSolverCell ))
                                print(config.cellsWalked)
                            else :
                                print(("ISSUES end {} (cell index:{})  new lead = {}").format(x,config.cellsWalked[x],config.leadSolverCell ))
                                print(test)

                        break
        else :
            print(("cant proceed {}").format(cell.i))


def drawSolved():
    lastRow =0
    lastCol =0
    lastPoint = len(config.cellsWalked )

    for c in config.decisionCells :
        config.cells[c].pathok = 4

    for cref in config.bridgeCells :
        c1 = config.cells[cref[0]]
        c2 = config.cells[cref[1]]
        xPos = c1.col * config.cellSize + config.cellSize/2
        yPos = c1.row * config.cellSize + config.cellSize/2
        xPos2 = c2.col * config.cellSize + config.cellSize/2
        yPos2 = c2.row * config.cellSize + config.cellSize/2
        config.draw.line((xPos, yPos, xPos2, yPos2), fill=config.infoColor2)

    for c in range(1, lastPoint):

        cell = config.cells[config.cellsWalked[c-1]]
        cell.wallColor = tuple(int(i) for i in config.wallColor_w)
        xPos = cell.col * config.cellSize + config.cellSize/2
        yPos = cell.row * config.cellSize + config.cellSize/2


        cell2 = config.cells[config.cellsWalked[c]]
        cell2.wallColor = tuple(int(i) for i in config.wallColor_w)
        xPos2 = cell2.col * config.cellSize + config.cellSize/2
        yPos2 = cell2.row * config.cellSize + config.cellSize/2

        rowDiff = abs(yPos2 - yPos)
        colDiff = abs(xPos2 - xPos)


        dontDrawLine = True if (rowDiff > config.cellSize or colDiff > config.cellSize) or (rowDiff == config.cellSize and colDiff == config.cellSize) else False

        if (dontDrawLine == False and cell.pathok == 1) :
            config.draw.line((xPos, yPos, xPos2, yPos2), fill=config.failColor)
            config.draw.line((xPos+1, yPos+1, xPos2+1, yPos2+1), fill=(0, 0, 0, 100))
        elif dontDrawLine == False or c == 1 or (config.solved == True and c == lastPoint-1)  :
            config.draw.line((xPos, yPos, xPos2, yPos2), fill=config.okColor)
            config.draw.line((xPos+1, yPos+1, xPos2+1, yPos2+1), fill=(0, 0, 0, 100))
        elif dontDrawLine == False and cell.pathok == 2 :
            config.draw.line((xPos, yPos, xPos2, yPos2), fill=config.infoColor)

        if config.debug == True :
            if cell.pathok == 0 :
                config.draw.rectangle((xPos-2, yPos-2, xPos+2, yPos+2), fill=config.okColor)
            if cell.pathok == 1 :
                config.draw.rectangle((xPos-2, yPos-2, xPos+2, yPos+2), fill=config.failColor)
            if cell.pathok == 2 :
                config.draw.rectangle((xPos-2, yPos-2, xPos+2, yPos+2), fill=config.infoColor)
            if cell.pathok == 4 :
                config.draw.rectangle((xPos-2, yPos-2, xPos+2, yPos+2), fill=config.infoColor2)
        if cell.pathok == 3 :
            config.draw.rectangle((xPos-2, yPos-2, xPos+2, yPos+2), fill=config.okColor)


        lastCol = cell2.col
        lastRow = cell2.row


def getAdjacentOpenCells(n):
    cell = config.cells[n]
    adjacentCells = []
    rowPosition = cell.row
    colPosition = cell.col

    # Bit of a bias here because it favors finding in the order
    # e.g at the start cell it finds North a lot more often first ...

    if cell.n == 0 :
        c = cell.col + config.cols * (cell.row - 1)
        config.cells[c].wallColor = tuple(int(i) for i in config.wallColor_w)
        if c not in config.cellsWalked :
            adjacentCells.append([c,"n"])

    if cell.e == 0 :
        c = (cell.col + 1) + config.cols * (cell.row)
        config.cells[c].wallColor = tuple(int(i) for i in config.wallColor_w)
        if c not in config.cellsWalked :
            adjacentCells.append([c,"e"])

    if cell.s == 0 :
        c = cell.col + config.cols * (cell.row + 1)
        config.cells[c].wallColor = tuple(int(i) for i in config.wallColor_w)
        if c not in config.cellsWalked :
            adjacentCells.append([c,"s"])

    if cell.w == 0 :
        c = (cell.col - 1) + config.cols * (cell.row)
        config.cells[c].wallColor = tuple(int(i) for i in config.wallColor_w)
        if c not in config.cellsWalked :
            adjacentCells.append([c,"w"])

    return adjacentCells


def getAdjacentCells(n):
    cell = config.cells[n]
    adjacentCells = []
    rowPosition = cell.row
    colPosition = cell.col

    # Bit of a bias here because it favors finding in the order
    # e.g at the start cell it finds North a lot more often first ...

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
            config.complete == True
            if config.saveImages == True:
                writeImage(config.image,startSolving)
            else :
                startSolving()
    elif config.progressive == False:
        randomWalk()


def rebuild():
    if config.solved == True :
        print("DOING rebuild")
        # config.solved = False
        # config.done = False
        # reDraw(config)
        # drawPathsAfter(config)
        # config.render(config.image, 0, 0, config.canvasWidth, config.canvasHeight)
        # time.sleep(config.reDoDelay)
        # setupMaze()


        # config.timeOut = Timeout(config)
        # config.timeOut.delay = config.reDoDelay


def startSolving():
    if config.done == False :
        print("STARTING TO SOLVE")
        config.done = True
        config.directorController.slotRate = config.slotRateSolver
        config.decisionCells.append(config.leadCellInit)
        config.wallColor_w = newColorAlt()

        # for c in config.cells :
        #     c.wallColor = tuple(int(i) for i in config.backgroundColor)


def reDraw(config):

    if config.complete == False :
        wallColor_s = tuple(config.wallColor_s)
        wallColor_n = tuple(config.wallColor_n)
        wallColor_e = tuple(config.wallColor_e)
        wallColor_w = tuple(config.wallColor_w)
        wallColor = tuple(int(i) for i in config.wallColor_w)
        config.draw.rectangle((0, 0, config.canvasWidth, config.canvasHeight), fill=config.backgroundColor, outline=wallColor)
        n = 0
        w = 0

        correction = 0 if config.pWalls == 0 else config.pWalls - 1

        for row in range(0, config.rows):
            for col in range(0, config.cols):
                n = row * config.cols + col
                if n < config.rows * config.cols :
                    cell = config.cells[n]
                    xPos = cell.col * config.cellSize
                    yPos = cell.row * config.cellSize
                    # n north
                    if cell.n == 1:
                        for l in range(-config.pWalls, config.pWalls):
                            config.draw.rectangle((xPos, yPos + l + correction, xPos + config.cellSize, yPos + w + l - correction), fill=cell.wallColor)
                            #config.draw.rectangle((xPos, yPos, xPos + config.cellSize, yPos + w), fill=wallColor)
                    # s south
                    if cell.s == 1:
                        config.draw.rectangle((xPos + correction, yPos + config.cellSize, xPos + config.cellSize - correction, yPos + config.cellSize + w), fill=cell.wallColor)
                    # w west
                    if cell.w == 1:
                        for l in range(-config.pWalls, config.pWalls):
                            config.draw.rectangle((xPos + l, yPos - correction, xPos + w + l, yPos + config.cellSize), fill=cell.wallColor)
                            #config.draw.rectangle((xPos, yPos, xPos + w, yPos + config.cellSize), fill=wallColor)
                    # e east
                    if cell.e == 1:
                        config.draw.rectangle((xPos + config.cellSize, yPos, xPos + config.cellSize + w, yPos + config.cellSize), fill=cell.wallColor)

                if n in config.obstacleIndex:
                    config.draw.rectangle((xPos, yPos, xPos + config.cellSize, yPos + config.cellSize), fill=wallColor)

                if cell.pathok == 3 :
                    config.draw.rectangle((xPos, yPos, xPos + config.cellSize, yPos + config.cellSize), fill=config.okColor)


def drawPathsAfter(config):
    xPos = 0
    yPos = 0
    lastRow = 0
    lastCol = 0
    numCells = len(config.cellsCleared)

    lineColor_w = tuple(int(i) for i in config.lineColor_w)
    lineColor_s = tuple(int(i) for i in config.lineColor_s)
    lineColor_n = tuple(int(i) for i in config.lineColor_n)
    lineColor_e = tuple(int(i) for i in config.lineColor_e)

    correction = config.pLines - 1

    if config.hidePath == True :
        lineColor_w = tuple(int(i) for i in config.backgroundColor)
        lineColor_s = tuple(int(i) for i in config.backgroundColor)
        lineColor_n = tuple(int(i) for i in config.backgroundColor)
        lineColor_e = tuple(int(i) for i in config.backgroundColor)


    # startcell
    cRef = config.cells[config.leadCellInit]
    cRefxPos = cRef.col * config.cellSize + config.cellSize/2
    cRefyPos = cRef.row * config.cellSize + config.cellSize/2
    # config.draw.rectangle((cRefxPos-2, cRefyPos-2, cRefxPos+2, cRefyPos+2), fill=(255, 1000, 0, 100))

    for n in range(0, numCells):
        c = config.cells[config.cellsCleared[n][0]]
        if n == 0:
            xPos = c.col * config.cellSize + config.cellSize/2
            yPos = c.row * config.cellSize + config.cellSize/2

        xPos2 = c.col * config.cellSize + config.cellSize/2
        yPos2 = c.row * config.cellSize + config.cellSize/2

        rowDiff = abs(lastRow - c.row)
        colDiff = abs(lastCol - c.col)

        # if n == 0 :
        #     config.draw.line((cRefxPos, cRefyPos, xPos2, yPos2), fill=lineColor_w)

        if (rowDiff > 1 or colDiff > 1) or (rowDiff == colDiff) or n == 0:
            # config.draw.line((xPos, yPos, xPos2, yPos2), fill=(0, 100, 0, 100))
            # config.draw.rectangle((xPos-2, yPos-2, xPos+2, yPos+2), fill=(255, 0, 0, 100))
            # config.draw.rectangle((xPos2-2, yPos2-2, xPos2+2, yPos2+2), fill=(0, 255, 0, 100))
            # config.draw.rectangle((xPos-2, yPos-2, xPos+2, yPos+2), fill=(0, 255, 0, 100))
            pass
        else:
            # config.draw.ellipse((xPos - config.cellSize/2, yPos- config.cellSize/2, xPos + config.cellSize/2, yPos + config.cellSize/2), fill=None, outline=(0, 100, 0, 100))
            # config.draw.ellipse((xPos - config.cellSize/4, yPos- config.cellSize/4, xPos + config.cellSize/4, yPos + config.cellSize/4), fill=None, outline=(0, 100, 0, 100))
            # for p in range(0, lines):

            if config.cellsCleared[n][1] == "n":
                for l in range(-config.pLines,config.pLines):
                    config.draw.line((xPos + l, yPos, xPos2 + l, yPos2), fill=lineColor_n)
                if config.pLines == 0 :
                    l = 0
                    config.draw.line((xPos + l, yPos, xPos2 + l, yPos2), fill=lineColor_n)


            if config.cellsCleared[n][1] == "s" :
                for l in range(-config.pLines,config.pLines):
                    config.draw.line((xPos + l, yPos, xPos2 + l, yPos2), fill=lineColor_s)
                if config.pLines == 0 :
                    l = 0
                    config.draw.line((xPos + l, yPos, xPos2 + l, yPos2), fill=lineColor_s)


            if config.cellsCleared[n][1] == "e" :
                for l in range(-config.pLines,config.pLines):
                    config.draw.line((xPos - correction - 1, yPos + l, xPos2 + correction , yPos2 + l), fill=lineColor_e)
                if config.pLines == 0 :
                    l = 0
                    config.draw.line((xPos, yPos + l, xPos2, yPos2 + l), fill=lineColor_e)


            if config.cellsCleared[n][1] == "w" :
                for l in range(-config.pLines,config.pLines):
                    config.draw.line((xPos + correction, yPos + l, xPos2 - correction - 1, yPos2 + l), fill=lineColor_w)
                if config.pLines == 0 :
                    l = 0
                    config.draw.line((xPos, yPos + l, xPos2, yPos2 + l), fill=lineColor_w)


        xPos = xPos2
        yPos = yPos2

        lastRow = c.row
        lastCol = c.col


def iterate():
    global config
    if config.progressive == True :
        randomWalk()
    reDraw(config)
    drawPathsAfter(config)
    if config.done == True :
        solver()
        drawSolved()
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
            if config.solved == True :
                time.sleep(config.reDoDelay)
                setupMaze()
        time.sleep(config.redrawSpeed)
        if config.standAlone == False:
            config.callBack()
