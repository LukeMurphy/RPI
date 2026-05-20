import argparse
import datetime
import itertools
import math
import random
import textwrap
import time
from modules.configuration import bcolors
from modules import badpixels, coloroverlay, colorutils, panelDrawing
from PIL import Image, ImageChops, ImageDraw, ImageEnhance, ImageFont, ImageOps


class unit:
    def __init__(self, config):
        self.config = config
        self.xPos = 0
        self.yPos = 0
        self.xPosR = self.config.screenWidth / 2
        self.yPosR = self.config.screenHeight / 2
        self.move = True

        self.dx = random.uniform(-3, 3)
        self.dy = random.uniform(-3, 3)

        self.image = Image.new("RGBA", (100, 100))
        self.fillColor = colorutils.getRandomRGB()
        self.outlineColor = colorutils.getRandomRGB(config.brightness)
        self.objWidth = 20
        self.objWidthMax = 26
        self.objWidthMin = 13

        self.draw = ImageDraw.Draw(self.image)

    def update(self):
        self.xPos += self.dx
        self.yPos += self.dy

        self.xPosR += self.dx
        self.yPosR += self.dy

        if self.xPosR + self.objWidth > self.config.screenWidth:
            self.xPosR = self.config.screenWidth - self.objWidth
            self.xPos = self.config.screenWidth - self.objWidth
            self.changeColor()
            self.dx *= -1
        if self.yPosR + self.objWidth > self.config.screenHeight:
            self.yPosR = self.config.screenHeight - self.objWidth
            self.yPos = self.config.screenHeight - self.objWidth
            self.changeColor()
            self.dy *= -1
        if self.xPosR < 0:
            self.xPosR = 0
            self.xPos = 0
            self.changeColor()
            self.dx *= -1
        if self.yPosR < 0:
            self.yPosR = 0
            self.yPos = 0
            self.changeColor()
            self.dy *= -1

        if self.dx == 0 and self.dy == 0:
            if random.random() > 0.5:
                self.dx = 2 * random.random()
            if random.random() > 0.5:
                self.dy = 2 * random.random()

    def render(self):
        xPos = int(self.xPosR)
        yPos = int(self.yPosR)
        self.config.draw.rectangle(
            (xPos, yPos, xPos + self.objWidth, yPos + self.objWidth),
            fill=self.fillColor,
            outline=self.outlineColor,
        )

    def changeColor(self):
        self.fillColor = colorutils.randomColor(random.random())
        self.outlineColor = colorutils.getRandomRGB()
        if random.random() > 0.5:
            self.dx = 4 * random.random() + 2
        if random.random() > 0.5:
            self.dy = 4 * random.random() + 2
        if random.random() > 0.5:
            self.objWidth = int(random.uniform(self.objWidthMin, self.objWidthMax))


"""""" """""" """""" """""" """""" """""" """""" """""" """""" """""" ""


def displayTest():
    global config
    # config.draw.rectangle((0,0,config.screenWidth, config.screenHeight), fill=(0,0,0), outline=(0,0,0))
    # config.draw.rectangle(
    #     (0, 0, config.screenWidth - 1, config.screenHeight - 1),
    #     fill=(0, 0, 0),
    #     outline=config.outlineColor,
    # )
    # config.draw.rectangle(
    #     (1, 1, config.screenWidth - 2, config.screenHeight - 2),
    #     fill=(0, 0, 0),
    #     outline=(0, 0, int(220 * config.brightness)),
    # )
    if config.showWhitesGreys:
        rgbWheel = [
            (255, 255, 255),
            (255, 255, 255),
            (255, 255, 255),
            (255, 255, 255),
            (255, 255, 255),
            (255, 255, 255),
            (255, 255, 255),
            (255, 255, 255),
            (255, 255, 255),
        ]
    else:
        rgbWheel = [
            (255, 0, 0),
            (255, 255, 0),
            (255, 200, 0),
            (0, 255, 0),
            (0, 255, 255),
            (0, 0, 255),
            (255, 0, 255),
            (255, 255, 255),
        ]

    w = 8
    h = 16
    for _ii, _i in itertools.product(range(6), range(4)):
        xp = 0
        yp = h * _ii * 2
        d = _i * (len(rgbWheel) * w)
        for item in rgbWheel:
            colorBlock = tuple(map(lambda x: int(int(x) * config.brightness), item))
            config.draw.rectangle((xp + d, yp, xp + w + d, yp + h), fill=colorBlock, outline=colorBlock)
            xp += w

        xp = 0
        for item_ in rgbWheel:
            colorBlock = tuple(map(lambda x: int(int(x) * config.brightness * 0.75), item_))
            config.draw.rectangle((xp + d, yp + h / 2, xp + w + d, yp + h), fill=colorBlock, outline=colorBlock)
            xp += w

        yp += h + 0
        xp = 0

        for _ in range(len(rgbWheel)):
            colorBlock = tuple(map(lambda x: int(int(x) * config.brightness * 0.5), rgbWheel[7]))
            config.draw.rectangle((xp + d, yp, xp + w + d, yp + h / 2), fill=colorBlock, outline=colorBlock)
            xp += w
        xp = 0

        for _ in range(len(rgbWheel)):
            colorBlock = tuple(map(lambda x: int(int(x) * config.brightness * 1.0), rgbWheel[7]))
            config.draw.rectangle((xp + d, yp + h / 2, xp + w + d, yp + h), fill=colorBlock, outline=colorBlock)
            xp += w

    # for i in range(config.numUnits):
    #     obj = config.unitArray[i]
    #     if obj.move == True:
    #         obj.update()
    #     obj.render()

    config.draw.text((1, 0), "TOP", config.fontColor, font=config.font)
    config.draw.text((1, config.screenHeight - 32), "BOTTOM", config.fontColor, font=config.font)

    tm = datetime.datetime.now()
    tm = time.ctime()
    config.draw.text((10, 36), tm, config.fontColor, font=config.font)

    config.render(config.image, 0, 0)


"""""" """""" """""" """""" """""" """""" """""" """""" """""" """""" ""


def showGrid():
    # global config

    config.draw.rectangle(
        (0, 0, config.canvasWidth, config.canvasHeight),
        fill=config.bgColor,
        outline=(0, 0, 0),
    )
    config.canvasDraw.rectangle(
        (0, 0, config.canvasWidth - 1, config.canvasHeight - 1),
        fill=config.bgColor,
        outline=config.outlineColor,
    )
    config.canvasDraw.rectangle(
        (1, 1, config.canvasWidth - 2, config.canvasHeight - 2),
        fill=config.bgColor,
        outline=(0, 0, int(220 * config.brightness)),
    )

    # print(config.imageXOffset)

    for row in range(config.rows):
        for col in range(config.cols):
            yPos = row * config.tileSizeHeight

            if config.rowsToShow == 0 or row in config.rowsToShow:
                xPos = col * config.tileSizeWidth
                config.canvasDraw.rectangle(
                    (
                        xPos,
                        yPos,
                        xPos + config.tileSizeWidth - 1,
                        yPos + config.tileSizeHeight - 1,
                    ),
                    fill=config.bgColor,
                    outline=config.outlineColor,
                )
                displyInfo = f"x:{str(col)}" + "\ny:" + str(row) + ""
                config.canvasDraw.multiline_text((xPos + 2, yPos - 1), displyInfo, config.fontColor, font=config.font, spacing=0)
                displyInfo = "\n" + str(col * config.tileSizeWidth) + " " + str(row * config.tileSizeHeight)
                config.canvasDraw.multiline_text((xPos + 2, yPos - 1 + config.fontSize / 1.0), displyInfo, config.fontColor2, font=config.font, spacing=0)

    config.image.paste(
        config.canvasImage,
        (config.imageXOffset, config.imageYOffset),
        config.canvasImage,
    )

    if config.useImage == True:
        config.image.paste(
            config.testImage,
            (config.imageXOffset, config.imageYOffset),
            config.testImage,
        )

    # config.draw.rectangle((0,64,8,72), fill=(200,200,0), outline = (0,0,200))

    # config.image=config.image.rotate(-config.rotation)

    # config.image = config.image.rotate(-config.rotation)

    ########### RENDERING AS A MOCKUP OR AS REAL ###########
    if config.useDrawingPoints == True:
        config.panelDrawing.canvasToUse = config.image
        config.panelDrawing.render()
    else:
        # config.render(config.canvasImage, 0, 0, config.canvasWidth, config.canvasHeight)
        # config.render(config.image, 0, 0)
        config.render(config.image, 0, 0)


"""""" """""" """""" """""" """""" """""" """""" """""" """""" """""" ""


def drawTVPalette():
    config.draw.rectangle(
        (0, 0, config.screenWidth, config.screenHeight),
        fill=config.bgColor,
        outline=(0, 0, 0),
    )
    config.canvasDraw.rectangle(
        (0, 0, config.canvasWidth - 1, config.canvasHeight - 1),
        fill=config.bgColor,
        outline=config.outlineColor,
    )
    config.canvasDraw.rectangle(
        (1, 1, config.canvasWidth - 2, config.canvasHeight - 2),
        fill=config.bgColor,
        outline=(0, 0, int(255 * config.brightness)),
    )

    tileSizeWidth = round(config.canvasWidth / 7)
    tileSizeHeight = round(config.canvasHeight / 3)
    bottomY = 2 * round(tileSizeHeight + tileSizeHeight / 6) - 1
    bottomH = 2 * round(tileSizeHeight / 3)

    # Top 2/3: 7 primary/secondary SMPTE bars at 75%
    for col, hsv in enumerate([
        (0, 0, 0.75), (60, 1.0, 0.75), (180, 1.0, 0.75), (120, 1.0, 0.75),
        (300, 1.0, 0.75), (0, 1.0, 0.75), (220, 1.0, 0.75),
    ]):
        xPos = col * tileSizeWidth
        config.canvasDraw.rectangle(
            (xPos, 0, xPos + tileSizeWidth, 2 * tileSizeHeight),
            fill=colorutils.HSVToRGB(*hsv), outline=None,
        )

    # Middle strip: reversed colors interleaved with near-black
    for col, hsv in enumerate([
        (220, 1.0, 0.75), (0, 0, 0.07), (300, 1.0, 0.75), (0, 0, 0.07),
        (180, 1.0, 0.75), (0, 0, 0.07), (0, 0, 0.75),
    ]):
        xPos = col * tileSizeWidth
        config.canvasDraw.rectangle(
            (xPos, 2 * tileSizeHeight, xPos + tileSizeWidth - 1, 2 * tileSizeHeight + round(tileSizeHeight / 3) - 1),
            fill=colorutils.HSVToRGB(*hsv), outline=None,
        )

    # Bottom-left: I, White, Q tiles across left half
    leftTileWidth = round(config.canvasWidth / 2 / 3)
    for col, hsv in enumerate([(214, 1.0, 0.3), (0, 0, 1.0), (268, 1.0, 0.42)]):
        xPos = col * leftTileWidth
        config.canvasDraw.rectangle(
            (xPos, bottomY, xPos + leftTileWidth, bottomY + bottomH),
            fill=colorutils.HSVToRGB(*hsv), outline=None,
        )

    # Bottom-center: near-black from midpoint to 5th column
    config.canvasDraw.rectangle(
        (round(config.canvasWidth / 2), bottomY, round(5 * tileSizeWidth) - 1, bottomY + bottomH),
        fill=colorutils.HSVToRGB(0, 0, 0.07), outline=None,
    )

    # Bottom-right: 6 near-black gradient tiles
    smallTileWidth = tileSizeWidth / 3
    for col, hsv in enumerate([
        (0, 0, 0.0), (0, 0, 0.04), (0, 0, 0.07),
        (0, 0, 0.11), (0, 0, 0.07), (0, 0, 0.07),
    ]):
        xPos = round(5 * tileSizeWidth) + int(smallTileWidth * col)
        config.canvasDraw.rectangle(
            (xPos, bottomY, xPos + int(smallTileWidth), bottomY + bottomH),
            fill=colorutils.HSVToRGB(*hsv), outline=None,
        )

    config.image.paste(
        config.canvasImage,
        (config.imageXOffset, config.imageYOffset),
        config.canvasImage,
    )
    config.render(config.image, 0, 0)


"""""" """""" """""" """""" """""" """""" """""" """""" """""" """""" ""


def drawPalette():
    global config

    config.draw.rectangle(
        (0, 0, config.screenWidth, config.screenHeight),
        fill=config.bgColor,
        outline=(0, 0, 0),
    )
    config.canvasDraw.rectangle(
        (0, 0, config.canvasWidth - 1, config.canvasHeight - 1),
        fill=config.bgColor,
        outline=config.outlineColor,
    )
    config.canvasDraw.rectangle(
        (1, 1, config.canvasWidth - 2, config.canvasHeight - 2),
        fill=config.bgColor,
        outline=(0, 0, int(255 * config.brightness)),
    )

    # print(config.imageXOffset)
    config.rows = 2
    config.cols = 16
    config.tileSizeWidth = config.tileSizeWidth
    hues = 360 / config.cols
    vals = 1 / config.rows
    sat = 1  # / config.rows

    for row in range(config.rows + 1):
        for col in range(config.cols):
            ## Draw colors 0 thru 360
            xPos = col * config.tileSizeWidth
            yPos = row * config.tileSizeHeight

            hue = col * hues
            val = row * vals
            # sat = row * vals

            bgColor = colorutils.HSVToRGB(hue, sat, val)
            config.canvasDraw.rectangle(
                (
                    xPos,
                    yPos,
                    xPos + config.tileSizeWidth - 1,
                    yPos + config.tileSizeHeight - 1,
                ),
                fill=bgColor,
                outline=config.outlineColor,
            )

            displyInfo = str(round(hue)) + "\n " + str(round(val * 10) / 10) + "\n"
            config.canvasDraw.text((xPos + 2, yPos - 1), displyInfo, config.fontColor, font=config.font)
            # displyInfo  =  "\n" + str(col * config.tileSizeWidth) + ", " + str(row * config.tileSizeHeight)
            # config.canvasDraw.text((xPos + 2,yPos - 1),displyInfo,config.fontColor2,font=config.font)

    config.image.paste(
        config.canvasImage,
        (config.imageXOffset, config.imageYOffset),
        config.canvasImage,
    )

    # config.draw.rectangle((0,64,8,72), fill=(200,200,0), outline = (0,0,200))

    # config.renderDrawOver.rectangle((0, 0, 100, 100), fill=(100, 0, 0, 0.5))

    config.render(config.image, 0, 0)


"""""" """""" """""" """""" """""" """""" """""" """""" """""" """""" ""


def main(run=True):
    global config, directionOrder
    global workConfig
    print("** ---------------------")
    print("** Diag Loaded **")

    colorutils.brightness = config.brightness
    # config.canvasImageWidth = config.screenWidth
    # config.canvasImageHeight = config.screenHeight
    # config.canvasImageWidth -= 4
    # config.canvasImageHeight -= 4
    config.delay = 0.02
    config.numUnits = 1

    config.fontColorVals = (workConfig.get("diag", "fontColor")).split(",")
    config.fontColor = tuple(map(lambda x: int(int(x) * config.brightness), config.fontColorVals))
    config.outlineColorVals = (workConfig.get("diag", "outlineColor")).split(",")
    config.outlineColor = tuple(map(lambda x: int(int(x) * config.brightness), config.outlineColorVals))
    config.bgColorVals = (workConfig.get("diag", "bgColor")).split(",")
    config.bgColor = tuple(map(lambda x: int(int(x) * config.brightness), config.bgColorVals))
    config.useLastOverlay = False
    print(config.bgColor)

    config.angle = 0

    try:
        config.rowsVals = (workConfig.get("diag", "rowsToShow")).split(",")
        config.rowsToShow = tuple(map(lambda x: int(x), config.rowsVals))
    except Exception as e:
        print(e)
        config.rowsToShow = 0

    try:
        config.fontSize = int(workConfig.get("diag", "fontSize"))
    except Exception as e:
        print(e)
        config.fontSize = 14
    try:
        config.imageXOffset = int(workConfig.get("displayconfig", "imageXOffset"))
    except Exception as e:
        print(e)
        config.imageXOffset = 0
    try:
        config.showGrid = workConfig.getboolean("diag", "showGrid")
    except Exception as e:
        print(e)
        config.showGrid = False
    try:
        config.showWhitesGreys = workConfig.getboolean("diag", "showWhitesGreys")
    except Exception as e:
        print(e)
        config.showWhitesGreys = False
    try:
        fontColor2 = workConfig.get("diag", "fontColor2").split(",")
    except Exception as e:
        print(e)
        fontColor2 = [0, 200, 0]
    config.fontColor2 = tuple(map(lambda x: int(int(x) * config.brightness), fontColor2))

    try:
        config.useImage = workConfig.getboolean("diag", "useImage")
        config.showAsOverLay = workConfig.getboolean("diag", "showAsOverLay")
        config.imgPath = workConfig.get("diag", "imgPath")
    except Exception as e:
        print(e)
        config.useImage = False
        config.showAsOverLay = False
        config.imgPath = ""

    config.tileSizeWidth = int(workConfig.get("displayconfig", "tileSizeWidth"))
    config.tileSizeHeight = int(workConfig.get("displayconfig", "tileSizeHeight"))

    config.screenPositionX = 0
    config.screenPositionY = 0

    try:
        config.colorPalette = workConfig.getboolean("diag", "colorPalette")
    except Exception as e:
        print(e)
        config.colorPalette = False

    try:
        config.TVPalette = workConfig.getboolean("diag", "TVPalette")
    except Exception as e:
        print(e)
        config.TVPalette = False

    """""" """""" """""" """""" """""" """""" """""" """""" """""" """"""

    config.image = Image.new("RGBA", (config.canvasWidth, config.canvasHeight))
    config.draw = ImageDraw.Draw(config.image)
    config.canvasImage = Image.new("RGBA", (config.canvasWidth, config.canvasHeight))
    config.canvasDraw = ImageDraw.Draw(config.canvasImage)
    config.font = ImageFont.truetype(
        f"{config.path}/assets/fonts/freefont/FreeSansBold.ttf",
        config.fontSize,
    )

    if config.useImage:
        config.testImage = Image.open(config.imgPath, "r")
        config.testImage.load()
        config.imgHeight = config.testImage.getbbox()[3]

    """""" """""" """""" """""" """""" """""" """""" """""" """""" """"""
    config.unitArray = []
    for _ in range(config.numUnits):
        obj = unit(config)
        # obj.move = False
        obj.objWidth = 5
        obj.objWidthMax = 4
        obj.objWidthMin = 3
        config.unitArray.append(obj)

    config.renderDiagnosticsCall = renderDiagnosticsCall

    setUp()

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


"""""" """""" """""" """""" """""" """""" """""" """""" """""" """""" ""


def renderDiagnosticsCall():
    config.renderImageFullOverlay = Image.new("RGBA", (config.screenWidth, config.screenHeight))
    config.renderDrawOver = ImageDraw.Draw(config.renderImageFullOverlay)

    config.lastOverlayBox1 = (64, 0, 256, 128)
    config.lastOverlayBox3 = (256, 0, 448, 128)
    config.lastOverlayBox2 = (64, 128, 256, 256)
    config.lastOverlayBox4 = (256, 128, 448, 256)

    config.renderDrawOver.rectangle(config.lastOverlayBox1, fill=(255, 0, 0, 100), outline=(255, 255, 0, 255))
    config.renderDrawOver.rectangle(config.lastOverlayBox2, fill=(255, 0, 0, 100), outline=(255, 255, 0, 255))
    config.renderDrawOver.rectangle(config.lastOverlayBox3, fill=(255, 0, 0, 100), outline=(255, 255, 0, 255))
    config.renderDrawOver.rectangle(config.lastOverlayBox4, fill=(255, 0, 0, 100), outline=(255, 255, 0, 255))
    config.renderImageFull.paste(config.renderImageFullOverlay, (0, 0), config.renderImageFullOverlay)


"""""" """""" """""" """""" """""" """""" """""" """""" """""" """""" ""


def setUp():
    pass
    # arg = "./assets/imgs/sks/skull-s2.png"
    # config.loadedImage = Image.open(arg , "r")
    # config.loadedImage.load()


"""""" """""" """""" """""" """""" """""" """""" """""" """""" """""" ""


def runWork():
    print(f"{bcolors.OKGREEN}** {bcolors.BOLD}")
    print("RUNNING DIAGNOSTICS diagnostics.py")
    print(bcolors.ENDC)
    # gc.enable()

    while config.isRunning == True:
        iterate()
        time.sleep(config.delay)
        if config.standAlone == False:
            config.callBack()


"""""" """""" """""" """""" """""" """""" """""" """""" """""" """""" ""


def iterate():

    if config.screenPositionX != config.cnvs.winfo_rootx() or config.screenPositionY != config.cnvs.winfo_rooty() - 22:
        print(config.cnvs.winfo_rootx(), config.cnvs.winfo_rooty() - 22)
        config.screenPositionX = config.cnvs.winfo_rootx()
        config.screenPositionY = config.cnvs.winfo_rooty() - 22

    if config.TVPalette == True:
        drawTVPalette()
    elif config.colorPalette == True:
        drawPalette()
    elif config.showGrid == True:
        showGrid()
    else:
        displayTest()


"""""" """""" """""" """""" """""" """""" """""" """""" """""" """""" ""


def callBack():
    global config, XOs
    return True


"""""" """""" """""" """""" """""" """""" """""" """""" """""" """""" ""
