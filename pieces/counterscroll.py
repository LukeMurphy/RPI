import math
import random
import time

from modules import badpixels, coloroverlay, colorutils
from modules.configuration import bcolors, pieceLogger
from PIL import Image, ImageChops, ImageDraw, ImageEnhance, ImageFont, ImageOps

blocks = []
XOsBlocks = []


# ------------------------------------------------------------------- #
# LEFT means text or icon moves to the left (i.e. comes from the right)
# RIGHT means text or icon moves to the right (i.e. comes from the left)
directionOrder = ["LEFT", "RIGHT"]


# ------------------------------------------------------------------- #

class ScrollMessage:

    # ------------------------------------------------------------------- #

    # scroll speed and steps per cycle
    # ------------------------------------------------------------------- #
    scrollSpeed = 0.004
    steps = 1
    fontSize = 14

    def __init__(self, messageString, direction, config, scrllrMngr, clr=""):
        # pieceLogger ("init: " + messageString)
        self.messageString = messageString
        self.direction = direction

        self.config = config
        self.scrllrMngr = scrllrMngr
        if clr == "":
            if scrllrMngr.colorMode == "getRandomRGB":
                self.clr = colorutils.getRandomRGB()
            if scrllrMngr.colorMode == "randomColor":
                self.clr = colorutils.randomColor()
            if scrllrMngr.colorMode == "getRandomColorWheel":
                self.clr = colorutils.getRandomColorWheel()
        else:
            self.clr = clr
        # self.clr = colorutils.randomColor()
        # self.clr = colorutils.getSunsetColors()

        # if(config.colorOverlay == True) : self.clr = (200,200,200)

        # ------------------------------------------------------------------- #
        # draw the message to get its size
        if scrllrMngr.sansSerif:
            # font = ImageFont.truetype(config.path + "/assets/fonts/freefont/FreeSansBold.ttf", scrllrMngr.fontSize)
            font = ImageFont.truetype(config.path + "/assets/fonts/roboto/RobotoCondensed-Bold.ttf", scrllrMngr.fontSize)
        else:
            font = ImageFont.truetype(
                config.path + "/assets/fonts/freefont/FreeSerifBold.ttf",
                scrllrMngr.fontSize,
            )
        tempImage = Image.new("RGBA", (1200, 196))
        draw = ImageDraw.Draw(tempImage)
        self.pixLen = draw.textbbox((0,0),self.messageString, font=font)
        self.fontHeight = int(self.pixLen[1] * 2)
        pieceLogger("\n\n***************************")
        pieceLogger(self.pixLen)
        pieceLogger(self.messageString)
        pieceLogger(self.fontHeight)
        pieceLogger(self.clr)
        # For some reason textsize is not getting full height !

        # ------------------------------------------------------------------- #
        # make a new image with the right size
        # self.config.renderImage = Image.new("RGBA", (config.actualScreenWidth , config.screenHeight))
        # self.scrollImage = Image.new("RGBA", pixLen)

        self.scrollImage = Image.new("RGBA", (self.pixLen[0] + 2, self.fontHeight))
        self.draw = ImageDraw.Draw(self.scrollImage)
        self.iid = self.scrollImage.im.id

        # ------------------------------------------------------------------- #
        # self.draw.rectangle((0,0,self.pixLen[0]+4, self.pixLen[1]), fill = (0,0,0))
        # Draw the text with "borders"
        indent = int(0.05 * config.tileSize[0])
        for i in range(1, scrllrMngr.shadowSize):
            self.draw.text((indent + -i, -i), self.messageString, (0, 0, 0), font=font)
            self.draw.text((indent + i, i), self.messageString, (0, 0, 0), font=font)

        self.draw.text((2, 0), self.messageString, self.clr, font=font)

        self.xPos = 0
        self.yPos = scrllrMngr.vOffset

        # self.end = config.screenWidth * config.displayRows

    def scroll(self):
        if self.direction == "LEFT":
            self.xPos += scrllrMngr.steps
        else:
            self.xPos -= scrllrMngr.steps

        # if(self.xPos > self.end) :
        #     self.xPos = self.start = -self.scrollImage.size[0]


class XOx:

    # ------------------------------------------------------------------- #

    # scroll speed and steps per cycle
    scrollSpeed = 0.004
    steps = 1.5
    lineThickness = 4
    bufferSpacing = 40
    xsWidth = 54
    maxNumXOs = 12
    minNumXOs = 5
    XColor = [255, 0, 0]
    OColor = [255, 0, 0]
    ArrowColor = [255, 2, 0]

    def __init__(self, direction, config, n, rng, scrllrMngr):
        # pieceLogger ("init: " + messageString)

        self.direction = direction
        self.config = config
        self.scrllrMngr = scrllrMngr
        self.clr = (int(255 * config.brightness), 0, 0)

        self.xsWidth = int(0.85 * scrllrMngr.fontSize)
        self.maxNumXOs = int(self.xsWidth / 2)

        self.xoString = self.makeBlock(scrllrMngr.useArrows)

        prv = n - 1
        nxt = n + 1
        if n < 3:
            if prv < 0:
                prv = 3 - 1
            if nxt == 3:
                nxt = 0
        else:
            if prv < 3:
                prv = rng - 1
            if nxt == rng:
                nxt = 3

        self.prvBlock = prv
        self.nxtBlock = nxt

    def makeBlock(self, dash=False):
        strg = ""

        num = int(random.uniform(self.minNumXOs, self.maxNumXOs))

        for n in range(0, num):
            if dash:
                strg += "-"
            else:
                if random.random() > self.scrllrMngr.oProb:
                    strg += "X"
                else:
                    strg += "O"

        self.width = n * (self.xsWidth + 8)

        if self.direction == "RIGHT":
            self.xPos = self.config.screenWidth + self.scrllrMngr.bufferSpacing
            self.end = -self.width
        else:
            self.xPos = 0
            self.end = self.config.screenWidth * self.scrllrMngr.displayRows
        self.yPos = 0

        return strg

    def drawCounterXO(self):
        ## Try with drawing xo's first then by pasting block ..

        # draw  = ImageDraw.Draw(self.config.renderImageFull)
        draw = ImageDraw.Draw(self.config.canvasImage)
        leng = 0
        for n in range(0, len(self.xoString)):

            startX = self.xPos + n * self.xsWidth + 8
            endX = self.xPos + n * self.xsWidth + self.xsWidth

            startY = 0
            endY = self.xsWidth

            if (self.xoString[n]) == "X":
                clr = (
                    round(self.XColor[0] * config.brightness),
                    round(self.XColor[1] * config.brightness),
                    round(self.XColor[2] * config.brightness),
                )
                draw.line(
                    (startX, startY, endX, endY), fill=clr, width=self.lineThickness
                )
                draw.line(
                    (endX, startY, startX, endY), fill=clr, width=self.lineThickness
                )
            elif (self.xoString[n]) == "O":
                clr = (
                    round(self.OColor[0] * config.brightness),
                    round(self.OColor[1] * config.brightness),
                    round(self.OColor[2] * config.brightness),
                )
                draw.ellipse((startX, startY, endX, endY), outline=clr, width=4)
                draw.ellipse((startX + 1, startY + 1, endX - 1, endY - 1), outline=clr, width=4)
            else:
                clr = (
                    round(self.ArrowColor[0] * config.brightness),
                    round(self.ArrowColor[1] * config.brightness),
                    round(self.ArrowColor[2] * config.brightness),
                )
                y0 = startY + self.xsWidth / 2 + scrllrMngr.arrowOffset
                yA = self.xsWidth / 4 + scrllrMngr.arrowOffset

                if self.direction == "RIGHT":
                    xA = startX + (yA - scrllrMngr.arrowOffset) * math.tan(math.pi / 4)
                    # the horizontal
                    draw.line(
                        (startX, y0, endX, y0), fill=clr, width=self.lineThickness
                    )
                    # the blades
                    draw.line((xA, yA, startX, y0), fill=clr, width=self.lineThickness)
                    draw.line(
                        (xA, yA + self.xsWidth / 2, startX, y0),
                        fill=clr,
                        width=self.lineThickness,
                    )
                else:
                    xA = endX - (yA - scrllrMngr.arrowOffset) * math.tan(math.pi / 4)
                    # the horizontal
                    draw.line(
                        (startX, y0, endX, y0), fill=clr, width=self.lineThickness
                    )
                    # the blades
                    draw.line((xA, yA, endX, y0), fill=clr, width=self.lineThickness)
                    draw.line(
                        (xA, yA + self.xsWidth / 2, endX, y0),
                        fill=clr,
                        width=self.lineThickness,
                    )

            leng += endX - startX

        if self.direction == "RIGHT":
            self.xPos -= self.steps
        else:
            self.xPos += self.steps


class ScrollerManager:
    def __init__(self, config):
        self.config = config

    def setUp(self, workConfig):
        global directionOrder
        config = self.config
        pieceLogger("---------------------")
        pieceLogger("CounterScroll Loaded")
        colorutils.brightness = config.brightness

        self.displayRows = int(workConfig.get("scroll", "displayRows"))
        self.displayCols = int(workConfig.get("scroll", "displayCols"))

        self.canvasImageWidth = int(round(config.canvasWidth * self.displayRows))
        self.canvasImageHeight = int(round(config.canvasHeight / self.displayRows))

        self.fontSize = int(workConfig.get("scroll", "fontSize"))
        self.vOffset = int(workConfig.get("scroll", "vOffset"))
        self.scrollSpeed = float(workConfig.get("scroll", "scrollSpeed"))
        self.steps = int(workConfig.get("scroll", "steps"))
        self.shadowSize = int(workConfig.get("scroll", "shadowSize"))

        self.usingEmoties = workConfig.getboolean("scroll", "usingEmoties")
        self.counterScrollText = workConfig.getboolean("scroll", "counterScrollText")
        self.useXOs = workConfig.getboolean("scroll", "useXOs")
        self.useArrows = workConfig.getboolean("scroll", "useArrows")
        try:
            self.numberOfDeadPixels = int(workConfig.get("scroll", "numberOfDeadPixels"))
            self.arrowOffset = int(workConfig.get("scroll", "arrowOffset"))
            self.overlayX = int(workConfig.get("scroll", "overlayX"))
            self.overlayY = int(workConfig.get("scroll", "overlayY"))
            self.overlayWidth = int(workConfig.get("scroll", "overlayWidth"))
            self.overlayHeight = int(workConfig.get("scroll", "overlayHeight"))

        except Exception as e:
            pieceLogger(str(e))
            self.numberOfDeadPixels = 20
            self.arrowOffset = 0
            self.overlayX = 0
            self.overlayY = 0
            self.overlayWidth = config.screenWidth
            self.overlayHeight = config.screenHeight

        self.sansSerif = workConfig.getboolean("scroll", "sansSerif")
        self.useBlanks = workConfig.getboolean("scroll", "useBlanks")
        self.useThreeD = workConfig.getboolean("scroll", "useThreeD")
        self.directionOrder = workConfig.get("scroll", "directionOrder")
        self.bgColorVals = (workConfig.get("scroll", "bgColor")).split(",")
        self.bgColor = tuple(map(lambda x: int(x), self.bgColorVals))
        self.txt1 = " " + (workConfig.get("scroll", "txt1")) + " "
        self.txt2 = " " + (workConfig.get("scroll", "txt2")) + " "
        self.txtfile = ""
        try:
            self.txtfile = workConfig.get("scroll", "txtfile")
        except Exception as e:
            pieceLogger(str(e))

        self.colorMode = workConfig.get("scroll", "colorMode")
        self.colorOverlay = workConfig.getboolean("scroll", "colorOverlay")

        try:
            self.coloroverlayBackgroundOnly = workConfig.getboolean("scroll", "coloroverlayBackgroundOnly")
        except Exception as e:
            pieceLogger(str(e))
            self.coloroverlayBackgroundOnly = False

        if self.colorOverlay == True:

            self.colorOverlayObjA = coloroverlay.ColorOverlay()
            self.colorOverlayObjB = coloroverlay.ColorOverlay()

            self.colorOverlayObjA.colorTransitionSetup()
            self.colorOverlayObjB.colorTransitionSetup()

            self.colorOverlayObjB.minHue = 180
            self.colorOverlayObjB.maxHue = 180
            self.colorOverlayObjB.minSaturation = .8
            self.colorOverlayObjB.maxSaturation = .99
            self.colorOverlayObjB.minValue = .5
            self.colorOverlayObjB.maxValue = .5
            self.colorOverlayObjB.setStartColor()


            self.colorOverlayObjA.minHue = 0
            self.colorOverlayObjA.maxHue = 360
            self.colorOverlayObjA.minSaturation = .8
            self.colorOverlayObjA.maxSaturation = .99
            self.colorOverlayObjA.minValue = .5
            self.colorOverlayObjA.maxValue = .5
            self.colorOverlayObjA.setStartColor()

            # config.colorA = colorutils.randomColor()
            # config.colorB = colorutils.randomColor()
            # config.currentColor = config.colorA

            # colorTransitionSetup()

        createImageLayers(config, self)

        # ------------------------------------------------------------------- #
        # config.drawBeforeConversion = callBack
        self.actualScreenWidth = config.canvasImage.size[0]

        if self.useBlanks:
            badpixels.numberOfDeadPixels = self.numberOfDeadPixels
            badpixels.sizeTarget = list(config.canvasImageFinal.size)
            pieceLogger(badpixels.sizeTarget)
            badpixels.config = config
            badpixels.setBlanksOnScreen()

        if self.directionOrder == "RIGHT-LEFT":
            directionOrder = ["RIGHT", "LEFT"]

        if self.txtfile != "":
            self.textArray = []
            fh = open("" + self.txtfile, "r")
            lines = fh.readlines()
            self.txt1 = "  "

            # ------------------------------------------------------------------- #
            # not really necessary but maybe need some scrubs

            for text in lines:
                # text = fh.readline()
                self.textArray.append(text.replace("\n", ""))
                self.txt1 = self.txt1 + " -- " + text.replace("\n", "")

            self.txt2 = self.txt1
            self.breaksArray = [i for i, ltr in enumerate(self.txt1) if ltr == "-"]


        self.oProb = 0.5



# ------------------------------------------------------------------- #


def createImageLayers(config, scrllrMngr):
    # ------------------------------------------------------------------- #
    # Used to composite XO's and message text
    # config.canvasImage = Image.new("RGBA", (config.canvasImageWidth, int(config.screenHeight / config.displayRows)))
    config.canvasImage = Image.new(
        "RGBA", (scrllrMngr.canvasImageWidth, scrllrMngr.canvasImageHeight)
    )


    pieceLogger(scrllrMngr.canvasImageHeight)
    # ------------------------------------------------------------------- #
    # Used to be final image sent to renderImageFull after canvasImage has been chopped up and reordered to fit
    config.canvasImageFinal = Image.new(
        "RGBA", (config.canvasWidth, config.canvasHeight)
    )

    """
    if(abs(config.rotation) == 90) :
        #config.canvasImageWidth = config.canvasWidth * config.displayRows
        config.canvasImageFinal = Image.new("RGBA", (config.canvasHeight, config.canvasWidth))
        cw = config.canvasWidth
        ch = config.canvasHeight
    """

    imageWrapLength = config.screenWidth * 50
    config.warpedImage = Image.new("RGBA", (imageWrapLength, config.screenHeight))

    if config.rotation == -90:
        imageWrapLength = config.screenWidth * 50
        config.warpedImage = Image.new("RGBA", (imageWrapLength, config.screenWidth))


def main(run=True):
    global config, scrllrMngr
    global workConfig

    scrllrMngr = ScrollerManager(config)
    scrllrMngr.setUp(workConfig)

    config.directorController = Director(config)
    config.directorController.slotRate = .02

    setUp()

    if run:
        runWork()


# ------------------------------------------------------------------- # ""


def makeBlock(n, rng=3, direction="LEFT", strgArg=""):
    global config, scrllrMngr
    strg = strgArg

    if strgArg == "":
        # if n in[1,3,5] :
        if n < 3:
            strg = scrllrMngr.txt1
        else:
            strg = scrllrMngr.txt2

    clrseq = ((100, 0, 0), (0, 100, 0), (0, 0, 100))
    c = n if n < 3 else n - 3

    # block = ScrollMessage(makeText(config.usingEmoties, strg), direction ,config, clrseq[c])
    block = ScrollMessage(makeText(scrllrMngr.usingEmoties, strg), direction, config, scrllrMngr)

    prv = n - 1
    nxt = n + 1
    if n < 3:
        if prv < 0:
            prv = 3 - 1
        if nxt == 3:
            nxt = 0
    else:
        if prv < 3:
            prv = rng - 1
        if nxt == rng:
            nxt = 3

    block.prvBlock = prv
    block.nxtBlock = nxt
    block.width = block.scrollImage.size[0]
    block.bufferSpacing = 8

    # pieceLogger(n, block.prvBlock, block.nxtBlock, block.width, direction, strg)
    return block


# ------------------------------------------------------------------- # ""


def makeText(emotis=False, arg=" FEEL BAD "):
    global config, scrllrMngr
    space = "  "
    strg = ""
    if emotis:
        maxNums = int(scrllrMngr.fontSize / 2)
        num = int(random.uniform(3, maxNums))
        for n in range(0, num):
            '''
            strg += "."
            '''
            strg += "(:" + space
            if random.random() > 0.5:
                strg += "o:" + space
            if random.random() > 0.75:
                strg += "(;" + space

        # strg ="| oTESTx |"
    else:
        strg = arg
    return strg


# ------------------------------------------------------------------- # ""


def setUp():
    global config, XOsBlocks, overlayImage, blocks, usingEmoties, directionOrder, scrllrMngr

    # overlayImage = Image.new("RGBA", (config.actualScreenWidth , config.screenHeight))
    lastWidth = scrllrMngr.canvasImageWidth
    direction = directionOrder[0]

    # Used if there are 2 text statements running against eachother
    rng = 3 if (scrllrMngr.usingEmoties == True or scrllrMngr.counterScrollText == False) else 6

    for n in range(0, rng):

        if n >= 3:
            direction = directionOrder[1]
        if n == 3:
            lastWidth = 0

        block = makeBlock(n, rng, direction)

        if block.direction == "RIGHT":
            block.start = lastWidth
            block.end = (
                -block.width
            )  # - lastWidth -config.screenWidth * config.displayRows
        elif block.direction == "LEFT":
            block.start = -block.width - lastWidth
            block.end = config.screenWidth * scrllrMngr.displayRows

        lastWidth += block.width
        block.xPos = block.start
        blocks.append(block)

    # lastWidth = 0
    # direction = directionOrder[1]

    if scrllrMngr.useXOs:
        lastWidth = 0
        direction = directionOrder[1]
        for n in range(0, 3):
            XOs = XOx(direction, config, n, 3, scrllrMngr)
            if XOs.direction == "RIGHT":
                XOs.xPos = XOs.start = scrllrMngr.canvasImageWidth + lastWidth
            else:
                XOs.xPos = XOs.start = -lastWidth - XOs.width
            lastWidth += XOs.width + XOs.bufferSpacing
            XOsBlocks.append(XOs)


# ------------------------------------------------------------------- # ""

def runWork():
    global config, scrllrMngr
    pieceLogger("**", 2)
    pieceLogger("RUNNING counterscroll.py", 2)

    while config.isRunning == True:
        config.directorController.checkTime()
        if config.directorController.advance == True:
            iterate()
        time.sleep(scrllrMngr.scrollSpeed)
        if config.standAlone == False :
            config.callBack()


# ------------------------------------------------------------------- # ""


def iterate():
    global config, blocks, x, y, XOsBlocks, usingEmoties, scrllrMngr

    # Blank out canvases
    draw = ImageDraw.Draw(config.renderImageFull)
    draw.rectangle((0, 0, config.screenWidth, config.screenHeight), fill=(0, 0, 0))

    draw = ImageDraw.Draw(config.canvasImage)

    if scrllrMngr.coloroverlayBackgroundOnly == True :
        draw.rectangle(
            (0, 0, scrllrMngr.canvasImageWidth, config.screenHeight), fill=tuple([int(a) for a in scrllrMngr.colorOverlayObjA.currentColor])
        )
    else :
        draw.rectangle(
            (0, 0, scrllrMngr.canvasImageWidth, config.screenHeight), fill=(scrllrMngr.bgColor)
        )

    displayWidth = config.screenWidth * scrllrMngr.displayRows

    # ------------------------------------------------------------------- #
    # Scroll message

    rng = 3 if scrllrMngr.usingEmoties == True or scrllrMngr.counterScrollText == False else 6

    for i in range(0, rng):

        # ------------------------------------------------------------------- #
        ## This reverses the pasting so the text scrolling from right to left is on top
        ## Right to Left scrolling is the normal for readability ....
        if rng != 3:
            n = (rng - 1) - i
        else:
            n = i

        block = blocks[n]
        block.scroll()

        # ------------------------------------------------------------------- #

        # paste scrollImage into the canvasImage - but eventually chop and flip

        config.canvasImage.paste(
            block.scrollImage, (block.xPos, scrllrMngr.vOffset), block.scrollImage
        )
        config.canvasImage.paste(
            block.scrollImage, (0, 0), block.scrollImage
        )

        # if block.xPos > displayWidth and block.direction == "LEFT":
        #     # a block moves off-screen, possibly change message, then move to back of queue
        #     if random.random() > 0.5:
        #         strg = config.txt1 if random.random() > 0.5 else config.txt2
        #         blocks[n] = makeBlock(n, rng, block.direction, strg)
        #         block = blocks[n]
        #         block.end = displayWidth

        #     nxtBlockStartPoint = blocks[block.prvBlock].xPos
        #     if (nxtBlockStartPoint - block.width) > 0:
        #         block.xPos = -block.width
        #     else:
        #         block.xPos = nxtBlockStartPoint - block.width

        # if block.xPos < block.end and block.direction == "RIGHT":
        #     if random.random() > 0.5:
        #         strg = config.txt1 if random.random() > 0.5 else config.txt2
        #         blocks[n] = makeBlock(n, rng, block.direction, strg)
        #         block = blocks[n]
        #         block.end = -block.width

        #     prevBlockEndPoint = (
        #         blocks[block.prvBlock].xPos + blocks[block.prvBlock].width
        #     )
        #     if prevBlockEndPoint < displayWidth:
        #         block.xPos = config.canvasImageWidth + block.width
        #     else:
        #         block.xPos = prevBlockEndPoint + block.bufferSpacing


    # ------------------------------------------------------------------- #

    if scrllrMngr.useXOs:
        # Add the counter XO's

        for n in range(0, 3):
            XOsBlock = XOsBlocks[n]
            XOsBlock.drawCounterXO()

            if XOsBlock.xPos > displayWidth and XOsBlock.direction == "LEFT":
                if random.random() > 0.5:
                    XOsBlocks[n].xoString = XOsBlocks[n].makeBlock(scrllrMngr.useArrows)
                    XOsBlock.end = displayWidth

                nxtBlockStartPoint = XOsBlocks[XOsBlock.prvBlock].xPos
                if (nxtBlockStartPoint - XOsBlock.width) > 0:
                    XOsBlock.xPos = -XOsBlock.width
                else:
                    XOsBlock.xPos = nxtBlockStartPoint - XOsBlock.width

                # pieceLogger (n,XOsBlock.xPos,XOsBlock.end, XOsBlock.width)
                # XOsBlocks[n].xPos = XOsBlocks[n].start =  XOsBlocks[XOsBlock.prvBlock].xPos - XOsBlock.width - XOsBlock.bufferSpacing

            elif (
                XOsBlocks[n].xPos < -XOsBlocks[n].width
                and XOsBlocks[n].direction == "RIGHT"
            ):
                if random.random() > 0.5:
                    XOsBlock.xoString = XOsBlock.makeBlock(scrllrMngr.useArrows)
                    XOsBlock.end = -XOsBlock.width

                prevBlockEndPoint = (
                    XOsBlocks[XOsBlock.prvBlock].xPos
                    + XOsBlocks[XOsBlock.prvBlock].width
                )
                if prevBlockEndPoint < displayWidth:
                    XOsBlock.xPos = scrllrMngr.canvasImageWidth + XOsBlock.width
                else:
                    XOsBlock.xPos = prevBlockEndPoint + XOsBlock.bufferSpacing
                # XOsBlock.xPos = XOsBlock.start = XOsBlocks[XOsBlock.prvBlock].xPos + XOsBlocks[XOsBlock.prvBlock].width + XOsBlock.bufferSpacing

    # ------------------------------------------------------------------- #

    # Chop up the scrollImage into "rows"
    for n in range(0, scrllrMngr.displayRows):
        segmentHeight = int(config.canvasHeight / scrllrMngr.displayRows)
        segmentWidth = config.canvasWidth
        segment = config.canvasImage.crop(
            (
                n * config.canvasWidth,
                0,
                segmentWidth + n * config.canvasWidth,
                segmentHeight,
            )
        )

        # At some point go to modulo for even/odd ... but for now not more than 5 rows
        if (n == 0 or n == 2 or n == 4) and (scrllrMngr.displayRows > 1):
            segment = ImageOps.flip(segment)
            segment = ImageOps.mirror(segment)
        config.canvasImageFinal.paste(segment, (0, n * segmentHeight))

    # ------------------------------------------------------------------- #

    ### Colorizing filter that transitions from colorA to colorB ###

    if scrllrMngr.colorOverlay == True:
        scrllrMngr.colorOverlayObjA.stepTransition()
        scrllrMngr.colorOverlayObjB.stepTransition()

        segmentColorizer = Image.new(
            "RGBA", (scrllrMngr.overlayWidth, scrllrMngr.overlayHeight)
        )

        draw = ImageDraw.Draw(segmentColorizer)
        draw.rectangle(
            (
                scrllrMngr.overlayX,
                scrllrMngr.overlayY,
                scrllrMngr.overlayWidth + scrllrMngr.overlayX,
                scrllrMngr.overlayHeight + scrllrMngr.overlayY,
            ),
            fill=tuple([int(a) for a in scrllrMngr.colorOverlayObjA.currentColor]),
        )
        # draw.rectangle((projectedWidth/2,0,projectedWidth,config.screenHeight), fill = tuple( [int(a) for a in config.colorOverlayObjB.currentColor] ))

        if scrllrMngr.coloroverlayBackgroundOnly == False :
            temp = ImageChops.multiply(config.canvasImageFinal, segmentColorizer)
            config.canvasImageFinal.paste(temp, (0, 0), temp)

    # ------------------------------------------------------------------- #


    if scrllrMngr.useBlanks:
        badpixels.drawBlanks(config.canvasImageFinal, False)

    if random.random() > 0.998 and (scrllrMngr.useBlanks):
        badpixels.setBlanksOnScreen()


    # ------------------------------------------------------------------- #
    # ------------------------------------------------------------------- #
    # Debug geometry for rotation
    # tS = config.canvasImageFinal.size
    # tDraw = ImageDraw.Draw(config.canvasImageFinal)
    # tDraw.rectangle((0,0,tS[0],tS[1]), fill = None, outline=(0,255,0))

    if scrllrMngr.useThreeD:
        ThreeD(config.canvasImageFinal)
        # drw = ImageDraw.Draw(config.warpedImage)
        # drw.rectangle((0,0, config.canvasWidth -4 , config.canvasHeight - 2), fill = None, outline=(222,100,0))
        config.render(
            config.warpedImage, 0, 0, config.canvasWidth, config.canvasHeight, False
        )
    else:
        config.render(
            config.canvasImageFinal,
            0,
            0,
            config.canvasWidth,
            config.canvasHeight,
            False,
        )

    # ------------------------------------------------------------------- #
    # ------------------------------------------------------------------- #
    # ------------------------------------------------------------------- #


# ------------------------------------------------------------------- # ""


def ThreeD(imageToRender):

    numSegments = 64
    dFactor = 1.0
    offset = 0
    angle = math.pi / numSegments

    if abs(config.rotation) == 90:
        numSegments = 32
        dFactor = 1.415
        angle = math.pi / numSegments
        width = config.screenHeight * 0.8
        height = config.canvasWidth

    else:
        width = config.screenWidth
        height = config.screenHeight

    segmentWidth = round((width) * math.sin(angle) / 1.0)
    useColorFLicker = False
    placementx = 0

    segmentWidth = 4
    numSegments = round(config.screenWidth / segmentWidth)
    angle = math.pi / numSegments * 2

    for n in range(0, numSegments):
        pCropx = n * segmentWidth + offset
        pWidth = math.fabs( segmentWidth * math.sin(angle * n * .5) + 1.5)
        projectedWidth = round(pWidth/dFactor)

        segmentImage = Image.new("RGBA", (projectedWidth, height))
        croppedSegment = imageToRender.crop((pCropx, 0, pCropx + segmentWidth, height))
        segmentImage = croppedSegment.resize((projectedWidth, height))
        br = pWidth / segmentWidth

        if useColorFLicker:
            segmentColorizer = Image.new("RGBA", (projectedWidth, height))
            draw = ImageDraw.Draw(segmentColorizer)
            draw.rectangle((0, 0, projectedWidth, height), fill=config.randomColor())
            segmentImage = ImageChops.multiply(segmentImage, segmentColorizer)

        enhancer = ImageEnhance.Brightness(segmentImage)
        segmentImage = enhancer.enhance(br)
        # segmentImage = segmentImage.filter(ImageFilter.BLUR)
        # warpedImage.paste(segmentColorizer , (placementx,0))
        config.warpedImage.paste(segmentImage, (placementx, 0))
        placementx += projectedWidth

    # debug
    # draw = ImageDraw.Draw(config.warpedImage)
    # draw.rectangle((0,0,config.screenWidth,config.screenHeight), outline=(0,0,255))

    # config.render(warpedImage,0,0, config.screenWidth, config.screenHeight)


# ------------------------------------------------------------------- # ""

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


# ------------------------------------------------------------------- # ""

def callBack():
    global config, XOs
    return True


# ------------------------------------------------------------------- # ""
