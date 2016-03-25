import time
import random
import PIL.Image, PIL.ImageTk
from PIL import ImageDraw, ImageFont
import textwrap
import math
from modules import colorutils

########################
#scroll speed and steps per cycle
scrollSpeed = 0.0006
stroopSpeed = 0.0001
steps = 2
stroopSteps = 2
stroopFontSize = 30

fontSize = 14
vOffset  = -1
opticalOpposites = True
countLimit = 6
count = 0

# fcu present will start with the opposite
paintColor = "GREEN"

r=g=b=0


def stroopSequence() :
	directionStr = getDirection()
	#directionStr = "Bottom"
	lim  = .1 #.7
	if(random.random() > lim) :stroop("YELLOW",(255,0,225),directionStr)
	if(random.random() > lim) :stroop("VIOLET",(230,225,0),directionStr)
	if(random.random() > lim) :stroop("RED",(0,255,0),directionStr)
	if(random.random() > lim) :stroop("BLUE",(225,100,0),directionStr)
	if(random.random() > lim) :stroop("GREEN",(255,0,0),directionStr)
	if(random.random() > lim) :stroop("ORANGE",(0,0,200),directionStr)

def getDirection() :
	d = int(random.uniform(1,4))
	direction = "Left"
	if (d == 1) : direction = "Left"
	if (d == 2) : direction = "Right"
	if (d == 3) : direction = "Bottom"
	return direction

def startAnimation() :
	try :
		while True :
			runStroop()
	except TclError, details:
		print(details)
		pass
		exit()

def runStroop() :
	global config
    	while True:
    		numRuns = int(random.uniform(2,6))
    		numRuns =  1
    		for i in range(0,numRuns) : 
    			if(config.opticalOpposites) : 
    				config.opticalOpposites = False
    			else : 
    				config.opticalOpposites = True
    			stroopSequence()

def main() :
	global config, workConfig
	global fontSize,vOffset,scrollSpeed,stroopSpeed,stroopSteps,stroopFontSize,useColorFlicker
	print("Stroop Loaded")
	#[stroop]

	fontSize = int(workConfig.get("stroop", 'fontSize'))
	vOffset = int(workConfig.get("stroop", 'vOffset'))
	scrollSpeed = float(workConfig.get("stroop", 'scrollSpeed'))
	stroopSpeed = float(workConfig.get("stroop", 'stroopSpeed'))
	stroopSteps = float(workConfig.get("stroop", 'stroopSteps'))
	stroopFontSize = int(workConfig.get("stroop", 'stroopFontSize'))
	config.opticalOpposites = True
	runStroop()

def stroop( arg, clr, direction = "Left") :

        global r,g,b,config, opticalOpposites, stroopSpeed, stroopSteps, stroopFontSize

        brightness = config.brightness
        brightness = random.random()

        clr = tuple(int(a*brightness) for a in (clr))

        # Setting 2 fonts - one for the main text and the other for its "border"... not really necessary
        font = ImageFont.truetype( config.path + '/fonts/freefont/FreeSansBold.ttf',stroopFontSize)
        font2 = ImageFont.truetype(config.path + '/fonts/freefont/FreeSansBold.ttf',stroopFontSize)
        pixLen = config.draw.textsize(arg, font = font)

        dims = [pixLen[0],pixLen[1]]
        if(dims[1] < 32) : dims[1] = 34


        # Draw Background Color
        # Optical (RBY) or RGB opposites

        if(opticalOpposites) :
            if(arg == "RED") : bgColor = tuple(int(a*brightness) for a in ((255,0,0)))
            if(arg == "GREEN") : bgColor = tuple(int(a*brightness) for a in ((0,255,0)))
            if(arg == "BLUE") : bgColor = tuple(int(a*brightness) for a in ((0,0,255)))
            if(arg == "YELLOW") : bgColor = tuple(int(a*brightness) for a in ((255,255,0)))
            if(arg == "ORANGE") : bgColor = tuple(int(a*brightness) for a in ((255,125,0)))
            if(arg == "VIOLET") : bgColor = tuple(int(a*brightness) for a in ((200,0,255)))
        else:
             bgColor = colorutils.colorCompliment(clr, brightness)

        
        count  = start  =  0

        if(direction == "Top" or direction == "Bottom") :
            #config.image = config.Image.new("RGBA", (dims[1], dims[0]*2))
            vPadding = 42
            config.image = PIL.Image.new("RGBA", (dims[1],dims[0]+vPadding))
            config.draw  = ImageDraw.Draw(config.image)
            config.id = config.image.im.id
            bgColorV = (0,0,0)
            config.draw.rectangle((0,0,config.image.size[1], dims[0] + vPadding), fill=bgColorV)

            chars = list(arg)
            end = config.image.size[1]+3
            offset = int(random.uniform(1,config.screenWidth-20))

            # Generate vertical text
            for letter in chars :
                    # rough estimate to create vertical text
                    xD = 2
                    # "kerning ... hahhaha ;) "
                    if (letter == "I") : xD = 8
                    config.draw.text((xD, count * 28),letter,clr,font=font)
                    count += 1
            start = -end
            end = end - int(random.random() * config.screenHeight)

            # Scroll vertical text UP
            for n in range(start,end, int(stroopSteps)):
                    config.render(config.image, offset, -n, dims[1], dims[0]*2)
                    time.sleep(stroopSpeed)

        if(direction == "Left" or direction == "Right") :
            # Left Scroll
            config.image = PIL.Image.new("RGBA", (dims[0],dims[1]))
            config.draw  = ImageDraw.Draw(config.image)
            config.id = config.image.im.id
            config.draw.rectangle((0,0,config.image.size[0]+32, config.screenHeight), fill=bgColor)

            # Draw the text with "borders"
            config.draw.text((-1,-1),arg,(0,0,0),font=font2)
            config.draw.text((1,1),arg,(0,0,0),font=font2)
            config.draw.text((0,0),arg,clr,font=font)

            end = config.image.size[0]+32
            offset = int(random.uniform(1,config.screenWidth-20))
            end = config.screenWidth - int(random.uniform(0,config.image.size[0])) #+ config.image.size[0] 

            if(direction == "Right") :
                start = -end
                end = int(random.uniform(0,config.image.size[0]))

            
            #vOffset = -1
            vOffset = int(random.uniform(0,config.rows)) * 32

            for n in range(start, end, int(stroopSteps)):
                    if(direction == "Left") :
                            #config.matrix.SetImage(config.id, 0, -2)
                            #config.matrix.SetImage(config.id, config.screenWidth-n, -2)
                            config.render(config.image, config.screenWidth-n, vOffset, dims[0], dims[1])
                    else :
                            #config.matrix.SetImage(config.id, n, -2)
                            config.render(config.image, n, vOffset, dims[0], dims[1])
                    time.sleep(stroopSpeed)
