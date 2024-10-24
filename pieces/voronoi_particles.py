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

    def setUp(self, p, n):
        # variation in initial velocity
        direction = 1.0 if p.directionProb < 0.5 else -1.0
        directionx = 1.0 if random.random() < 0.5 else -1.0
        directiony = 1.0 if random.random() < 0.5 else -1.0
        orbit = True if p.orbitProb <= config.orbitProb else False
        fx = random.random() * p.fFactor + 0
        fy = random.random() * p.fFactor + 0
        # vx = math.cos(p.angle * n) * fx * direction
        # vy = math.sin(p.angle * n) * fy * direction
        r = int(random.uniform(0, 255) * p.brightness)
        g = int(random.uniform(0, 200) * p.brightness)
        b = int(random.uniform(0, 255) * p.brightness)
        radius = random.uniform(1, p.maxRadius)

        vx = fx * directionx * config.particleXSpeed
        vy = fy * directiony * config.particleYSpeed

        # Make radius fall into one of the systems bands - like quanta

        radialBand = round(random.uniform(1,12))

        radius = p.radialBand * radialBand

        rSpeed = random.uniform(config.rSpeedMin, config.rSpeedMax)
        
        if config.rSpeedRadialProportional == True:
            rSpeed = random.uniform(config.rSpeedMin, config.rSpeedMax)/ radius * 100.0

        xPos = p.x
        yPos = p.y
        angle = p.angle * n

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
        self.mode = 0
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

        self.brightness = config.brightness


    def setNewAttributes(self):
        self.bands = round(random.uniform(12, 24))
        self.wBase = round(random.uniform(220, config.canvasWidth))

        self.xSpeed = random.random() * config.particleXSpeed
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
        for i in range(0, self.radials):
            ir = innerRadius + random.uniform(-config.innerRadius, config.innerRadius)
            outr = outerRadius + random.uniform(-config.innerRadius, config.outerRadius)
            skip = 0 if random.random() < skipRatio else 1
            self.radialsArray.append([ir, outr, skip])

    def setCenter(self):
        # initial center position
        self.x = round(random.uniform(self.initXRange[0], self.initXRange[1]))
        self.y = round(random.uniform(self.initYRange[0], self.initYRange[1]))

    def setUp(self):
        self.directionProb = random.uniform(0, 1)
        self.orbitProb = config.orbitProb
        # Number of sparks
        self.p = int(5 + (random.uniform(config.minParticles, config.maxParticles)))
        self.angle = 2 * math.pi / self.p

        config.numberDone = round(self.p / 5)

        # Speed factor
        self.fFactor = float(random.uniform(config.speedFactorMin, config.speedFactorMax))

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
            * 2.5
        )

        self.radialBand = self.maxRadius / 12
         
        if random.random() < .5 :
            config.movementMode = 0
        else :
            config.movementMode = 1

        for n in range(0, self.p):
            pDot = ParticleDot()
            pDot.setUp(self, n)
            pDot.mode = 0
            # pDot.mode = config.movementMode 
            self.particles.append(pDot)

    def move(self):

        self.x += self.xSpeed
        self.y += self.ySpeed

        # if self.x > config.canvasWidth - round(self.wBase / 4):
        #     self.xSpeed = 0

        for q in range(0, self.p):
            ref = self.particles[q]

            ref.mode  = 1
            if ref.mode == 1:
                ref.xPos += ref.vx
                ref.yPos += ref.vy

                dx = ref.xPos - self.x
                dy = ref.yPos - self.y

                r = round(math.sqrt(dx * dx + dy * dy))

                # if r > ref.radius/1 and ref.orbit:
                #     # print(r, ref.radius, ref.orbit)
                #     ref.mode = 0

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

            if (
                xDisplayPos > config.xRange 
                or yDisplayPos > config.yRange
                or yDisplayPos < -config.yRange
                or xDisplayPos < -config.xRange
            ):
                ref.setUp(self, ref.id)

            if random.random() < config.particleResetProb:
                ref.setUp(self, ref.id)



        # for y in range(0,config.imgy,config.resolutionOfSquares):
        #     for x in range(0,config.imgx,config.resolutionOfSquares):
        #         dmin = math.hypot(config.imgx - 1, config.imgy - 1)
        #         j = -1
        #         for i in range(config.num_cells):
        #             ref = self.particles[i]
        #             d = math.hypot(ref.xPos - x, ref.yPos - y)
        #             if d < dmin:
        #                 dmin = d
        #                 j = i

        #         config.draw.rectangle((x,y,x+config.resolutionOfSquares,y+config.resolutionOfSquares), fill = (config.nr[j], config.ng[j], config.nb[j],90))
 
 
        # Draw the Voronoi cells 
        pointsArray = []
        for i in range(config.num_cells):
            ref = self.particles[i]
            pointsArray.append([ref.xPos,ref.yPos])
            # config.draw.rectangle((ref.xPos,ref.yPos,ref.xPos+3,ref.yPos+3), fill=(200,200,200,255))
            
        points = np.array(pointsArray)
        vor = Voronoi(points)
        
        vVertices = vor.vertices
        vRegions = vor.regions
        vPoints = vor.points
        vPointRegion = (vor.point_region).tolist()
        
        j = 0
        clrIndex = 0
        for region in vRegions:
            for i in range(0, len(vPointRegion)) :
                if j == vPointRegion[i] :
                    break

            if -1 not in region:
                polygon = [tuple(vVertices[p].tolist()) for p in region]
                if len(polygon) > 0 and i < config.num_cells :
                    
                    if withinRange(self.particles[j].xPos, self.x, 3) and withinRange(self.particles[j].yPos, self.y, 3) :
                        pass
                    else :
                        config.draw.polygon(polygon, outline=(40,0,0,round(config.lineAlpha) ), width = 2 , fill = (config.nr[i], config.ng[i], config.nb[i],round(config.cellAlpha) )) 
                        # config.draw.polygon(polygon, outline=(40,0,0,round(config.lineAlpha) ), width = 2 , fill = (config.nr[i], config.ng[i], config.nb[i],round(config.fadeRate))) 
                    # config.draw.polygon(polygon, outline=(100,0,0,255), width = 1 , fill = None) 
            j+=1
            
        # exit()

        


"""""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" ""

def withinRange(arg, target, diff) :
    val = round(arg)
    test1 = round(target + diff)
    test2 = round(target - diff)
    if val <= test1 and val >= test2 :
        return True
    else :
        return False


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

        '''
        config.draw.ellipse((x0, y0, x1, y1), fill=(4, 4, bBase, round(a)))

        if i == 1:
            config.draw.ellipse((x0, y0, x1, y1), fill=(rBase, gBase, bBase, round(a)))

        if i == 0 or i == 12:
            config.draw.ellipse(
                (x0, y0, x1, y1), fill=(rBase2, gBase2, bBase, round(a))
            )
        '''
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
            config.draw.line((x0, y0, x1, y1), fill=(250, 180, 0, 55))


"""""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" ""



# def generate_voronoi_diagram(width, height, num_cells):

#     for i in range(config.num_cells):
#         config.nx[i] += config.nvx[i]
#         config.ny[i] += config.nvy[i]

#         if config.nx[i] > config.canvasWidth or config.nx[i] < -2 :
#             config.nvx[i] *= -1
#         if config.ny[i] > config.canvasHeight or config.ny[i] < -2 :
#             config.nvy[i] *= -1

#     for y in range(0,config.imgy,config.resolutionOfSquares):
#         for x in range(0,config.imgx,config.resolutionOfSquares):
#             dmin = math.hypot(config.imgx - 1, config.imgy - 1)
#             j = -1
#             for i in range(config.num_cells):
#                 d = math.hypot(config.nx[i] - x, config.ny[i] - y)
#                 if d < dmin:
#                     dmin = d
#                     j = i
#             #putpixel((x, y), (nr[j], ng[j], nb[j]))
#             #putpixel((x, y), (nr[j], ng[j], nb[j]))
            
            
#             config.draw.rectangle((x,y,x+config.resolutionOfSquares,y+config.resolutionOfSquares), fill = (config.nr[j], config.ng[j], config.nb[j]))
#             # config.draw.line((x,y,x+config.resolutionOfSquares,y+config.resolutionOfSquares), fill = (0,0,0),width = 1)





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
            255
            # round(config.fadeRate),
        ),
    )


    PS.move()

    # drawBands(PS)

    #generate_voronoi_diagram(256, 256, 70)


    config.fadeRate += config.fadeRateDelta
    # if random.random() < config.totalResetProb:
    #     PS.setUp()

    '''
    '''
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
        config.useFilters = True
        config.remapImageBlock = False

        startX = round(random.uniform(0, config.filterRemapRangeX))
        startY = round(random.uniform(0, config.filterRemapRangeY))
        endX = round(random.uniform(config.filterRemapMinHorzSize, config.filterRemapMaxHorzSize))
        endY = round(random.uniform(config.filterRemapMinVertSize, config.filterRemapMaxVertSize))
        config.remapImageBlockSection = [startX, startY, startX + endX, startY + endY]
        config.remapImageBlockDestination = [startX, startY]

            
    config.render(config.image, 0, 0, config.canvasWidth, config.canvasHeight)

    # Done


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
    config.rSpeedRadialProportional = (workConfig.getboolean("particles", "rSpeedRadialProportional"))

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

    config.innerRadius = int(workConfig.get("particles", "innerRadius"))
    config.outerRadius = int(workConfig.get("particles", "outerRadius"))
    config.xRange = int(workConfig.get("particles", "xRange"))
    config.yRange = int(workConfig.get("particles", "yRange"))

    config.fadeRate = float(workConfig.get("particles", "fadeRate"))
    config.lineAlpha = float(workConfig.get("particles", "lineAlpha"))
    config.cellAlpha = float(workConfig.get("particles", "cellAlpha"))
    config.fadeRateDelta = float(workConfig.get("particles", "fadeRateDelta"))
    config.sparkleProb = float(workConfig.get("particles", "sparkleProb"))
    config.fadeRateNewSystemThreshold = float(workConfig.get("particles", "fadeRateNewSystemThreshold"))

    config.particleResetProb = float(workConfig.get("particles", "particleResetProb"))
    config.totalResetProb = float(workConfig.get("particles", "totalResetProb"))
    config.orbitProb = float(workConfig.get("particles", "orbitProb"))

    config.image = Image.new("RGBA", (config.canvasWidth, config.canvasHeight))
    config.draw = ImageDraw.Draw(config.image)
    

    try:
        config.filterRemapping = workConfig.getboolean("particles", "filterRemapping")
        config.filterRemappingProb = float(workConfig.get("particles", "filterRemappingProb"))
        config.filterRemapMinHorzSize = int(workConfig.get("particles", "filterRemapMinHorzSize"))
        config.filterRemapMinVertSize = int(workConfig.get("particles", "filterRemapMinVertSize"))
        config.filterRemapMaxHorzSize = int(workConfig.get("particles", "filterRemapMaxHorzSize"))
        config.filterRemapMaxVertSize = int(workConfig.get("particles", "filterRemapMaxVertSize"))
        config.filterRemapRangeX = int(workConfig.get("particles", "filterRemapRangeX"))
        config.filterRemapRangeY = int(workConfig.get("particles", "filterRemapRangeY"))
    except Exception as e:
        print(str(e))
        config.filterRemapping = False
        config.filterRemappingProb = 0.0
        config.filterRemapMinHorzSize = 24
        config.filterRemapMinVertSize = 24
        config.filterRemapMaxHorzSize = 24
        config.filterRemapMaxVertSize = 24
        config.filterRemapRangeX = config.canvasWidth
        config.filterRemapRangeY = config.canvasHeight


    config.num_cells = config.maxParticles
    config.resolutionOfSquares = int(workConfig.get("particles", "resolutionOfSquares"))

    config.imgx, config.imgy = config.image.size
    config.nx = []
    config.ny = []
    config.nvx = []
    config.nvy = []
    config.nr = []
    config.ng = []
    config.nb = []


    #  for now, just have two color sets to blend the colors
    rawColorSetAVals = workConfig.get("particles", "colorSetA").replace("\n","")
    rawColorSetAVals = rawColorSetAVals.replace(" ","")
    colorSetAVals = rawColorSetAVals.split("|")
    colorSetA = []
    for element in colorSetAVals :
        if element != "" :
            clr = list(int(x) for x in element.split(","))
            colorSetA.append(clr)

    rawColorSetBVals = workConfig.get("particles", "colorSetB").replace("\n","")
    rawColorSetBVals = rawColorSetBVals.replace(" ","")
    colorSetBVals = rawColorSetBVals.split("|")
    colorSetB = []
    for element in colorSetBVals :
        if element != "" :
            clr = list(int(x) for x in element.split(","))
            colorSetB.append(clr)


    for i in range(config.num_cells):
        config.nx.append(random.randrange(-config.xRange/4,1.25 * config.xRange))
        config.ny.append(random.randrange(-config.yRange/4,1.25 * config.yRange))
        config.nvx.append(random.randrange(-2,2) )
        config.nvy.append(random.randrange(-2,2) )


        '''
        nr.append(c[0])
        ng.append(c[1])
        nb.append(c[2])
        '''
        # config.nr.append(random.randrange(256))
        # config.ng.append(random.randrange(256))
        # config.nb.append(random.randrange(256))
        
        if random.random() < .50 :
            clr = colorSetA[round(random.uniform(0,len(colorSetA)-1))]
        else :    
            clr = colorSetB[round(random.uniform(0,len(colorSetB)-1))]
        
        # clr = colorutils.randomColor()
        config.nr.append(round(clr[0] * config.brightness))
        config.ng.append(round(clr[1] * config.brightness))
        config.nb.append(round(clr[2] * config.brightness))
        
    config.movementMode = 0
    PS = ParticleSystem(config)
    PS.setCenter()
    PS.setNewAttributes()
    PS.setUp()
    

    # managing speed of animation and framerate
    config.directorController = Director(config)
    config.directorController.slotRate = 0.03
    

    if run:
        runWork()
