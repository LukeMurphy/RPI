################################
# This file exists to create
# an empty configuration object
################################

import time
import random
import math
import sys
from PIL import ImageChops, ImageOps

screenWidth =  128
screenHeight = 64

tileSize = (32,64)
rows = 2
cols = 1
imageRows = [] * rows
actualScreenWidth = tileSize[1]*cols*rows
path = "/home/pi"
useMassager = False
brightness = 1
transWiring = True

#global imageTop,imageBottom,image,config,transWiring

def configuration() :
	pass

