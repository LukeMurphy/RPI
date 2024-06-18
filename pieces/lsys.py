#!/usr/bin/python
import PIL.Image
from PIL import Image, ImageDraw, ImageMath, ImageEnhance
from PIL import ImageChops
#from modules import colorutils
# Import the essentials to everything
import time, random, math

''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

class LPoint :
    def __init__(self) :
        self.xPos = 0
        self.yPos = 0
        self.scale = 1
        self.isTerminal = 0
        self.angle = 0
        self.angleDisplay = 0
        self.segmentLength = 1
    

class Lsys :
    

    recursionLimit = 4
    strg = ""
    
    # F draws a terminal line
    # B draws a line
    # () denotes a branch
    # + - are angle changes
    
    
    Axiom = "F"
    Rule1 = "BB"
    segmentLength = 18
    segmentDecrement = .9
    # Every B gets replaced with this
    Rule2 = "B(+F)(-F)B(+F)(-F)B(+F)(-F)F(F++F+F)"	
    
    # tree with 3 branches per cycle
    Rule2 = "B(+F)(-F)B(+F)(-F)B(+F)(-F)F"
    
    
     # simple tree no extra branches
    Rule2 = "B(+B)(-B)"
    
    # tree with 3 splits
    Rule2 = "B(B)(+F)(-F)"
    
    # simple tree no extra branches
    Rule2 = "B(B)(+B)(-B)"

    Rule2 = "B(B)(+B(+B))(-B(-B))"
    
    Rule2 = "B(B(FB)(++FB)(--FB))"
    
    Rule2 = "B(-FF)(+FF)(BFF)"
    
    recursionLimit = 5
    segmentLength = 12
    segmentDecrement = .9
    # simple branching tree 1 split
    # Axiom = "F"
    # Rule1 = "BB"
    # most basic binary tree
    # Rule2 = "B(+F)(-F)"
    # Rule2 = "B(+FFF)(-FFF)(BFBF)"

    # Etruscan Tree
    # recursionLimit = 3
    # segmentLength = 18
    # segmentDecrement = .97
    # Rule2 = "B(+F)(-F)(B(B(+F)(-F)(B(B(+F)(-F)(B(B(+F)(-F)B))))))"
    

    useRandom = False
    foliage = True

    angle = math.pi/4
    branchPoint = []
    drawingPoints = []    
    
    def __init__(self, config) :
        print("========================")
        print("Init Lsys")
        self.config = config
        self.setUpNewDrawingParameters()
        print("========================")

    
    def setUpNewDrawingParameters(self) :
        self.c = 0
        self.strg = ""
        self.strg = self.parse(self.Axiom)
        print("------------------")
        print(self.strg)
        print("------------------")
        
        self.produceDrawingPoints()
            
    def setupDrawing(self) :
        self.branchPoint = []
        self.xPos = self.origin['xPos']
        self.yPos = self.origin['yPos']

            
    def redraw(self, e):
        if (incrStart < strg.length-incrRange) :
            produceDrawingPoints()
        
    def parse(self, arg):
        self.finalString = arg
        self.c+=1
        l = len(self.Rule2 )
        if (self.c<self.recursionLimit) :
            arg = arg.replace("F", self.Rule2)
            arg = arg.replace("B", self.Rule1)
            return self.parse(arg)
        return arg
       
    def produceDrawingPoints(self) :
        xPos = 0
        yPos = 0
        a = -math.pi/2
        d = 1
        c = 0
        
        lpt = LPoint()
        lpt.xPos = 0
        lpt.yPos = 0
        lpt.angle = -math.pi/2
        lpt.angleDisplay = -math.pi/2
        lpt.scale = 1
        lpt.isTerminal = 0
        lpt.name = ""
        
        self.branchPoint = []
        self.drawingPoints = []  
        
        self.config.segmentLength = self.segmentLength
        self.drawingPoints.append(lpt)
        self.branchPoint.append(lpt)
        
        # print(self.strg)
        
        for i in range(0, len(self.strg)) :
            instruction = self.strg[i]
            
            if instruction not in ("(",")") :
                if instruction == "+" :
                    a += math.pi/4 * random.uniform(.9,1.1)
                if instruction == "-" :
                    a -= math.pi/4 * random.uniform(.9,1.1)
                if instruction == "F" :
                    xPos += self.segmentLength * d * math.cos(a) * 2
                    yPos += self.segmentLength * d * math.sin(a) * 2
                    lpt = LPoint()
                    lpt.xPos = xPos
                    lpt.yPos = yPos
                    lpt.angle = a
                    lpt.angleDisplay = a
                    lpt.scale = d
                    lpt.isTerminal = c
                    lpt.name = "F"
                    lpt.segmentLength = self.segmentLength * d
                    self.drawingPoints.append(lpt)
                    
                if instruction == "B" :
                    xPos += self.segmentLength * d * math.cos(a) * 1
                    yPos += self.segmentLength * d * math.sin(a) * 1
                    lpt = LPoint()
                    lpt.xPos = xPos
                    lpt.yPos = yPos
                    lpt.angle = a
                    lpt.angleDisplay = a * random.uniform(.9,1.1)
                    lpt.scale = d
                    lpt.isTerminal = c
                    lpt.name = "B"
                    lpt.segmentLength = self.segmentLength * d * 1
                    self.drawingPoints.append(lpt)
                    
            if instruction == "(" :
                d *= self.segmentDecrement
                c = 1
                lpt = LPoint()
                lpt.xPos = xPos
                lpt.yPos = yPos
                lpt.angle = a
                lpt.scale = d
                lpt.isTerminal = c
                lpt.name = "X"
                self.branchPoint.append(lpt)
            if instruction == ")" :
                a = self.branchPoint[-1].angle
                d = self.branchPoint[-1].scale
                c = self.branchPoint[-1].isTerminal
                c = 2
                xPos = self.branchPoint[-1].xPos
                yPos = self.branchPoint[-1].yPos
                self.branchPoint = self.branchPoint[:-1]
                
            
            
    
''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
def drawLines(arg) :
    if config.rendered == False :
        # print("running")
        config.imageDraw.rectangle((0,0,config.canvasWidth, config.canvasHeight), fill = (220,210,200,210))
        for i in range(0, len(L.drawingPoints)):
            xPos = L.drawingPoints[i].xPos + 200
            yPos = L.drawingPoints[i].yPos + 500
            d = L.drawingPoints[i].scale
            l = L.drawingPoints[i].segmentLength
            
            temp = Image.new("RGBA", (config.segmentLength*2, config.segmentLength*2))
            tDraw = ImageDraw.Draw(temp)
            
            angle = round((math.pi/2  - L.drawingPoints[i].angleDisplay) * 180/math.pi)
            
            if abs(angle) != 90 :
                angle -= 90
            

            if L.drawingPoints[i].isTerminal == 0 :
                # tDraw.rectangle((l/2,l/2,l/2+ l, l/2 + 2), fill = (0,250,0))
                tDraw.rectangle((0,0,0 + l, 0 + l), fill = (0,50,0,130))
                temp2 = temp.rotate(angle,expand=1,translate=(-0,-0))
                config.image.paste(temp2,(round(xPos),round(yPos)),temp2)
            if L.drawingPoints[i].isTerminal == 1 :
                # tDraw.rectangle((l/2,l/2,l/2 + l, l/2 + 2), fill = (255,0,0))
                tDraw.ellipse((0,0,0 + l*2, 0 + l), fill = (20,0,0,230))
                temp2 = temp.rotate(angle,expand=1,translate=(-0,0))
                config.image.paste(temp2,(round(xPos),round(yPos)),temp2)
            if L.drawingPoints[i].isTerminal == 2 :
                # tDraw.rectangle((l/2,l/2,l/2 + l, l/2 + 2), fill = (255,0,0))
                tDraw.ellipse((0,0,0 + l*2, 0 + l), fill = (100,100,0,230))
                temp2 = temp.rotate(angle,expand=1,translate=(-0,0))
                config.image.paste(temp2,(round(xPos),round(yPos)),temp2)
            if i > 0 :
                if L.drawingPoints[i-1].angle !=  L.drawingPoints[i].angle:
                    # tDraw.rectangle((l/2,l/2,l/2 + l, l/2 + 2), fill = (255,0,0))
                    tDraw.ellipse((0,0,0 + l*2, 0 + l), fill = (100,5,0,230))
                    temp2 = temp.rotate(angle,expand=1,translate=(-0,0))
                    config.image.paste(temp2,(round(xPos),round(yPos)),temp2)


            # config.rendered = True


''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

def main(run = True) :
    global config, workConfig
    setUp()
    if(run) : 
        runWork()

''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

def setUp() :
    global L, config
    config.rendered = False
    config.image = Image.new("RGBA", (config.screenWidth, config.screenHeight))
    config.imageDraw  = ImageDraw.Draw(config.image)
    config.canvasImage = Image.new("RGBA", (config.canvasWidth, config.canvasHeight))
    config.draw  = ImageDraw.Draw(config.canvasImage)
    config.id = config.image.im.id
    L = Lsys(config)

''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

def runWork():
    global runRun
    while True:
        iterate()
        time.sleep(.1)

''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

def iterate() :
    global config, L, pos, runRun
    if config.rendered == False : 
        L.produceDrawingPoints()
        drawLines(L)
    config.render(config.image, 0, 0,192,192)

''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

def callBack() :
    global config
    pass

''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''


