from pydoc import doc
import time
import inspect
import sys

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


def pieceLogger(args=None, clr=0, showLine=False, prefixTxt=""):
    """
    0 - Fail |
    1 - FullFail |
    2 - OkGreen |
    3 - OKBLUE |
    4 - YELLOWONBLUE |
    5 - BASIC |
    6 - CYAN |

    2nd param shows lines |
    3 rd param adds a prefix text
    """

    _moduleName = ""
    _functionName = ""
    try:
        _val = sys._getframe(1)
        _moduleName = inspect.getmodule(_val).__name__
        _functionName = inspect.currentframe().f_back.f_code.co_name
        # comment:
    except Exception as e:
        print(e)
    # end try

    # parent_frame_info = inspect.stack()[1]
    # parent_frame_info2 = inspect.stack()[2]
    # mod = inspect.getmodule(parent_frame_info.frame)
    # mod2 = inspect.getmodule(parent_frame_info2.frame)

    fstr = bcolors.YELLOWONBLUE
    if clr == 6:
        fstr = bcolors.CYAN
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

    if showLine:
        print(
            f"{fstr}-------------------------------------------------------------------------------------------------------------------------------------------------{bcolors.ENDC}"
        )
    print(f"{prefixTxt}{bcolors.DARKGREY}{_moduleName}.[{bcolors.ENDC}{_functionName}{bcolors.DARKGREY}]{bcolors.ENDC} {fstr}{args}{bcolors.ENDC}")

    # if showLine:
    # print(f"{fstr}---------------------------------------------------------------------------------------{bcolors.ENDC}")
    # print("\n")
    # print(bcolors.ENDC)


class bcolors:
    # YELLOWONBLUE = "\033[1;33;4;44m"
    # 0 norm
    # 1 bold
    # 2 dim
    # 3 italics

    # ;1 bold
    # ; 4 undeline

    ENDC = "\033[0m"
    BOLD = "\033[1m"
    DARKGREY = "\033[2m"
    UNDERLINE = "\033[4m"
    DARKCYAN = "\033[36m"
    BASIC = "\033[90m"
    RED = "\033[91m"
    FULLFAIL = "\033[91m"
    OKGREEN = "\033[92m"
    GREEN = "\033[92m"
    WARNING = "\033[93m"
    YELLOW = "\033[93m"
    YELLOWONBLUE = "\033[0;94;1;43m"
    BLUE = "\033[94m"
    OKBLUE = "\033[94m"
    HEADER = "\033[95m"
    PURPLE = "\033[95m"
    CYAN = "\033[96m"
    FAIL = "\033[99m"


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

    brightness = 1.0
    minBrightness = 0

    useFilters = False
    ditherfilterbrightness = 1.0

    remapImageBlock = False
    remapImageBlockSection = [0, 0, 256, 256]
    remapImageBlockDestination = [0, 0]
    remapImageBlockSectionRotation = 0

    remapImageBlock2 = False
    remapImageBlockSection2 = [0, 0, 256, 256]
    remapImageBlockDestination2 = [0, 0]
    remapImageBlockSection2Rotation = 1

    remapImageBlock3 = False
    remapImageBlockSection3 = [0, 0, 256, 256]
    remapImageBlockDestination3 = [0, 0]
    remapImageBlockSection3Rotation = 0

    remapImageBlock4 = False
    remapImageBlockSection4 = [0, 0, 256, 256]
    remapImageBlockDestination4 = [0, 0]
    remapImageBlockSection4Rotation = 0

    remapImageBlock5 = False
    remapImageBlockSection5 = [0, 0, 256, 256]
    remapImageBlockDestination5 = [0, 0]
    remapImageBlockSection5Rotation = 0

    remapImageBlock6 = False
    remapImageBlockSection6 = [0, 0, 256, 256]
    remapImageBlockDestination6 = [0, 0]
    remapImageBlockSection6Rotation = 0

    remapImageBlock7 = False
    remapImageBlockSection7 = [0, 0, 256, 256]
    remapImageBlockDestination7 = [0, 0]
    remapImageBlockSection7Rotation = 0

    remapImageBlockShift = False
    remapImageBlockShiftSection = [0, 0, 256, 256]
    remapImageBlockShiftStableSection = [0, 0, 0, 0]
    remapImageBlockShiftDestination = [-0, 0]

    remapImageBlockShift2 = False
    remapImageBlockShiftSection2 = [0, 0, 256, 256]
    remapImageBlockShiftStableSection2 = [0, 0, 0, 0]
    remapImageBlockShiftDestination2 = [-0, 0]

    remapImageBlockShift2 = False
    remapImageBlockShiftSection3 = [0, 0, 256, 256]
    remapImageBlockShiftStableSection3 = [0, 0, 0, 0]
    remapImageBlockShiftDestination3 = [-0, 0]

    remapImageBlockShift2 = False
    remapImageBlockShiftSection3 = [0, 0, 256, 256]
    remapImageBlockShiftStableSection3 = [0, 0, 0, 0]
    remapImageBlockShiftDestination3 = [-0, 0]

    remapImageBlockShift2 = False
    remapImageBlockShiftSection4 = [0, 0, 256, 256]
    remapImageBlockShiftStableSection4 = [0, 0, 0, 0]
    remapImageBlockShiftDestination4 = [-0, 0]

    remapImageBlockShift2 = False
    remapImageBlockShiftSection5 = [0, 0, 256, 256]
    remapImageBlockShiftStableSection5 = [0, 0, 0, 0]
    remapImageBlockShiftDestination5 = [-0, 0]

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

    # Common images and drawing
    image = None
    imageDraw = None
    draw = None
    canvasImage = None
    destinationImage = None
    destinationImageDraw = None
    overlayImage = None
    overlayImageDraw = None
    underLayer = None
    underLayerDraw = None

    # Rendering controls
    renderImageFull = None
    renderDraw = None
    convertRenderImageFullToRGB = True

    redrawSpeed = 0.03
    slotRate = 0.03
    directorController = None

    def __init__(self, args=None, _silent=False):
        if not _silent:
            pieceLogger(f"** Config instance init {args}", 3, True)

    def debugSelf(self):
        allArgs = self.__dict__
        pieceLogger("---------------------------------------------------------------------------------------\n")
        for element in allArgs:
            pieceLogger(f"{element}  : ({type(allArgs[element]).__name__}) {allArgs[element]}")
        # pieceLogger("---------------------------------------------------------------------------------------\n")k

        method_list = [attribute for attribute in dir(self) if callable(getattr(self, attribute)) and attribute.startswith("__") is False]
        pieceLogger(f"{method_list}")
        pieceLogger("---------------------------------------------------------------------------------------\n")

        # allFuncs = dir(self)
        # pieceLogger(allFuncs)

    def spaceBarAction(self):
        pieceLogger(">> SPACE BAR PRESSED")

    def __getattribute__(self, name):
        return super().__getattribute__(name)
        # try:
        # except Exception as e:
        #     print(f" ** {e}")
        #     return False
