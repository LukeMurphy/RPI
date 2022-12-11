import math
import random
import threading
import time

from modules import colorutils
from PIL import Image, ImageDraw, ImageEnhance, ImageFont, ImageOps

"""""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" ""


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


"""""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" ""


class ParticleDot:
    def __init__(self):
        pass

    def setUp(self, p, n):
        # variation in initial velocity
        direction = 1 if p.directionProb < 0.5 else -1
        orbit = True if p.orbitProb <= config.orbitProb else False
        fx = random.random() * p.fFactor + 1
        fy = random.random() * p.fFactor + 1
        vx = math.cos(p.angle * n) * fx * direction
        vy = math.sin(p.angle * n) * fy * direction
        r = int(random.uniform(0, 255) * p.brightness)
        g = int(random.uniform(0, 200) * p.brightness)
        b = int(random.uniform(0, 255) * p.brightness)
        radius = random.uniform(1, p.maxRadius)


        # Make radius fall into one of the systems bands - like quata

        radialBand = round(random.uniform(1,12))

        radius = p.radialBand * radialBand

        rSpeed = random.uniform(100, 200) / radius / 10.0

        xPos = p.x
        yPos = p.y
        angle = p.angle * n

        if direction == -1:
            xPos = round(random.uniform(0, config.canvasWidth))
            yPos = round(random.uniform(0, config.canvasHeight))
            angle = math.atan2(yPos - p.y, xPos - p.x)
            vx = math.cos(angle) * fx * direction
            vy = math.sin(angle) * fy * direction

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
        self.mode = 1
        self.orbit = orbit
        self.sizeNum = 1 if random.random() < 0.5 else 2


"""""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" ""


class ParticleSystem:
    def __init__(self, config):
        self.config = config
        self.x = 0
        self.y = 0
        self.particles = []
        self.done = False
        self.orientation = 1
        self.initXRange = [config.initXRangeMin, config.initXRangeMax]
        self.initYRange = [config.initYRangeMin, config.initYRangeMax]

    def setNewAttributes(self):
        self.bands = round(random.uniform(12, 24))
        self.wBase = round(random.uniform(220, config.canvasWidth))

        self.xSpeed = random.random() / 2.0
        self.ySpeed = random.random()
        self.ySpeed = 0

        self.radialsArray = []
        self.radials = round(random.uniform(120, 300))
        self.rads = 2 * math.pi / self.radials

        self.angleOffset = 0.0
        self.angleOffsetSpeed = random.uniform(0, math.pi / 300)
        innerRadius = self.wBase / 3
        outerRadius = self.wBase
        skipRatio = random.random() + 0.3
        for i in range(0, self.radials):
            ir = innerRadius + random.uniform(-50, 50)
            outr = outerRadius + random.uniform(-50, 50)
            skip = 0 if random.random() < skipRatio else 1
            self.radialsArray.append([ir, outr, skip])

    def setCenter(self):
        # initial center position
        self.x = round(random.uniform(self.initXRange[0], self.initXRange[1]))
        self.y = round(random.uniform(self.initYRange[0], self.initYRange[1]))

    def setUp(self):

        self.directionProb = random.uniform(0.4, 0.6)
        self.orbitProb = config.orbitProb
        # Number of sparks
        self.p = int(5 + (random.uniform(config.minParticles, config.maxParticles)))
        self.angle = 2 * math.pi / self.p

        config.numberDone = round(self.p / 5)

        # Speed factor
        self.fFactor = int(random.uniform(config.speedFactorMin, config.speedFactorMax))

        """
		if config.rotation != 0:
			approxVisibleArea = self.config.canvasWidth * 0.6
			ran = random.random() * approxVisibleArea
			ran = 64 + random.uniform(-96, 96)
			self.x = int(ran + self.config.canvasWidth / 2)
		"""

        # print (int(self.config.canvasWidth/2 + approxVisibleArea/2), self.x)

        self.brightness = self.config.brightness
        self.sparkleBrightness = self.config.brightness
        self.brightness = 0.9
        self.sparkleBrightness = 0.8

        # speed that each light fades to black / sparkle

        self.decr_r = round(random.uniform(0.25, 1))
        self.decr_g = round(random.uniform(0.25, 1))
        self.decr_b = round(random.uniform(0.25, 1))

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
            * 1.5
        )

        self.radialBand = self.maxRadius / 12


        for n in range(0, self.p):
            pDot = ParticleDot()
            pDot.setUp(self, n)
            self.particles.append(pDot)

    def move(self):

        self.x += self.xSpeed
        self.y += self.ySpeed

        if self.x > config.canvasWidth - round(self.wBase / 4):
            self.xSpeed = 0

        for q in range(0, self.p):
            ref = self.particles[q]

            if ref.mode == 1:
                ref.xPos += ref.vx
                ref.yPos += ref.vy

                dx = ref.xPos - self.x
                dy = ref.yPos - self.y

                r = round(math.sqrt(dx * dx + dy * dy))

                if r > ref.radius/2 and ref.orbit == True:
                    # print(r, ref.radius, ref.orbit)
                    ref.mode = 0

            else:
                ref.xPos = self.x + ref.radius/1 * math.cos(ref.angle) * 0.2
                ref.yPos = self.y + ref.radius/1 * math.sin(ref.angle) * 0.2
                ref.angle += ref.rSpeed

            """
			"""

            self.particles[q].clr[0] = self.particles[q].clr[0] - self.decr_r
            self.particles[q].clr[1] = self.particles[q].clr[1] - self.decr_g
            self.particles[q].clr[2] = self.particles[q].clr[2] - self.decr_b

            if self.particles[q].clr[0] <= 0:
                self.particles[q].clr[0] = 0
            if self.particles[q].clr[1] <= 0:
                self.particles[q].clr[1] = 0
            if self.particles[q].clr[2] <= 0:
                self.particles[q].clr[2] = 0

            r = self.particles[q].clr[0]
            g = self.particles[q].clr[1]
            b = self.particles[q].clr[2]

            sumOfClrs = (
                self.particles[q].clr[0]
                + self.particles[q].clr[1]
                + self.particles[q].clr[2]
            )

            """
			# a pixel wind changes the cascade
			if self.config.sideWind and sumOfClrs > 100:
				config.vx = round(2 - random.random() * 4)
				ref.vx = config.vx
				self.deacellerationx = 0.75
			"""

            # Sparkles !!
            if random.random() < config.sparkleProb:
                r = int(220 * self.sparkleBrightness)
                g = int(220 * self.sparkleBrightness)
                b = int(255 * self.sparkleBrightness)

            # if (q ==0) : print (particles[q]['c'][0])
            xDisplayPos = ref.xPos
            yDisplayPos = ref.yPos

            if (
                xDisplayPos < self.config.canvasWidth
                and xDisplayPos > 0
                and yDisplayPos > 0
                and yDisplayPos <= config.canvasHeight
            ):
                try:

                    if ref.sizeNum == 2:
                        config.draw.rectangle(
                            (
                                round(xDisplayPos),
                                round(yDisplayPos),
                                round(xDisplayPos) + 1,
                                round(yDisplayPos) + 0,
                            ),
                            fill=(r, g, b, 255),
                        )
                    else:
                        config.draw.rectangle(
                            (
                                round(xDisplayPos),
                                round(yDisplayPos),
                                round(xDisplayPos) + 0,
                                round(yDisplayPos) + 0,
                            ),
                            fill=(r, g, b, 255),
                        )
                    # config.image.putpixel((round(xDisplayPos), round(yDisplayPos)), (r, g, b))
                    # config.image.putpixel((round(xDisplayPos)+1, round(yDisplayPos)), (r, g, b))
                    # config.image.putpixel((round(xDisplayPos), round(yDisplayPos)+1), (r, g, b))
                    # config.image.putpixel((round(xDisplayPos)+1, round(yDisplayPos)+1), (r, g, b))
                except Exception as e:
                    print(str(e))

            """
			"""
            if (
                xDisplayPos > config.canvasWidth
                or yDisplayPos > config.canvasHeight
                or yDisplayPos < 0
                or xDisplayPos < 0
            ):
                ref.setUp(self, ref.id)

            if random.random() < config.particleResetProb:
                ref.setUp(self, ref.id)


"""""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" ""


def drawBands(p):

    wBase = p.wBase
    wDiff = round(wBase / p.bands)

    aBase = 0
    aDiff = 10

    rBase = config.rBase
    gBase = config.gBase
    bBase = config.bBase

    rBase2 = config.rBase2
    gBase2 = config.gBase2
    bBase2 = config.bBase2

    rDiff = config.rDiff
    gDiff = config.gDiff
    bDiff = config.bDiff

    for i in range(0, p.bands):

        w = wBase - i * wDiff
        x0 = p.x - w / 2
        y0 = p.y - w / 2
        x1 = p.x + w / 2
        y1 = p.y + w / 2

        a = (
            round(config.fadeRate + aBase)
            if config.fadeRate > aBase
            else config.fadeRate
        )

        config.draw.ellipse((x0, y0, x1, y1), fill=(4, 4, bBase, round(a)))

        if i == 1:
            config.draw.ellipse((x0, y0, x1, y1), fill=(rBase, gBase, bBase, round(a)))

        if i == 0 or i == 12:
            config.draw.ellipse(
                (x0, y0, x1, y1), fill=(rBase2, gBase2, bBase, round(a))
            )
        rBase += rDiff
        gBase += gDiff
        bBase += bDiff

    i = 0
    p.angleOffset += p.angleOffsetSpeed
    for n in range(0, len(p.radialsArray)):
        a = i * p.rads + p.angleOffset
        x0 = math.cos(a) * p.radialsArray[n][0] + p.x
        y0 = math.sin(a) * p.radialsArray[n][0] + p.y
        x1 = math.cos(a) * p.radialsArray[n][1] + p.x
        y1 = math.sin(a) * p.radialsArray[n][1] + p.y
        i += 1
        if p.radialsArray[n][2] == 0:
            config.draw.line((x0, y0, x1, y1), fill=(50, 30, 0, 75))


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

    # Fade out the sparkle

    config.draw.rectangle(
        (0, 0, config.canvasWidth, config.canvasHeight),
        fill=(
            config.bgColor[0],
            config.bgColor[1],
            config.bgColor[2],
            round(config.fadeRate),
        ),
    )

    drawBands(PS)

    PS.move()

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

    config.render(config.image, 0, 0, config.canvasWidth, config.canvasHeight)

    # Done


def main(run=True):
    global config
    global redrawSpeed
    global PS

    config.minParticles = int(workConfig.get("particles", "minParticles"))
    config.maxParticles = int(workConfig.get("particles", "maxParticles"))

    config.speedFactorMin = float(workConfig.get("particles", "speedFactorMin"))
    config.speedFactorMax = float(workConfig.get("particles", "speedFactorMax"))

    config.initXRangeMin = int(workConfig.get("particles", "initXRangeMin"))
    config.initXRangeMax = int(workConfig.get("particles", "initXRangeMax"))
    config.initYRangeMin = int(workConfig.get("particles", "initYRangeMin"))
    config.initYRangeMax = int(workConfig.get("particles", "initYRangeMax"))

    config.systemRotation = float(workConfig.get("particles", "systemRotation"))

    bgColorSets = (workConfig.get("particles", "bgColorSets")).split(",")
    config.bgColorSets = []
    for bg in bgColorSets:
        bgColor = (workConfig.get(bg, "bgColor")).split(",")
        bgColors = list(int(x) for x in bgColor)
        config.bgColorSets.append(bgColors)

    # choose the first bg color - generally the dark one
    config.bgColor = config.bgColorSets[0]

    config.rBase = int(workConfig.get("particles", "rBase"))
    config.gBase = int(workConfig.get("particles", "gBase"))
    config.bBase = int(workConfig.get("particles", "bBase"))
    config.rBase2 = int(workConfig.get("particles", "rBase2"))
    config.gBase2 = int(workConfig.get("particles", "gBase2"))
    config.bBase2 = int(workConfig.get("particles", "bBase2"))
    config.rDiff = int(workConfig.get("particles", "rDiff"))
    config.gDiff = int(workConfig.get("particles", "gDiff"))
    config.bDiff = int(workConfig.get("particles", "bDiff"))

    config.fadeRate = float(workConfig.get("particles", "fadeRate"))
    config.fadeRateDelta = float(workConfig.get("particles", "fadeRateDelta"))
    config.sparkleProb = float(workConfig.get("particles", "sparkleProb"))
    config.fadeRateNewSystemThreshold = float(
        workConfig.get("particles", "fadeRateNewSystemThreshold")
    )

    config.particleResetProb = float(workConfig.get("particles", "particleResetProb"))
    config.totalResetProb = float(workConfig.get("particles", "totalResetProb"))
    config.orbitProb = float(workConfig.get("particles", "orbitProb"))

    config.image = Image.new("RGBA", (config.canvasWidth, config.canvasHeight))
    config.draw = ImageDraw.Draw(config.image)
    PS = ParticleSystem(config)
    PS.setCenter()
    PS.setNewAttributes()
    PS.setUp()

    # managing speed of animation and framerate
    config.directorController = Director(config)
    config.directorController.slotRate = 0.03

    if run:
        runWork()