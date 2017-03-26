#colorutils
import random
import math
import sys
from PIL import ImageChops, ImageOps
import operator

colorWheel = ["RED","VERMILLION","ORANGE","AMBER","YELLOW","CHARTREUSE","GREEN","TEAL","BLUE","VIOLET","PURPLE","MAGENTA"]
wheel = [(255,2,2),(253,83,8),(255,153,1),(250,188,2),(255,255,0),(0,125,0),(146,206,0),(0,255,255),(0,0,255),(65,0,165),(135,0,175),(167,25,75)]

#rgbColorWheel = ["RED","GREEN","BLUE","YELLOW","MAGENTA","CYAN"]
#rgbWheel = [(255,0,0),(0,255,0),(0,0,255),(255,255,0),(255,0,255),(0,255,255)]

rgbColorWheel = ["RED","YELLOW","GREEN","CYAN","BLUE","MAGENTA"]
rgbWheel = [(255,0,0),(255,0,0),(255,255,0),(0,255,0),(0,255,255),(0,0,255),(255,0,255)]

sunset = dict(drk1=(57,36,25),drk2=(124,77,56),drk3=(153,95,56),mid1=(177,177,78),mid2=(173,104,51),yellow=(218,172,71),ltyellow=(246,232,171),ltorange=(221,144,82),warmwht=(255,255,238) )
sky = dict(coolblue=(254,254,248),ltblue=(190,200,202),grayblue=(182,186,182))
#sorted_sunset = {k: (sum(v)/3) for k, v in sunset.iteritems()}
sorted_sunset = sorted({k: (sum(v)/3) for k, v in sunset.iteritems()}.items(), key=operator.itemgetter(1))

brightness = 1



def getSunsetColors(brtns=1) :
	global brightness, sunset, sorted_sunset
	if(brtns == 1) : brtns = brightness
	indx = int(random.uniform(0,len(sunset)))
	vals = sunset.values()
	clr = vals[indx]
	r = int(clr[0] * brtns)
	g = int(clr[1] * brtns)
	b = int(clr[2] * brtns)
	return (r,g,b)


def getRandomRGB(brtns=1) :
	global brightness, rgbColorWheel, rgbWheel
	if(brtns == 1) : brtns = brightness
	indx = int(random.uniform(0,len(rgbWheel)))
	clr = rgbWheel[indx]
	r = int(clr[0] * brtns)
	g = int(clr[1] * brtns)
	b = int(clr[2] * brtns)
	return (r,g,b)

def getRandomColorWheel(brtns=1) :
	global brightness, colorWheel, wheel
	if(brtns == 1) : brtns = brightness
	indx = int(random.uniform(0,len(colorWheel)))
	clr = wheel[indx]
	r = int(clr[0] * brtns)
	g = int(clr[1] * brtns)
	b = int(clr[2] * brtns)
	return (r,g,b) 

def randomColor(brtns=1) :
	global brightness
	if(brtns == 1) : brtns = brightness
	r = int((random.uniform(0,255)) * brtns)
	g = int((random.uniform(0,255)) * brtns)
	b = int((random.uniform(0,255)) * brtns)
	return (r,g,b) 

def randomBaseColor(brtns=1) :
	global brightness
	if(brtns == 1) : brtns = brightness
	b = int((random.uniform(0,255)) * brtns)
	r = int((random.uniform(0,100)) * brtns)
	g = int((random.uniform(0,100)) * brtns)
	return (r,g,b) 

def colorCompliment((r,g,b), brtns=1) :
	global brightness
	if(brtns == 1) : brtns = brightness
	minRGB = min(r,min(g,b))
	maxRGB = max(r,max(g,b))
	minmax = minRGB + maxRGB
	r = int((minmax - r) * brtns)
	g = int((minmax - g) * brtns)
	b = int((minmax - b) * brtns)
	return (r,g,b)    

def randomGray(brtns=1) :
	global brightness
	if(brtns == 1) : brtns = brightness
	grey = int((random.uniform(0,255)) * brtns)
	r = grey
	g = grey
	b = grey
	return (r,g,b)     

# Find the closest point 
def closestRBYfromRGB((r,g,b)) :
	global brightness, wheel
	# d = sqrt( x2-x1 ^ 2 ....)
	dMax = 0
	dArray = []
	for n in range (0, len(wheel)) :
		d = int(math.sqrt( (r-wheel[n][0])**2 + (g-wheel[n][1])**2 + (b-wheel[n][2])**2 ))
		dArray.append([n,d])
	dArray = sorted(dArray, key=lambda n:n[1], reverse=False)
	return wheel[dArray[0][0]]


def HSVToRGB(h,s,v,a=255) :
	c = v * s
	huex = h / 60.0
	x = c * ( 1 - abs(huex%2 - 1))
	r1=g1=b1=0
	if huex <= 1 and huex >= 0 : (r1,g1,b1) = (c,x,0)
	if huex <= 2 and huex >= 1 : (r1,g1,b1) = (x,c,0) 
	if huex <= 3 and huex >= 2 : (r1,g1,b1) = (0,c,x) 
	if huex <= 4 and huex >= 3 : (r1,g1,b1) = (0,x,c) 
	if huex <= 5 and huex >= 4 : (r1,g1,b1) = (x,0,c) 
	if huex <= 6 and huex >= 5 : (r1,g1,b1) = (c,0,x) 
	m = v - c
	rgb  = [r1 + m, g1 + m, b1 + m, a]

	rgbCol = tuple(int(round(i * 255)) for i in rgb)
	return rgbCol

def HSLToRGB(h,s,l,a=255) :
	c = s * (1- abs(2*l -1))
	huex = h / 60.0
	x = c * ( 1 - abs(huex%2 - 1))
	r1=g1=b1=0
	if huex <= 1 and huex >= 0 : r1,g1,b1 = c,x,0
	if huex <= 2 and huex >= 1 : r1,g1,b1 = x,c,0
	if huex <= 3 and huex >= 2 : r1,g1,b1 = 0,c,x
	if huex <= 4 and huex >= 3 : r1,g1,b1 = 0,x,c
	if huex <= 5 and huex >= 4 : r1,g1,b1 = x,0,c
	if huex <= 6 and huex >= 5 : r1,g1,b1 = c,0,x
	#m = l - (.3 * r1 + .59 * g1 + .11 * b1)
	m = l - c/2
	rgb  = [r1 + m, g1 + m, b1 + m, a]
	rgbCol = tuple(int(round(i * 255)) for i in rgb)
	return rgbCol


def subtractiveColors(arg) :
	color = (0,0,0)
	if(arg == "RED") : color = tuple(int(a*brightness) for a in ((255,2,2)))
	if(arg == "VERMILLION") : color = tuple(int(a*brightness) for a in ((253,83,8)))
	if(arg == "ORANGE") : color = tuple(int(a*brightness) for a in ((255,153,1)))
	if(arg == "AMBER") : color = tuple(int(a*brightness) for a in ((250,188,2)))
	if(arg == "YELLOW") : color = tuple(int(a*brightness) for a in ((255,255,0)))
	if(arg == "CHARTREUSE") : color = tuple(int(a*brightness) for a in ((0,255,0)))
	if(arg == "GREEN") : color = tuple(int(a*brightness) for a in ((0,125,0)))
	if(arg == "TEAL") : color = tuple(int(a*brightness) for a in ((146,206,0)))
	if(arg == "BLUE") : color = tuple(int(a*brightness) for a in ((0,0,255)))
	if(arg == "VIOLET") : color = tuple(int(a*brightness) for a in ((65,0,165)))    
	if(arg == "PURPLE") : color = tuple(int(a*brightness) for a in ((135,0,175)))    
	if(arg == "MAGENTA") : color = tuple(int(a*brightness) for a in ((167,25,75)))    
	return color
	
def colorComplimentRBY(arg) :
	global colorWheel
	l = len(colorWheel) / 2
	indx = colorWheel.index(arg)
	oppIndx  =  indx + l 
	if(oppIndx > 11) : oppIndx -= (l*2)
	return subtractiveColors(colorWheel[oppIndx])

def changeColor(rnd = False) :
	global brightness           
	if (rnd == False) :
					if(r == 255) :
									r = 0
									g = 255
									b = 0
					else :
									g = 0
									r = 255
									b = 0
	else :
					r = int(random.uniform(0,255) * brightness)
					g = int(random.uniform(0,255) * brightness)
					b = int(random.uniform(0,255) * brightness)
