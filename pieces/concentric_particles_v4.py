import math
import random
import time
from modules import colorutils
from PIL import Image, ImageDraw, ImageChops

# from modules.holder_director import Holder
from modules.configuration import pieceLogger
from modules.holder_director import Director


class ParticleDot:
    def __init__(self):
        pass

    def setUp(self, p, n):
        # variation in initial velocity
        direction = 1 if p.directionProb < 0.5 else -1
        orbit = p.orbitProb <= cpMngr.orbitProb
        fx = random.SystemRandom().random() * p.fFactor + 0
        fy = random.SystemRandom().random() * p.fFactor + 0
        vx = math.cos(p.angle * n) * fx * direction
        vy = math.sin(p.angle * n) * fy * direction

        radius = random.SystemRandom().uniform(1, p.maxRadius)
        self.circuitCount = 0

        # Make radius fall into one of the systems bands - like quata
        radialBand = round(random.SystemRandom().uniform(1, 12))

        radius = p.radialBand * radialBand

        rSpeed = random.SystemRandom().uniform(100, 200) / radius / cpMngr.radialSpeedFactor

        xPos = p.x
        yPos = p.y
        angle = p.angle * n

        if direction == -1:
            xPos = round(random.SystemRandom().uniform(0, cpMngr.imageCanvasWidth))
            yPos = round(random.SystemRandom().uniform(0, cpMngr.imageCanvasHeight))
            angle = math.atan2(yPos - p.y, xPos - p.x)
            vx = math.cos(angle) * fx * direction
            vy = math.sin(angle) * fy * direction

        self.id = n
        self.xPos = xPos
        self.yPos = yPos
        self.vx = vx
        self.vy = vy
        pClrRange = cpMngr.particleColorRange
        clr = colorutils.getRandomColorHSVSaturated(pClrRange[0], pClrRange[1], pClrRange[2], pClrRange[3], pClrRange[4], pClrRange[5])
        self.clr = [clr[0], clr[1], clr[2]]
        self.done = 0
        self.angle = angle
        self.radius = radius
        self.rSpeed = rSpeed
        self.mode = 1
        self.orbit = orbit
        self.sizeNum = 1 if random.SystemRandom().random() < 0.85 else 2


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

        self.angleOffsetSpeed = random.SystemRandom().uniform(-math.pi / 300, math.pi / 300) / cpMngr.rotationSpeedFactor

        radialSetInnerRadiusFactor = self.radialSetInnerRadiusFactor
        # if self.useFixedBandColors:
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

        # pieceLogger(f"wBase {self.wBase} innerRadius = {innerRadius}")


class ParticleSystem:
    def __init__(self, config):
        self.config = config
        self.x = 0
        self.y = 0
        self.particles = []
        self.done = False
        self.drawRadialPolys = True
        self.orientation = 1
        self.initXRange = [cpMngr.initXRangeMin, cpMngr.initXRangeMax]
        self.initYRange = [cpMngr.initYRangeMin, cpMngr.initYRangeMax]
        self.useFixedBandColors = random.random() < cpMngr.useFixedBandColorsProb

        # there is really no need for this to change the bands randomly
        self.bandWVariabilityProb = 0.00
        self.xMaxFactor = 4
        self.yMaxFactor = 4
        self.wDiff = 17
        # self.bandWidth = 1
        # self.bandDecriment = 1
        self.bandAlpha = round(random.uniform(cpMngr.bandAlphaRange[0], cpMngr.bandAlphaRange[1]))

    def setNewAttributes(self, _i=0):
        self.radialSets = []

        # The rings around the center
        # if not self.useFixedBandColors:
        self.bands = round(random.SystemRandom().uniform(cpMngr.PSMinBands, cpMngr.PSMaxBands))
        self.wBase = round(random.SystemRandom().uniform(cpMngr.PSRadiusMin, cpMngr.PSRadiusMax))
        self.wDiff = round(random.SystemRandom().uniform(cpMngr.bandWidthMin, cpMngr.bandWidthMax))

        # if self.useFixedBandColors:

        self.bandWidth = round(random.uniform(cpMngr.bandWidthRange[0], cpMngr.bandWidthRange[1]))
        self.bandDecriment = round(random.uniform(cpMngr.bandDecrimentRange[0], cpMngr.bandDecrimentRange[1]))
        self.bandAlpha = round(random.uniform(cpMngr.bandAlphaRange[0], cpMngr.bandAlphaRange[1]))

        if self.useFixedBandColors:
            self.setBandColors()
        else:
            self.setRings()

        self.setBandSizes()

        self.xSpeed = random.SystemRandom().random() * cpMngr.PSXSpeed
        self.ySpeed = random.SystemRandom().random() * cpMngr.PSYSpeed

        self.xMaxFactor = cpMngr.xMaxFactor
        self.yMaxFactor = cpMngr.yMaxFactor

        self.drawRadialPolys = random.SystemRandom().random() < 0.5

        radialSet = RadialSet(config, self.wBase)
        radialSet.radialSetMinNum = cpMngr.radialSetMinNum
        radialSet.radialSetMaxNum = cpMngr.radialSetMaxNum
        radialSet.radialSetInnerRadiusFactor = cpMngr.radialSetInnerRadiusFactor
        radialSet.radialSetInnerRadiusFactorFixedBands = cpMngr.radialSetInnerRadiusFactorFixedBands
        radialSet.radialSetInnerRadiusRange = cpMngr.radialSetInnerRadiusRange
        radialSet.radialSetOuterRadiusRange = cpMngr.radialSetOuterRadiusRange
        radialSet.useFixedBandColors = self.useFixedBandColors

        radialSet.makeRadialsSet(cpMngr.radialSetMinNum, cpMngr.radialSetMaxNum)
        self.radialSets.append(radialSet)

        # the 33s hand
        radialSet = RadialSet(config, self.wBase)
        radialSet.makeRadialsSet(1, 1)
        self.radialSets.append(radialSet)

    def setRings(self):
        self.bandColorsAdjusted = []
        for _ in range(self.bands):
            if random.random() < cpMngr.probGoldBand:
                _clr = colorutils.getRandomColorHSV(
                    cpMngr.bandGoldColorsRange[0],
                    cpMngr.bandGoldColorsRange[1],
                    cpMngr.bandGoldColorsRange[2],
                    cpMngr.bandGoldColorsRange[3],
                    cpMngr.bandGoldColorsRange[4],
                    cpMngr.bandGoldColorsRange[5],
                )
            else:
                _clr = colorutils.getRandomColorHSV(
                    cpMngr.bandBlueColorsRange[0],
                    cpMngr.bandBlueColorsRange[1],
                    cpMngr.bandBlueColorsRange[2],
                    cpMngr.bandBlueColorsRange[3],
                    cpMngr.bandBlueColorsRange[4],
                    cpMngr.bandBlueColorsRange[5],
                )
                # _clr = colorutils.getRandomColorHSV()

            self.bandColorsAdjusted.extend([_clr])

    def setBandColors(self):
        self.bandColors = cpMngr.bandColors

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

    def setBandSizes(self):
        self.wBase = round(
            random.SystemRandom().uniform(cpMngr.PSRadiusMin + cpMngr.PSRadiusFixedColorMinInternalRadius, cpMngr.PSRadiusMax + cpMngr.PSRadiusFixedColorMinInternalRadius)
        )
        self.wDiff = round(random.SystemRandom().uniform(cpMngr.bandWidthMin, cpMngr.bandWidthMax))

        self.bandWidthsSet = []
        self.bandWidthsSet.extend(
            round(
                random.SystemRandom().uniform(
                    cpMngr.PSFixedColorRadiusDiffMin,
                    cpMngr.PSFixedColorRadiusDiffMax,
                )
            )
            for _ in range(self.bands)
        )

    def setCenter(self, _i=0):
        # initial center position
        self.x = round(random.SystemRandom().uniform(self.initXRange[0], self.initXRange[1]))
        self.y = round(random.SystemRandom().uniform(self.initYRange[0], self.initYRange[1]))

        if _i == 0:
            self.x = round(random.SystemRandom().uniform(0, 128))

    def setUp(self, _i=0):

        self.directionProb = random.SystemRandom().uniform(0.4, 0.6)
        self.orbitProb = cpMngr.orbitProb
        # Number of sparks
        self.p = int(5 + (random.SystemRandom().uniform(cpMngr.minParticles, cpMngr.maxParticles)))
        self.angle = 2 * math.pi / self.p

        cpMngr.numberDone = round(self.p / 5)

        # Speed factor
        self.fFactor = int(random.SystemRandom().uniform(cpMngr.speedFactorMin, cpMngr.speedFactorMax))

        self.brightness = self.config.brightness
        self.sparkleBrightness = self.config.brightness

        # speed that each light fades to black / sparkle
        self.decr_r = round(random.SystemRandom().uniform(0.25, 1))
        self.decr_g = round(random.SystemRandom().uniform(0.25, 1))
        self.decr_b = round(random.SystemRandom().uniform(0.25, 1))

        # vertical deacelleration
        self.deacelleration = random.SystemRandom().uniform(0.8, 0.99)

        # horizontal deacelleration
        self.deacellerationx = random.SystemRandom().uniform(0.8, 0.95)

        self.maxRadius = math.sqrt(cpMngr.imageCanvasWidth * cpMngr.imageCanvasWidth + cpMngr.imageCanvasHeight * cpMngr.imageCanvasHeight) * cpMngr.PSRadiusFactor1

        self.radialBand = self.maxRadius / 12

        for n in range(self.p):
            pDot = ParticleDot()
            pDot.setUp(self, n)
            self.particles.append(pDot)


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

        if random.SystemRandom().random() < cpMngr.particleResetProb:
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

        if cpMngr.horizontalContinuity:
            ref.xPos %= cpMngr.imageCanvasWidth
        if cpMngr.verticalContinuity:
            ref.xPos %= cpMngr.imageCanvasWidth
            ref.yPos %= cpMngr.imageCanvasHeight

    def _move_particle_orbit(self, ref):
        """Updates the particle's position based on orbital movement."""
        ref.xPos = self.x + ref.radius / 1 * math.cos(ref.angle) * 0.2
        ref.yPos = self.y + ref.radius / 1 * math.sin(ref.angle) * 0.2
        ref.angle += ref.rSpeed

    def _update_particle_color(self, q):
        """Updates the color of a single particle, including sparkle effect."""
        for i in range(3):
            self.particles[q].clr[i] = max(0, self.particles[q].clr[i] - getattr(self, "decr_" + "rgb"[i]))

        if random.SystemRandom().random() < cpMngr.sparkleProb:
            self.particles[q].clr = [int(220 * self.sparkleBrightness)] * 2 + [int(255 * self.sparkleBrightness)]

    def _draw_particle(self, ref, q):
        """Draws a single particle on the canvas with continuity handling."""
        xDisplayPos = ref.xPos
        yDisplayPos = ref.yPos

        if cpMngr.horizontalContinuity:
            xDisplayPos %= config.canvasWidth
        if cpMngr.verticalContinuity:
            xDisplayPos %= cpMngr.imageCanvasWidth
            yDisplayPos %= cpMngr.imageCanvasHeight

        if 0 <= xDisplayPos <= cpMngr.imageCanvasWidth and 0 <= yDisplayPos <= cpMngr.imageCanvasHeight:
            try:
                if ref.sizeNum == 2:
                    config.particleDraw.rectangle(
                        (round(xDisplayPos), round(yDisplayPos), round(xDisplayPos) + 1, round(yDisplayPos)),
                        fill=tuple(self.particles[q].clr + [255]),
                    )
                else:
                    config.particleDraw.rectangle(
                        (round(xDisplayPos), round(yDisplayPos), round(xDisplayPos), round(yDisplayPos)),
                        fill=tuple(self.particles[q].clr + [255]),
                    )
            except Exception as e:
                pieceLogger(e,1)

        if yDisplayPos > cpMngr.imageCanvasHeight or yDisplayPos < 0:
            ref.setUp(self, ref.id)


class ConcentricParticlesManager:
    def __init__(self, config):
        self.config = config

    def setUp(self, workConfig):
        self.minParticles = int(workConfig.get("particles", "minParticles"))
        self.maxParticles = int(workConfig.get("particles", "maxParticles"))

        self.speedFactorMin = float(workConfig.get("particles", "speedFactorMin"))
        self.speedFactorMax = float(workConfig.get("particles", "speedFactorMax"))

        self.initXRangeMin = int(workConfig.get("particles", "initXRangeMin"))
        self.initXRangeMax = int(workConfig.get("particles", "initXRangeMax"))
        self.initYRangeMin = int(workConfig.get("particles", "initYRangeMin"))
        self.initYRangeMax = int(workConfig.get("particles", "initYRangeMax"))

        bgColorSets = (workConfig.get("particles", "bgColorSets")).split(",")
        self.bgColorSets = []
        for bg in bgColorSets:
            bgColor = (workConfig.get(bg, "bgColor")).split(",")
            bgColors = [int(x) for x in bgColor]
            self.bgColorSets.append(bgColors)

        # choose the first bg color - generally the dark one
        self.bgColor = random.choice(self.bgColorSets)

        self.radialAlpha = int(workConfig.get("particles", "radialAlpha"))
        self.radialSpeedFactor = float(workConfig.get("particles", "radialSpeedFactor"))

        self.radialRed = int(workConfig.get("particles", "radialRed"))
        self.radialGreen = int(workConfig.get("particles", "radialGreen"))
        self.radialBlue = int(workConfig.get("particles", "radialBlue"))
        self.radial2Red = int(workConfig.get("particles", "radial2Red"))
        self.radial2Green = int(workConfig.get("particles", "radial2Green"))
        self.radial2Blue = int(workConfig.get("particles", "radial2Blue"))

        self.radialSetMinNum = int(workConfig.get("particles", "radialSetMinNum"))
        self.radialSetMaxNum = int(workConfig.get("particles", "radialSetMaxNum"))
        self.radialSetInnerRadiusFactor = int(workConfig.get("particles", "radialSetInnerRadiusFactor"))
        self.radialSetInnerRadiusFactorFixedBands = float(workConfig.get("particles", "radialSetInnerRadiusFactorFixedBands"))
        self.radialSetInnerRadiusRange = [int(x) for x in (workConfig.get("particles", "radialSetInnerRadiusRange").split(","))]
        self.radialSetOuterRadiusRange = [int(x) for x in (workConfig.get("particles", "radialSetOuterRadiusRange").split(","))]
        self.rotationSpeedFactor = float(workConfig.get("particles", "rotationSpeedFactor"))

        self.backgroundAlpha = float(workConfig.get("particles", "backgroundAlpha"))
        self.backgroundAlphaMin = float(workConfig.get("particles", "backgroundAlphaMin"))
        self.backgroundAlphaMax = float(workConfig.get("particles", "backgroundAlphaMax"))
        self.backgroundAlphaDelta = float(workConfig.get("particles", "backgroundAlphaDelta"))
        self.backgroundAlphaDeltaSpeed = float(workConfig.get("particles", "backgroundAlphaDeltaSpeed"))
        self.sparkleProb = float(workConfig.get("particles", "sparkleProb"))
        self.backgroundAlphaNewSystemThreshold = float(workConfig.get("particles", "backgroundAlphaNewSystemThreshold"))

        self.particleResetProb = float(workConfig.get("particles", "particleResetProb"))
        self.totalResetProb = float(workConfig.get("particles", "totalResetProb"))
        self.orbitProb = float(workConfig.get("particles", "orbitProb"))

        # set the actual drawing space
        try:
            self.imageCanvasWidth = int(workConfig.get("particles", "imageCanvasWidth"))
            self.imageCanvasHeight = int(workConfig.get("particles", "imageCanvasHeight"))

        except Exception as e:
            pieceLogger(e, 1)
            self.imageCanvasWidth = self.config.canvasWidth
            self.imageCanvasHeight = self.config.canvasHeight

        # comment: # for some towers the seam between the
        # start and end needs to become semi-continuous
        # so I make the particles appear to move around the piece
        # and overlap one side with some of the drawing
        # if every thing was drawn pixel by pixel this would
        # probably not need to be so complicated
        self.horizontalContinuity = workConfig.getboolean("particles", "horizontalContinuity")
        self.horizontalOverlapFraction = int(workConfig.get("particles", "horizontalOverlapFraction"))

        self.verticalContinuity = workConfig.getboolean("particles", "verticalContinuity")
        self.verticalOverlapFraction = int(workConfig.get("particles", "verticalOverlapFraction"))

        self.PSXSpeed = float(workConfig.get("particles", "PSXSpeed"))
        self.PSYSpeed = float(workConfig.get("particles", "PSYSpeed"))
        self.PSRadiusFactor1 = float(workConfig.get("particles", "PSRadiusFactor1"))
        self.PSRadiusFactor2 = float(workConfig.get("particles", "PSRadiusFactor2"))
        self.PSRadiusMin = float(workConfig.get("particles", "PSRadiusMin"))
        self.PSRadiusMax = float(workConfig.get("particles", "PSRadiusMax"))
        self.PSMinBands = int(workConfig.get("particles", "PSMinBands"))
        self.PSMaxBands = int(workConfig.get("particles", "PSMaxBands"))

        self.bandWidthMin = int(workConfig.get("particles", "bandWidthMin"))
        self.bandWidthMax = int(workConfig.get("particles", "bandWidthMax"))
        self.PSFixedColorRadiusDiffMin = int(workConfig.get("particles", "PSFixedColorRadiusDiffMin"))
        self.PSFixedColorRadiusDiffMax = int(workConfig.get("particles", "PSFixedColorRadiusDiffMax"))

        self.useFixedBandColorsProb = float(workConfig.get("particles", "useFixedBandColorsProb"))

        bandColorsRaw = workConfig.get("particles", "bandColors").split("|")
        self.bandColors = []
        self.bandColors.extend([int(x) for x in n.split(",")] for n in bandColorsRaw)

        self.probGoldBand = float(workConfig.get("particles", "probGoldBand"))

        bandGoldColorsRange = workConfig.get("particles", "bandGoldColorsRange").split(",")
        self.bandGoldColorsRange = []
        self.bandGoldColorsRange.extend(float(n) for n in bandGoldColorsRange)

        bandBlueColorsRange = workConfig.get("particles", "bandBlueColorsRange").split(",")
        self.bandBlueColorsRange = []
        self.bandBlueColorsRange.extend(float(n) for n in bandBlueColorsRange)

        bandWidthRange = workConfig.get("particles", "bandWidthRange").split(",")
        self.bandWidthRange = []
        self.bandWidthRange.extend(int(n) for n in bandWidthRange)

        bandDecrimentRange = workConfig.get("particles", "bandDecrimentRange").split(",")
        self.bandDecrimentRange = []
        self.bandDecrimentRange.extend(int(n) for n in bandDecrimentRange)

        bandAlphaRange = workConfig.get("particles", "bandAlphaRange").split(",")
        self.bandAlphaRange = []
        self.bandAlphaRange.extend(float(n) for n in bandAlphaRange)

        # only has to happen once, I had it happening every turn
        self.bandColors.reverse()

        try:
            self.PSRadiusFixedColorMinInternalRadius = int(workConfig.get("particles", "PSRadiusFixedColorMinInternalRadius"))
        except Exception as e:
            pieceLogger(e, 1)
            self.PSRadiusFixedColorMinInternalRadius = 1

        try:
            self.xMaxFactor = float(workConfig.get("particles", "xMaxFactor"))
            self.yMaxFactor = float(workConfig.get("particles", "yMaxFactor"))

        except Exception as e:
            pieceLogger(e, 1)
            self.xMaxFactor = 4
            self.yMaxFactor = 8

        particleColorRangeVals = workConfig.get("particles", "particleColorRange").split(",")
        self.particleColorRange = [float(i) for i in particleColorRangeVals]
        self.numberOfCenters = workConfig.getint("particles", "numberOfCenters", fallback=1)
        self.pieceId = workConfig.getint("particles", "pieceId", fallback=0)

##########################################################################


def drawBands(p):
    # pieceLogger("----")
    drawBandRings(p)
    drawRadials(p)


def drawBandRings(p):
    _b = p.bandWidth
    _decriment = p.bandDecriment
    _startWidth = p.wBase - cpMngr.PSRadiusFixedColorMinInternalRadius
    _setsOfRings = 1
    _alpha = p.bandAlpha

    # if p.useFixedBandColors:
    _rings = len(p.bandColorsAdjusted)
    _clrs = p.bandColorsAdjusted
    # else:
    #     _rings = len(p.bandGoldColors)
    #     _clrs = p.bandGoldColors

    _ringNum = 0
    for _ii in range(_setsOfRings):
        for _i in range(_rings):
            _xoff = round(p.x - _startWidth / 2 + _decriment * _i / 2) + round(_ii * _decriment * _rings / 2)
            _yoff = round(p.y - _startWidth / 2 + _decriment * _i / 2) + round(_ii * _decriment * _rings / 2)
            _alphaToUse = _alpha

            # if not p.useFixedBandColors:
            #     _alphaToUse = 20 if _clrs[_i][0] < 10 else 150
            if ringImage := ringMaker(_startWidth - _decriment * _i, _b, 0, 0, (round(_clrs[_i][0]), round(_clrs[_i][1]), round(_clrs[_i][2]), _alphaToUse)):
                # config.image.paste(ringImage, (_xoff, _yoff), mask=ringImage)
                config.drawingImage.paste(ringImage, (_xoff, _yoff), mask=ringImage)

            _ringNum += 1
        _startWidth -= _decriment * _rings


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
                config.drawingImageDraw.line((x0, y0, x1, y1), fill=(cpMngr.radialRed, cpMngr.radialGreen, cpMngr.radialBlue, cpMngr.radialAlpha))
                config.drawOverFlow.line((x0, y0, x1, y1), fill=(cpMngr.radialRed, cpMngr.radialGreen, cpMngr.radialBlue, cpMngr.radialAlpha))
            if numLines == 1:
                config.drawingImageDraw.line((x0, y0, x1, y1), fill=(cpMngr.radial2Red, cpMngr.radial2Green, cpMngr.radial2Blue, cpMngr.radialAlpha))
                config.drawOverFlow.line((x0, y0, x1, y1), fill=(cpMngr.radial2Red, cpMngr.radial2Green, cpMngr.radial2Blue, cpMngr.radialAlpha))

        if rSet.drawRadialPolys:
            config.drawingImageDraw.polygon(
                polyArray,
                fill=(cpMngr.radialRed, cpMngr.radialGreen, cpMngr.radialBlue, 10),
                outline=(cpMngr.radialRed, cpMngr.radialGreen, cpMngr.radialBlue, cpMngr.radialAlpha + 2),
            )
            config.drawOverFlow.polygon(
                polyArray,
                fill=(cpMngr.radialRed, cpMngr.radialGreen, cpMngr.radialBlue, 10),
                outline=(cpMngr.radialRed, cpMngr.radialGreen, cpMngr.radialBlue, cpMngr.radialAlpha + 2),
            )


def changeACenter(cpMngr, PSArray):
    # cpMngr.backgroundAlpha = round(random.uniform(20,120))
    i = round(random.uniform(0, cpMngr.numberOfCenters-1))
    _PS = PSArray[i]
    _PS.useFixedBandColors = random.SystemRandom().random() < cpMngr.useFixedBandColorsProb
    _PS.setCenter(i)
    _PS.setNewAttributes(i)
    _PS.setUp(i)


    # config.drawingImage.paste(config.particleLayer, (0,0), config.particleLayer)
    # config.image.paste(config.particleLayer, (0, 0), config.particleLayer)

    # _temp = ImageChops.lighter(config.image, config.particleLayer)
    # config.image.paste(config.drawingImage, (0, 0), config.drawingImage)
    # config.image.paste(_temp, (0, 0), _temp)
    # config.render(config.image, 0, 0, config.canvasWidth, config.canvasHeight)
    # config.render(config.particleLayer, 0, 0, config.canvasWidth, config.canvasHeight)

    # config.finalCompositeDraw.rectangle((0,0,300,300), fill = (0,0,0,255))

    # config.finalCompositeDraw.rectangle((0,0,config.canvasWidth,config.canvasHeight), fill=(0,0,0,25))

    # config.finalComposite.paste(config.image, (0, 0), config.image)
    # config.finalComposite.paste(config.drawingImage, (0, 0), config.drawingImage)
    # config.finalComposite.paste(config.particleLayer, (0,0), config.particleLayer)
    # config.finalComposite.paste(config.drawingImage, (0, 0), config.drawingImage)
    # config.render(config.finalComposite, 0, 0, config.canvasWidth, config.canvasHeight)


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


def _verticalContinuitySetup(config, cpMngr):
    # config.image  = ImageChops.add(config.image,config.imageOverFlow, scale = 1.0, offset= 0)

    yCrop = round(cpMngr.imageCanvasHeight)
    yCrop2 = round(cpMngr.imageCanvasHeight - cpMngr.imageCanvasHeight / cpMngr.verticalOverlapFraction)
    # pieceLogger(yCrop2)

    # temp = config.imageOverFlow.crop((0,yCrop,config.canvasWidth, yCrop + config.canvasHeight / cpMngr.verticalOverlapFraction))
    # temp2 = config.image.crop((0,yCrop2,config.canvasWidth, config.canvasHeight))

    temp = config.imageOverFlow.crop((0, yCrop, cpMngr.imageCanvasWidth, yCrop + cpMngr.imageCanvasHeight / cpMngr.verticalOverlapFraction))
    temp2 = config.drawingImage.crop((0, yCrop2, cpMngr.imageCanvasWidth, cpMngr.imageCanvasHeight))

    temp3 = ImageChops.add(temp, config.drawingImage, scale=1.0, offset=0)
    config.drawingImage.paste(temp3, (0, 0), temp2)


def _horizontalContinuitySetup(config, cpMngr):
    # config.image  = ImageChops.add(config.image,config.imageOverFlow, scale = 1.0, offset= 0)

    xCrop = round(cpMngr.imageCanvasWidth)
    xCrop2 = round(cpMngr.imageCanvasWidth - cpMngr.imageCanvasWidth / cpMngr.horizontalOverlapFraction)
    temp = config.imageOverFlow.crop((xCrop, 0, xCrop + cpMngr.imageCanvasWidth / cpMngr.horizontalOverlapFraction, config.canvasHeight))
    temp2 = config.drawingImage.crop((xCrop2, 0, cpMngr.imageCanvasWidth, cpMngr.imageCanvasHeight))
    temp3 = ImageChops.add(config.drawingImage, temp, scale=1.0, offset=0)
    config.image.paste(temp3, (0, 0), temp2)

    # Done


def createLayers():
    config.image = Image.new("RGBA", (config.canvasWidth, config.canvasHeight))

    config.drawingImage = Image.new("RGBA", (cpMngr.imageCanvasWidth, cpMngr.imageCanvasHeight))
    config.drawingImageDraw = ImageDraw.Draw(config.drawingImage)

    config.particleLayer = Image.new("RGBA", (cpMngr.imageCanvasWidth, cpMngr.imageCanvasHeight))
    config.particleDraw = ImageDraw.Draw(config.particleLayer)

    config.imageOverFlow = Image.new("RGBA", (config.canvasWidth * 2, config.canvasHeight * 2))
    config.drawOverFlow = ImageDraw.Draw(config.imageOverFlow)

    config.finalComposite = Image.new("RGBA", (cpMngr.imageCanvasWidth, cpMngr.imageCanvasHeight))
    config.finalCompositeDraw = ImageDraw.Draw(config.finalComposite)

# -------------------------------------------------------- #
# -------------------------------------------------------- #

def runWork():
    global redrawSpeed
    global PS
    redrawSpeed = 0.02
    pieceLogger("concentric_particles_v4.py running", 2)
    while True:
        config.directorController.checkTime()
        if config.directorController.advance:
            iterate()
        time.sleep(redrawSpeed)


def iterate():
    global config
    global cpMngr
    global PSArray

    cpMngr.vx = 0

    # Fade out the sparkle
    config.drawingImageDraw.rectangle(
        (0, 0, cpMngr.imageCanvasWidth, cpMngr.imageCanvasHeight),
        fill=(
            cpMngr.bgColor[0],
            cpMngr.bgColor[1],
            cpMngr.bgColor[2],
            round(cpMngr.backgroundAlpha),
        ),
    )
    config.drawOverFlow.rectangle(
        (0, 0, cpMngr.imageCanvasWidth, cpMngr.imageCanvasHeight),
        fill=(
            cpMngr.bgColor[0],
            cpMngr.bgColor[1],
            cpMngr.bgColor[2],
            round(cpMngr.backgroundAlpha),
        ),
    )

    config.drawOverFlow.rectangle((0, 0, 100, 200), fill=(200, 0, 0))

    config.particleLayer = Image.new("RGBA", (cpMngr.imageCanvasWidth, cpMngr.imageCanvasHeight))
    config.particleDraw = ImageDraw.Draw(config.particleLayer)
    # config.particleDraw.rectangle((0,0,300,300), fill = (0,0,0,255))

    if cpMngr.horizontalContinuity:
        _horizontalContinuitySetup(config, cpMngr)
    if cpMngr.verticalContinuity:
        _verticalContinuitySetup(config, cpMngr)

    for i in range(cpMngr.numberOfCenters):
        _PS = PSArray[i]
        drawBands(_PS)
        _PS.move()

    cpMngr.backgroundAlpha += cpMngr.backgroundAlphaDelta
    # if random.SystemRandom().random() < cpMngr.totalResetProb:
    #     PS.setUp()

    if cpMngr.backgroundAlpha < cpMngr.backgroundAlphaMin :
        cpMngr.backgroundAlphaDelta = cpMngr.backgroundAlphaDeltaSpeed
    if cpMngr.backgroundAlpha > cpMngr.backgroundAlphaMax :
        cpMngr.backgroundAlphaDelta = -cpMngr.backgroundAlphaDeltaSpeed


    if random.SystemRandom().random() < cpMngr.totalResetProb:
        changeACenter(cpMngr, PSArray)
    # if cpMngr.backgroundAlpha > 255:
    #     cpMngr.backgroundAlpha = 30
    #     cpMngr.backgroundAlphaDelta = random.SystemRandom().uniform(0.1, 2)

    #     if cpMngr.backgroundAlphaDelta <= cpMngr.backgroundAlphaNewSystemThreshold:
    #         # when the system reaches a visible chaotic crescendo that will last a few seconds, remake the system
    #         # behind the chaos and start again - choose a new background, reset the center, set new radial attributes
    #         # renew the particle dots that travel
    #         # bgChoice = math.floor(random.SystemRandom().uniform(0,len(cpMngr.bgColorSets)))
    #         cpMngr.bgColor = random.choice(cpMngr.bgColorSets)
    #         for i in range(cpMngr.numberOfCenters):
    #             _PS = PSArray[i]
    #             if random.SystemRandom().random() < cpMngr.totalResetProb:
    #                 _PS.useFixedBandColors = random.SystemRandom().random() < cpMngr.useFixedBandColorsProb
    #                 _PS.setCenter(i)
    #                 _PS.setNewAttributes(i)
    #                 _PS.setUp(i)


    config.drawingImage.paste(config.particleLayer, (0,0), config.particleLayer)
    config.image.paste(config.drawingImage, (0, 0), config.drawingImage)

    # _temp = ImageChops.lighter(config.drawingImage, config.particleLayer)
    # config.image.paste(_temp, (0, 0), _temp)
    config.render(config.image, 0, 0, config.canvasWidth, config.canvasHeight)


def main(run=True):
    global config
    global workConfig
    global redrawSpeed
    global PS
    global PS2
    global PSArray
    global cpMngr

    pieceLogger("concentric_particles_v4.py piece loading and running\n",2,True)

    PSArray = []

    cpMngr = ConcentricParticlesManager(config)
    cpMngr.setUp(workConfig)

    createLayers()

    for i in range(cpMngr.numberOfCenters):

        _PS = ParticleSystem(config)
        _PS.setCenter(i)
        _PS.setNewAttributes(i)
        _PS.setUp(i)

        PSArray.append(_PS)

    # managing speed of animation and framerate
    config.slotRate = float(workConfig.get("particles", "slotRate", fallback=.03))
    config.directorController = Director(config)
    config.directorController.slotRate = config.slotRate

    if run:
        runWork()


"""
new system either using set of band colors 
or
random gold and blue bands

set gold and blue via HSV ranges instead of direct RGBA

set each radial spoke to use HSV range instead of direct RGBA


"""
