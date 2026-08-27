import random
from modules.configuration import bcolors, pieceLogger
from PIL import Image, ImageDraw, ImageChops

"""
# initiate
#-------------------------------------------------------
global overlayControls
overlayControls = BlanksAndDitherRemapping(config,  workConfig, "[PIECE SECTION NAME]")

# For blanks
#-------------------------------------------------------
overlayControls.altColor = config.bgBackGroundEndColor
overlayControls.targetImageRef = config.destinationImage
overlayControls.destinationImageDraw = config.destinationImageDraw

# for overlay blocks
#-------------------------------------------------------
overlayControls.overlayImage = config.overlayImage
overlayControls.overlayImageDraw = config.overlayImageDraw
overlayControls.setPanelOverlays()

# Run every cycle:
#-------------------------------------------------------
global overlayControls
if overlayControls.usingPanelOverlays :
    overlayControls.targetImageRef = config.destinationImage
if overlayControls.useBlanks :
    config.destinationImageDraw = ImageDraw.Draw(config.destinationImage)
    overlayControls.destinationImageDraw = config.destinationImageDraw
overlayControls.handleOverlayActions()



#-------------------------------------------------------
#----- for blanks_and_dither_remapping module ----------
#---------------------  blanks blocks ------------------
useBlanks = True
resetBlanksProb = .0005
numberOfDeadPixels = 3
blankColorAsColorProb = .0
sizeTarget = 200,240
colsRange = 64,128
rowsRange = 32,128
blankPolyVariation = 2

#--------------------- filterRemapping  ------------------
filterRemapping = True
filterRemappingProb = .0001
filterRemapMinHoriSize = 32
filterRemapMinVertSize = 32
filterRemapMaxHoriSize = 200
filterRemapMaxVertSize = 200
filterRemapRangeX = 200
filterRemapRangeY = 200

contractXSpeed = 20
contractYSpeed = 20
expandXSpeed = 20
expandYSpeed = 20

#----- adding panel modulation to mimic physical panel differences
usingPanelOverlays = True
panelColumns = 5
panelRows = 4
panelWidth = 64
panelHeight = 64
panelOverlayRange = 5,10
panelOverlayChangeProb = .0001
panelOverlayAmount = .11
#-------------------------------------------------------



"""


class BlanksAndDitherRemapping:
    ''' Sets up blanks (absent light sections) and dither sections that move around'''
    altColor = (0, 0, 0, 15)
    useBlanks = False
    filterRemapping = False
    usingPanelOverlays = False

    def __init__(self, configRef, workConfig, configSectionName):
        self.configRef = configRef
        self._load_filter_remapping(workConfig, configSectionName)
        self._load_blank_configs(workConfig, configSectionName)
        self._load_overlay_configs(workConfig, configSectionName)


    # ---- dither remapping ------------

    def _load_filter_remapping(self, workConfig, configSectionName):
        pieceLogger(f"blanks_and_dither_remappaing loading - done {self}", 3, True)
        self.filterRemapping = workConfig.getboolean(configSectionName, "filterRemapping", fallback=False)
        self.filterRemappingProb = float(workConfig.get(configSectionName, "filterRemappingProb", fallback=0.0))
        self.filterRemappingReappearProb = float(workConfig.get(configSectionName, "filterRemappingReappearProb", fallback=0.10))
        self.filterRemapMinHoriSize = int(workConfig.get(configSectionName, "filterRemapMinHoriSize", fallback=1))
        self.filterRemapMaxHoriSize = int(workConfig.get(configSectionName, "filterRemapMaxHoriSize", fallback=1))
        self.filterRemapMinVertSize = int(workConfig.get(configSectionName, "filterRemapMinVertSize", fallback=1))
        self.filterRemapMaxVertSize = int(workConfig.get(configSectionName, "filterRemapMaxVertSize", fallback=1))
        self.filterRemapRangeY = int(workConfig.get(configSectionName, "filterRemapRangeY", fallback=1))
        self.filterRemapRangeX = int(workConfig.get(configSectionName, "filterRemapRangeX", fallback=1))
        self.contractXSpeed = int(workConfig.get(configSectionName, "contractXSpeed", fallback=1))
        self.contractYSpeed = int(workConfig.get(configSectionName, "contractYSpeed", fallback=1))
        self.expandXSpeed = int(workConfig.get(configSectionName, "expandXSpeed", fallback=1))
        self.expandYSpeed = int(workConfig.get(configSectionName, "expandYSpeed", fallback=1))

        self.filterRemappingChangeProb = self.filterRemappingProb
        self.filterRemapContracting = 0
        self.basefilterRemappingProb = self.filterRemappingProb
        self.use_filters = self.filterRemapping


    def _expand_filter_remap(self):
        _pos = list(self.configRef.remapImageBlockSection)
        _pos[0] = max(_pos[0] - self.expandXSpeed, self.newFilterStartX)
        _pos[2] += self.expandXSpeed

        if _pos[0] <= self.newFilterStartX:
            self.filterRemappingProb = self.basefilterRemappingProb
            self.configRef.remapImageBlockSection = (_pos[0], _pos[1], _pos[2], _pos[3])
            self.configRef.remapImageBlockDestination = [_pos[0], _pos[1]]
            self.filterRemapContracting = 1
            self.filterRemappingChangeProb = self.filterRemappingProb
        else:
            self.configRef.remapImageBlockSection = (_pos[0], _pos[1], _pos[2], _pos[3])
            self.configRef.remapImageBlockDestination = [_pos[0], _pos[1]]
            self.filterRemappingChangeProb = 1.0


    def _contract_filter_remap(self):
        _pos = list(self.configRef.remapImageBlockSection)
        _pos[3] -= self.contractYSpeed

        if _pos[0] >= _pos[2] or _pos[1] >= _pos[3]:
            self.filterRemappingProb = self.basefilterRemappingProb
            self.filterRemapContracting = 0
            self.configRef.remapImageBlockSection = (_pos[2], _pos[3], _pos[2], _pos[3])
            self.configRef.remapImageBlockDestination = [_pos[0], _pos[1]]
            self.filterRemappingChangeProb = self.filterRemappingReappearProb
        else:
            self.configRef.remapImageBlockSection = tuple(_pos)
            self.configRef.remapImageBlockDestination = [_pos[0], _pos[1]]
            self.filterRemappingChangeProb = 1.0


    def remap_filter(self):
        """Remaps the filter block section."""
        self.filterRemap = True
        if self.filterRemappingProb != 1.0 and self.filterRemapContracting == 0:
            self.filterRemapContracting = 2
            self.newFilterStartX = round(random.uniform(0, self.filterRemapRangeX))
            self.newFilterStartY = round(random.uniform(0, self.filterRemapRangeY))
            self.newFilterEndX = round(random.uniform(self.filterRemapMinHoriSize, self.filterRemapMaxHoriSize))
            self.newFilterEndY = round(random.uniform(self.filterRemapMinVertSize, self.filterRemapMaxVertSize))
            self.configRef.remapImageBlockSection = (
                self.newFilterStartX + self.newFilterEndX,
                self.newFilterStartY,
                self.newFilterStartX + self.newFilterEndX,
                self.newFilterStartY + self.newFilterEndY,
            )

        if self.filterRemapContracting == 1:
            self._contract_filter_remap()

        if self.filterRemapContracting == 2:
            self._expand_filter_remap()

    # ---- blanks ------------

    def reset_poly_blanks(self):
        self.blanks_list = []
        self.blanks_numberOfDeadPixels = random.randint(1, self.blanks_maxNumberOfDeadPixels)

        if random.random() < self.blankColorAsColorProb:
            self.blankColor = self.altColor
        else:
            self.blankColor = self.blankColorBase

        for _ in range(self.blanks_numberOfDeadPixels):
            width1 = random.randint(self.blanks_colsRange[0], self.blanks_colsRange[1])
            height1 = random.randint(self.blanks_rowsRange[0], self.blanks_rowsRange[1])
            width2 = width1 + random.randint(-self.blankPolyVariation, self.blankPolyVariation)

            x0 = random.randint(0, self.blanks_sizeTarget[0])
            y0 = random.randint(0, self.blanks_sizeTarget[1])
            x1 = x0 + width1
            y1 = y0 + random.randint(-self.blankPolyVariation, self.blankPolyVariation)
            x2 = x1 + random.randint(-self.blankPolyVariation, self.blankPolyVariation)
            y2 = y1 + height1
            x3 = x2 - width2
            y3 = y2 + random.randint(-self.blankPolyVariation, self.blankPolyVariation)

            _poly = ((x0, y0), (x1, y1), (x2, y2), (x3, y3), (x0, y0))
            self.blanks_list.append(_poly)


    def draw_poly_blanks(self, draw_ref=None):
        _draw = draw_ref or self.destinationImageDraw

        for p in range(self.blanks_numberOfDeadPixels):
            _poly = self.blanks_list[p]
            _draw.polygon(_poly, fill=self.blankColor)


    def _load_blank_configs(self, workConfig, configSectionName):
        self.useBlanks = workConfig.getboolean(configSectionName, "useBlanks", fallback=False)
        self.resetBlanksProb = float(workConfig.get(configSectionName, "resetBlanksProb", fallback="0.001"))
        self.blankColorAsColorProb = float(workConfig.get(configSectionName, "blankColorAsColorProb", fallback="0.5"))
        self.blanks_maxNumberOfDeadPixels = int(workConfig.get(configSectionName, "numberOfDeadPixels", fallback="1"))
        self.blanks_probabilityOfBlockBlanks = 0.0
        self.blanks_sizeTarget = [int(x) for x in workConfig.get(configSectionName, "sizeTarget", fallback="128,128").split(",")]
        self.blanks_colsRange = [int(x) for x in workConfig.get(configSectionName, "colsRange", fallback="32,256").split(",")]
        self.blanks_rowsRange = [int(x) for x in workConfig.get(configSectionName, "rowsRange", fallback="32,256").split(",")]
        self.blankPolyVariation = int(workConfig.get(configSectionName, "blankPolyVariation", fallback="10"))
        # self.destinationImageDraw = destinationImageDraw
        self.blankColorBase = (0, 0, 0, 15)
        self.blankColor = (0, 0, 0, 15)
        self.reset_poly_blanks()

    # ----- panel based overlays ---------

    # adding panel modulation to mimic physical panel differences
    def _load_overlay_configs(self, workConfig, configSectionName):
        self.usingPanelOverlays = workConfig.getboolean(configSectionName, "usingPanelOverlays", fallback=False)
        self.panelWidth = int(workConfig.get(configSectionName, "panelWidth", fallback=64))
        self.panelHeight = int(workConfig.get(configSectionName, "panelHeight", fallback=32))
        self.panelColumns = int(workConfig.get(configSectionName, "panelColumns", fallback=10))
        self.panelRows = int(workConfig.get(configSectionName, "panelRows", fallback=10))
        self.panelOverlayChangeProb = float(workConfig.get(configSectionName, "panelOverlayChangeProb", fallback=0.0003))
        self.panelOverlayAmount = float(workConfig.get(configSectionName, "panelOverlayAmount", fallback=0.1) )
        self.panelOverlayRange = workConfig.get(configSectionName, "panelOverlayRange", fallback="1,30")
        self.panelOverlayRange = [int(x) for x in self.panelOverlayRange.split(",")]


    def setPanelOverlays(self):
        if not self.usingPanelOverlays:
            return

        self.panelOverLayList = []
        self.fullpanelOverLayList = []
        self.overlayImageDraw.rectangle((0, 0, self.configRef.canvasWidth, self.configRef.canvasHeight), fill=(0, 0, 0, 0))

        _totalPanels = self.panelRows * self.panelColumns
        _numPanels = random.randint(self.panelOverlayRange[0], min(_totalPanels, self.panelOverlayRange[1]))


        # create an array of panel spots then joggle it
        for c in range(0, self.panelColumns):
            for r in range(0, self.panelRows):
                self.fullpanelOverLayList.append([c, r])

        random.shuffle(self.fullpanelOverLayList)

        # self.overlayImage = Image.new("RGBA", (self.configRef.canvasWidth, self.configRef.canvasHeight))
        # self.overlayImageDraw = ImageDraw.Draw(self.overlayImage)

        for i in range(_numPanels):
            self.panelOverLayList.append(self.fullpanelOverLayList[i])

        # pieceLogger(f"{self.panelOverLayList}   {_numPanels}")


    def drawPanelVariations(self):
        if not self.usingPanelOverlays:
            return

        for p in self.panelOverLayList:
            x0 = p[0] * self.panelWidth
            y0 = p[1] * self.panelHeight
            x1 = x0 + self.panelWidth
            y1 = y0 + self.panelHeight
            self.overlayImageDraw.rectangle((x0, y0, x1, y1), fill=(255, 0, 0, 200))

        tempImage = ImageChops.add(self.targetImageRef, self.overlayImage, round(100 * self.panelOverlayAmount))
        self.targetImageRef.paste(tempImage, (0, 0), tempImage)
        # self.targetImageRef.paste(self.overlayImage, (0, 0), self.overlayImage)

    # ----- per cycle---------

    def handleOverlayActions(self):
        """Handles filter remapping if enabled."""

        # pieceLogger("---------")
        # pieceLogger(f"self.filterRemappingChangeProb: {self.filterRemappingChangeProb} self.use_filters: {self.use_filters} self.filterRemapping:{self.filterRemapping}")
        # pieceLogger("---------")
        # pieceLogger(f"self.resetBlanksProb: {self.resetBlanksProb} self.useBlanks: {self.useBlanks} ")
        # pieceLogger("---------")
        # pieceLogger(f"self.panelOverlayChangeProb: {self.panelOverlayChangeProb} self.usingPanelOverlays: {self.usingPanelOverlays} ")
        # pieceLogger("---------")


        if random.random() < self.filterRemappingChangeProb and (self.use_filters and self.filterRemapping):
            self.remap_filter()

        if random.random() < self.resetBlanksProb and self.useBlanks:
            self.reset_poly_blanks()

        if self.useBlanks:
            self.draw_poly_blanks()

        if random.random() < self.panelOverlayChangeProb and self.usingPanelOverlays:
            self.setPanelOverlays()

        if self.usingPanelOverlays:
            self.drawPanelVariations()
