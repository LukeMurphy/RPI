#!/usr/bin/python
import PIL.Image
from PIL import Image, ImageDraw, ImageMath, ImageEnhance
from PIL import ImageChops
#from modules import colorutils
# Import the essentials to everything
import time, random, math

''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

class Lsys :
	
	n = 5
	c = 0
	recursionLimit = 5
	strg = ""
	AxiomSelected = "F"
	PatternSetSelected = "F+F-F-F"
	PatternSetSelected2 = ""
	useRandom = True
	foliage = False
	incrRange = 6
	incrEnd = 6
	angle = 20
	d = 80
	dFactor = 1
	dFactorMultiplier = .8
	
	s = ""
	incrStart = 0
	instruction = ""
	xPos = 0
	yPos = 0
	origin = dict(xpos=0,ypos=0)
	a = 0
	branchPoint = []
	branch = 0

	canvasBase =  dict(width=160,height=160)

	
	#nodeSpriteContainer:Sprite
	

			
	def __init__(self) :
		print("Init Lsys")
		incrRange = 100
		incrEnd = 100
		incrStart = 0
		origin = {"xPos":self.canvasBase["width"]/2,"yPos":self.canvasBase["height"]-5}
		self.setUpNewDrawingParameters()
		
			
	def restore(self):
		canvasBaseHolder.x = 0
		canvasBaseHolder.y = 0
	
	
	def setUpNewDrawingParameters(self) :
		self.c = 0
		self.strg = ""
		if (self.PatternSetSelected2 == ""): self.PatternSetSelected2 = "B"
		self.strg = self.parse(self.AxiomSelected)
		print(self.strg)
		#self.setupDrawing()
			
	def stopBuild(self) :
		if (ti) :
			ti.stop()
			ti = null
		self.xPos = self.origin['xPos']
		self.yPos = self.origin['yPos']
		self.branchPoint = []
		self.dFactor = 1
		self.a = 0
		self.incrStart = 0
		self.incrEnd = 100
			
	def setupDrawing(self) :
		self.branchPoint = []
		self.xPos = self.origin['xPos']
		self.yPos = self.origin['yPos']
		#if (s) : canvasBaseHolder.removeChild(s)
		#s = new UIComponent()
		#canvasBaseHolder.addChild(s)
		#s.graphics.moveTo(xPos,yPos)

		#ti =  new Timer(1)
		#ti.addEventListener(TimerEvent.TIMER, redraw)
		#ti.start()
			
	def redraw(self, e):
		if (incrStart < strg.length-incrRange) :
			performAction()
		
	
	def parse(self, A):
		finalString = A
		self.c+=1
		if (self.c<self.recursionLimit) :
			for i in range(0, len(A)) :
				if (A == "F")  :
					finalString += self.PatternSetSelected;
				elif (A == "B") :
					finalString += self.PatternSetSelected2;
				else :
					finalString += A[i];
			return self.parse(finalString)
		else :
			return A	
		return finalString
	
		
	def performAction(self) :
		for incr in range(incrStart, incrEnd) :
			drawTerminal = false
			instruction =  strg.charAt(incr)
			if (instruction == "[") :
				branchPoint.push( {x:xPos,y:yPos,a:a})
				dFactor*=dFactorMultiplier
				if (instruction == "]") :
					branch  = branchPoint.length-1
				if (branch>0 and useRandom):
					angle += random() - random()
				
				if (branch>1 and foliage) :
					#node = new Sprite()
					#nodeMark = new Sprite()
					node.x = xPos
					node.y = yPos
					#nodeMark.graphics.beginFill(0x000000,.5)
					
					foliageWidth = branch/dFactor
					foliageHeight = branch*5/dFactor
					
					if (foliageWidth > 20):foliageWidth = 20
					if (foliageHeight > 10):foliageHeight = 10
					
					#nodeMark.graphics.drawEllipse(0,0,foliageWidth,foliageHeight)
					#nodeMark.rotation =  180/Math.PI *  Math.sin(a)
					#nodeMark.graphics.endFill()
					#node.addChild(nodeMark)
					#s.addChild(node)
									
				xPos = branchPoint[branch].x
				yPos = branchPoint[branch].y
				a = branchPoint[branch].a
				#s.graphics.moveTo(xPos,yPos)
				branchPoint.pop()
				dFactor*=(1/dFactorMultiplier)
				drawTerminal = true
				if (instruction == "-" or instruction == "=") :
					a += -angle
				if (instruction == "+") :
					a += angle
				if (instruction.toLowerCase() == "f" or instruction.toLowerCase() == "b") :
					x1 = Math.cos(a * Math.PI/180 - Math.PI/2) * d*dFactor
				if (random) : x1 *= random()*2
				y1 = Math.sin(a * Math.PI/180 - PI/2) * d*dFactor
				xPos += x1
				yPos += y1
				baseColor = 0xcc0000
				f = 1/branch
				if (branch == 0 or isNaN(branch)) : f = 1
				colorOfLine = Math.round(baseColor - baseColor * dFactor*5)
				
				#s.graphics.lineStyle(dFactor*3.5,colorOfLine,f)
				#s.graphics.lineTo(xPos,yPos)

				
				incrStart += incrRange
				incrEnd = incrStart +  incrRange


''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''


l = Lsys()
