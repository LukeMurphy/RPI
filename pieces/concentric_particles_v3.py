import math
import random
import threading
import time

from modules import colorutils
from PIL import Image, ImageDraw, ImageEnhance, ImageFont, ImageOps, ImageChops

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

        radialBand = round(random.SystemRandom().uniform(1,12))

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
        clr = colorutils.getRandomColorHSVSaturated(pClrRange[0],pClrRange[1],pClrRange[2],pClrRange[3],pClrRange[4],pClrRange[5])
        self.clr = [clr[0],clr[1],clr[2]]
        self.done = 0
        self.angle = angle
        self.radius = radius
        self.rSpeed = rSpeed
        self.mode = 1
        self.orbit = orbit
        self.sizeNum = 1 if random.SystemRandom().random() < 0.5 else 2


"""""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" ""

class RadialSet:
    def __init__(self, config, wBase):
        self.config = config
        self.x = 0
        self.y = 0
        self.wBase = wBase
        self.drawRadialPolys = False

    def makeRadialsSet(self, minNum=120, maxNum=300):
        self.radialsArray = []
        self.radials = round(random.SystemRandom().uniform(minNum, maxNum))
        self.rads = 2 * math.pi / self.radials

        self.angleOffset = 0.0
        self.angleOffsetSpeed = random.SystemRandom().uniform(0, math.pi / 300)
        innerRadius = self.wBase / 3
        outerRadius = self.wBase
        skipRatio = random.SystemRandom().random() + 0.3

        if minNum == 1 and maxNum == 1 :
            self.radials = 1
            self.rads = 2 * math.pi
            self.angleOffsetSpeed = math.pi/290
            innerRadius = 10

        for i in range(0, self.radials):
            ir = innerRadius + random.SystemRandom().uniform(-50, 50)
            outr = outerRadius + random.SystemRandom().uniform(-50, 50)
            skip = 0 if random.SystemRandom().random() < skipRatio else 1
            self.radialsArray.append([ir, outr, skip])


"""""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" ""

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
        self.bandWVariabilityProb = .005
        self.xMaxFactor = 4
        self.yMaxFactor = 4


    def setNewAttributes(self):
        self.radialSets = []
        
        self.bandColors = [
        [50,10,50],
        [120,90,90],
        [120,50,50],
        [50,120,90],
              [151,165,194],

        [222,208,182],
        [120,74,52],
        [187,189,168],
        [129,137,158],
        [204,228,232],
        [253,240,195],
        
        [199,166,151],
        [151,165,194],
        [89,113,175],
        [53,73,136],
        [27,38,83],
        [27,38,83],

        ]
        self.__bandColors = [
             
        [0,0,0],
        [50,10,50],
        [120,50,50],
        [50,120,90],
        [222,208,182],
        [120,74,52],
        [129,137,158],
        [204,228,232],

        
        [50,10,50],
        [120,50,50],
        [50,120,90],
        [222,208,182],
        [120,74,52],
        [129,137,158],
        [204,228,232],
        [253,240,195],
        [199,166,151],
        [151,165,194],
        [89,113,175],
        [53,73,136],
        [27,38,83],
        [27,38,83],
        [27,38,253],
        

        ]

        self._bandColors = [
        [255,0,0],
        [255,255,0],
        [0,255,0],
        [0,255,255],
        [0,0,250],
        [255,0,250],


    
        ]


                    
        # created transition bands
        
        self.bandColorsAdjusted = []
        bandColorSteps = 3
        self.bandColors.reverse()
        
        for c in range(0, len(self.bandColors)-1) :
            color1 = self.bandColors[c]
            color2 = self.bandColors[c + 1]
            
            rDiff = (color2[0] - color1[0]) / bandColorSteps
            gDiff = (color2[1] - color1[1]) / bandColorSteps
            bDiff = (color2[2] - color1[2]) / bandColorSteps
            
            for i in range(0, bandColorSteps) :
                self.bandColorsAdjusted.append([
                    round(color1[0] + rDiff * i),
                    round(color1[1] + gDiff * i),
                    round(color1[2] + bDiff * i)
                                                ])
                

        # adjusting the apparent brightness of some bands as they
        # read over-bright - can be modified anytime
        for c in range(0, len(self.bandColorsAdjusted)) :
            color = self.bandColorsAdjusted[c]
            sumOfColors = color[0] + color[1] + color[2]
            if sumOfColors > 330 and c < 13 :
                for cx in range(0,3):
                    color[cx] *= .8
        # self.bandColorsAdjusted = self.bandColors.copy()        
        
        # The rings around the center
        self.bands = round(random.SystemRandom().uniform(config.PSMinBands, config.PSMaxBands))
        self.wBase = round(random.SystemRandom().uniform(config.PSRadiusMin, config.PSRadiusMax))
        
        self.bands = bandColorSteps * len(self.bandColors)
        
        print(self.bands)
        
        self.bandWidthsSet = []
        for b in range(0, self.bands) :
            self.bandWidthsSet.append(round(random.SystemRandom().uniform(config.PSFixedColorRadiusDiffMin,config.PSFixedColorRadiusDiffMax)))
        
        if self.useFixedBandColors == True:
            self.wBase = round(random.SystemRandom().uniform(config.PSRadiusMin, config.PSRadiusMax))
            # self.bands = len(self.bandColors)
            self.wDiff = round(random.SystemRandom().uniform(config.bandWidthMin, config.bandWidthMax))
        
        self.xSpeed = random.SystemRandom().random()  * config.PSXSpeed
        self.ySpeed = random.SystemRandom().random() * config.PSYSpeed
        
        self.xMaxFactor = config.xMaxFactor
        self.yMaxFactor = config.yMaxFactor

        self.drawRadialPolys = True if random.SystemRandom().random() < .5 else False

        radialSet = RadialSet(config, self.wBase)
        radialSet.makeRadialsSet(120,300)
        self.radialSets.append(radialSet)

        # self.bands = 20
        # self.wDiff = 30
        # print(self.bands)
        
        # the 33s hand
        radialSet = RadialSet(config, self.wBase)
        radialSet.makeRadialsSet(1,1)
        self.radialSets.append(radialSet)

    
    def setCenter(self):
        # initial center position
        self.x = round(random.SystemRandom().uniform(self.initXRange[0], self.initXRange[1]))
        self.y = round(random.SystemRandom().uniform(self.initYRange[0], self.initYRange[1]))

    
    def setUp(self):

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


        dx = config.canvasWidth - self.x
        dy = config.canvasHeight - self.y
        self.maxRadius = (
            math.sqrt(
                config.imageCanvasWidth * config.imageCanvasWidth
                + config.imageCanvasHeight * config.imageCanvasHeight
            )
            * config.PSRadiusFactor1
        )

        self.radialBand = self.maxRadius / 12


        for n in range(0, self.p):
            pDot = ParticleDot()
            pDot.setUp(self, n)
            self.particles.append(pDot)

    
    def move(self):

        self.x += self.xSpeed
        self.y += self.ySpeed

        if self.x > config.canvasWidth - round(self.wBase / self.xMaxFactor):
            self.xSpeed = 0
        if self.y > config.canvasHeight - round(self.wBase / self.yMaxFactor):
            self.ySpeed = 0
        if self.y < 0 - 2:
            self.ySpeed = 0
            

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

                # horizontal Continuity
                if config.horizontalContinuity == True :
                    if ref.xPos  > config.imageCanvasWidth :
                        ref.xPos = 0
                        
                    if ref.xPos  < 0 :
                        ref.xPos  = config.imageCanvasWidth   
                # vertical Continuity
                if config.verticalContinuity == True :
                    if ref.xPos  > config.imageCanvasWidth :
                        ref.xPos = 0
                        
                    if ref.xPos  < 0 :
                        ref.xPos  = config.imageCanvasWidth   
                        
                    if ref.yPos  > config.imageCanvasHeight :
                        ref.yPos = 0
                        
                    if ref.yPos  < 0 :
                        ref.yPos  = config.imageCanvasHeight   
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
				config.vx = round(2 - random.SystemRandom().random() * 4)
				ref.vx = config.vx
				self.deacellerationx = 0.75
			"""

            # Sparkles !!
            if random.SystemRandom().random() < config.sparkleProb:
                r = int(220 * self.sparkleBrightness)
                g = int(220 * self.sparkleBrightness)
                b = int(255 * self.sparkleBrightness)

            # if (q ==0) : print (particles[q]['c'][0])
            xDisplayPos = ref.xPos
            yDisplayPos = ref.yPos
            
            # horizontal Continuity
            if config.horizontalContinuity == True :
                if xDisplayPos  > config.canvasWidth :
                    xDisplayPos = ref.xPos - config.imageCanvasWidth
                    
                if xDisplayPos  < 0 :
                    xDisplayPos  = config.imageCanvasWidth  - ref.xPos
            # vertical Continuity
            if config.verticalContinuity == True :
                if xDisplayPos  > config.imageCanvasWidth :
                    xDisplayPos = ref.xPos - config.imageCanvasWidth
                    
                if xDisplayPos  < 0 :
                    xDisplayPos  = config.imageCanvasWidth  - ref.xPos
                    
                if yDisplayPos  > config.imageCanvasHeight :
                    yDisplayPos = ref.yPos - config.imageCanvasHeight
                    
                if yDisplayPos  < 0 :
                    yDisplayPos  = config.imageCanvasHeight  - ref.yPos

            if (
                xDisplayPos <= self.config.imageCanvasWidth
                and xDisplayPos >= 0
                and yDisplayPos >= 0
                and yDisplayPos <= config.imageCanvasHeight
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
                    # faster procesor, better c subroutines and maybe we could do it this way ...
                    # config.image.putpixel((round(xDisplayPos), round(yDisplayPos)), (r, g, b))
                    # config.image.putpixel((round(xDisplayPos)+1, round(yDisplayPos)), (r, g, b))
                    # config.image.putpixel((round(xDisplayPos), round(yDisplayPos)+1), (r, g, b))
                    # config.image.putpixel((round(xDisplayPos)+1, round(yDisplayPos)+1), (r, g, b))
                except Exception as e:
                    print(str(e))

            """
			"""
            if (

                yDisplayPos > config.imageCanvasHeight
                or yDisplayPos < 0

            ):
                ref.setUp(self, ref.id)
            # if (
            #     xDisplayPos > config.canvasWidth
            #     or yDisplayPos > config.canvasHeight
            #     or yDisplayPos < 0
            #     or xDisplayPos < 0
            # ):
            #     ref.setUp(self, ref.id)




            if random.SystemRandom().random() < config.particleResetProb:
                ref.setUp(self, ref.id)


"""""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" ""


def drawBands(p):
        
    wBase = p.wBase
    
    wDiff = round(wBase / p.bands)
    
    if p.useFixedBandColors == True :
        wDiff = p.wDiff
        # print(wDiff, p.bands, wBase)

    aBase = 0
    aDiff = 10

    rBase = config.rBase
    gBase = config.gBase
    bBase = config.bBase
    aBase = config.aBase

    rBase2 = config.rBase2
    gBase2 = config.gBase2
    bBase2 = config.bBase2
    aBase2 = config.aBase2

    rDiff = config.rDiff
    gDiff = config.gDiff
    bDiff = config.bDiff
    
    
    # Draw from the outside-in
    colorBandIndex = 0
    goldenBandIndex = 0


    calculatedRingSize = wBase/p.bands
    

    for i in range(0, p.bands):
        
        if p.useFixedBandColors == True :
            wDiff = p.bandWidthsSet[i]
            
        w = wBase - i * wDiff
        
        if p.useFixedBandColors == True or random.SystemRandom().random() < p.bandWVariabilityProb:
            w = (p.bands - i) * calculatedRingSize
        
        if w > 10 :
            x0 = p.x - w / 2
            y0 = p.y - w / 2
            x1 = p.x + w / 2
            y1 = p.y + w / 2
            
            if x1 < 0 or x1 < x0 :
                x1 = x0
            if y1 < 0 or y1 < y0 :
                y1 = y0

            a = (round(config.fadeRate + aBase) if config.fadeRate > aBase else round(config.fadeRate))
            
            # OVERRIDE
            a = 255

            #config.draw.ellipse((x0, y0, x1, y1), fill=(5, 30, 60, round(a)))
            
            
            if p.useFixedBandColors == True :
                # index = p.bands - i - 1
                index = colorBandIndex
                # index = i
                
                rBase = round(p.bandColorsAdjusted[index][0] * config.brightness)
                gBase = round(p.bandColorsAdjusted[index][1] * config.brightness)
                bBase = round(p.bandColorsAdjusted[index][2] * config.brightness)
                aBase = 255
                colorBandIndex += 1
                
                if colorBandIndex >= len(p.bandColorsAdjusted) :
                    colorBandIndex = 0

    
            '''
            if i == 1:
                config.draw.ellipse((x0, y0, x1, y1), fill=(rBase, gBase, bBase, round(a)))
            '''
            # Should try to interleave the bands so that the fixed color bands integrate better
            # with the prescribed golden ones
      
            if i == 0 :
                a = 20
            try :
                # Golden Rings
                if i in config.goldenRingsArray and p.useFixedBandColors == False:
                    config.draw.ellipse( (x0, y0, x1, y1), fill=(rBase2, gBase2, bBase, aBase2) )
                    config.drawOverFlow.ellipse( (x0, y0, x1, y1), fill=(rBase2, gBase2, bBase, aBase2) )
                else :
                    # OVERRIDE 
                    if p.useFixedBandColors == True and index == 4:
                        config.draw.ellipse((x0, y0, x1, y1), outline=(rBase, gBase, bBase, a))
                        # config.draw.ellipse((x0-1, y0-1, x1-1, y1-1), outline=(rBase, gBase, bBase, a))
                        config.drawOverFlow.ellipse((x0, y0, x1, y1), outline=(rBase, gBase, bBase, a))
                    else :
                        config.draw.ellipse((x0, y0, x1, y1), fill=(rBase, gBase, bBase, a))
                        config.drawOverFlow.ellipse((x0, y0, x1, y1), fill=(rBase, gBase, bBase, a))
            except Exception as e :
                print("==>" + str(e))

            if p.useFixedBandColors == False :
                rBase += rDiff
                gBase += gDiff
                bBase += bDiff
                aBase += aDiff

            if rBase < 0 : rBase = 0
            if gBase < 0 : gBase = 0
            if bBase < 0 : bBase = 0

    i = 0


    
    for rSet in p.radialSets :

        rSet.angleOffset += rSet.angleOffsetSpeed
        polyArray = []
        numLines  = len(rSet.radialsArray)

        for n in range(0, numLines):
            a = i * rSet.rads + rSet.angleOffset
            x0 = math.cos(a) * rSet.radialsArray[n][0] + p.x
            y0 = math.sin(a) * rSet.radialsArray[n][0] + p.y
            x1 = math.cos(a) * rSet.radialsArray[n][1] + p.x
            y1 = math.sin(a) * rSet.radialsArray[n][1] + p.y
            i += 1
            polyArray.append((x0,y0))
            polyArray.append((x1,y1))
            if rSet.radialsArray[n][2] == 0:
                config.draw.line((x0, y0, x1, y1), fill=(config.radialRed, config.radialGreen, config.radialBlue, config.radialAlpha))
                config.drawOverFlow.line((x0, y0, x1, y1), fill=(config.radialRed, config.radialGreen, config.radialBlue, config.radialAlpha))
            if numLines == 1 :
                config.draw.line((x0, y0, x1, y1), fill=(config.radial2Red, config.radial2Green, config.radial2Blue, config.radialAlpha))
                config.drawOverFlow.line((x0, y0, x1, y1), fill=(config.radial2Red, config.radial2Green, config.radial2Blue, config.radialAlpha))


        if rSet.drawRadialPolys == True:
            config.draw.polygon(polyArray, fill=(config.radialRed, config.radialGreen, config.radialBlue,10), outline=(config.radialRed, config.radialGreen, config.radialBlue, config.radialAlpha+20))
            config.drawOverFlow.polygon(polyArray, fill=(config.radialRed, config.radialGreen, config.radialBlue,10), outline=(config.radialRed, config.radialGreen, config.radialBlue, config.radialAlpha+20))
    



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
    
    config.drawOverFlow.rectangle((0,0,100,200), fill=(200,0,0))

    if config.horizontalContinuity == True :
        # config.image  = ImageChops.add(config.image,config.imageOverFlow, scale = 1.0, offset= 0)
        
        xCrop  = round(config.imageCanvasWidth)
        xCrop2 = round(config.imageCanvasWidth - config.imageCanvasWidth/ config.horizontalOverlapFraction)
        temp = config.imageOverFlow.crop((xCrop,0,xCrop + config.imageCanvasWidth / config.horizontalOverlapFraction, config.canvasHeight))
        temp2 = config.drawingImage.crop((xCrop2,0,config.imageCanvasWidth, config.imageCanvasHeight))
        temp3 = ImageChops.add(config.drawingImage, temp, scale=1.0, offset = 0)
        config.image.paste(temp3, (0,0), temp2)
        
        
    if config.verticalContinuity == True :
        # config.image  = ImageChops.add(config.image,config.imageOverFlow, scale = 1.0, offset= 0)
        
        yCrop  = round(config.imageCanvasHeight)
        yCrop2 = round(config.imageCanvasHeight - config.imageCanvasHeight/ config.verticalOverlapFraction)
        # print(yCrop2)
        
        
        # temp = config.imageOverFlow.crop((0,yCrop,config.canvasWidth, yCrop + config.canvasHeight / config.verticalOverlapFraction))
        # temp2 = config.image.crop((0,yCrop2,config.canvasWidth, config.canvasHeight))

        temp = config.imageOverFlow.crop((0,yCrop,config.imageCanvasWidth,yCrop + config.imageCanvasHeight / config.verticalOverlapFraction))
        temp2 = config.drawingImage.crop((0,yCrop2,config.imageCanvasWidth,config.imageCanvasHeight))
        
        temp3 = ImageChops.add(temp,config.drawingImage, scale=1.0, offset = 0)
        config.drawingImage.paste(temp3, (0,0), temp2)
        
    drawBands(PS)

    PS.move()

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
            print(f"ALL NEW {config.bgColor}  {config.fadeRateDelta}")
            if random.SystemRandom().random() < config.totalResetProb:
                PS.useFixedBandColors = True if random.SystemRandom().random() < config.useFixedBandColorsProb else False
                PS.setCenter()
                PS.setNewAttributes()
                PS.setUp()

    config.image.paste(config.drawingImage, (0,0),config.drawingImage)
    config.render(config.image, 0, 0, config.canvasWidth, config.canvasHeight)

    # Done


def main(run=True):
    global config
    global workConfig
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
    config.bgColor = random.choice(config.bgColorSets)
    #config.bgColor = config.bgColorSets[1]

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

    config.fadeRate = float(workConfig.get("particles", "fadeRate"))
    config.fadeRateDelta = float(workConfig.get("particles", "fadeRateDelta"))
    config.sparkleProb = float(workConfig.get("particles", "sparkleProb"))
    config.fadeRateNewSystemThreshold = float(workConfig.get("particles", "fadeRateNewSystemThreshold"))

    config.particleResetProb = float(workConfig.get("particles", "particleResetProb"))
    config.totalResetProb = float(workConfig.get("particles", "totalResetProb"))
    config.orbitProb = float(workConfig.get("particles", "orbitProb"))
    
    
    # set the actual drawing space
    try:
        config.imageCanvasWidth = int(workConfig.get("particles","imageCanvasWidth"))
        config.imageCanvasHeight = int(workConfig.get("particles","imageCanvasHeight"))
        
    except Exception as e:
        print(str(e))
        config.imageCanvasWidth = config.canvasWidth
        config.imageCanvasHeight = config.canvasHeight
    


    # comment: # for some towers the seam between the 
    # start and end needs to become semi-continuous
    # so I make the particles appear to move around the piece
    # and overlap one side with some of the drawing
    # if every thing was drawn pixel by pixel this would
    # probably not need to be so complicated
    config.horizontalContinuity = workConfig.getboolean("particles","horizontalContinuity")
    config.horizontalOverlapFraction = int(workConfig.get("particles","horizontalOverlapFraction"))

    config.verticalContinuity = workConfig.getboolean("particles","verticalContinuity")
    config.verticalOverlapFraction = int(workConfig.get("particles","verticalOverlapFraction"))


    config.PSXSpeed = float(workConfig.get("particles", "PSXSpeed"))
    config.PSYSpeed = float(workConfig.get("particles", "PSYSpeed"))
    config.PSRadiusFactor1 = float(workConfig.get("particles", "PSRadiusFactor1"))
    config.PSRadiusFactor2 = float(workConfig.get("particles", "PSRadiusFactor2"))
    config.PSRadiusMin = float(workConfig.get("particles", "PSRadiusMin"))
    config.PSRadiusMax = float(workConfig.get("particles", "PSRadiusMax"))
    config.PSMinBands = int(workConfig.get("particles", "PSMinBands"))
    config.PSMaxBands = int(workConfig.get("particles", "PSMaxBands"))
    config.PSRadiusFixedColorMin = int(workConfig.get("particles", "PSRadiusFixedColorMin"))

    config.bandWidthMin = int(workConfig.get("particles","bandWidthMin"))
    config.bandWidthMax = int(workConfig.get("particles","bandWidthMax"))
    config.PSFixedColorRadiusDiffMin = int(workConfig.get("particles","PSFixedColorRadiusDiffMin"))
    config.PSFixedColorRadiusDiffMax = int(workConfig.get("particles","PSFixedColorRadiusDiffMax"))

    goldenRingsArray = workConfig.get("particles","goldenRingsArray").split(',')
    config.goldenRingsArray = list(int(x) for x in goldenRingsArray)
    
    config.useFixedBandColorsProb = float(workConfig.get("particles","useFixedBandColorsProb"))
    try:
        config.xMaxFactor = float(workConfig.get("particles","xMaxFactor"))
        config.yMaxFactor = float(workConfig.get("particles","yMaxFactor"))
        
    except Exception as e:
        print(str(e))
        config.xMaxFactor = 4
        config.yMaxFactor = 8

    try:
        config.rRange = int(workConfig.get("particles","rRange"))
        config.gRange = int(workConfig.get("particles","gRange"))
        config.bRange = int(workConfig.get("particles","bRange"))
        config.rRangeMin = int(workConfig.get("particles","rRangeMin"))
        config.gRangeMin = int(workConfig.get("particles","gRangeMin"))
        config.bRangeMin = int(workConfig.get("particles","bRangeMin"))
    except Exception as e:
        print(str(e))
        config.rRange = 255
        config.gRange = 200
        config.bRange = 255
        config.rRangeMin = 0
        config.gRangeMin = 0
        config.bRangeMin = 0
        
        
    particleColorRangeVals  = workConfig.get("particles","particleColorRange").split(",")
    config.particleColorRange = list(float(i) for  i in particleColorRangeVals)
        

        


    config.image = Image.new("RGBA", (config.canvasWidth, config.canvasHeight))
    config.drawingImage = Image.new("RGBA", (config.imageCanvasWidth, config.imageCanvasHeight))
    config.draw = ImageDraw.Draw(config.drawingImage)
    
    config.imageOverFlow = Image.new("RGBA", (config.canvasWidth * 2, config.canvasHeight * 2))
    config.drawOverFlow = ImageDraw.Draw(config.imageOverFlow)
    
    
    PS = ParticleSystem(config)
    PS.setCenter()
    PS.setNewAttributes()
    PS.setUp()

    # managing speed of animation and framerate
    config.directorController = Director(config)
    config.directorController.slotRate = 0.03

    if run:
        runWork()
