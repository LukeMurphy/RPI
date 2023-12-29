#!/usr/bin/python
import math
import random
# Import the essentials to everything
import time

import PIL.Image
from modules import colorutils
from PIL import (
    Image,
    ImageChops,
    ImageDraw,
    ImageEnhance,
    ImageFilter,
    ImageMath,
    ImagePalette,
)


def ScaleRotateTranslate(
    image, angle, center=None, new_center=None, scale=None, expand=False
):
    if center is None:
        return image.rotate(angle)
    angle = -angle / 180.0 * math.pi
    nx, ny = x, y = center
    sx = sy = 1.0
    if new_center:
        (nx, ny) = new_center
    if scale:
        (sx, sy) = scale
    cosine = math.cos(angle)
    sine = math.sin(angle)
    a = cosine / sx
    b = sine / sx
    c = x - nx * a - ny * b
    d = -sine / sy
    e = cosine / sy
    f = y - nx * d - ny * e
    return image.transform(
        image.size, Image.AFFINE, (a, b, c, d, e, f), resample=Image.BICUBIC
    )


class ImageSprite:

    color = (255, 0, 0)
    bgColor = (0, 0, 255)
    speed = 2
    speedMultiplier = 4
    x = xPos = 0
    y = yPos = 0
    dX = -1
    dY = 0
    startX = 0
    startY = 0
    endX = 0
    endY = 0
    xOffset = 0
    yOffset = 0
    yOffsetFactor = 40

    reveal = 0
    revealSpeed = 1
    revealSpeedMax = 3
    setForRemoval = False

    r = g = b = 0
    count = 0
    frame = 1
    countLimit = 1
    clrIndex = 0

    imgHeight = 0
    panRangeLimit = 0
    useJitter = False
    jitterRate = 0.05
    jitterResetRate = 0.25
    jitterRange = 0.3

    useBlink = False
    blink = False
    blinkNum = 0
    blinkCount = 0
    blinkStationary = False

    presentTime = 10
    brightnessFactor = 0.5
    rate = 0
    gifPlaySpeed = 0.03
    scrollSpeed = 0.04
    bgFillColor = 0x000000

    action = "play"
    direction = "right"
    directionStr = "Left"
    brightnessFlux = False
    brightnessFluxRate = 8  # As a factor or PI/brightnessFluxRate
    resizeToWidth = False
    resizeToHeight = False

    processImage = True
    resizeImage = True
    resizeMin = 1.1
    resizeMax = 1.2
    randomizeColor = False
    randomizeDirection = True
    colorMode = "random"
    colorModeDirectional = True
    yOffsetChange = True

    resizeMin = 0.1
    resizeMax = 1.2

    lastPictureIndex = 0
    debug = False

    tempClrCount = 60
    frameCount = 1

    imageRotation = 10

    channelHeight = 170

    # Helps with lousy looping gifs
    forceGlitchFrameCount = 300
    imageGlitchCount = 0
    imageGlitchCountLimit = 20
    holdAnimation = False
    pausePlayProb = 0.0
    releasePauseProb = 0.0
    glitchChanceWhenPausedFactor =10.0

    colorModes = ["colorWheel", "random", "colorRGB", 'hsvFlame']

    rowCount = 0
    colCount = 0
    frameCount = 0
    # the spritesheet frame dimensions
    frameWidth = 230
    frameHeight = 224
    totalFrames = 223
    frameCols = 16
    frameRows = 14

    # slice parameters
    sliceWidthMin = 230
    sliceWidth = 230
    sliceHeightMin = 224
    sliceHeight = 224
    
    animationWidth = 100
    animationHeight = 100
    
    resizeAnimationtoFit = False

    def __init__(self, config, iid=0):

        print("ImageSprite Initiated")
        
        self.iid = iid
        self.config = config

        self.clrUtils = colorutils
        self.clrUtils.brightness = self.config.brightness

        self.brightnessFactor = config.minBrightness
        pass

    """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" ""
    ## This is called every time an object moves off the screen
    ## can update color, size etc
    def callBack(self, *args):

        if args[0] == True:
            # print(self.dX)
            # self.imageRotation = random.uniform(-30,30)
            # direction = -1 if self.dX < 0 else 1
            direction = 1
            self.dX = random.uniform(1.0, 3.0) * direction * self.config.speedFactor
            self.image = self.imageOriginal.copy()
            self.process()

            # This turns out to be less interesting - somehow the uniformity of speed
            # is a better counter point to the randomness of color and scale - 6-24-16
            """
            if(random.random() > .8) : 
                speedMultiplier = random.uniform(1,10)
                self.dX *= speedMultiplier 
            """

        return True

    """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" ""

    def make(
        self,
        img="",
        setvX=0,
        setvY=0,
        processImage=True,
        resizeImage=True,
        randomizeDirection=True,
        randomizeColor=True,
        ):

        self.frame = 0
        self.dX = setvX
        self.dY = setvY

        self.processImage = processImage
        self.resizeImage = resizeImage
        self.randomizeColor = randomizeColor
        self.randomizeDirection = randomizeDirection

        if random.random() > 0.5 and randomizeDirection:
            pass
            #self.dX *= -1.0
        print("-----------")
        print("Trying to load " + img + "")
        print("-----------")

        if self.loadImage(img):
            if self.resizeImage :
            # scale to the WIDTH of the screen
                if self.image.size[0] != self.config.screenWidth and self.resizeToWidth:
                    self.ratio = float(self.config.screenWidth) / self.image.size[0]
                    self.image = self.image.resize(
                        (self.config.screenWidth, int(self.ratio * self.image.size[1]))
                    )

                if self.image.size[1] != self.config.channelHeight and self.channelHeight:
                    self.ratio = float(self.config.channelHeight) / self.image.size[1]
                    self.image = self.image.resize(
                        (int(self.ratio * self.image.size[0]), self.config.channelHeight)
                    )

            if self.dX < 0:
                # Reverse image
                pass
                #self.image = self.image.rotate(-180)

            # self.imageOriginal = self.image.copy()
            self.process()

            self.imageCopy = Image.new(
                "RGBA", (self.config.screenWidth, self.config.channelHeight)
            )
            self.imageCopy.paste(
                self.image.convert("RGBA"), (0, 0), self.image.convert("RGBA")
            )

            self.debugMessage(img + " loaded")
            # init()
        else:
            self.debugMessage("could not load")

    """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" ""

    def process(self):
        change = 1

        if random.random() > 0.5 and self.randomizeDirection:
            self.dX *= -1.0
            self.image = self.image.rotate(-180)


            # Reverse image
        
        #print("Processing -----------", self.processImage)

        if self.processImage:
            if self.resizeImage:

                #print("resize")
                # change = random.uniform(.1,1.2) * self.scalingFactor
                change = (
                    random.uniform(self.resizeMin, self.resizeMax) * self.scalingFactor
                )
                newSizeX = change * self.image.size[0]
                newSizeY = change * self.image.size[1]
                self.image = self.image.resize(
                    (int(newSizeX), int(newSizeY))
                )  # , Image.ANTIALIAS

            brt = random.random() + self.config.minBrightness

            # This was really just set up for the multiple-planes piece
            if self.randomizeColor:

                # "Optical" or RBY Color Wheel
                if self.colorMode == "colorWheel":
                    clrIndex = int(random.random() * len(self.clrUtils.colorWheel))
                    if self.colorModeDirectional:
                        # Ones from LEFT are different
                        if self.dX < 0:
                            clrIndex = int(
                                random.uniform(6, len(self.clrUtils.colorWheel))
                            )
                        else:
                            clrIndex = int(random.uniform(0, 5))
                    clr = self.clrUtils.wheel[clrIndex]

                # RGB Color Wheel
                if self.colorMode == "colorRGB":
                    clrIndex = int(random.random() * len(self.clrUtils.rgbColorWheel))
                    if self.colorModeDirectional:
                        # Ones from LEFT are different
                        if self.dX < 0:
                            clrIndex = int(
                                random.uniform(3, len(self.clrUtils.rgbColorWheel))
                            )
                        else:
                            clrIndex = int(random.uniform(0, 3))
                    clr = self.clrUtils.rgbWheel[clrIndex]

                # Specific palette
                if self.colorMode == "getRedShiftedColors":
                    clr = self.clrUtils.getRedShiftedColors(self.config.brightness)
                # Any RGB color
                if self.colorMode == "random":
                    clr = self.clrUtils.randomColor(brt)

                # Any HSV color
                if self.colorMode == "hsvFlame":
                    clr = self.clrUtils.getRandomColorHSV(350,60,.8,1.0,.8,1.0,0,0,255,brt)

            else:
                r = int(random.uniform(200, 255))
                g = int(random.uniform(0, 100))
                b = int(random.uniform(0, 10))
                a = 255
                if random.random() > 0.5:
                    r = int(random.uniform(0, 100))
                    b = int(random.uniform(200, 255))
                clr = (r, g, b, a)

            #print("Colorizing ....")
            #print("-----------")
            self.colorize(clr)

            # Not so great - yOffset is rendered useless by this  ....
            if self.processImage and self.yOffsetChange:
                self.yOffset = int(
                    random.uniform(
                        self.config.screenHeight / 2 - self.yOffsetFactor * change,
                        self.config.screenHeight / 2 + self.yOffsetFactor,
                    )
                )

    """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" ""

    def colorize(self, clr, recolorize=False):

        # Colorize via overlay etc
        clrBlock = PIL.Image.new("RGBA", (self.image.size[0], self.image.size[1]))
        clrBlockDraw = ImageDraw.Draw(clrBlock)

        if self.debug == True : print("self.image",self.image)
        # print("self.imageOriginal", self.imageOriginal)
        # print("clrBlock",clrBlock)

        # Color overlay on b/w PNG sprite
        # EVERYTHING HAS TO BE PNG  / have ALPHA
        clrBlockDraw.rectangle((0, 0, self.image.size[0], self.image.size[1]), fill=clr)
        
        if recolorize == True:
            self.image = ImageChops.multiply(clrBlock, self.imageOriginal)
        else:
            self.image = ImageChops.multiply(clrBlock, self.image)

        self.imageCopy = Image.new("RGBA", (self.image.size[0], self.image.size[1]))
        self.imageCopy.paste(self.image, (0, 0), self.image)

        enhancer = ImageEnhance.Brightness(self.imageCopy)
        self.image = enhancer.enhance(self.brightnessFactor)
        self.imageCopy = enhancer.enhance(self.brightnessFactor)
        self.draw = ImageDraw.Draw(self.image)

    """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" ""

    def filterize(self):

        # Create a box and crop
        """""" """""" """""" """""" """"""
        lines = self.config.lines
        boxHeight = self.config.boxHeight
        boxWidth = self.config.boxWidth
        xPos1 = self.config.xPos1
        yPosBase = self.config.yPosBase
        targetClrs = self.config.targetClrs
        imageFilterProb = self.config.imageFilterProb
        bgFilterProb = self.config.bgFilterProb
        numTargetColors = len(targetClrs)
        targetPalette = self.config.targetPalette

        for n in range(0, lines, boxHeight):

            yPos1 = yPosBase + n
            xPos2 = xPos1 + boxWidth
            # Randomize the width of the box -- when image is NOT rotated this needs to be changed
            yPos2 = yPos1 + int(random.uniform(1, boxHeight))
            box = (xPos1, yPos1, xPos2, yPos2)
            region = self.image.crop(box)

            if random.random() < imageFilterProb:
                ran = random.random() * 64
                # ran = 206.5
                region = region.point(lambda i: i - ran if (i > 116 and i < 128) else i)

                # exit()
            if random.random() < bgFilterProb:
                if targetPalette == "selective":
                    tartClr = targetClrs[int(random.random() * numTargetColors)]
                else:
                    tartClr = int(random.uniform(1, 128))

                # print(tartClr)
                region = region.point(lambda i: tartClr if (i >= 0 and i < 10) else i)


            self.image.paste(region, box)

    """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" ""

    def glitchBox(self, imageGlitchDisplacementHorizontal=10, imageGlitchDisplacementVertical=10, orientation=1):

        # if self.debug == True :  print("Glitch")
        apparentWidth = self.image.size[0]
        apparentHeight = self.image.size[1]
        dx = round(random.uniform(-imageGlitchDisplacementHorizontal, imageGlitchDisplacementHorizontal))
        dy = round(random.uniform(-imageGlitchDisplacementVertical, imageGlitchDisplacementVertical))
        #dx = int(random.uniform(1, self.config.imageGlitchSize))
        #dx = 0

        orientation = self.config.verticalOrientation

        if orientation == 1 : 
            dx = 0
            # really doing "vertical" or y-axis glitching
            # block height is uniform but width is variable

            sectionWidth = round(random.uniform(2, apparentWidth - dx))
            #sectionHeight = apparentHeight
            sectionHeight = round(random.uniform(2, apparentHeight - dy))

            # 95% of the time they dance together as mirrors
            if random.random() < 0.97:
                cp1 = self.image.crop((dx, dy, dx + sectionWidth, dy + sectionHeight))
                self.image.paste(cp1, (round(0 + dx), round(0 + dy)), cp1)
                #self.image = self.image.rotate(random.uniform(-50,50))
        else :
            # HORIZONTAL GLITCH
            #dy = 0
                    # really doing "vertical" or y-axis glitching
            # block height is uniform but width is variable

            sectionHeight = round(random.uniform(2, apparentHeight - dy))
            sectionWidth = apparentWidth

            # 95% of the time they dance together as mirrors
            if random.random() < 0.97:
                cp1 = self.image.crop((0, 0, dx + sectionWidth, sectionHeight))
                self.image.paste(cp1, (round(dx), round(0 + dy)))


    """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" ""

    def augment(self):
        if self.frameCount > 39:
            # print(self.tempClrCount)
            self.tempClrCount += 1
            self.frameCount = 0

    """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" ""

    def remove(self, arrayList):
        arrayList.remove(self)
        pass

    """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" ""

    def move(self):
        if self.setForRemoval != True:
            # self.image.paste(self.presentationImage, (0,0))

            self.xPos += self.dX
            self.yPos += self.dY

            if self.dY > 0 and self.yPos >= self.endY:
                self.callBack(self.yPos, -self.image.size[1])
                # self.yPos = -self.image.size[1]

            if self.dY < 0 and self.yPos < 0:
                self.callBack(self.yPos, self.endY)
                # self.yPos = self.endY

            if self.dX > 0 and self.xPos >= self.endX:
                self.callBack(True, self.xPos, -self.image.size[0])
                self.xPos = -self.image.size[0]

            if self.dX < 0 and self.xPos < -self.image.size[0]:
                self.callBack(True, self.xPos, self.endX)
                self.xPos = self.endX

            self.x = self.xPos + self.xOffset
            self.y = self.yPos + self.yOffset + self.config.vOffset

            rangeOfRot = 20  # + (self.x /100)

            self.imageRotation = random.uniform(-rangeOfRot, rangeOfRot)

            # self.image = self.image.rotate(self.imageRotation, expand=True)
            # self.image = ScaleRotateTranslate(self.image,self.imageRotation, (self.image.size[0]/2,self.image.size[1]/2), None, (1.03,1.0) )

    """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" ""

    def loadImage(self, arg):
        self.image = Image.open(arg, "r")
        self.image.load()
        self.imgHeight = self.image.getbbox()[3]
  
        self.imageOriginal = Image.open(arg, "r")
        self.imageOriginal.load()
  
        return True

    """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" ""

    def update(self):
        if self.useBlink == True:
            if random.random() > 0.9998 and self.blink == False:
                self.blink = True
                self.blinkNum = int(random.uniform(32, 256))
                self.blinkCount = 0
                self.blinkStationary = True if (random.random() > 0.15) else False

            if self.blink:
                self.blinkCount += 1
                # self.x -= self.dX
                if self.blinkCount % 8 == 0:
                    self.draw.rectangle(
                        (0, 0, self.image.size[0], self.image.size[1]), fill=(0)
                    )
                    # self.y = -100
                elif self.blinkCount % 4 == 0:
                    # self.y = 0
                    self.image.paste(self.imageCopy, (0, 0), self.imageCopy)

                if self.blinkCount >= self.blinkNum:
                    self.image.paste(self.imageCopy, (0, 0), self.imageCopy)
                    if random.random() > 0.5:
                        self.x += self.image.size[1]
                    self.blink = False

            if self.blinkStationary == False:
                self.panImage()
            elif random.random() > 0.995:
                self.blinkStationary = False

        else:
            self.panImage()

    """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" ""

    def init(self):
        global action, countLimit

        # print(countLimit)
        count = 0
        # fillColor(True)
        # Constantly re-calls the requested action util
        # the count runs out - for long running plays
        # the countlimit just gets reset
        while count < countLimit:
            try:
                if action == "play":
                    playImage(False, 7)
                elif action == "pan":
                    panImage()
                elif action == "present":
                    presentImage()
                count += 1
            except KeyboardInterrupt:
                print("Stopping....")
                exit()
                break

    """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" ""

    def debugMessage(self, arg):

        if self.debug:
            print(arg)

    """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" ""

    def presentImage(self):
        global frame, count, xOffset, yOffset, dX, dY, image, panRangeLimit, scrollSpeed, useJitter, useBlink, imageCopy, presentTime
        imageCopyTemp = imageCopy
        enhancer = ImageEnhance.Brightness(imageCopyTemp)
        imageCopyTemp = enhancer.enhance(brightnessFactor)

        config.render(
            imageCopyTemp,
            int(xOffset),
            int(yOffset),
            imageCopy.size[0],
            imageCopy.size[1],
            False,
        )
        config.actions.drawBlanks()
        time.sleep(presentTime)

    """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" ""

    def panImage(self):

        self.jitter = False

        # this doesnt work because it just draws to the existing size of the loaded image ... so gets cut off
        # if(random.random() > .9) : draw.rectangle((0,image.size[1] -10,32,image.size[1] + config.screenHeight), fill = (12), outline = (0))

        self.stepSize = 1
        if abs(self.dY) > 1:
            self.stepSize = abs(self.dY)

        if self.useJitter:
            # Correct jitter
            if random.random() < self.jitterResetRate:
                self.jitter = False
                self.dY = 0
                self.yPos = 0
            # Allow jitter
            if random.random() < self.jitterRate:
                self.jitter = True
            # Do jitter
            if self.jitter:
                self.dY = random.uniform(-self.jitterRange, self.jitterRange)

        self.move()

    """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" ""

    def fillColor(self, force=False):
        global bgFillColor
        if random.random() > 0.8 or force:
            config.matrix.Fill(bgFillColor)
        else:
            config.matrix.Fill(bgFillColor)

    """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" ""

    def rotateImage(self, angle):
        global image, matrix
        image = config.image.resize((32, 32))
        image = image.rotate(angle, Image.BICUBIC, 1)
        config.matrix.Clear()
        config.matrix.SetImage(config.image.im.id, -8, -8)

    """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" ""

    # Even still images get this called as it runs the glitches as well ...
    def animate(self, holdAnimation=False, forceGlitch=False):

        # This needs fixing  - currently requires extra frame
        # at end of gif  --
        skipTime = False


        if random.random() < self.config.pausePlayProb :
            #print ("Holding 2 " + str(self.config.pausePlayProb))
            self.holdAnimation = True

        realFrame = 0
        try:
            if self.holdAnimation != True:
                self.image.seek(self.image.tell() + 1)
                realFrame = self.image.tell()

                if realFrame > self.config.forceGlitchFrameCount:
                    forceGlitch = True

        except EOFError:
            self.image.seek(0)
            #print("fail", realFrame)
            skipTime = True
            pass

        #self.frameCount += 1

        glitchChance  = self.config.imageGlitchProb
        if self.holdAnimation == True :
            glitchChance *= self.glitchChanceWhenPausedFactor
            
        if random.random() < glitchChance or forceGlitch:
            r = int(random.uniform(2, 10))
            if self.holdAnimation == True : 
                #print("Glitch :" + str(self.imageGlitchCount))
                self.imageGlitchCount += 1

            for i in range(0, r):
                self.glitchBox(-self.config.imageGlitchDisplacement,self.config.imageGlitchDisplacement,)

        if self.config.useImageFilter:
            if random.random() < self.config.imageFilterProb:
                #print("filterize")
                self.filterize()

        #self.augment()
        
    
    """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" ""
    
    def setupSpriteSheetSlices(self) :
        self.sliceImages = []
        for r in range(0, self.frameRows):
            for c in range(0, self.frameCols):
                xPos = self.sliceWidth * c
                yPos = self.sliceHeight * r
                xPos2 = xPos + self.sliceWidth
                yPos2 = yPos + self.sliceHeight
                slice = self.imageOriginal.crop((xPos,yPos,xPos2,yPos2))
                if self.resizeAnimationtoFit == True :
                    slice = slice.resize((self.animationWidth, self.animationHeight))
                self.sliceImages.append(slice)
    
    
    """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" "" 
  
    # Even still images get this called as it runs the glitches as well ...
    def animateSpriteSheet(self, holdAnimation=False, forceGlitch=False):
    
     
        # This needs fixing  - currently requires extra frame
        # at end of gif  --
        skipTime = False


        if random.random() < self.config.pausePlayProb :
            #print ("Holding 2 " + str(self.config.pausePlayProb))
            self.holdAnimation = True

        realFrame = 0
  
  
        try:
            if self.holdAnimation != True:
                self.image = self.sliceImages[self.frameCount]
                # print(self.frameCount,self.totalFrames)
                if self.frameCount >= (self.totalFrames) :
                    self.frameCount  = 0
                else :
                    self.frameCount += 1
                
                if realFrame > self.config.forceGlitchFrameCount:
                    forceGlitch = True

        except EOFError:
            # self.image.seek(0)
            #print("fail", realFrame)
            skipTime = True
            pass

        #self.frameCount += 1

        glitchChance  = self.config.imageGlitchProb
        if self.holdAnimation == True :
            glitchChance *= self.glitchChanceWhenPausedFactor
            
        if random.random() < glitchChance or forceGlitch:
            r = int(random.uniform(2, 10))
            if self.holdAnimation == True : 
                #print("Glitch :" + str(self.imageGlitchCount))
                self.imageGlitchCount += 1

            for i in range(0, r):
                self.glitchBox(-self.config.imageGlitchDisplacement,self.config.imageGlitchDisplacement,)

        if self.config.useImageFilter:
            if random.random() < self.config.imageFilterProb:
                #print("filterize")
                self.filterize()

        #self.augment()
        
    """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" ""

    def playImage(self, randomizeTiming=False, frameLimit=3):
        global config
        animate(randomizeTiming, frameLimit)


###############################
