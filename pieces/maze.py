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

#############################################

def newSolverColor(arg=0, adj=1.0):

    cp = config.colorPalettes[0]
    avgVal = (cp.lines_minValue + cp.lines_maxValue)/2

    color =  colorutils.getRandomColorHSV(
        arg,
        arg,
        1.0,
        1.0,
        config.L  * adj,
        config.L  * adj,
        cp.bg_dropHueMinValue,
        cp.bg_dropHueMaxValue,
        round(random.uniform(cp.bg_minAlpha, cp.bg_maxAlpha))
    )
    return (round(color[0] ), round(color[1] ), round(color[2] ), color[3] )


def setSolvePathColors():
    config.okColor = newSolverColor(120)
    config.failColor = newSolverColor(0)
    config.infoColor = newSolverColor(40)
    config.infoColor2 = newSolverColor(180)

    # print(("okColor = {}  failColor = {}").format(config.okColor,config.failColor))


def newColor(arg=0, val=1):

    cp = config.colorPalettes[arg]

    color =  colorutils.getRandomColorHSV(
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

    return (round(color[0] * val), round(color[1] * val), round(color[2] * val), color[3] )


def newColorAlt(arg=0, val=1):
    cp = config.colorPalettes[arg]

    color =  colorutils.getRandomColorHSV(
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

    return (round(color[0] * val), round(color[1] * val), round(color[2] * val), color[3] )


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

    config.saveImages = (workConfig.getboolean("forms", "saveImages"))
    config.outPutPath = workConfig.get("forms", "outPutPath")

    config.pathValueAugment = float(workConfig.get("forms", "pathValueAugment"))

    # config.okColor = tuple(int(i) for i in (workConfig.get("forms", "okColor")).split(","))
    # config.failColor = tuple(int(i) for i in (workConfig.get("forms", "failColor")).split(","))
    # config.infoColor = tuple(int(i) for i in (workConfig.get("forms", "infoColor")).split(","))
    # config.infoColor2 = tuple(int(i) for i in (workConfig.get("forms", "infoColor2")).split(","))

    config.recursionCount = 0
    setupMaze()


def writeImage(renderImage, callBack):
    #baseName = "outputquad3/comp2_"
    currentTime = time.time()
    baseName = config.outPutPath + str(currentTime)
    fn = baseName+".png"
    renderImage.save(fn)
    callBack()


def drawLine(cellRefDirection,xPos,yPos,xPos2,yPos2,fillColor):
    correction = config.pLines - 1

    if cellRefDirection == "n":
        for l in range(-config.pLines,config.pLines):
            config.draw.line((xPos + l, yPos, xPos2 + l, yPos2), fill=fillColor[0])
        if config.pLines == 0 :
            l = 0
            config.draw.line((xPos + l, yPos, xPos2 + l, yPos2), fill=fillColor[0])


    if cellRefDirection == "s" :
        for l in range(-config.pLines,config.pLines):
            config.draw.line((xPos + l, yPos, xPos2 + l, yPos2), fill=fillColor[1])
        if config.pLines == 0 :
            l = 0
            config.draw.line((xPos + l, yPos, xPos2 + l, yPos2), fill=fillColor[1])


    if cellRefDirection == "e" :
        for l in range(-config.pLines,config.pLines):
            config.draw.line((xPos - correction - 1, yPos + l, xPos2 + correction , yPos2 + l), fill=fillColor[2])
        if config.pLines == 0 :
            l = 0
            config.draw.line((xPos, yPos + l, xPos2, yPos2 + l), fill=fillColor[2])


    if cellRefDirection == "w" :
        for l in range(-config.pLines,config.pLines):
            config.draw.line((xPos + correction, yPos + l, xPos2 - correction - 1, yPos2 + l), fill=fillColor[3])
        if config.pLines == 0 :
            l = 0
            config.draw.line((xPos, yPos + l, xPos2, yPos2 + l), fill=fillColor[3])

#############################################


def solveForL(r,g,b) :
    L  = math.sqrt(0.299 * math.pow(r/255,2) + 0.587 * math.pow(g/255,2) + 0.114 * math.pow(b/255,2))
    return L


def setupMaze():

    config.doneMakingMaze = False
    config.hidePath = True
    config.solved = False
    config.debug = False
    config.fixedStart = True
    config.imageWasWritten = False

    config.directorController.slotRate = config.slotRateMaker

    config.delayTimer = Director(config)
    config.slotRate = config.reDoDelay

    config.cellsCleared = []
    config.cellsWalked = []
    config.decisionCells = []
    config.bridgeCells = []
    config.cells = []

    config.cellSize = round(random.uniform(config.cellSizeMin,config.cellSizeMax))


    pLinesMax = config.pLinesMax
    pWallsMax = config.pWallsMax

    if config.cellSize < 12 :
        pLinesMax = 3
        pWallsMax = 3

    config.pLines = round(random.uniform(config.pLinesMin,pLinesMax))
    config.pWalls = round(random.uniform(config.pWallsMin,pWallsMax))
    config.hidePath = True if random.random() < .1 else False

    config.backgroundColor = newColor()

    print(config.backgroundColor)

    r = config.backgroundColor[0]
    g = config.backgroundColor[1]
    b = config.backgroundColor[2]

    config.L  = solveForL(r,g,b) * config.pathValueAugment

    print(config.L )

    # cp = config.colorPalettes[0]
    # cp.lines_minValue = config.L
    # cp.lines_maxValue = config.L


    # sqrt( 0.299*R^2 + 0.587*G^2 + 0.114*B^2 )

    config.wallColor_w = newColorAlt()
    config.wallColor_n = newColorAlt()
    config.wallColor_s = newColorAlt()
    config.wallColor_e = newColorAlt()

    config.lineColor_w = newColorAlt()
    config.lineColor_n = newColorAlt()
    config.lineColor_s = newColorAlt()
    config.lineColor_e = newColorAlt()

    print(config.wallColor_w )



    # config.cellSize = 20
    # config.debug = True
    # config.pLines = 0
    # config.pWalls = 0
    # config.hidePath = True

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
            # _c.wallColor = tuple(int(i) for i in config.wallColor_w)
            _c.wallColor = tuple(int(i) for i in config.backgroundColor)
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
    print("Building Maze")
    # print(("Cell size: {}").format(config.cellSize))
    # print(("Rows {}  Cols {}  ").format(config.rows, config.cols))
    # print(("Initial Cell: {}").format(config.leadCell))
    # print(("Finals Cell: {}").format(config.endCell))
    # print(("background:  {}").format(config.backgroundColor))
    # print(("wallColor_w:  {}").format(config.wallColor_w))


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
    # this seems to make more complicated mazes with more
    # chance for false paths vs picking up at last open cell
    # for i in range(len(config.cellsCleared)-1, 0, -1):
    # so start at beginning - a bit slower but maybe better
    for i in range(0,len(config.cellsCleared)):
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

    cell.wallColor = tuple(int(i) for i in config.wallColor_w)

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

        # if random.random() < .25 :
        #     cell.n = 0
        #     cellRef.s = 0


    if len(adjCells) == 0:
        totalCellsToClear  = config.rows * config.cols - len(config.obstacleIndex) - 1
        if len(config.cellsCleared) < totalCellsToClear:
            if config.debug  == True:
                print(("Cleared {}   {}").format( len(config.cellsCleared), totalCellsToClear))
            walkBack()
        elif config.progressive == True:
            config.doneMakingMaze == True
            if config.saveImages == True and config.imageWasWritten == False :
                writeImage(config.image,startSolving)
                config.imageWasWritten = True
            else :
                startSolving()
    # elif config.progressive == False:
    #     randomWalk()

#############################################


def addBridgePoints(indexA = 0, indexB = 0, val = 0) :
    rowDiff = abs(config.cells[indexA].row - config.cells[indexB].row)
    colDiff = abs(config.cells[indexA].col - config.cells[indexB].col)

    if (rowDiff > 1 or rowDiff > 1 or (rowDiff == 1 and colDiff ==1)) :
        if config.debug == True : print(rowDiff, colDiff)
    else :
        config.bridgeCells.append([indexA,indexB,val])


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

    elif config.solved == False :
        if config.debug == True :
            print(("leadCellInit {} n={} s={} e={} w={}").format(cell.i,cell.n,cell.s,cell.e,cell.w))

        if cell.i not in config.cellsWalked :
            config.cellsWalked.append(cell.i)
            cell.wallColor = tuple(int(i) for i in config.wallColor_w)

            # assume this is an ok path for now
            cell.pathok = 0

            # see if there is anything ahead that is ok
            availables = (getAdjacentOpenCells(cell.i))

            # if at least one choice
            if len(availables) > 0 :
                choice = random.choice(availables)
                config.leadSolverCell = choice[0]
                # shows more than one choice avail
                if len(availables) > 1 :
                    cell.pathok = 2
                    config.decisionCells.append(cell.i)

                # config.bridgeCells.append([cell.i,choice[0],0])
                addBridgePoints(cell.i,choice[0],0)

                # otherwise mark this cell as a dead end and then
                # walk back to the start of this branch and mark
                # them all as bad paths ..
                # not doeing a recursive solution...
                # solver(choice[0])
            else :
                cell.pathok = 1
                addBridgePoints(cell.i,config.cellsWalked[-2],1)

                if config.debug == True :
                    changeCell = config.cellsWalked.index(cell.i)
                    print(("Some kind of end {}").format(changeCell))
                    print("")

                walkBackCount = 0
                walkBacks = len(config.cellsWalked)
                for x in range(walkBacks-1, 0, -1) :
                    # mark the cells as bad paths
                    if walkBackCount != 0 :
                        config.cells[config.cellsWalked[x]].pathok = 1
                    else:
                        config.cells[config.cellsWalked[x]].pathok = 2

                    if x < walkBacks - 1 and x > 0:
                        # remove/replace any paths that are not good in the stack
                        testArg1 = [config.cellsWalked[x+1],config.cellsWalked[x],0]
                        testArg2 = [config.cellsWalked[x],config.cellsWalked[x+1],0]

                        if (testArg1 in config.bridgeCells) :
                            config.bridgeCells.remove(testArg1)
                            # addBridgePoints(testArg1[0],testArg1[1],1)
                        if (testArg2 in config.bridgeCells) :
                            config.bridgeCells.remove(testArg2)
                            addBridgePoints(testArg2[0],testArg2[1],1)


                    # if at any point in the walkback there is an available cell
                    # to go to, stop the walk back are restart the path following there
                    availables = (getAdjacentOpenCells(config.cellsWalked[x]))
                    walkBackCount +=1

                    if len(availables) > 0 :
                        choice = random.choice(availables)
                        config.leadSolverCell = choice[0]
                        config.cells[config.cellsWalked[x]].pathok = 1
                        # make this bridge a decision marker
                        addBridgePoints(config.cellsWalked[x],choice[0],2)
                        break
        else :
            print(("cant proceed {}").format(cell.i))
            config.solved = True


def drawSolved():
    lastRow =0
    lastCol =0
    lastPoint = len(config.cellsWalked )

    correction = config.pLines - 1

    # for c in config.decisionCells :
    #     config.cells[c].pathok = 4

    for cref in config.bridgeCells :
        c1 = config.cells[cref[0]]
        c2 = config.cells[cref[1]]
        xPos = c1.col * config.cellSize + config.cellSize/2
        yPos = c1.row * config.cellSize + config.cellSize/2
        xPos2 = c2.col * config.cellSize + config.cellSize/2
        yPos2 = c2.row * config.cellSize + config.cellSize/2

        rowDiff = abs(yPos2 - yPos)
        colDiff = abs(xPos2 - xPos)

        dontDraw = 0
        if rowDiff > 0 and colDiff > 0 :
            if config.debug == True :
                print(("SHOULD NOT BE DRAWING ... {}").format(c1))
            dontDraw = 1

        direction = "n"
        if colDiff > 0 :
            direction = "e"
        # config.draw.line((xPos, yPos, xPos2, yPos2), fill=config.infoColor2)


        colors = [config.infoColor2,config.infoColor2,config.infoColor2,config.infoColor2]

        if cref[2] == 0 :
            colors = [config.okColor,config.okColor,config.okColor,config.okColor]
        if cref[2] == 1:
            colors = [config.failColor,config.failColor,config.failColor,config.failColor]

        if dontDraw == 0 :
            drawLine(direction,xPos,yPos,xPos2,yPos2,colors)


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


def startSolving():
    if config.doneMakingMaze == False :
        print("STARTING TO SOLVE")

        for cell in config.cells :
            cell.wallColor = tuple(int(i) for i in config.wallColor_w)

        config.doneMakingMaze = True
        config.imageWasWritten = False
        config.directorController.slotRate = config.slotRateSolver
        config.decisionCells.append(config.leadCellInit)
        config.wallColor_w = newColorAlt()
        r = config.wallColor_w[0]
        g = config.wallColor_w[1]
        b = config.wallColor_w[2]

        config.L  = solveForL(r,g,b) * config.pathValueAugment
        setSolvePathColors()
        # for c in config.cells :
        #     c.wallColor = tuple(int(i) for i in config.backgroundColor)

#############################################

def reDraw(config):

    # if config.doneMakingMaze == False :
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

            drawLine(config.cellsCleared[n][1],xPos,yPos,xPos2,yPos2,[lineColor_n,lineColor_s,lineColor_e,lineColor_w])

        xPos = xPos2
        yPos = yPos2

        lastRow = c.row
        lastCol = c.col

#############################################


def iterate():
    global config
    if config.progressive == True :
        randomWalk()
    reDraw(config)
    drawPathsAfter(config)
    if config.doneMakingMaze == True :
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
                if config.saveImages == True:
                    writeImage(config.image,startSolving)
                    config.imageWasWritten = True
                else :
                    startSolving()
                time.sleep(config.reDoDelay)
                setupMaze()
        time.sleep(config.redrawSpeed)
        if config.standAlone == False:
            config.callBack()

#############################################
