import gc
import math
import random
import textwrap
import time
from modules.configuration import bcolors
import PIL.Image
import PIL.ImageTk
from modules import colorutils
from PIL import Image, ImageDraw, ImageFont, ImageTk

"""""" """""" """""" """""" """""" """""" """""" """""" """""" """""" ""

# scroll speed and steps per cycle
scrollSpeed = 0.0006
stroopSpeed = 0.1
steps = 2
stroopSteps = 2
fontSize = 14
vOffset = -1
opticalOpposites = True
higherVariability = False
verticalBg = False
verticalBgColor = (0, 0, 0)
# countLimit = 6
count = 0
blocks = []

# Number of blocks that can chage at once
simulBlocks = 6

# B/W or COLOR
colorMode = True

# To produce cascade effect
nextRow = 0

# For video out
x = y = 0

class Director:
    """docstring for Director"""

    slotRate = 0.5

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



"""""" """""" """""" """""" """""" """""" """""" """""" """""" """""" ""


class Block:

    direction = "down"
    color = (255, 0, 0)
    bgColor = (0, 255, 255)
    speed = 2
    speedMultiplier = 4
    x = 0
    y = 0
    dx = -1
    dy = 0
    startx = 0
    starty = 0
    endx = 0
    endy = 0

    reveal = 0
    revealSpeed = 3
    revealSpeedMax = 6
    revealSpeedMin = 6

    colorWord = "RED"
    colorOfWord = (0, 0, 0)
    directionStr = "Left"

    setForRemoval = False

    # Options are reveal, revealmove, move
    movementMode = "reveal"

    orientation = 1

    def __init__(self, iid=0):
        self.iid = iid

    def remove(self, arrayList):
        arrayList.remove(self)

    def make(self, colorMode=True, nextRow=-1):

        config = self.config
        choice = round(random.uniform(1, len(config.wordsList)))
        brightness = config.brightness
        brightness = random.uniform(
            self.config.minBrightness, self.config.brightness + 0.1
        )
        opticalOpposites = False if (random.random() > 0.5) else True
        self.verticalTileSize = round(config.screenHeight / self.displayRows) if self.displayRows != config.rows else config.tileSize[1]
        self.verticalTileSize = 32

        listToUse = config.wordsList
        if colorMode != True:
            choice = round(random.uniform(1, len(config.wordsList)))

        if config.mode == "colors":
            choice = round(random.uniform(1, len(config.colorList)))
            listToUse = config.colorList



        # choice = 3 if (random.random() > .5) else 5
        # choice = 4 if (random.random() > .5) else 6
        # choice = 9

        if choice == 1:
            colorWord, colorOfWord = listToUse[0], (255, 0, 225)
        if choice == 2:
            colorWord, colorOfWord = listToUse[1], (230, 225, 0)
        if choice == 3:
            colorWord, colorOfWord = listToUse[2], (0, 255, 0)
        if choice == 4:
            colorWord, colorOfWord = listToUse[3], (225, 100, 0)
        if choice == 5:
            colorWord, colorOfWord = listToUse[4], (255, 0, 0)
        if choice == 6:
            colorWord, colorOfWord = listToUse[5], (0, 0, 200)
        if choice == 7:
            colorWord, colorOfWord = listToUse[6], (50, 50, 50)
        if choice == 8:
            colorWord, colorOfWord = listToUse[7], (255, 255, 255)
        if choice == 9:
            colorWord, colorOfWord = listToUse[8], (0, 0, 0)
        if choice > 9:
            colorWord, colorOfWord = listToUse[choice-1], (255, 0, 0)

        self.colorWord = colorWord

        # print(colorWord)

        clr = colorOfWord

        # Draw Background Color
        # Optical (RBY) or RGB opposites

        bgColor = tuple(round(a * brightness) for a in ((200, 200, 200)))
        if opticalOpposites:
            if colorWord == "RED":
                bgColor = tuple(round(a * brightness) for a in ((255, 0, 0)))
            if colorWord == "GREEN":
                bgColor = tuple(round(a * brightness) for a in ((0, 255, 0)))
            if colorWord == "BLUE":
                bgColor = tuple(round(a * brightness) for a in ((0, 0, 255)))
            if colorWord == "YELLOW":
                bgColor = tuple(round(a * brightness) for a in ((255, 255, 0)))
            if colorWord == "ORANGE":
                bgColor = tuple(round(a * brightness) for a in ((255, 125, 0)))
            if colorWord == "VIOLET":
                bgColor = tuple(round(a * brightness) for a in ((200, 0, 255)))
            if colorWord == "BLACK":
                bgColor = tuple(round(a * brightness) for a in ((0, 0, 0)))
            if colorWord == "WHITE":
                bgColor = tuple(round(a * brightness) for a in ((250, 250, 250)))
            if colorWord == "GRAY":
                bgColor = tuple(round(a * brightness) for a in ((200, 200, 200)))
        else:
            bgColor = colorutils.colorCompliment(clr, brightness)

        if config.mode == "words":
       	    _bgColor = colorutils.getRandomColorHSV(0, 360, .4, 1.0, .5, 1.0)
            bgColor = (round(_bgColor[0] * brightness),round(_bgColor[1] * brightness),round(_bgColor[2] * brightness),round(_bgColor[3] * 1.0))

        clr = tuple(round(a * brightness) for a in (clr))

        # Setting 2 fonts - one for the main text and the other for its "border"... not really necessary
        font = ImageFont.truetype(
            config.path + "/assets/fonts/freefont/FreeSansBold.ttf", self.fontSize
        )
        font2 = ImageFont.truetype(
            config.path + "/assets/fonts/freefont/FreeSansBold.ttf", self.fontSize
        )

        pixLen = config.draw.textsize(colorWord, font=font)

        dims = [pixLen[0], pixLen[1]]
        if dims[1] < self.verticalTileSize:
            dims[1] = self.verticalTileSize + 4


        vPadding = 5
        hPadding = 5


        if random.random() < config.verticalOrientationProb:
            self.orientation = 0

        if self.orientation == 1:
            self.presentationImage = PIL.Image.new("RGBA", (dims[0] + hPadding, dims[1]+ vPadding))
            self.image = PIL.Image.new("RGBA", (dims[0] + vPadding, 1))
        else:
            self.presentationImage = PIL.Image.new("RGBA", (dims[1] + vPadding, round(dims[0]*1.5)))
            self.image = PIL.Image.new("RGBA", (dims[0] + vPadding, 1))

        draw = ImageDraw.Draw(self.presentationImage)
        iid = self.image.im.id


        #print(("vPadding:{} orientation:{} vert:{}").format(vPadding,self.orientation,dims[1] ))

        if self.orientation == 1:
            draw.rectangle((0, 0, dims[0] + hPadding, dims[1] + vPadding), fill=bgColor)

            # Draw the text with "borders"
            indent = round(0.05 * config.tileSize[0])

            for i in range(1, self.shadowSize):
                draw.text((indent + -i, -i), colorWord, (0, 0, 0), font=font2)
                draw.text((indent + i, i), colorWord, (0, 0, 0), font=font2)
            draw.text((indent + 0, 0), colorWord, clr, font=font)

        else:

            draw.rectangle((0, 0, dims[1] - 5, round(dims[0]*1.5)), fill=bgColor)
            counter = 0
            # Generate vertical text

            for letter in colorWord:
                # rough estimate to create vertical text
                xD = 2
                # "kerning ... hahhaha ;) "
                if letter == "I":
                    xD = 6 * int(self.fontSize / 30)

                # Draw the text with "borders"
                indent = xD

                for i in range(1, self.shadowSize):
                    draw.text(
                        (indent + -i, -i + counter * (self.fontSize - 1)),
                        letter,
                        (0, 0, 0),
                        font=font2,
                    )
                    draw.text(
                        (indent + i, i + counter * (self.fontSize - 1)),
                        letter,
                        (0, 0, 0),
                        font=font2,
                    )
                draw.text((xD, counter * (self.fontSize - 1)), letter, clr, font=font)
                counter += 1

        if nextRow == -1:
            vOffset = round(random.uniform(0, self.displayRows)) * self.verticalTileSize
        else:
            vOffset = nextRow * self.verticalTileSize

        if config.higherVariability:
            vOffset += round(
                random.uniform(-config.tileSize[0] * 2, config.tileSize[0] * 2)
            )
            vOffset = round(random.uniform(0, config.screenHeight))

        self.wd = dims[0]
        self.ht = dims[1]

        self.y = vOffset
        # self.y = round(random.uniform(0,config.screenHeight))
        self.x = round(random.uniform(-self.wd / 2, config.screenWidth - self.wd / 2))
        # self.x = config.screenWidth/2

        self.startx = self.x
        self.starty = self.y

        self.dx = round(random.uniform(-self.speed, self.speed)) * self.speedMultiplier
        self.dy = round(random.uniform(-self.speed, self.speed)) * self.speedMultiplier

        if self.dx == 0:
            self.dx = -1
        if self.dy == 0:
            self.dy = -1

        self.endx = -self.wd if self.dx < 0 else config.screenWidth
        self.endy = -self.ht if self.dy < 0 else config.screenHeight

        self.revealSpeed = round(random.uniform(self.revealSpeedMin, self.revealSpeedMax))

        if self.orientation == 0:
            self.revealSpeed = self.revealSpeedMax * 2

    def callBack(self):
        self.setForRemoval = True
        pass

    def move(self):
        if self.setForRemoval != True:
            self.image.paste(self.presentationImage, (0, 0))

            self.x += self.dx
            self.y += self.dy

            if self.dy > 0 and self.y >= self.endy:
                self.callBack()
            if self.dy < 0 and self.y < self.endy:
                self.callBack()
            if self.dx > 0 and self.x >= self.endx:
                self.callBack()
            if self.dx < 0 and self.x < self.endx:
                self.callBack()

    def appear(self):
        dims = self.presentationImage.size
        if self.setForRemoval != True:
            self.reveal += self.revealSpeed
            self.image = PIL.Image.new("RGBA", (dims[0], self.reveal))

            # dr = ImageDraw.Draw(self.image)
            # dr.rectangle((0,0,100,5), fill=(0,255,0))

            segment = self.presentationImage.crop((0, 0, dims[0], self.reveal))
            self.image.paste(segment, (0, 0), segment)

            if self.orientation == 1:
                if self.reveal > dims[1]:
                    self.callBack()
            else:
                if self.reveal > dims[1]*2:
                    self.callBack()
                # prround(self.colorWord, self.reveal, self.revealSpeed, self.image.size, dims)

    def update(self):
        if self.movementMode == "reveal" or self.movementMode == "revealmove":
            self.appear()
        if self.movementMode == "move" or self.movementMode == "revealmove":
            self.move()


"""""" """""" """""" """""" """""" """""" """""" """""" """""" """""" ""

# Create each display block and add to the global array of blocks


def makeBlock():
    global config, workConfig, blocks, colorMode, nextRow

    if random.random() < config.moveProbability:
        config.movementMode = "revealmove"
    if random.random() > 0.95:
        config.movementMode = "reveal"

    config.opticalOpposites = True

    block = Block()
    block.config = config
    block.fontSize = round(random.uniform(config.fontSizeMin,config.fontSizeMax))
    block.shadowSize = config.shadowSize
    block.displayRows = config.displayRows
    block.displayCols = config.displayCols
    block.movementMode = config.movementMode
    block.speedMultiplier = config.speedMultiplier
    block.revealSpeedMin = config.revealSpeedMin
    block.revealSpeedMax = config.revealSpeedMax
    block.make(colorMode, nextRow)
    block.blocksRef = blocks

    blocks.append(block)

    nextRow = nextRow + 1 if (nextRow <= config.displayRows) else 0

    # Not really sure the garbage collection works ...
    gc.collect()

    if colorMode == False:
        if random.random() < config.colorProbabilityReturn:  # .92
            colorMode = True
            # prround("ColorMode changed back")
    else:
        if random.random() < config.colorProbability:  # .985
            colorMode = False
            # prround("ColorMode change  to b/w")


"""""" """""" """""" """""" """""" """""" """""" """""" """""" """""" ""


def runStroop(run=True):
    global config, opticalOpposites
    while run:
        numRuns = round(random.uniform(2, 6))
        numRuns = 1
        for i in range(0, numRuns):
            opticalOpposites = False if (opticalOpposites == True) else True
            stroopSequence()


"""""" """""" """""" """""" """""" """""" """""" """""" """""" """""" ""


def getDirection():
    d = round(random.uniform(1, 4))
    direction = "Left"
    if d == 1:
        direction = "Left"
    if d == 2:
        direction = "Right"
    if d == 3:
        direction = "Bottom"
    return direction


"""""" """""" """""" """""" """""" """""" """""" """""" """""" """""" ""


def main(run=True):
    global config, workConfig, blocks, simulBlocks

    print("Stroop2 What Color Loaded")
    simulBlocks = int(workConfig.get("stroop", "simulBlocks"))
    config.vOffset = int(workConfig.get("stroop", "vOffset"))
    config.stroopSpeed = float(workConfig.get("stroop", "stroopSpeed"))
    config.stroopSteps = float(workConfig.get("stroop", "stroopSteps"))
    config.fontSizeMin = int(workConfig.get("stroop", "fontSizeMin"))
    config.fontSizeMax = int(workConfig.get("stroop", "fontSizeMax"))
    config.shadowSize = int(workConfig.get("stroop", "shadowSize"))
    config.higherVariability = workConfig.getboolean("stroop", "higherVariability")
    config.verticalBg = workConfig.getboolean("stroop", "verticalBg")
    config.displayRows = int(workConfig.get("stroop", "displayRows"))
    config.displayCols = int(workConfig.get("stroop", "displayCols"))
    config.movementMode = workConfig.get("stroop", "movementMode")
    config.speedMultiplier = int(workConfig.get("stroop", "speedMultiplier"))
    config.revealSpeedMax = int(workConfig.get("stroop", "revealSpeedMax"))
    config.revealSpeedMin = int(workConfig.get("stroop", "revealSpeedMin"))
    config.moveProbability = float(workConfig.get("stroop", "moveProbability"))
    config.colorProbability = float(workConfig.get("stroop", "colorProbability"))
    config.verticalOrientationProb = float(workConfig.get("stroop", "verticalOrientationProb"))
    config.wordsList = (workConfig.get("stroop", "wordsList")).split(",")

    # managing speed of animation and framerate
    config.directorController = Director(config)

    try:
        config.delay = float(workConfig.get("stroop", "delay"))
    except Exception as e:
        print(str(e))
        config.delay = 0.01
    try:
        config.directorController.slotRate = float(
            workConfig.get("stroop", "slotRate")
        )
    except Exception as e:
        print(str(e))
        print("SHOULD ADJUST TO USE slotRate AS FRAMERATE ")
        config.directorController.slotRate = 0.03

    config.colorProbabilityReturn = float(workConfig.get("stroop", "colorProbabilityReturn"))
    config.modeChangeProb = float(workConfig.get("stroop", "modeChangeProb"))
    config.colorList = ["RED", "GREEN", "BLUE", "YELLOW", "ORANGE", "VIOLET", "BLACK", "WHITE", "GRAY"]
    config.mode = "words"
    # for attr, value in config.__dict__.iteritems():print (attr, value)
    blocks = []
    for i in range(0, simulBlocks):
        makeBlock()

    if run:
        runWork()


"""""" """""" """""" """""" """""" """""" """""" """""" """""" """""" ""


def runWork():
    global config
    print(bcolors.OKGREEN + "** " + bcolors.BOLD)
    print("RUNNING adwords.py")
    print(bcolors.ENDC)

    while config.isRunning == True:
        config.directorController.checkTime()
        if config.directorController.advance == True:
            iterate()
        time.sleep(config.delay)
        if config.standAlone == False:
            config.callBack()


"""""" """""" """""" """""" """""" """""" """""" """""" """""" """""" ""


def iterate(n=0):
    global config, blocks, x, y
    for n in range(0, len(blocks)):
        block = blocks[n]
        config.render(
            block.image,
            block.x,
            block.y,
            block.image.size[0],
            block.image.size[1],
            False,
            False,
            False,
        )

        if config.rendering == "out":
            # config.image = block.image.copy()
            try:
                config.image.paste(block.image, (block.x, block.y), block.image)
            except:
                config.image.paste(block.image, (block.x, block.y))

        # config.image = PIL.Image.new("RGBA", (block.image.size[0], block.image.size[1]))
        # config.image.paste(block.image, (0,0), block.image)
        # x = block.x
        # y = block.y

        block.update()
        if block.setForRemoval == True:
            block.update()
            makeBlock()

    # cleanup the list
    blocks[:] = [block for block in blocks if block.setForRemoval != True]
    if config.rendering == "hub":
        config.updateCanvas()
    # if(config.rendering == "out") : config.image = config.renderImageFull.copy()

    if len(blocks) == 0:
        exit()
    '''
    '''
    if random.random() < config.modeChangeProb:
        if config.mode == "words":
            config.mode = "colors"
        else:
            config.mode = "words"


"""""" """""" """""" """""" """""" """""" """""" """""" """""" """""" ""


def callBack():
    global config
    pass


"""""" """""" """""" """""" """""" """""" """""" """""" """""" """""" ""
