################################
# This file exists to create
# an empty configuration object
################################

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



class Config:

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

	rotation = 0

	def __init__(self):
		print("Config instance init")

