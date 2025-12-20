import math
import random
import time

from PIL import (
    Image,
    ImageDraw,
    ImageEnhance,
)

# config.canvasImage is the final layer or image to be rendered
# everything else gets pasted on to this image layer
# the filtering happens to this canvasImage as well

# ----------------------------------------------------##----------------------------------------------------#
def pieceLogger(arg):
    print(arg)

# ----------------------------------------------------##----------------------------------------------------#
class SpriteAnimation:

    frameWidth = 64
    frameHeight = 64
    totalFrames = 24
    frameCols = 4
    frameRows = 5
    sliceCol = 0
    sliceRow = 0

    sliceWidth = 64
    sliceHeight = 64

    sliceXOffset = 0
    sliceYOffset = 0

    startFrame = 0
    endFrame = 24
    currentFrame = 0
    playCount = 0
    step = 1
    animSpeedMin = 2
    animSpeedMax = 4

    direction = 1
    reversing = False

    animationRotation = 0
    animationRotationRate = 0

    randomPlacement = True
    resizeAnimationToFit = False
    animationWidth = 256
    animationHeight = 256

    name = "default"

    xPos = 0
    yPos = 0

    frameArray = []

    pause = False

    def __init__(self, config):
        self.config = config
        self.imageFrame = Image.new("RGBA", (self.frameWidth, self.frameHeight))

    # ----------------------------------------------------##----------------------------------------------------#
    def prepSlices(self):
        frame = 0
        self.frameArray = []
        for r in range(self.frameRows):
            for c in range(self.frameCols):
                if frame < self.totalFrames:
                    xPos = c * self.frameWidth + self.sliceXOffset
                    yPos = r * self.frameHeight + self.sliceYOffset

                    frameSlice = self.image.crop((xPos, yPos, xPos + self.sliceWidth, yPos + self.sliceHeight))

                    if self.resizeAnimationToFit:
                        frameSlice = frameSlice.resize((self.animationWidth, self.animationHeight))

                    if self.animationRotation != 0:
                        frameSlice = frameSlice.rotate(self.animationRotation, 0, 1)

                    if self.config.brightness != 1.0:
                        enhancer = ImageEnhance.Brightness(frameSlice)
                        frameSlice = enhancer.enhance(self.config.brightness)

                    if frame == 0:
                        self.firstFrame = frameSlice.copy()
                    self.frameArray.append(frameSlice)
                    frame += 1

        pieceLogger(f"{self.name} prep done. Number of Frames:{len(self.frameArray)}")
        # exit()

    # ----------------------------------------------------##----------------------------------------------------#
    
    def saveSlices(self,baseName = "img") :
        count  = 0
        
        for f in self.frameArray :
            f = f.convert("RGBA")
            suffix = "00"
            if count > 9 :
                suffix = "0"
            fn = f"{baseName}{suffix}{count}.png"
            f.save(fn)
            count += 1

    # ----------------------------------------------------##----------------------------------------------------#

    def getNextFrame(self):
        # img = self.frameArray[self.currentFrame]

        if self.totalFrames == 1:
            self.currentFrame = 0
        elif not self.pause:
            self.playCount += self.step
            if self.reversing:
                if self.playCount % self.animSpeed == 0:
                    self.currentFrame += self.direction

                if self.currentFrame >= self.endFrame:
                    self.direction *= -1
                    self.currentFrame = self.endFrame - 1

                    # if self.direction > 0 :
                    #     self.currentFrame = self.endFrame

                if self.currentFrame < self.startFrame:
                    self.direction *= -1
                    self.currentFrame = self.startFrame
                    # if self.direction < 0 :
                    #     self.currentFrame = self.startFrame
            elif self.playCount % self.animSpeed == 0:
                self.currentFrame += 1
                if self.currentFrame >= self.endFrame:
                    self.currentFrame = self.startFrame

    # ----------------------------------------------------##----------------------------------------------------#

    def nextFrameImg(self):
        return self.frameArray[self.currentFrame]


# ----------------------------------------------------##----------------------------------------------------#
def loadImage(spriteSheet):
    image = Image.open(spriteSheet, "r")
    image.load()
    # imgHeight = image.getbbox()[3]
    return image

class Config() :
    def __init__(self) :
        pass

def start() :
    # img = loadImage("./spritesheets/babyanimalsheet-pensive-left.png")
    img = loadImage("./spritesheets/obear-turning.png")
    # img = loadImage("./spritesheets/bbear-2.png")
    # img = loadImage("./spritesheets/babyanimalsheet-bbunny-right.png")
    # img = loadImage("./spritesheets/babyanimalsheet-bear-head-left.png")
    # img = loadImage("./spritesheets/babyanimalsheet-bunny-right-4px-offset.png")
    # img = loadImage("./spritesheets/babyanimalsheet-fig-standing-left.png")
    # img = loadImage("./spritesheets/babyanimalsheet-mousey-left.png")
    print(img)
    config = Config()
    config.brightness = 1.0
    spritesheetobj = SpriteAnimation(config)
    spritesheetobj.image = img
    spritesheetobj.frameCols = 4
    spritesheetobj.frameRows = 5
    spritesheetobj.prepSlices()
    spritesheetobj.saveSlices("obeart")

start()

