import math
import random
import time

from modules import colorutils
from PIL import Image, ImageDraw, ImageChops

# from modules.holder_director import Holder
from modules.holder_director import Director


class ParticleDot:
    def __init__(self):
        pass

    def setUp(self, p, n):
        # variation in initial velocity
        direction = 1 if p.directionProb < 0.5 else -1
        orbit = p.orbitProb <= config.orbitProb
        fx = random.SystemRandom().random() * p.fFactor + 1
        fy = random.SystemRandom().random() * p.fFactor + 1
        vx = math.cos(p.angle * n) * fx * direction
        vy = math.sin(p.angle * n) * fy * direction
        r = int(random.SystemRandom().uniform(config.rRangeMin, config.rRange) * p.brightness)
        g = int(random.SystemRandom().uniform(config.gRangeMin, config.gRange) * p.brightness)
        b = int(random.SystemRandom().uniform(config.bRangeMin, config.bRange) * p.brightness)

        radius = random.SystemRandom().uniform(1, p.maxRadius)
        self.circuitCount = 0

        # Make radius fall into one of the systems bands - like quata

        radialBand = round(random.SystemRandom().uniform(1, 12))

        radius = p.radialBand * radialBand

        rSpeed = random.SystemRandom().uniform(100, 200) / radius / 10.0

        xPos = p.x
        yPos = p.y
        angle = p.angle * n

        if direction == -1:
            xPos = round(random.SystemRandom().uniform(0, config.imageCanvasWidth))
            yPos = round(random.SystemRandom().uniform(0, config.imageCanvasHeight))
            angle = math.atan2(yPos - p.y, xPos - p.x)
            vx = math.cos(angle) * fx * direction
            vy = math.sin(angle) * fy * direction

        self.id = n
        self.xPos = xPos
        self.yPos = yPos
        self.vx = vx
        self.vy = vy
        self.clr = [r, g, b]
        pClrRange = config.particleColorRange
        clr = colorutils.getRandomColorHSVSaturated(pClrRange[0], pClrRange[1], pClrRange[2], pClrRange[3], pClrRange[4], pClrRange[5])
        self.clr = [clr[0], clr[1], clr[2]]
        self.done = 0
        self.angle = angle
        self.radius = radius
        self.rSpeed = rSpeed
        self.mode = 1
        self.orbit = orbit
        self.sizeNum = 1 if random.SystemRandom().random() < 0.5 else 2


class RadialSet:
    def __init__(self, config, wBase):
        self.config = config
        self.x = 0
        self.y = 0
        self.wBase = wBase
        self.drawRadialPolys = False
        self.radialSetMinNum = 120
        self.radialSetMaxNum = 300
        self.radialSetInnerRadiusFactor = 3
        self.radialSetInnerRadiusFactorFixedBands = 3
        self.radialSetInnerRadiusRange = [0, 0]
        self.radialSetOuterRadiusRange = [0, 0]
        self.useFixedBandColors = False

    def makeRadialsSet(self, minNum=120, maxNum=300):
        self.radialsArray = []
        self.radials = round(random.SystemRandom().uniform(minNum, maxNum))
        self.rads = 2 * math.pi / self.radials

        self.angleOffset = 0.0
        self.angleOffsetSpeed = random.SystemRandom().uniform(-math.pi / 300, math.pi / 300)

        radialSetInnerRadiusFactor = self.radialSetInnerRadiusFactor
        if self.useFixedBandColors:
            # self.radialSetInnerRadiusRange[0] = self.radialSetOuterRadiusRange[0]
            radialSetInnerRadiusFactor = self.radialSetInnerRadiusFactorFixedBands

        innerRadius = self.wBase / radialSetInnerRadiusFactor
        outerRadius = self.wBase
        skipRatio = random.SystemRandom().random() + 0.3

        if minNum == 1 and maxNum == 1:
            self.radials = 1
            self.rads = 2 * math.pi
            self.angleOffsetSpeed = math.pi / 290
            innerRadius = 10

        for _ in range(self.radials):
            ir = innerRadius + random.SystemRandom().uniform(self.radialSetInnerRadiusRange[0], self.radialSetInnerRadiusRange[1])
            outr = outerRadius + random.SystemRandom().uniform(self.radialSetOuterRadiusRange[0], self.radialSetOuterRadiusRange[1])
            skip = 0 if random.SystemRandom().random() < skipRatio else 1
            self.radialsArray.append([ir, outr, skip])

        # print(f"wBase {self.wBase} innerRadius = {innerRadius}")


class ParticleSystem:
    def __init__(self, config):
        self.config = config
        self.x = 0
        self.y = 0
        self.particles = []
        self.done = False
        self.drawRadialPolys = True
        self.orientation = 1
        self.initXRange = [config.initXRangeMin, config.initXRangeMax]
        self.initYRange = [config.initYRangeMin, config.initYRangeMax]
        self.useFixedBandColors = True
        # there is really no need for this to change the bands randomly
        self.bandWVariabilityProb = 0.00
        self.xMaxFactor = 4
        self.yMaxFactor = 4
        self.wDiff = 17

    def setNewAttributes(self, _i=0):
        self.radialSets = []

        # The rings around the center
        if not self.useFixedBandColors:
            self.bands = round(random.SystemRandom().uniform(config.PSMinBands, config.PSMaxBands))
            self.wBase = round(random.SystemRandom().uniform(config.PSRadiusMin, config.PSRadiusMax))
            self.wDiff = round(random.SystemRandom().uniform(config.bandWidthMin, config.bandWidthMax))

        if self.useFixedBandColors:
            self.setBandColors()
        self.xSpeed = random.SystemRandom().random() * config.PSXSpeed
        self.ySpeed = random.SystemRandom().random() * config.PSYSpeed

        self.xMaxFactor = config.xMaxFactor
        self.yMaxFactor = config.yMaxFactor

        self.drawRadialPolys = random.SystemRandom().random() < 0.5

        radialSet = RadialSet(config, self.wBase)
        radialSet.radialSetMinNum = config.radialSetMinNum
        radialSet.radialSetMaxNum = config.radialSetMaxNum
        radialSet.radialSetInnerRadiusFactor = config.radialSetInnerRadiusFactor
        radialSet.radialSetInnerRadiusFactorFixedBands = config.radialSetInnerRadiusFactorFixedBands
        radialSet.radialSetInnerRadiusRange = config.radialSetInnerRadiusRange
        radialSet.radialSetOuterRadiusRange = config.radialSetOuterRadiusRange
        radialSet.useFixedBandColors = self.useFixedBandColors

        radialSet.makeRadialsSet(config.radialSetMinNum, config.radialSetMaxNum)
        self.radialSets.append(radialSet)

        # the 33s hand
        radialSet = RadialSet(config, self.wBase)
        radialSet.makeRadialsSet(1, 1)
        self.radialSets.append(radialSet)

    def setBandColors(self):
        self.bandColors = config.bandColors

        # created transition bands
        self.bandColorsAdjusted = []
        bandColorSteps = round(random.uniform(1, 3))

        for c in range(len(self.bandColors) - 1):
            color1 = self.bandColors[c]
            color2 = self.bandColors[c + 1]

            rDiff = (color2[0] - color1[0]) / bandColorSteps
            gDiff = (color2[1] - color1[1]) / bandColorSteps
            bDiff = (color2[2] - color1[2]) / bandColorSteps

            self.bandColorsAdjusted.extend(
                [
                    round(color1[0] + rDiff * i),
                    round(color1[1] + gDiff * i),
                    round(color1[2] + bDiff * i),
                ]
                for i in range(bandColorSteps)
            )
        # adjusting the apparent brightness of some bands as they
        # read over-bright - can be modified anytime
        for c in range(len(self.bandColorsAdjusted)):
            color = self.bandColorsAdjusted[c]
            sumOfColors = color[0] + color[1] + color[2]
            if sumOfColors > 330 and c < 13:
                for cx in range(3):
                    color[cx] *= 0.8

        self.bands = bandColorSteps * len(self.bandColors)

        self.bandGoldColors = config.bandGoldColors

        self.wBase = round(
            random.SystemRandom().uniform(config.PSRadiusMin + config.PSRadiusFixedColorMinInternalRadius, config.PSRadiusMax + config.PSRadiusFixedColorMinInternalRadius)
        )
        self.wDiff = round(random.SystemRandom().uniform(config.bandWidthMin, config.bandWidthMax))

        self.bandWidthsSet = []
        self.bandWidthsSet.extend(
            round(
                random.SystemRandom().uniform(
                    config.PSFixedColorRadiusDiffMin,
                    config.PSFixedColorRadiusDiffMax,
                )
            )
            for _ in range(self.bands)
        )

        self.bandWidth = round(random.uniform(3, 12))
        self.bandDecriment = round(random.uniform(3, 12))
        self.bandApha = round(random.uniform(140, 190))

    def setCenter(self, _i=0):
        # initial center position
        self.x = round(random.SystemRandom().uniform(self.initXRange[0], self.initXRange[1]))
        self.y = round(random.SystemRandom().uniform(self.initYRange[0], self.initYRange[1]))

        if _i == 0:
            self.x = round(random.SystemRandom().uniform(0, 128))


    def setUp(self, _i=0):

        self.directionProb = random.SystemRandom().uniform(0.4, 0.6)
        self.orbitProb = config.orbitProb
        # Number of sparks
        self.p = int(5 + (random.SystemRandom().uniform(config.minParticles, config.maxParticles)))
        self.angle = 2 * math.pi / self.p

        config.numberDone = round(self.p / 5)

        # Speed factor
        self.fFactor = int(random.SystemRandom().uniform(config.speedFactorMin, config.speedFactorMax))

        """
		if config.rotation != 0:
			approxVisibleArea = self.config.canvasWidth * 0.6
			ran = random.SystemRandom().random() * approxVisibleArea
			ran = 64 + random.SystemRandom().uniform(-96, 96)
			self.x = int(ran + self.config.canvasWidth / 2)
		"""

        # print (int(self.config.canvasWidth/2 + approxVisibleArea/2), self.x)

        self.brightness = self.config.brightness
        self.sparkleBrightness = self.config.brightness
        # self.brightness = 0.9
        # self.sparkleBrightness = 0.8

        # speed that each light fades to black / sparkle

        self.decr_r = round(random.SystemRandom().uniform(0.25, 1))
        self.decr_g = round(random.SystemRandom().uniform(0.25, 1))
        self.decr_b = round(random.SystemRandom().uniform(0.25, 1))

        # vertical deacelleration
        self.deacelleration = random.SystemRandom().uniform(0.8, 0.99)

        # horizontal deacelleration
        self.deacellerationx = random.SystemRandom().uniform(0.8, 0.95)

        # dx = config.canvasWidth - self.x
        # dy = config.canvasHeight - self.y
        self.maxRadius = math.sqrt(config.imageCanvasWidth * config.imageCanvasWidth + config.imageCanvasHeight * config.imageCanvasHeight) * config.PSRadiusFactor1

        self.radialBand = self.maxRadius / 12

        for n in range(self.p):
            pDot = ParticleDot()
            pDot.setUp(self, n)
            self.particles.append(pDot)

        # print("----------------")
        # print(f"PS.useFixedBandColors : {self.useFixedBandColors}")
        # print(f"config.bgColor: {config.bgColor} config.fadeRateDelta:{config.fadeRateDelta}")
        # print(f"PS.bands: {self.bands} PS.wDiff: {self.wDiff}  PS.wBase: {self.wBase}")
        # print("----------------")

    def move(self):
        """Updates the position of the particle system and its particles."""
        self._update_system_position()
        for q in range(self.p):
            self._update_particle(q)

    def _update_system_position(self):
        """Updates the position of the particle system."""
        self.x += self.xSpeed
        self.y += self.ySpeed

        if self.x > config.canvasWidth - round(self.wBase / self.xMaxFactor):
            self.xSpeed = 0
        if self.y > config.canvasHeight - round(self.wBase / self.yMaxFactor):
            self.ySpeed = 0
        if self.y < -2:
            self.ySpeed = 0

    def _update_particle(self, q):
        """Updates the position, color, and drawing of a single particle."""
        ref = self.particles[q]

        if ref.mode == 1:
            self._move_particle_linear(ref)
        else:
            self._move_particle_orbit(ref)

        self._update_particle_color(q)
        self._draw_particle(ref, q)

        if random.SystemRandom().random() < config.particleResetProb:
            ref.setUp(self, ref.id)

    def _move_particle_linear(self, ref):
        """Updates the particle's position based on linear movement."""
        ref.xPos += ref.vx
        ref.yPos += ref.vy

        dx = ref.xPos - self.x
        dy = ref.yPos - self.y

        r = round(math.sqrt(dx * dx + dy * dy))

        if r > ref.radius / 2 and ref.orbit:
            ref.mode = 0

        if config.horizontalContinuity:
            ref.xPos %= config.imageCanvasWidth
        if config.verticalContinuity:
            ref.xPos %= config.imageCanvasWidth
            ref.yPos %= config.imageCanvasHeight

    def _move_particle_orbit(self, ref):
        """Updates the particle's position based on orbital movement."""
        ref.xPos = self.x + ref.radius / 1 * math.cos(ref.angle) * 0.2
        ref.yPos = self.y + ref.radius / 1 * math.sin(ref.angle) * 0.2
        ref.angle += ref.rSpeed

    def _update_particle_color(self, q):
        """Updates the color of a single particle, including sparkle effect."""
        for i in range(3):
            self.particles[q].clr[i] = max(0, self.particles[q].clr[i] - getattr(self, "decr_" + "rgb"[i]))

        if random.SystemRandom().random() < config.sparkleProb:
            self.particles[q].clr = [int(220 * self.sparkleBrightness)] * 2 + [int(255 * self.sparkleBrightness)]

    def _draw_particle(self, ref, q):
        """Draws a single particle on the canvas with continuity handling."""
        xDisplayPos = ref.xPos
        yDisplayPos = ref.yPos

        if config.horizontalContinuity:
            xDisplayPos %= config.canvasWidth
        if config.verticalContinuity:
            xDisplayPos %= config.imageCanvasWidth
            yDisplayPos %= config.imageCanvasHeight

        if 0 <= xDisplayPos <= self.config.imageCanvasWidth and 0 <= yDisplayPos <= config.imageCanvasHeight:
            try:
                if ref.sizeNum == 2:
                    config.draw.rectangle(
                        (round(xDisplayPos), round(yDisplayPos), round(xDisplayPos) + 1, round(yDisplayPos)),
                        fill=tuple(self.particles[q].clr + [255]),
                    )
                else:
                    config.draw.rectangle(
                        (round(xDisplayPos), round(yDisplayPos), round(xDisplayPos), round(yDisplayPos)),
                        fill=tuple(self.particles[q].clr + [255]),
                    )
            except Exception as e:
                print(e)

        if yDisplayPos > config.imageCanvasHeight or yDisplayPos < 0:
            ref.setUp(self, ref.id)


"""""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" ""


def drawBands(p):
    # print("----")
    drawBandRings(p)
    drawRadials(p)


def drawBandRings(p):
    _b = p.bandWidth
    _decriment = p.bandDecriment
    _startWidth = p.wBase - config.PSRadiusFixedColorMinInternalRadius
    # _clrs = [(0, 100, 255, 50), (0, 120, 255, 50), (0, 0, 255, 50), (220, 240, 0, 50)]
    # _clrs = config.bandColors
    _setsOfRings = 1
    _alpha = p.bandApha

    if p.useFixedBandColors :
        _rings = len(p.bandColorsAdjusted)
        _clrs = p.bandColorsAdjusted
    else :
        _rings = len(p.bandGoldColors)
        _clrs = p.bandGoldColors



    _ringNum = 0
    for _ii in range(_setsOfRings):
        for _i in range(_rings):
            _xoff = round(p.x - _startWidth / 2 + _decriment * _i / 2) + round(_ii * _decriment * _rings / 2)
            _yoff = round(p.y - _startWidth / 2 + _decriment * _i / 2) + round(_ii * _decriment * _rings / 2)
            if ringImage := ringMaker(_startWidth - _decriment * _i, _b, 0, 0, (round(_clrs[_i][0]), round(_clrs[_i][1]), round(_clrs[_i][2]), _alpha)):
                # config.image.paste(ringImage, (_xoff, _yoff), mask=ringImage)
                config.drawingImage.paste(ringImage, (_xoff, _yoff), mask=ringImage)

            _ringNum += 1
        _startWidth -= _decriment * _rings


def _drawBandRings(p):
    wBase = p.wBase
    wDiff = round(wBase / p.bands)

    if p.useFixedBandColors:
        wBase = p.wBase - config.PSRadiusFixedColorMinInternalRadius
        wDiff = p.wDiff
        # print(wDiff, p.bands, wBase)

    aBase = 0
    aDiff = 1

    rBase = config.rBase
    gBase = config.gBase
    bBase = config.bBase
    aBase = config.aBase

    rBase2 = config.rBase2
    gBase2 = config.gBase2
    # bBase2 = config.bBase2
    aBase2 = config.aBase2

    rDiff = config.rDiff
    gDiff = config.gDiff
    bDiff = config.bDiff

    # Draw from the outside-in
    colorBandIndex = 0
    # goldenBandIndex = 0

    calculatedRingSize = wBase / p.bands

    aBase = 10
    aBase2 = 10

    for i in range(p.bands):

        if p.useFixedBandColors:
            wDiff = p.bandWidthsSet[i]

        w = wBase - i * wDiff

        if p.useFixedBandColors or random.SystemRandom().random() < p.bandWVariabilityProb:
            w = (p.bands - i) * calculatedRingSize
            w = max(w, config.PSRadiusFixedColorMinInternalRadius)

        if w != 0:
            x0 = p.x - w / 2
            y0 = p.y - w / 2
            x1 = p.x + w / 2
            y1 = p.y + w / 2

            if x1 < 0 or x1 < x0:
                x1 = x0
            if y1 < 0 or y1 < y0:
                y1 = y0

            a = round(config.fadeRate + aBase) if config.fadeRate > aBase else round(config.fadeRate)

            # OVERRIDE
            a = 50
            # config.draw.ellipse((x0, y0, x1, y1), fill=(5, 30, 60, round(a)))

            if p.useFixedBandColors:
                # index = p.bands - i - 1
                index = colorBandIndex
                # index = i
                rBase = round(p.bandColorsAdjusted[index][0] * config.brightness)
                gBase = round(p.bandColorsAdjusted[index][1] * config.brightness)
                bBase = round(p.bandColorsAdjusted[index][2] * config.brightness)
                aBase = 2
                colorBandIndex += 1

                if colorBandIndex >= len(p.bandColorsAdjusted):
                    colorBandIndex = 0

            # if i == 1:
            #     config.draw.ellipse((x0, y0, x1, y1), fill=(rBase, gBase, bBase, round(a)))

            # Should try to interleave the bands so that the fixed color bands integrate better
            # with the prescribed golden ones

            # if i < 0:
            #     config.draw.ellipse((x0, y0, x1, y1), fill=(255, 0, 0, 20))

            # Golden Rings
            aBase2 = 50
            if i in config.goldenRingsArray and not p.useFixedBandColors:
                config.draw.ellipse((x0, y0, x1, y1), fill=(rBase2, gBase2, bBase, aBase2))
                config.drawOverFlow.ellipse((x0, y0, x1, y1), fill=(rBase2, gBase2, bBase, aBase2))
            else:
                # OVERRIDE
                a = 50
                if p.useFixedBandColors and index == 1:
                    config.draw.ellipse((x0, y0, x1, y1), fill=(rBase, gBase, bBase, a))
                    config.draw.ellipse((x0, y0, x1, y1), outline=(rBase, gBase, bBase, a))
                    config.drawOverFlow.ellipse((x0, y0, x1, y1), outline=(rBase, gBase, bBase, a))
                else:
                    config.draw.ellipse((x0, y0, x1, y1), fill=(rBase, gBase, bBase, a))
                    config.drawOverFlow.ellipse((x0, y0, x1, y1), fill=(rBase, gBase, bBase, a))

                if i > p.bands - 3 and p.useFixedBandColors:
                    # config.draw.ellipse( (x0, y0, x1, y1), fill=(250,60,525,150) )
                    # config.draw.ellipse( (x0, y0, x1, y1), fill=(20,60,125,150) )
                    config.draw.ellipse((x0, y0, x1, y1), fill=(6, 46, 104, 2))

            if not p.useFixedBandColors:
                rBase += rDiff
                gBase += gDiff
                bBase += bDiff
                aBase += aDiff

            rBase = max(rBase, 0)
            gBase = max(gBase, 0)
            bBase = max(bBase, 0)


def drawRadials(p):
    i = 0
    for rSet in p.radialSets:
        rSet.angleOffset += rSet.angleOffsetSpeed
        polyArray = []
        numLines = len(rSet.radialsArray)

        for n in range(numLines):
            a = i * rSet.rads + rSet.angleOffset
            x0 = round(math.cos(a) * rSet.radialsArray[n][0] + p.x)
            y0 = round(math.sin(a) * rSet.radialsArray[n][0] + p.y)
            x1 = round(math.cos(a) * rSet.radialsArray[n][1] + p.x)
            y1 = round(math.sin(a) * rSet.radialsArray[n][1] + p.y)
            i += 1
            polyArray.extend(((x0, y0), (x1, y1)))
            if rSet.radialsArray[n][2] == 0:
                config.draw.line((x0, y0, x1, y1), fill=(config.radialRed, config.radialGreen, config.radialBlue, config.radialAlpha))
                config.drawOverFlow.line((x0, y0, x1, y1), fill=(config.radialRed, config.radialGreen, config.radialBlue, config.radialAlpha))
            if numLines == 1:
                config.draw.line((x0, y0, x1, y1), fill=(config.radial2Red, config.radial2Green, config.radial2Blue, config.radialAlpha))
                config.drawOverFlow.line((x0, y0, x1, y1), fill=(config.radial2Red, config.radial2Green, config.radial2Blue, config.radialAlpha))

        if rSet.drawRadialPolys:
            config.draw.polygon(
                polyArray,
                fill=(config.radialRed, config.radialGreen, config.radialBlue, 10),
                outline=(config.radialRed, config.radialGreen, config.radialBlue, config.radialAlpha + 2),
            )
            config.drawOverFlow.polygon(
                polyArray,
                fill=(config.radialRed, config.radialGreen, config.radialBlue, 10),
                outline=(config.radialRed, config.radialGreen, config.radialBlue, config.radialAlpha + 2),
            )


def runWork():
    global redrawSpeed
    global PS
    redrawSpeed = 0.02
    while True:
        config.directorController.checkTime()
        if config.directorController.advance:
            iterate()
        time.sleep(redrawSpeed)


def iterate():
    global config
    global PSArray
    config.vx = 0

    # Fade out the sparkle

    config.draw.rectangle(
        (0, 0, config.imageCanvasWidth, config.imageCanvasHeight),
        fill=(
            config.bgColor[0],
            config.bgColor[1],
            config.bgColor[2],
            round(config.fadeRate),
        ),
    )
    config.drawOverFlow.rectangle(
        (0, 0, config.imageCanvasWidth, config.imageCanvasHeight),
        fill=(
            config.bgColor[0],
            config.bgColor[1],
            config.bgColor[2],
            round(config.fadeRate),
        ),
    )

    config.drawOverFlow.rectangle((0, 0, 100, 200), fill=(200, 0, 0))

    if config.horizontalContinuity:
        _horizontalContinuitySetup(config)
    if config.verticalContinuity:
        _verticalContinuitySetup(config)

    for i in range(config.numberOfCenters):
        _PS = PSArray[i]
        drawBands(_PS)
        _PS.move()

    config.fadeRate += config.fadeRateDelta
    # if random.SystemRandom().random() < config.totalResetProb:
    #     PS.setUp()

    if config.fadeRate > 255:
        config.fadeRate = 30
        config.fadeRateDelta = random.SystemRandom().uniform(0.1, 2)

        if config.fadeRateDelta <= config.fadeRateNewSystemThreshold:
            # when the system reaches a visible chaotic crescendo that will last a few seconds, remake the system
            # behind the chaos and start again - choose a new background, reset the center, set new radial attributes
            # renew the particle dots that travel
            # bgChoice = math.floor(random.SystemRandom().uniform(0,len(config.bgColorSets)))
            config.bgColor = random.choice(config.bgColorSets)
            for i in range(config.numberOfCenters):
                _PS = PSArray[i]
                if random.SystemRandom().random() < config.totalResetProb:
                    _PS.useFixedBandColors = random.SystemRandom().random() < config.useFixedBandColorsProb
                    _PS.setCenter(i)
                    _PS.setNewAttributes(i)
                    _PS.setUp(i)

    config.image.paste(config.drawingImage, (0, 0), config.drawingImage)
    config.render(config.image, 0, 0, config.canvasWidth, config.canvasHeight)


def ringMaker(_ringWidth=200, _bandWidth=8, _xOffSet=0, _yOffSet=0, _fill=(255, 0, 0, 30)):
    if _ringWidth <= 0:
        return False
    _bandWidth = min(_bandWidth, _ringWidth / 2)
    _innerRingWidth = _ringWidth - _bandWidth

    _im1 = Image.new("RGBA", (_ringWidth, _ringWidth))
    _im1Draw = ImageDraw.Draw(_im1)
    _im1Draw.rectangle((0, 0, _ringWidth, _ringWidth), fill=_fill)

    mask = Image.new("L", (_ringWidth, _ringWidth))
    maskDraw = ImageDraw.Draw(mask)
    maskDraw.ellipse((0, 0, _ringWidth, _ringWidth), fill=(255))
    maskDraw.ellipse((_bandWidth + _xOffSet, _bandWidth + _yOffSet, _innerRingWidth, _innerRingWidth), fill=(0))

    ringImage = Image.new("RGBA", (200, 200))
    ringImage.paste(_im1, (0, 0), mask=mask)

    return ringImage


def _verticalContinuitySetup(config):
    # config.image  = ImageChops.add(config.image,config.imageOverFlow, scale = 1.0, offset= 0)

    yCrop = round(config.imageCanvasHeight)
    yCrop2 = round(config.imageCanvasHeight - config.imageCanvasHeight / config.verticalOverlapFraction)
    # print(yCrop2)

    # temp = config.imageOverFlow.crop((0,yCrop,config.canvasWidth, yCrop + config.canvasHeight / config.verticalOverlapFraction))
    # temp2 = config.image.crop((0,yCrop2,config.canvasWidth, config.canvasHeight))

    temp = config.imageOverFlow.crop((0, yCrop, config.imageCanvasWidth, yCrop + config.imageCanvasHeight / config.verticalOverlapFraction))
    temp2 = config.drawingImage.crop((0, yCrop2, config.imageCanvasWidth, config.imageCanvasHeight))

    temp3 = ImageChops.add(temp, config.drawingImage, scale=1.0, offset=0)
    config.drawingImage.paste(temp3, (0, 0), temp2)


def _horizontalContinuitySetup(config):
    # config.image  = ImageChops.add(config.image,config.imageOverFlow, scale = 1.0, offset= 0)

    xCrop = round(config.imageCanvasWidth)
    xCrop2 = round(config.imageCanvasWidth - config.imageCanvasWidth / config.horizontalOverlapFraction)
    temp = config.imageOverFlow.crop((xCrop, 0, xCrop + config.imageCanvasWidth / config.horizontalOverlapFraction, config.canvasHeight))
    temp2 = config.drawingImage.crop((xCrop2, 0, config.imageCanvasWidth, config.imageCanvasHeight))
    temp3 = ImageChops.add(config.drawingImage, temp, scale=1.0, offset=0)
    config.image.paste(temp3, (0, 0), temp2)

    # Done


def main(run=True):
    global config
    global workConfig
    global redrawSpeed
    global PS
    global PS2
    global PSArray

    PSArray = []

    config.minParticles = int(workConfig.get("particles", "minParticles"))
    config.maxParticles = int(workConfig.get("particles", "maxParticles"))

    config.speedFactorMin = float(workConfig.get("particles", "speedFactorMin"))
    config.speedFactorMax = float(workConfig.get("particles", "speedFactorMax"))

    config.initXRangeMin = int(workConfig.get("particles", "initXRangeMin"))
    config.initXRangeMax = int(workConfig.get("particles", "initXRangeMax"))
    config.initYRangeMin = int(workConfig.get("particles", "initYRangeMin"))
    config.initYRangeMax = int(workConfig.get("particles", "initYRangeMax"))

    bgColorSets = (workConfig.get("particles", "bgColorSets")).split(",")
    config.bgColorSets = []
    for bg in bgColorSets:
        bgColor = (workConfig.get(bg, "bgColor")).split(",")
        bgColors = [int(x) for x in bgColor]
        config.bgColorSets.append(bgColors)

    # choose the first bg color - generally the dark one
    config.bgColor = random.choice(config.bgColorSets)
    # config.bgColor = config.bgColorSets[1]

    config.rBase = int(workConfig.get("particles", "rBase"))
    config.gBase = int(workConfig.get("particles", "gBase"))
    config.bBase = int(workConfig.get("particles", "bBase"))
    config.aBase = int(workConfig.get("particles", "aBase"))
    config.rBase2 = int(workConfig.get("particles", "rBase2"))
    config.gBase2 = int(workConfig.get("particles", "gBase2"))
    config.bBase2 = int(workConfig.get("particles", "bBase2"))
    config.aBase2 = int(workConfig.get("particles", "aBase2"))
    config.rDiff = int(workConfig.get("particles", "rDiff"))
    config.gDiff = int(workConfig.get("particles", "gDiff"))
    config.bDiff = int(workConfig.get("particles", "bDiff"))
    config.radialAlpha = int(workConfig.get("particles", "radialAlpha"))

    config.radialRed = int(workConfig.get("particles", "radialRed"))
    config.radialGreen = int(workConfig.get("particles", "radialGreen"))
    config.radialBlue = int(workConfig.get("particles", "radialBlue"))
    config.radial2Red = int(workConfig.get("particles", "radial2Red"))
    config.radial2Green = int(workConfig.get("particles", "radial2Green"))
    config.radial2Blue = int(workConfig.get("particles", "radial2Blue"))

    try:
        config.radialSetMinNum = int(workConfig.get("particles", "radialSetMinNum"))
        config.radialSetMaxNum = int(workConfig.get("particles", "radialSetMaxNum"))
        config.radialSetInnerRadiusFactor = int(workConfig.get("particles", "radialSetInnerRadiusFactor"))
        config.radialSetInnerRadiusFactorFixedBands = float(workConfig.get("particles", "radialSetInnerRadiusFactorFixedBands"))
        config.radialSetInnerRadiusRange = [int(x) for x in (workConfig.get("particles", "radialSetInnerRadiusRange").split(","))]
        config.radialSetOuterRadiusRange = [int(x) for x in (workConfig.get("particles", "radialSetOuterRadiusRange").split(","))]
    except Exception as e:
        print(e)
        config.radialSetMinNum = 120
        config.radialSetMaxNum = 300
        config.radialSetInnerRadiusFactor = 3
        config.radialSetInnerRadiusFactorFixedBands = 4
        config.radialSetInnerRadiusRange = -100, 50
        config.radialSetOuterRadiusRange = -50, 50

    config.fadeRate = float(workConfig.get("particles", "fadeRate"))
    config.fadeRateDelta = float(workConfig.get("particles", "fadeRateDelta"))
    config.sparkleProb = float(workConfig.get("particles", "sparkleProb"))
    config.fadeRateNewSystemThreshold = float(workConfig.get("particles", "fadeRateNewSystemThreshold"))

    config.particleResetProb = float(workConfig.get("particles", "particleResetProb"))
    config.totalResetProb = float(workConfig.get("particles", "totalResetProb"))
    config.orbitProb = float(workConfig.get("particles", "orbitProb"))

    # set the actual drawing space
    try:
        config.imageCanvasWidth = int(workConfig.get("particles", "imageCanvasWidth"))
        config.imageCanvasHeight = int(workConfig.get("particles", "imageCanvasHeight"))

    except Exception as e:
        print(e)
        config.imageCanvasWidth = config.canvasWidth
        config.imageCanvasHeight = config.canvasHeight

    # comment: # for some towers the seam between the
    # start and end needs to become semi-continuous
    # so I make the particles appear to move around the piece
    # and overlap one side with some of the drawing
    # if every thing was drawn pixel by pixel this would
    # probably not need to be so complicated
    config.horizontalContinuity = workConfig.getboolean("particles", "horizontalContinuity")
    config.horizontalOverlapFraction = int(workConfig.get("particles", "horizontalOverlapFraction"))

    config.verticalContinuity = workConfig.getboolean("particles", "verticalContinuity")
    config.verticalOverlapFraction = int(workConfig.get("particles", "verticalOverlapFraction"))

    config.PSXSpeed = float(workConfig.get("particles", "PSXSpeed"))
    config.PSYSpeed = float(workConfig.get("particles", "PSYSpeed"))
    config.PSRadiusFactor1 = float(workConfig.get("particles", "PSRadiusFactor1"))
    config.PSRadiusFactor2 = float(workConfig.get("particles", "PSRadiusFactor2"))
    config.PSRadiusMin = float(workConfig.get("particles", "PSRadiusMin"))
    config.PSRadiusMax = float(workConfig.get("particles", "PSRadiusMax"))
    config.PSMinBands = int(workConfig.get("particles", "PSMinBands"))
    config.PSMaxBands = int(workConfig.get("particles", "PSMaxBands"))
    # config.PSRadiusFixedColorMin = int(workConfig.get("particles", "PSRadiusFixedColorMin"))

    config.bandWidthMin = int(workConfig.get("particles", "bandWidthMin"))
    config.bandWidthMax = int(workConfig.get("particles", "bandWidthMax"))
    config.PSFixedColorRadiusDiffMin = int(workConfig.get("particles", "PSFixedColorRadiusDiffMin"))
    config.PSFixedColorRadiusDiffMax = int(workConfig.get("particles", "PSFixedColorRadiusDiffMax"))

    goldenRingsArray = workConfig.get("particles", "goldenRingsArray").split(",")
    config.goldenRingsArray = [int(x) for x in goldenRingsArray]

    config.useFixedBandColorsProb = float(workConfig.get("particles", "useFixedBandColorsProb"))

    bandColorsRaw = workConfig.get("particles", "bandColors").split("|")
    config.bandColors = []
    config.bandColors.extend([int(x) for x in n.split(",")] for n in bandColorsRaw)

    bandGoldColorsRaw = workConfig.get("particles", "bandGoldColors").split("|")
    config.bandGoldColors = []
    config.bandGoldColors.extend([int(x) for x in n.split(",")] for n in bandGoldColorsRaw)

    # only has to happen once, I had it happening every turn
    config.bandColors.reverse()

    try:
        config.PSRadiusFixedColorMinInternalRadius = int(workConfig.get("particles", "PSRadiusFixedColorMinInternalRadius"))
    except Exception as e:
        print(e)
        config.PSRadiusFixedColorMinInternalRadius = 1

    try:
        config.xMaxFactor = float(workConfig.get("particles", "xMaxFactor"))
        config.yMaxFactor = float(workConfig.get("particles", "yMaxFactor"))

    except Exception as e:
        print(e)
        config.xMaxFactor = 4
        config.yMaxFactor = 8

    try:
        config.rRange = int(workConfig.get("particles", "rRange"))
        config.gRange = int(workConfig.get("particles", "gRange"))
        config.bRange = int(workConfig.get("particles", "bRange"))
        config.rRangeMin = int(workConfig.get("particles", "rRangeMin"))
        config.gRangeMin = int(workConfig.get("particles", "gRangeMin"))
        config.bRangeMin = int(workConfig.get("particles", "bRangeMin"))
    except Exception as e:
        print(e)
        config.rRange = 255
        config.gRange = 200
        config.bRange = 255
        config.rRangeMin = 0
        config.gRangeMin = 0
        config.bRangeMin = 0

    particleColorRangeVals = workConfig.get("particles", "particleColorRange").split(",")
    config.particleColorRange = [float(i) for i in particleColorRangeVals]

    config.image = Image.new("RGBA", (config.canvasWidth, config.canvasHeight))
    config.drawingImage = Image.new("RGBA", (config.imageCanvasWidth, config.imageCanvasHeight))
    config.draw = ImageDraw.Draw(config.drawingImage)

    config.imageOverFlow = Image.new("RGBA", (config.canvasWidth * 2, config.canvasHeight * 2))
    config.drawOverFlow = ImageDraw.Draw(config.imageOverFlow)

    config.numberOfCenters = workConfig.getint("particles", "numberOfCenters", fallback=1)

    for i in range(config.numberOfCenters):

        _PS = ParticleSystem(config)
        _PS.setCenter(i)
        _PS.setNewAttributes(i)
        _PS.setUp(i)

        PSArray.append(_PS)

    # managing speed of animation and framerate
    config.directorController = Director(config)
    config.directorController.slotRate = 0.03

    if run:
        runWork()
