import time

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


def pieceLogger(args, clr=0, showLine=False, prefixTxt=""):
    fstr = bcolors.YELLOWONBLUE
    if clr == 5:
        fstr = bcolors.BASIC
    if clr == 4:
        fstr = bcolors.YELLOWONBLUE
    if clr == 3:
        fstr = bcolors.OKBLUE
    if clr == 2:
        fstr = bcolors.OKGREEN
    if clr == 1:
        fstr = bcolors.FULLFAIL
    if clr == 0:
        fstr = bcolors.WARNING

    if showLine :
        print(f"\n{fstr}.......................................................................................{bcolors.ENDC}")
    print(f"{fstr}{prefixTxt}{args}          {bcolors.ENDC}")
    if showLine :
        print(f"{fstr}.......................................................................................{bcolors.ENDC}")
    # print("\n")
    # print(bcolors.ENDC)


class bcolors:
    HEADER = "\033[95m"
    OKBLUE = "\033[94m"
    # YELLOWONBLUE = "\033[1;33;4;44m"
    # 0 norm
    # 1 bold
    # 2 dim
    # 3 italics

    # ;1 bold
    # ; 4 undeline

    YELLOWONBLUE = "\033[0;94;1;43m"
    BASIC = "\033[90m"
    OKGREEN = "\033[92m"
    WARNING = "\033[93m"
    FULLFAIL = "\033[91m"
    FAIL = "\033[99m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"
    ENDC = "\033[0m"


# print(bcolors.WARNING + "Warning: No active frommets remain. Continue?" + bcolors.ENDC)


class ArtWorkConfig:

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
    isRPI = False

    rotation = 0
    fullRotation = True
    rotationTrailing = False

    checkForConfigChanges = True
    doFullReloadOnChange = True

    tileSizeHeight = 32
    tileSizeWidth = 64
    matrixTiles = 48
    rows = 7
    cols = 4

    # ---  Also determines the window geometry
    screenWidth = 256
    screenHeight = 256

    # ---  preparing for rotation
    windowWidth = 256
    windowHeight = 256

    canvasWidth = 256
    canvasHeight = 256

    canvasOffsetX = 3
    canvasOffsetY = 3

    # Window Offset
    windowXOffset = 50
    windowYOffset = 374

    brightness =  1.0
    minBrightness = 0

    useFilters = False
    ditherfilterbrightness = 1.0

    remapImageBlock = False
    remapImageBlockSection = [0,0,256,256]
    remapImageBlockDestination = [0,0]
    remapImageBlockSectionRotation = 0

    remapImageBlock2 = False
    remapImageBlockSection2 = [0,220,160,256]
    remapImageBlockDestination2 = [1,220]
    remapImageBlockSection2Rotation = 1

    remapImageBlock3 = False
    remapImageBlockSection3 = [224,0,256,384]
    remapImageBlockDestination3 = [0,0]
    remapImageBlockSection3Rotation = 0

    remapImageBlock4 = False
    remapImageBlockSection4 = [224,0,256,384]
    remapImageBlockDestination4 = [0,0]
    remapImageBlockSection4Rotation = 0

    remapImageBlock5 = False
    remapImageBlockSection5 = [224,0,256,384]
    remapImageBlockDestination5 = [0,0]
    remapImageBlockSection5Rotation = 0


    startTime = time.time()
    currentTime = time.time()
    doingReload = False
    brightnessOverride = None
    standAlone = True
    isRunning = True
    useDrawingPoints = False
    reloadConfig = False
    checkForConfigChanges = False
    noWindowChrome = False



    ## These are used in the filter effect filters.py
    lev = 0
    levdiff = 1
    ditherBlurRadius = 0
    ditherUnsharpMaskPercent = 30

    rotation = 0

    def __init__(self, args=None, _silent=False):
        if not _silent:
            print("\n[configuration.py: ArtWorkConfig] ---------------------------------------------------------------------------------------")
            print(f"[configuration.py: ArtWorkConfig] ** Config instance init {args}")
            print("[configuration.py: ArtWorkConfig] ---------------------------------------------------------------------------------------")

    def debugSelf(self):
        allArgs = self.__dict__
        print("\n[configuration.py: ArtWorkConfig] ---------------------------------------------------------------------------------------\n")
        for element in allArgs:
            print(f"[configuration.py: ArtWorkConfig] {element}  : ({type(allArgs[element]).__name__}) {allArgs[element]}")
        print("[configuration.py: ArtWorkConfig] ---------------------------------------------------------------------------------------\n")

        method_list = [attribute for attribute in dir(self) if callable(getattr(self, attribute)) and attribute.startswith("__") is False]
        print(f"[configuration.py: ArtWorkConfig] {method_list}")
        print("[configuration.py: ArtWorkConfig] ---------------------------------------------------------------------------------------\n")

        # allFuncs = dir(self)
        # print(allFuncs)

    def spaceBarAction(self):
        print("[configuration.py: ArtWorkConfig] >> SPACE BAR PRESSED")

    def __getattribute__(self, name):
        return super().__getattribute__(name)
        # try:
        # except Exception as e:
        #     print(f" ** {e}")
        #     return False
