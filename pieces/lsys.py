#!/usr/bin/python
import PIL.Image
from PIL import Image, ImageDraw, ImageMath, ImageEnhance
from PIL import ImageChops

# from modules import colorutils
# Import the essentials to everything
import time, random, math

"""""" """""" """""" """""" """""" """""" """""" """""" """""" """""" ""


class Director:
    targetSlotArray = []
    currentSlot = 0
    totalSlots = 0
    slotRate = 0.02
    advance = False
    color = [255, 255, 255]
    direction = 1

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


class LPoint:
    def __init__(self):
        self.xPos = 0
        self.yPos = 0
        self.scale = 1
        self.isTerminal = 0
        self.isBranch = 0
        self.angle = 0
        self.angleDisplay = 0
        self.segmentLength = 0
        self.segmentWidth = 0


"""""" """""" """""" """""" """""" """""" """""" """""" """""" """""" ""


class Lsys:

    def __init__(self, config):
        print("========================")
        print("Init Lsys")
        self.config = config
        strg = ""

        # F draws a terminal line
        # B draws a line
        # () denotes a branch
        # + - are angle changes

        self.Axiom = config.Axiom
        self.Rule1 = config.Rule1
        self.Rule2 = config.Rule2
        self.iternations = config.iternations

        self.segmentLength = config.segmentLength
        self.segmentWidth = config.segmentWidth
        self.segmentDecrement = config.segmentDecrement
        self.segmentWidthDecrement = config.segmentWidthDecrement
        self.Rule2 = config.Rule2

        self.useRandom = config.useRandom
        self.foliage = config.foliage

        self.angle = config.baseAngle
        self.branchPoints = []
        self.drawingPoints = []

        self.setUpNewDrawingParameters()
        print("========================")

    def setUpNewDrawingParameters(self):
        self.c = 0
        self.strg = ""
        self.strg = self.parse(self.Axiom)
        print("------------------")
        print(self.strg)
        print("------------------")

        self.produceDrawingPoints()

    def setupDrawing(self):
        self.branchPoints = []
        self.xPos = self.origin["xPos"]
        self.yPos = self.origin["yPos"]

    def redraw(self, e):
        if incrStart < strg.length - incrRange:
            produceDrawingPoints()

    def parse(self, arg):
        self.finalString = arg
        self.c += 1
        l = len(self.Rule2)
        if self.c < self.iternations + 1:
            arg = arg.replace("G", self.Rule1)
            arg = arg.replace("F", self.Rule2)
            return self.parse(arg)
        return arg

    def produceDrawingPoints(self):
        xPos = 0
        yPos = 0
        a = -math.pi / 2
        decriment = 1
        decrimentWidth = 1
        c = 0

        lpt = LPoint()
        lpt.xPos = 0
        lpt.yPos = 0
        lpt.angle = config.baseAngle
        lpt.angleDisplay = config.baseAngle
        lpt.scale = 1
        lpt.isTerminal = 0
        lpt.isBranch = 0
        lpt.name = ""
        lpt.previousPoint = LPoint()

        self.branchPoints = []
        self.drawingPoints = []
        config.branchPoints = []
        config.nodeSets = []

        self.drawingPoints.append(lpt)
        self.branchPoints.append(lpt)
        config.nodeSets.append([lpt, lpt])

        lastBranchPoint = self.branchPoints[0]
        lastPoint = config.nodeSets[len(config.nodeSets) - 1][1]

        lastxPos = xPos
        lastyPos = yPos

        for i in range(len(self.strg)):
            instruction = self.strg[i]

            if instruction not in ("(", ")"):
                if instruction == "+":
                    a += config.baseAngle + random.uniform(
                        -config.angleRange * math.pi, config.angleRange * math.pi
                    )
                elif instruction == "-":
                    a -= config.baseAngle + random.uniform(
                        -config.angleRange * math.pi, config.angleRange * math.pi
                    )
                elif instruction == "G" or instruction == "F":
                    previousPoint = lastPoint

                    lastPoint.isTerminal = 0

                    lpt = LPoint()
                    lpt.previousPoint = previousPoint
                    lpt.segmentLength = self.segmentLength * decriment
                    lpt.segmentWidth = self.segmentWidth * decrimentWidth
                    lpt.angle = a
                    lpt.angleDisplay = a
                    lpt.isTerminal = 1
                    lpt.isBranch = 0
                    lpt.scale = decriment
                    lpt.name = "F"

                    xPos += self.segmentLength * math.cos(a)
                    yPos += self.segmentLength * math.sin(a)

                    lpt.xPos = xPos
                    lpt.yPos = yPos

                    self.drawingPoints.append(lpt)

                    lastPoint = lpt
                    lastxPos = xPos
                    lastyPos = yPos

            if instruction == "(":
                lastBranchPoint = lpt
                lpt.isBranch = 1
                lastBranchPoint.scale = decriment
                lpt.name = "X"

                self.branchPoints.append(lpt)
                config.branchPoints.append(lpt)
                decriment *= self.segmentDecrement
                decrimentWidth *= self.segmentWidthDecrement

            elif instruction == ")":
                c = 0  # self.branchPoints[-1].isTerminal

                xPos = self.branchPoints[-1].xPos
                yPos = self.branchPoints[-1].yPos

                lastPoint = self.branchPoints[-1]
                decriment = lastPoint.scale
                a = lastPoint.angle

                self.branchPoints = self.branchPoints[:-1]

        print(len(self.drawingPoints))
        # print(len(self.branchPoints))


"""""" """""" """""" """""" """""" """""" """""" """""" """""" """""" ""

"""""" """""" """""" """""" """""" """""" """""" """""" """""" """""" ""


def drawLines(arg):
    # if config.rendered != False:
    #     return
    # print("running")
    config.imageDraw.rectangle(
        (0, 0, config.canvasWidth, config.canvasHeight), fill=(220, 210, 200, 100)
    )

    for i in range(len(L.drawingPoints)):
        # Draws trunks and branches
        p1 = L.drawingPoints[i]
        p2 = p1.previousPoint

        lineWidth = round(10 * p2.scale)
        config.imageDraw.line(
            (
                p1.xPos + config.lsysOrigin[0],
                p1.yPos + config.lsysOrigin[1],
                p2.xPos + config.lsysOrigin[0],
                p2.yPos + config.lsysOrigin[1],
            ),
            width=lineWidth,
            fill=(0, 0, 0, 100),
        )
        # l = round(math.hypot(p2.xPos - p1.xPos, p2.yPos - p1.yPos))

        # temp = Image.new("RGBA", (l, l))
        # tDraw = ImageDraw.Draw(temp)
        # angleDeg = round((math.pi / 2 - p2.angleDisplay) * 180 / math.pi)
        # pRef = p1
        # d = pRef.scale
        # w = pRef.segmentWidth
        # w = 10
        # mid = round(l/2 - w/2)
        # tDraw.rectangle((0, mid, l, mid + w/2), fill=(250, 50, 250, 130))

        # if abs(angleDeg) != 90:
        #     angleDeg -= 90
            
        # temp2 = temp.rotate(angleDeg, expand=1)
        # # temp2 = temp
        # config.image.paste(
        #     temp2,
        #     (
        #         round(pRef.xPos  + config.lsysOrigin[0]),
        #         round(pRef.yPos + config.lsysOrigin[1]),
        #     ),
        #     temp2,
        # )

        # draws the terminal points
        if p1.isTerminal == 1:
            eD = 5
            config.imageDraw.ellipse(
                (
                    p1.xPos - eD + config.lsysOrigin[0],
                    p1.yPos - eD + config.lsysOrigin[1],
                    p1.xPos + eD + config.lsysOrigin[0],
                    p1.yPos + eD + config.lsysOrigin[1],
                ),
                fill=(250, 250, 0, 100),
            )
            if random.random() < 0.002:
                p1.xPos += (5 - random.random() * 10) * (1 - p1.scale)
                p1.yPos += (5 - random.random() * 10) * (1 - p1.scale)

        # draws the branch juntions
        if p1.isBranch == 1 and p1.isTerminal == 0:
            eD = 2
            config.imageDraw.ellipse(
                (
                    p1.xPos - eD + config.lsysOrigin[0],
                    p1.yPos - eD + config.lsysOrigin[1],
                    p1.xPos + eD + config.lsysOrigin[0],
                    p1.yPos + eD + config.lsysOrigin[1],
                ),
                fill=(150, 0, 0, 100),
            )

            if random.random() < 0.001:
                p1.xPos += (5 - random.random() * 10) * (1 - p1.scale)
                p1.yPos += (5 - random.random() * 10) * (1 - p1.scale)

    # for i in range(len(config.branchPoints)):
    #     pRef = config.branchPoints[i]
    #     # print(
    #     #     f"L.branchPoints[i] {config.branchPoints[i].yPos + config.lsysOrigin[1]}  name: {config.branchPoints[i].name}"
    #     # )
    #     eD = 5
    #     if pRef.isTerminal >= 0:
    #         config.imageDraw.ellipse(
    #             (
    #                 pRef.xPos - eD + config.lsysOrigin[0],
    #                 pRef.yPos - eD + config.lsysOrigin[1],
    #                 pRef.xPos + eD + config.lsysOrigin[0],
    #                 pRef.yPos + eD + config.lsysOrigin[1],
    #             ),
    #             fill=(250, 0, 0, 100),
    #         )

    # for i in range(len(L.drawingPoints)):

    #     pRef = L.drawingPoints[i]
    #     xPos = pRef.xPos + config.lsysOrigin[0]
    #     yPos = pRef.yPos + config.lsysOrigin[1]
    #     d = pRef.scale
    #     l = pRef.segmentLength
    #     w = pRef.segmentWidth

    #     temp = Image.new("RGBA", (config.segmentLength, config.segmentWidth))
    #     tDraw = ImageDraw.Draw(temp)

    #     angleDeg = round((math.pi / 2 - pRef.angleDisplay) * 180 / math.pi)

    #     if abs(angleDeg) != 90:
    #         angleDeg -= 90

    # if pRef.isTerminal == 0:
    #     tDraw.rectangle((0, 0, 0 + l, w), fill=(50, 50, 250, 130))

    #     if l == 0:
    #         tDraw.rectangle((0, 0, 2, 2), fill=(0, 0, 255, 230))

    #     temp2 = temp.rotate(angleDeg, expand=1, translate=(-0, -0))
    #     # temp2 = temp
    #     # config.image.paste(temp2, (round(xPos), round(yPos)), temp2)

    # if pRef.isTerminal == 1:
    #     tDraw.rectangle(
    #         (0, 0, 0 + l, w), fill=(20, 0, 0, 130), outline=(255, 0, 0), width=1
    #     )

    #     temp2 = temp.rotate(angleDeg, expand=1, translate=(-0, 0))
    #     # temp2 = temp
    #     # config.image.paste(temp2, (round(xPos), round(yPos)), temp2)

    # if pRef.isTerminal == 1 or pRef.isTerminal == 1:

    #     eD = 3
    #     config.imageDraw.ellipse(
    #         (
    #             pRef.xPos - eD + config.lsysOrigin[0],
    #             pRef.yPos - eD + config.lsysOrigin[1],
    #             pRef.xPos + eD + config.lsysOrigin[0],
    #             pRef.yPos + eD + config.lsysOrigin[1],
    #         ),
    #         fill=(255, 0, 255, 100),
    #     )

    # tDraw.rectangle((0, 0, 0 + l, w), fill=(100, 10, 0, 230))
    # temp2 = temp.rotate(angleDeg, expand=1, translate=(-0, 0))
    # config.image.paste(temp2, (round(xPos), round(yPos)), temp2)

    # if i > 0 and L.drawingPoints[i - 1].angle != pRef.angle:
    #     tDraw.rectangle((0, 0, 0 + l + 3, w + 3), fill=(255, 5, 0, 150))
    #     temp2 = temp.rotate(angleDeg, expand=1, translate=(-0, 0))
    #     # temp2 = temp
    #     # config.image.paste(temp2, (round(xPos), round(yPos)), temp2)
    #     # print(f"{l} {w}")
    #     # print(pRef.yPos)

    config.rendered = True


"""""" """""" """""" """""" """""" """""" """""" """""" """""" """""" ""


def main(run=True):
    global config, workConfig
    config.redrawRate = float(workConfig.get("lsys", "redrawRate"))
    config.slotRate = float(workConfig.get("lsys", "slotRate"))
    config.iternations = int(workConfig.get("lsys", "iternations"))
    config.segmentLength = int(workConfig.get("lsys", "segmentLength"))
    config.segmentWidth = int(workConfig.get("lsys", "segmentWidth"))
    config.segmentDecrement = float(workConfig.get("lsys", "segmentDecrement"))
    config.segmentWidthDecrement = float(
        workConfig.get("lsys", "segmentWidthDecrement")
    )
    config.baseAngle = math.pi / 180 * float(workConfig.get("lsys", "baseAngle"))
    config.angleRange = float(workConfig.get("lsys", "angleRange"))
    config.lsysOrigin = list(
        map(lambda x: int(int(x)), workConfig.get("lsys", "lsysOrigin").split(","))
    )
    config.useRandom = workConfig.getboolean("lsys", "useRandom")
    config.foliage = workConfig.getboolean("lsys", "foliage")
    config.Axiom = workConfig.get("lsys", "Axiom")
    config.Rule1 = workConfig.get("lsys", "Rule1")
    config.Rule2 = workConfig.get("lsys", "Rule2")

    setUp()
    if run:
        runWork()


"""""" """""" """""" """""" """""" """""" """""" """""" """""" """""" ""


def setUp():
    global L, config
    config.rendered = False
    config.image = Image.new("RGBA", (config.screenWidth, config.screenHeight))
    config.imageDraw = ImageDraw.Draw(config.image)
    config.canvasImage = Image.new("RGBA", (config.canvasWidth, config.canvasHeight))
    config.draw = ImageDraw.Draw(config.canvasImage)
    config.id = config.image.im.id
    config.director = Director(config)
    L = Lsys(config)


"""""" """""" """""" """""" """""" """""" """""" """""" """""" """""" ""


def runWork():
    global runRun
    while True:
        iterate()


"""""" """""" """""" """""" """""" """""" """""" """""" """""" """""" ""


def iterate():
    global config, L, pos, runRun
    config.director.checkTime()
    if config.director.advance == True:
        if config.rendered == False:
            L.produceDrawingPoints()
        drawLines(L)
        config.render(config.image, 0, 0, 192, 192)


"""""" """""" """""" """""" """""" """""" """""" """""" """""" """""" ""


def callBack():
    global config


"""""" """""" """""" """""" """""" """""" """""" """""" """""" """""" ""
