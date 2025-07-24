################################
# This file exists to create
# an empty configuration object
################################

# from sys import exception


screenWidth = 128
screenHeight = 64

tileSize = (32, 64)
rows = 2
cols = 1
imageRows = [] * rows
actualScreenWidth = tileSize[1] * cols * rows
path = "/home/pi"
useMassager = False
brightness = 1
transWiring = True

# global imageTop,imageBottom,image,config,transWiring


def configuration():
    pass


class bcolors:
    HEADER = "\033[95m"
    OKBLUE = "\033[94m"
    OKGREEN = "\033[92m"
    WARNING = "\033[93m"
    FULLFAIL = "\033[91m"
    FAIL = "\033[99m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"


# print(bcolors.WARNING + "Warning: No active frommets remain. Continue?" + bcolors.ENDC)


class Config:

    screenWidth = 128
    screenHeight = 64
    instanceNumber = 0

    tileSize = (32, 64)
    rows = 2
    cols = 1
    imageRows = [] * rows
    actualScreenWidth = tileSize[1] * cols * rows
    path = "."
    useMassager = False
    brightness = 1
    transWiring = True


    ## These are used in the filter effect filters.py
    lev = 0
    levdiff = 1
    ditherBlurRadius = 0
    ditherUnsharpMaskPercent = 30

    rotation = 0

    def __init__(self):
        print("\n---------------------------------------------------------------------------------------")
        print("** Config instance init")
  
    def debugSelf(self) :
        allArgs = self.__dict__
        print("\n---------------------------------------------------------------------------------------\n")
        for element in allArgs :
            print(f"{element}  : ({type(allArgs[element]).__name__}) {allArgs[element]}")
            print("----------")
        print("\n---------------------------------------------------------------------------------------\n")
   
        method_list = [attribute for attribute in dir(self) if callable(getattr(self, attribute)) and attribute.startswith('__') is False]
        print(method_list)
        print("\n---------------------------------------------------------------------------------------\n")
   
        # allFuncs = dir(self)
        # print(allFuncs)

    def spaceBarAction(self) :
        print("SPACE BAR PRESSED")

    
    def __getattribute__(self, name):
        return super().__getattribute__(name)
        # try:
        # except Exception as e:
        #     print(f" ** {e}")
        #     return False