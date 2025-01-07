import math
import random
import threading
import time

from modules import colorutils
from PIL import Image, ImageDraw, ImageEnhance, ImageFont, ImageOps
from modules.holder_director import Holder
from modules.holder_director import Director

from scipy.spatial import Voronoi
import numpy as np

"""""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" ""


class ParticleDot:
    def __init__(self):
        pass

    def setUp(self, PSref, n):
        # variation in initial velocity
        direction = 1.0 if random.random() < PSref.directionProb else -1.0
        directionx = 1.0 if random.random() < PSref.directionProb else -1.0
        directiony = 1.0 if random.random() < PSref.directionProb else -1.0
        orbit = PSref.orbitProb <= config.orbitProb

        fx = random.random() * PSref.fFactor + 0
        fy = random.random() * PSref.fFactor + 0

        r = int(random.uniform(0, 255) * PSref.brightness)
        g = int(random.uniform(0, 200) * PSref.brightness)
        b = int(random.uniform(0, 255) * PSref.brightness)
        radius = random.uniform(1, PSref.maxRadius)

        vx = fx * directionx * config.particleXSpeed
        vy = fy * directiony * config.particleYSpeed

        # Make radius fall into one of the systems bands - like quanta

        radialBand = round(random.uniform(1, 12))

        radius = PSref.radialBand * radialBand

        rSpeed = random.uniform(config.rSpeedMin, config.rSpeedMax) * direction

        if config.rSpeedRadialProportional == True:
            rSpeed = random.uniform(config.rSpeedMin, config.rSpeedMax) / radius * 100.0 * direction

        xPos = PSref.x + round(random.uniform(0, config.canvasWidth))
        yPos = PSref.y + round(random.uniform(0, config.canvasHeight))
        
        angle = PSref.angle * n
        
        if PSref.movementMode == 0 :
            xPos = round(random.uniform(0, config.canvasWidth))
            yPos = round(random.uniform(0, config.canvasHeight))

        # if direction == -1:
        #     xPos = round(random.uniform(0, config.canvasWidth))
        #     yPos = round(random.uniform(0, config.canvasHeight))
        #     angle = math.atan2(yPos - p.y, xPos - p.x)
        #     vx = math.cos(angle) * fx * direction
        #     vy = math.sin(angle) * fy * direction

        self.id = n
        self.xPos = xPos
        self.yPos = yPos
        self.vx = vx
        self.vy = vy
        self.clr = [r, g, b]
        self.done = 0
        self.angle = angle
        self.radius = radius
        self.rSpeed = rSpeed
        self.movementMode = 0
        self.orbit = orbit
        self.sizeNum = 1 if random.random() < 0.5 else 2


"""""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" ""


class ParticleSystem:
    def __init__(self, config):
        print()
        print("===================")
        print("New Particle System")
        print()
        self.config = config
        self.x = 0
        self.y = 0
        self.particles = []
        self.done = False
        self.orientation = 1
        self.initXRange = [config.initXRangeMin, config.initXRangeMax]
        self.initYRange = [config.initYRangeMin, config.initYRangeMax]
        self.movementMode = config.movementMode
        self.brightness = config.brightness
        self.directionProb = random.uniform(0, 1)

    def setNewAttributes(self):
        self.bands = round(random.uniform(12, 24))
        self.wBase = round(random.uniform(220, config.canvasWidth))

        self.directionProb = config.directionProb
        self.xSpeed = random.SystemRandom().random() * config.particleXSpeed
        self.ySpeed = random.random() * config.particleYSpeed
        self.xSpeed = 0
        self.ySpeed = 0

        self.radialsArray = []
        self.radials = round(random.uniform(120, 300))
        self.rads = 2 * math.pi / self.radials

        self.angleOffset = 0.0
        self.angleOffsetSpeed = random.uniform(0, math.pi / 300)
        innerRadius = self.wBase / 3
        outerRadius = self.wBase
        skipRatio = random.random() + 0.3
        for _ in range(self.radials):
            ir = innerRadius + random.uniform(-config.innerRadius, config.innerRadius)
            outr = outerRadius + random.uniform(-config.innerRadius, config.outerRadius)
            skip = 0 if random.random() < skipRatio else 1
            self.radialsArray.append([ir, outr, skip])

    
    def setCenter(self):
        # initial center position
        self.x = round(random.uniform(self.initXRange[0], self.initXRange[1]))
        self.y = round(random.uniform(self.initYRange[0], self.initYRange[1]))

    
    def setUp(self):
        self.orbitProb = config.orbitProb
        # Number of sparks
        self.numParticles = int(
            5 + (random.uniform(config.minParticles, config.maxParticles))
        )
        self.angle = 2 * math.pi / self.numParticles

        config.numberDone = round(self.numParticles / 5)

        # Speed factor
        self.fFactor = random.uniform(config.speedFactorMin, config.speedFactorMax)
        self.brightness = self.config.brightness

        # vertical deacelleration
        self.deacelleration = random.uniform(0.8, 0.99)

        # horizontal deacelleration
        self.deacellerationx = random.uniform(0.8, 0.95)

        dx = config.canvasWidth - self.x
        dy = config.canvasHeight - self.y
        self.maxRadius = (
            math.sqrt(
                config.canvasWidth * config.canvasWidth
                + config.canvasHeight * config.canvasHeight
            )
            * 2.5
        )

        self.radialBand = self.maxRadius / 12
        # config.movementMode = 0 if random.random() < 0.5 else 1
        for n in range(self.numParticles):
            pDot = ParticleDot()
            pDot.setUp(self, n)
            pDot.movementMode = self.movementMode
            self.particles.append(pDot)

    
    def moveParticles(self):
        for q in range(self.numParticles):
            ref = self.particles[q]

            if ref.movementMode == 0:
                if (
                    random.SystemRandom().random()
                    < config.chanceParticleWillMove
                ):
                    ref.xPos += ref.vx
                    ref.yPos += ref.vy

                dx = ref.xPos - self.x
                dy = ref.yPos - self.y

                r = round(math.sqrt(dx * dx + dy * dy))

                # if r > ref.radius/1 and ref.orbit:
                #     # print(r, ref.radius, ref.orbit)
                #     ref.mode = 0

            else:
                ref.xPos = self.x + ref.radius / 1 * math.cos(ref.angle) * 0.2
                ref.yPos = self.y + ref.radius / 1 * math.sin(ref.angle) * 0.2
                ref.angle += ref.rSpeed

            if (
                ref.xPos > config.xRange
                or ref.yPos > config.yRange
                or ref.yPos < -config.yRange
                or ref.xPos < -config.xRange
            ):
                ref.setUp(self, ref.id)

            if random.random() < config.particleResetProb:
                ref.setUp(self, ref.id)


    def drawVoronoi(self):
        # Draw the Voronoi cells
        pointsArray = []
        for i in range(config.num_cells):
            ref = self.particles[i]
            pointsArray.append([ref.xPos, ref.yPos])
            # config.draw.rectangle((ref.xPos,ref.yPos,ref.xPos+3,ref.yPos+3), fill=(200,200,200,255))

        points = np.array(pointsArray)
        vor = Voronoi(points)

        vVertices = vor.vertices
        vRegions = vor.regions
        vPoints = vor.points
        vPointRegion = (vor.point_region).tolist()

        clrIndex = 0
        for j, region in enumerate(vRegions):
            for i in range(len(vPointRegion)):
                if j == vPointRegion[i]:
                    break

            if -1 not in region:
                polygon = [tuple(vVertices[p].tolist()) for p in region]
                if (
                    polygon
                    and i < config.num_cells
                    and (
                        not withinRange(self.particles[j].xPos, self.x, 3)
                        or not withinRange(self.particles[j].yPos, self.y, 3)
                    )
                ):
                    config.draw.polygon(
                        polygon,
                        outline=(40, 0, 0, round(config.lineAlpha)),
                        width=2,
                        fill=(
                            config.nr[i],
                            config.ng[i],
                            config.nb[i],
                            round(config.cellAlpha),
                        ),
                    )

    def drawParticlesDots(self):
        for q in range(self.numParticles):
            ref = self.particles[q]
            config.draw.ellipse(
                (
                    round(ref.xPos),
                    round(ref.yPos),
                    round(ref.xPos) + 10,
                    round(ref.yPos) + 10,
                ),
                fill=(200, 0, 0, 255),
            )
        
    def move(self):
        # the whole system
        self.x += self.xSpeed
        self.y += self.ySpeed
        self.moveParticles()
        self.drawVoronoi()



"""""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" ""

def withinRange(arg, target, diff):
    val = round(arg)
    test1 = round(target + diff)
    test2 = round(target - diff)
    return val <= test1 and val >= test2


"""""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" ""

def runWork():
    global redrawSpeed
    global PS
    redrawSpeed = 0.02
    while True:
        config.directorController.checkTime()
        if config.directorController.advance == True:
            iterate()
        time.sleep(redrawSpeed)


def iterate():
    global config
    global PS
    config.vx = 0

    config.draw.rectangle(
        (0, 0, config.canvasWidth, config.canvasHeight),
        fill=(
            config.bgColor[0],
            config.bgColor[1],
            config.bgColor[2],
            # config.bgColorAlpha,
            round(config.fadeRate),
        ),
    )

    PS.move()
    # drawBands(PS)

    config.fadeRate += config.fadeRateDelta
    # if random.random() < config.totalResetProb:
    #     PS.setUp()

    if config.fadeRate > 255:
        config.fadeRate = 30
        config.fadeRateDelta = random.uniform(0.1, 2)

        if config.fadeRateDelta <= config.fadeRateNewSystemThreshold:
            # when the system reaches a visible chaotic crescendo that will last a few seconds, remake the system
            # behind the chaos and start again - choose a new background, reset the center, set new radial attributes
            # renew the particle dots that travel
            # bgChoice = math.floor(random.uniform(0,len(config.bgColorSets)))
            config.bgColor = random.choice(config.bgColorSets)
            # print(f"ALL NEW {config.bgColor}  {config.fadeRateDelta}")
            if random.random() < config.totalResetProb:
                PS.setCenter()
                PS.setNewAttributes()
                PS.setUp()

    # dithering movement
    if random.random() < config.filterRemappingProb:
        filterRemapImage(config)

    config.render(config.image, 0, 0, config.canvasWidth, config.canvasHeight)


def filterRemapImage(config):
    if config.filterRemapping :
        config.useFilters = True
        config.remapImageBlock = False

        startX = round(random.uniform(0, config.filterRemapRangeX))
        startY = round(random.uniform(0, config.filterRemapRangeY))
        endX = round(
            random.uniform(config.filterRemapMinHorzSize, config.filterRemapMaxHorzSize)
        )
        endY = round(
            random.uniform(config.filterRemapMinVertSize, config.filterRemapMaxVertSize)
        )
        config.remapImageBlockSection = [startX, startY, startX + endX, startY + endY]
        config.remapImageBlockDestination = [startX, startY]


def structuredSetup():
    xD = 0
    yD = 0
    for i in range(1, len(PS.particles), 2):
        p = PS.particles[i]
        p2 = PS.particles[i - 1]
        p.xPos = 10 + xD
        p.yPos = 400 - yD
        p2.xPos = 300 - xD
        p2.yPos = 400 - yD
        yD += 30
        xD += 20


def main(run=True):
    global config
    global redrawSpeed
    global PS
    global workConfig

    config.minParticles = int(workConfig.get("particles", "minParticles"))
    config.maxParticles = int(workConfig.get("particles", "maxParticles"))

    config.speedFactorMin = float(workConfig.get("particles", "speedFactorMin"))
    config.speedFactorMax = float(workConfig.get("particles", "speedFactorMax"))
    config.particleXSpeed = float(workConfig.get("particles", "particleXSpeed"))
    config.particleYSpeed = float(workConfig.get("particles", "particleYSpeed"))

    config.rSpeedMin = float(workConfig.get("particles", "rSpeedMin"))
    config.rSpeedMax = float(workConfig.get("particles", "rSpeedMax"))
    config.rSpeedRadialProportional = workConfig.getboolean(
        "particles", "rSpeedRadialProportional"
    )

    config.initXRangeMin = int(workConfig.get("particles", "initXRangeMin"))
    config.initXRangeMax = int(workConfig.get("particles", "initXRangeMax"))
    config.initYRangeMin = int(workConfig.get("particles", "initYRangeMin"))
    config.initYRangeMax = int(workConfig.get("particles", "initYRangeMax"))

    config.systemRotation = float(workConfig.get("particles", "systemRotation"))
    
    try:
        config.directionProb = float(workConfig.get("particles", "directionProb"))
    except Exception as e:
        print(e)
        config.directionProb = .5

    bgColorSets = (workConfig.get("particles", "bgColorSets")).split(",")
    config.bgColorSets = []
    for bg in bgColorSets:
        bgColor = (workConfig.get(bg, "bgColor")).split(",")
        bgColors = [int(x) for x in bgColor]
        config.bgColorSets.append(bgColors)

    # choose the first bg color - generally the dark one
    config.bgColor = config.bgColorSets[0]

    config.bgColorAlpha = int(workConfig.get("particles", "bgColorAlpha"))
    config.innerRadius = int(workConfig.get("particles", "innerRadius"))
    config.outerRadius = int(workConfig.get("particles", "outerRadius"))
    config.xRange = int(workConfig.get("particles", "xRange"))
    config.yRange = int(workConfig.get("particles", "yRange"))

    try:
        config.chanceParticleWillMove = float(
            workConfig.get("particles", "chanceParticleWillMove")
        )
    except Exception as e:
        print(e)
        config.chanceParticleWillMove = 1.0
        
    config.fadeRate = float(workConfig.get("particles", "fadeRate"))
    config.lineAlpha = float(workConfig.get("particles", "lineAlpha"))
    config.cellAlpha = float(workConfig.get("particles", "cellAlpha"))
    config.fadeRateDelta = float(workConfig.get("particles", "fadeRateDelta"))

    config.fadeRateNewSystemThreshold = float(
        workConfig.get("particles", "fadeRateNewSystemThreshold")
    )

    config.particleResetProb = float(workConfig.get("particles", "particleResetProb"))
    config.totalResetProb = float(workConfig.get("particles", "totalResetProb"))
    config.orbitProb = float(workConfig.get("particles", "orbitProb"))

    config.image = Image.new("RGBA", (config.canvasWidth, config.canvasHeight))
    config.draw = ImageDraw.Draw(config.image)

    try:
        config.filterRemapping = workConfig.getboolean("particles", "filterRemapping")
        config.filterRemappingProb = float(
            workConfig.get("particles", "filterRemappingProb")
        )
        config.filterRemapMinHorzSize = int(
            workConfig.get("particles", "filterRemapMinHorzSize")
        )
        config.filterRemapMinVertSize = int(
            workConfig.get("particles", "filterRemapMinVertSize")
        )
        config.filterRemapMaxHorzSize = int(
            workConfig.get("particles", "filterRemapMaxHorzSize")
        )
        config.filterRemapMaxVertSize = int(
            workConfig.get("particles", "filterRemapMaxVertSize")
        )
        config.filterRemapRangeX = int(workConfig.get("particles", "filterRemapRangeX"))
        config.filterRemapRangeY = int(workConfig.get("particles", "filterRemapRangeY"))
    except Exception as e:
        print(e)
        config.filterRemapping = False
        config.filterRemappingProb = 0.0
        config.filterRemapMinHorzSize = 24
        config.filterRemapMinVertSize = 24
        config.filterRemapMaxHorzSize = 24
        config.filterRemapMaxVertSize = 24
        config.filterRemapRangeX = config.canvasWidth
        config.filterRemapRangeY = config.canvasHeight

    config.num_cells = config.maxParticles
    # config.resolutionOfSquares = int(workConfig.get("particles", "resolutionOfSquares"))

    config.imgx, config.imgy = config.image.size
    config.nx = []
    config.ny = []
    config.nvx = []
    config.nvy = []
    config.nr = []
    config.ng = []
    config.nb = []
    
    
    try:
        colorGroups = workConfig.get("particles", "colorGroups").split(",")
    except Exception as e:
        print(e)
        colorGroups = ["colorSetA","colorSetB"]

    #  for now, just have two color sets to blend the colors
    rawColorSetAVals = workConfig.get("particles", colorGroups[0]).replace("\n", "")
    rawColorSetAVals = rawColorSetAVals.replace(" ", "")
    colorSetAVals = rawColorSetAVals.split("|")
    colorSetA = []
    for element in colorSetAVals:
        if element != "":
            clr = [int(x) for x in element.split(",")]
            colorSetA.append(clr)

    rawColorSetBVals = workConfig.get("particles", colorGroups[1]).replace("\n", "")
    rawColorSetBVals = rawColorSetBVals.replace(" ", "")
    colorSetBVals = rawColorSetBVals.split("|")
    colorSetB = []
    for element in colorSetBVals:
        if element != "":
            clr = [int(x) for x in element.split(",")]
            colorSetB.append(clr)

    for _ in range(config.num_cells):
        config.nx.append(random.randrange(-config.xRange / 4, 1.25 * config.xRange))
        config.ny.append(random.randrange(-config.yRange / 4, 1.25 * config.yRange))
        config.nvx.append(random.randrange(-2, 2))
        config.nvy.append(random.randrange(-2, 2))

        clr = (
            colorSetA[round(random.uniform(0, len(colorSetA) - 1))]
            if random.random() < 0.50
            else colorSetB[round(random.uniform(0, len(colorSetB) - 1))]
        )
        # clr = colorutils.randomColor()
        config.nr.append(round(clr[0] * config.brightness))
        config.ng.append(round(clr[1] * config.brightness))
        config.nb.append(round(clr[2] * config.brightness))

    try:
        config.movementMode = int(workConfig.get("particles", "movementMode"))
    except Exception as e:
        print(e)
        config.movementMode = 0

    PS = ParticleSystem(config)
    PS.setCenter()
    PS.setNewAttributes()
    PS.setUp()

    # structuredSetup()

    # managing speed of animation and framerate
    config.directorController = Director(config)
    config.directorController.slotRate = 0.03

    if run:
        runWork()
