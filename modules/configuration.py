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

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

#print(bcolors.WARNING + "Warning: No active frommets remain. Continue?" + bcolors.ENDC)

class Config:

	screenWidth =  128
	screenHeight = 64
	instanceNumber = 0

	tileSize = (32,64)
	rows = 2
	cols = 1
	imageRows = [] * rows
	actualScreenWidth = tileSize[1]*cols*rows
	path = "."
	useMassager = False
	brightness = 1
	transWiring = True

	rotation = 0

	def __init__(self):
		print("** Config instance init")

