import math
import random
import time

import numpy as np
from PIL import Image, ImageDraw
from scipy.spatial import Voronoi

from modules.holder_director import Director

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

        vx = fx * directionx * config.particleXSpeed
        vy = fy * directiony * config.particleYSpeed

        # Initially, make radius fall into one of the systems bands - like quanta
        radialBand = round(random.uniform(1, config.numOrbits))
        radius = PSref.radialBand * radialBand
        # radius = random.uniform(1, PSref.maxRadius)
        rSpeed = random.uniform(config.rSpeedMin, config.rSpeedMax) * direction

        if config.rSpeedRadialProportional:
            rSpeed = (
                random.uniform(config.rSpeedMin, config.rSpeedMax)
                / radius
                * 100.0
                * direction
            )

        # xPos = round(random.uniform(0, config.canvasWidth))
        # yPos = round(random.uniform(0, config.canvasHeight))
        # angle = PSref.angle * n

        angle = 2 * math.pi * random.SystemRandom().random()
        xPos = PSref.x + radius * math.cos(angle)
        yPos = PSref.y + radius * math.sin(angle)

        if PSref.movementMode == 0:
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
        # self.movementMode = 0
        self.orbit = orbit
        self.sizeNum = 1 if random.random() < 0.5 else 2

    def setNewAttributes(self):
        pass


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
        self.movementMode = config.movementMode
        self.wBase = round(random.uniform(10, config.outerRadius))

        self.directionProb = config.directionProb
        self.xSpeed = random.SystemRandom().random() * config.systemSpeed
        self.ySpeed = random.SystemRandom().random() * config.systemSpeed

    def setCenter(self):
        # initial center position
        self.x = round(random.uniform(self.initXRange[0], self.initXRange[1]))
        self.y = round(random.uniform(self.initYRange[0], self.initYRange[1]))

    def resetParticles(self):
        # after they have drifted, calculate new parameters
        for pRef in self.particles:
            pRef.movementMode = self.movementMode
            dx = pRef.xPos - self.x
            dy = pRef.yPos - self.y
            pRef.radius = round(math.sqrt(dx * dx + dy * dy))
            pRef.angle = math.atan2(dy, dx)

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

        # dx = config.canvasWidth - self.x
        # dy = config.canvasHeight - self.y
        # self.maxRadius = (
        #     math.sqrt(
        #         config.canvasWidth * config.canvasWidth
        #         + config.canvasHeight * config.canvasHeight
        #     )
        #     * .5
        # )
        self.maxRadius = config.maxRadius
        self.radialBand = self.maxRadius / config.numOrbits

        for n in range(self.numParticles):
            pDot = ParticleDot()
            pDot.setUp(self, n)
            pDot.movementMode = self.movementMode
            self.particles.append(pDot)

    def moveParticles(self):
        for ref in self.particles:
            if ref.movementMode == 0:
                if random.SystemRandom().random() < config.chanceParticleWillMove:
                    ref.xPos += ref.vx
                    ref.yPos += ref.vy

                # dx = ref.xPos - self.x
                # dy = ref.yPos - self.y

                # r = round(math.sqrt(dx * dx + dy * dy))

                # if r > ref.radius/1 and ref.orbit:
                #     # print(r, ref.radius, ref.orbit)
                #     ref.mode = 0

                if ref.xPos >= config.xRange or ref.xPos <= 0:
                    ref.vx *= -1
                if ref.yPos >= config.yRange or ref.yPos <= 0:
                    # ref.setUp(self, ref.id)
                    ref.vy *= -1
            else:
                ref.xPos = self.x + ref.radius * math.cos(ref.angle)
                ref.yPos = self.y + ref.radius * math.sin(ref.angle)
                ref.angle += ref.rSpeed

            # if random.random() < config.particleResetProb:
            #     ref.setUp(self, ref.id)

    def drawVoronoi(self):
        # Draw the Voronoi cells
        pointsArray = []
        for i in range(config.num_cells):
            ref = self.particles[i]
            pointsArray.append([ref.xPos, ref.yPos])

        points = np.array(pointsArray)
        vor = Voronoi(points)

        vVertices = vor.vertices
        vRegions = vor.regions
        # vPoints = vor.points
        vPointRegion = (vor.point_region).tolist()

        # clrIndex = 0
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
                        outline=(config.lineColor[0], config.lineColor[1], config.lineColor[2], round(config.lineAlpha)),
                        width=config.lineWidth,
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
                    round(ref.xPos) + 1,
                    round(ref.yPos) + 1,
                ),
                fill=(200, 0, 0, 255),
            )

    def move(self):
        # the whole system
        self.x += self.xSpeed
        self.y += self.ySpeed
        self.moveParticles()
        self.drawVoronoi()

        if config.showParticlePostions:
            self.drawParticlesDots()


"""""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" ""


def withinRange(arg, target, diff):
    val = round(arg)
    test1 = round(target + diff)
    test2 = round(target - diff)
    return val <= test1 and val >= test2


# an override
def structuredSetup():
    xD = 18
    yD = 5
    rows = math.floor(math.sqrt(len(PS.particles)))
    # print(f"rows = {rows}")
    cols = rows
    i = 0
    rads = math.pi / cols * 1
    for r in range(cols):
        for c in range(cols):
            xD = round(
                config.canvasWidth / 2 + (math.cos(rads * c)) * config.canvasWidth / 2
            )
            p = PS.particles[i]
            p2 = PS.particles[i - 1]
            p.xPos = 1 + xD
            p.yPos = 1 + yD * r
            # p2.xPos = 300 - xD
            # p2.yPos = 400 - yD
            # yD += 30
            # xD += 20
            p.movementMode = 0
            p2.movementMode = 0
            i += 1
        yD += 2
        # for i in range(1, len(PS.particles), 2):
    #     p = PS.particles[i]
    #     p2 = PS.particles[i - 1]
    #     p.xPos = 10 + xD
    #     p.yPos = 400 - yD
    #     p2.xPos = 300 - xD
    #     p2.yPos = 400 - yD
    #     yD += 30
    #     xD += 20
    #     p.movementMode = 0
    #     p2.movementMode = 0


def filterRemapImage(config):
    if config.filterRemapping:
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


def changePalettes():
    config.colorSetA = config.colorSets[
        math.floor(random.SystemRandom().random() * len(config.colorSets))
    ]
    config.colorSetB = config.colorSets[
        math.floor(random.SystemRandom().random() * len(config.colorSets))
    ]
    setColors()


def setColors():
    for i in range(config.num_cells):
        clr = (
            config.colorSetA[round(random.uniform(0, len(config.colorSetA) - 1))]
            if random.random() < 0.50
            else config.colorSetB[round(random.uniform(0, len(config.colorSetB) - 1))]
        )
        # clr = colorutils.randomColor()
        config.nr[i] = round(clr[0] * config.brightness)
        config.ng[i] = round(clr[1] * config.brightness)
        config.nb[i] = round(clr[2] * config.brightness)


def initializeParameters():
    config.nx = []
    config.ny = []
    config.nvx = []
    config.nvy = []
    config.nr = []
    config.ng = []
    config.nb = []

    for _ in range(config.num_cells):
        _setCellAttributes()


# TODO Rename this here and in `initializeParameters`
def _setCellAttributes():
    config.nx.append(random.randrange(-config.xRange / 4, 1.25 * config.xRange))
    config.ny.append(random.randrange(-config.yRange / 4, 1.25 * config.yRange))
    config.nvx.append(random.randrange(-2, 2))
    config.nvy.append(random.randrange(-2, 2))
    config.nr.append(50)
    config.ng.append(50)
    config.nb.append(50)


def resetSystem(fullReset=False):
    global PS, config

    if not fullReset:
        # if random.SystemRandom().random() < config.changeMovementModeProb :
        #     config.movementMode = 1 if random.SystemRandom().random() < .5 else 0

        config.movementMode = 1 if config.movementMode == 0 else 0
        if config.movementMode == 0 and random.SystemRandom().random() < 0.5:
            config.useStructuredSetup = config.useStructuredSetup == False
        else:
            config.useStructuredSetup = False

        PS.setNewAttributes()
        # PS.setCenter()
        PS.resetParticles()

    else:
        regularParticleSetup()
    if config.useStructuredSetup:
        structuredSetup()


# TODO Rename this here and in `resetSystem`
def regularParticleSetup():
    global PS, config
    initializeParameters()
    setColors()

    PS = ParticleSystem(config)
    PS.setCenter()
    PS.setNewAttributes()
    PS.setUp()

    # print(f"new sys {config.movementMode }  useStructuredSetup {config.useStructuredSetup}")


"""""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" ""


def runWork():
    global redrawSpeed
    global PS
    redrawSpeed = 0.02
    while True:
        _loopChecksAndActions(redrawSpeed)


# TODO Rename this here and in `runWork`
def _loopChecksAndActions(redrawSpeed):
    config.directorController.checkTime()
    if config.directorController.advance:
        iterate()
    if config.changeColorSetTime > 0:
        config.paletteController.checkTime()
        if config.paletteController.advance:
            changePalettes()
    if config.changeTime > 0:
        config.changeTimeController.checkTime()
        if config.changeTimeController.advance:
            resetSystem(False)
    if config.totalResetTime > 0:
        config.systemController.checkTime()
        if config.systemController.advance:
            resetSystem(True)

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

    config.fadeRate += config.fadeRateDelta

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

    # dithering movement
    if random.random() < config.filterRemappingProb:
        filterRemapImage(config)

    config.render(config.image, 0, 0, config.canvasWidth, config.canvasHeight)


def main(run=True):
    """Initializes and runs the Voronoi particle system."""
    global config
    global redrawSpeed
    global PS
    global workConfig

    _load_particle_config(config)
    _load_background_config(config)
    _load_rendering_config(config)
    _load_filter_config(config)
    _load_color_config(config)
    _initialize_system(config)

    if run:
        runWork()


def _load_particle_config(config):
    """Loads particle-related configuration parameters."""
    config.minParticles = int(workConfig.get("particles", "minParticles"))
    config.maxParticles = int(workConfig.get("particles", "maxParticles"))
    config.speedFactorMin = float(workConfig.get("particles", "speedFactorMin"))
    config.speedFactorMax = float(workConfig.get("particles", "speedFactorMax"))
    config.particleXSpeed = float(workConfig.get("particles", "particleXSpeed"))
    config.particleYSpeed = float(workConfig.get("particles", "particleYSpeed"))
    config.rSpeedMin = float(workConfig.get("particles", "rSpeedMin"))
    config.rSpeedMax = float(workConfig.get("particles", "rSpeedMax"))
    config.rSpeedRadialProportional = workConfig.getboolean("particles", "rSpeedRadialProportional")
    config.showParticlePostions = workConfig.getboolean("particles", "showParticlePostions", fallback=False)
    config.numOrbits = int(workConfig.get("particles", "numOrbits", fallback=12))

    config.initXRangeMin = int(workConfig.get("particles", "initXRangeMin"))
    config.initXRangeMax = int(workConfig.get("particles", "initXRangeMax"))
    config.initYRangeMin = int(workConfig.get("particles", "initYRangeMin"))
    config.initYRangeMax = int(workConfig.get("particles", "initYRangeMax"))
    config.systemRotation = float(workConfig.get("particles", "systemRotation"))
    config.systemSpeed = float(workConfig.get("particles", "systemSpeed", fallback=0))
    config.directionProb = float(workConfig.get("particles", "directionProb", fallback=0.5))
    config.maxRadius = float(workConfig.get("particles", "maxRadius", fallback=config.canvasWidth / 2))
    config.innerRadius = int(workConfig.get("particles", "innerRadius"))
    config.outerRadius = int(workConfig.get("particles", "outerRadius"))
    config.xRange = int(workConfig.get("particles", "xRange"))
    config.yRange = int(workConfig.get("particles", "yRange"))

    config.useStructuredSetup = workConfig.getboolean("particles", "useStructuredSetup", fallback=False)
    config.movementMode = int(workConfig.get("particles", "movementMode", fallback=0))
    config.particleResetProb = float(workConfig.get("particles", "particleResetProb"))
    config.chanceParticleWillMove = float(workConfig.get("particles", "chanceParticleWillMove", fallback=1.0))
    config.changeMovementModeProb = float(workConfig.get("particles", "changeMovementModeProb", fallback=0.0))
    config.orbitProb = float(workConfig.get("particles", "orbitProb"))


def _load_background_config(config):
    """Loads background-related configuration parameters."""
    bgColorSets = workConfig.get("particles", "bgColorSets").split(",")
    config.bgColorSets = []
    for bg in bgColorSets:
        bgColor = workConfig.get(bg, "bgColor").split(",")
        bgColors = [int(x) for x in bgColor]
        config.bgColorSets.append(bgColors)
    config.bgColor = config.bgColorSets[0]
    config.bgColorAlpha = int(workConfig.get("particles", "bgColorAlpha"))


def _load_rendering_config(config):
    """Loads rendering-related configuration parameters."""
    config.fadeRate = float(workConfig.get("particles", "fadeRate"))
    config.lineAlpha = float(workConfig.get("particles", "lineAlpha"))
    config.lineWidth = int(workConfig.get("particles", "lineWidth", fallback=2))
    config.lineColor = list(map(int, workConfig.get("particles", "lineColor", fallback="40,0,0").split(",")))
    config.cellAlpha = float(workConfig.get("particles", "cellAlpha"))
    config.fadeRateDelta = float(workConfig.get("particles", "fadeRateDelta"))
    config.fadeRateNewSystemThreshold = float(workConfig.get("particles", "fadeRateNewSystemThreshold"))

    config.totalResetTime = float(workConfig.get("particles", "totalResetTime", fallback=33))
    config.changeTime = float(workConfig.get("particles", "changeTime", fallback=10))

    if config.totalResetTime > 0:
        config.systemController = Director(config)
        config.systemController.slotRate = config.totalResetTime

    if config.changeTime > 0:
        config.changeTimeController = Director(config)
        config.changeTimeController.slotRate = config.changeTime

    config.image = Image.new("RGBA", (config.canvasWidth, config.canvasHeight))
    config.draw = ImageDraw.Draw(config.image)


def _load_filter_config(config):
    """Loads filter-related configuration parameters."""
    config.filterRemapping = workConfig.getboolean("particles", "filterRemapping", fallback=False)
    config.filterRemappingProb = float(workConfig.get("particles", "filterRemappingProb", fallback=0.0))
    config.filterRemapMinHorzSize = int(workConfig.get("particles", "filterRemapMinHorzSize", fallback=24))
    config.filterRemapMinVertSize = int(workConfig.get("particles", "filterRemapMinVertSize", fallback=24))
    config.filterRemapMaxHorzSize = int(workConfig.get("particles", "filterRemapMaxHorzSize", fallback=24))
    config.filterRemapMaxVertSize = int(workConfig.get("particles", "filterRemapMaxVertSize", fallback=24))
    config.filterRemapRangeX = int(workConfig.get("particles", "filterRemapRangeX", fallback=config.canvasWidth))
    config.filterRemapRangeY = int(workConfig.get("particles", "filterRemapRangeY", fallback=config.canvasHeight))


def _load_color_config(config):
    """Loads color-related configuration parameters."""
    config.colorSets = []
    config.colorGroupsList = workConfig.get("particles", "colorGroups", fallback="colorSetA,colorSetB").split(",")
    config.mixColorSets = workConfig.getboolean("particles", "mixColorSets", fallback=False)
    config.changeColorSetTime = float(workConfig.get("particles", "changeColorSetTime", fallback=0))

    if config.changeColorSetTime > 0:
        config.paletteController = Director(config)
        config.paletteController.slotRate = config.changeColorSetTime

    for grp in config.colorGroupsList:
        rawColorSetAVals = workConfig.get("particles", grp).replace("\n", "").replace(" ", "")
        colorSetAVals = rawColorSetAVals.split("|")
        colorSet = []
        for element in colorSetAVals:
            if element != "":
                clr = [int(x) for x in element.split(",")]
                colorSet.append(clr)
        config.colorSets.append(colorSet)

    config.colorSetA = config.colorSets[0]
    config.colorSetB = config.colorSets[1]
    config.num_cells = config.maxParticles
    config.imgx, config.imgy = config.image.size


def _initialize_system(config):
    """Initializes the particle system and related parameters."""
    global PS
    resetSystem(True)
    config.slotRate = float(workConfig.get("particles", "slotRate", fallback=0.03))
    config.directorController = Director(config)
    config.directorController.slotRate = config.slotRate
'''
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

    try:
        config.showParticlePostions = workConfig.getboolean(
            "particles", "showParticlePostions"
        )
    except Exception as e:
        print(e)
        config.showParticlePostions = False

    try:
        config.useStructuredSetup = workConfig.getboolean(
            "particles", "useStructuredSetup"
        )
    except Exception as e:
        print(e)
        config.useStructuredSetup = False

    try:
        config.numOrbits = int(workConfig.get("particles", "numOrbits"))
    except Exception as e:
        print(e)
        config.numOrbits = 12
    
    try:
        config.lineWidth = int(workConfig.get("particles", "lineWidth"))
        config.lineColor = list( 
            map(
                lambda x : int(x), workConfig.get("particles", "lineColor").split(",")
                )
            )
    except Exception as e:
        print(e)
        config.lineWidth = 2
        config.lineColor = [40,0,0]

    try:
        config.movementMode = int(workConfig.get("particles", "movementMode"))
    except Exception as e:
        print(e)
        config.movementMode = 0

    config.initXRangeMin = int(workConfig.get("particles", "initXRangeMin"))
    config.initXRangeMax = int(workConfig.get("particles", "initXRangeMax"))
    config.initYRangeMin = int(workConfig.get("particles", "initYRangeMin"))
    config.initYRangeMax = int(workConfig.get("particles", "initYRangeMax"))

    config.systemRotation = float(workConfig.get("particles", "systemRotation"))

    try:
        config.maxRadius = float(workConfig.get("particles", "maxRadius"))
    except Exception as e:
        print(e)
        config.maxRadius = config.canvasWidth / 2

    try:
        config.systemSpeed = float(workConfig.get("particles", "systemSpeed"))
    except Exception as e:
        print(e)
        config.systemSpeed = 0

    try:
        config.directionProb = float(workConfig.get("particles", "directionProb"))
    except Exception as e:
        print(e)
        config.directionProb = 0.5

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
    try:
        config.changeMovementModeProb = float(
            workConfig.get("particles", "changeMovementModeProb")
        )
    except Exception as e:
        print(e)
        config.changeMovementModeProb = 0.0

    config.fadeRate = float(workConfig.get("particles", "fadeRate"))
    config.lineAlpha = float(workConfig.get("particles", "lineAlpha"))
    config.cellAlpha = float(workConfig.get("particles", "cellAlpha"))
    config.fadeRateDelta = float(workConfig.get("particles", "fadeRateDelta"))

    config.fadeRateNewSystemThreshold = float(
        workConfig.get("particles", "fadeRateNewSystemThreshold")
    )

    config.particleResetProb = float(workConfig.get("particles", "particleResetProb"))

    try:
        config.totalResetTime = float(workConfig.get("particles", "totalResetTime"))
    except Exception as e:
        print(e)
        config.totalResetTime = 33

    try:
        config.changeTime = float(workConfig.get("particles", "changeTime"))
    except Exception as e:
        print(e)
        config.changeTime = 10

    if config.totalResetTime > 0:
        config.systemController = Director(config)
        config.systemController.slotRate = config.totalResetTime

    if config.changeTime > 0:
        config.changeTimeController = Director(config)
        config.changeTimeController.slotRate = config.changeTime

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

    config.colorSets = []

    try:
        config.colorGroupsList = workConfig.get("particles", "colorGroups").split(",")
        config.mixColorSets = workConfig.getboolean("particles", "mixColorSets")
        config.changeColorSetTime = float(
            workConfig.get("particles", "changeColorSetTime")
        )
        config.paletteController = Director(config)
        config.paletteController.slotRate = config.changeColorSetTime
    except Exception as e:
        print(e)
        config.colorGroupsList = ["colorSetA", "colorSetB"]
        config.mixColorSets = False
        config.changeColorSetTime = 0

    for grp in config.colorGroupsList:
        rawColorSetAVals = workConfig.get("particles", grp).replace("\n", "")
        rawColorSetAVals = rawColorSetAVals.replace(" ", "")
        colorSetAVals = rawColorSetAVals.split("|")
        colorSet = []
        for element in colorSetAVals:
            if element != "":
                clr = [int(x) for x in element.split(",")]
                colorSet.append(clr)
        config.colorSets.append(colorSet)

    config.colorSetA = config.colorSets[0]
    config.colorSetB = config.colorSets[1]

    config.num_cells = config.maxParticles
    config.imgx, config.imgy = config.image.size

    resetSystem(True)

    try:
        config.slotRate = float(workConfig.get("particles", "slotRate"))
    except Exception as e:
        print(e)
        config.slotRate = 0.03

    # managing speed of animation and framerate
    config.directorController = Director(config)
    config.directorController.slotRate = config.slotRate

    if run:
        runWork()
'''