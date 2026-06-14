import random
from modules.configuration import bcolors, pieceLogger


class BlanksAndDitherRemapping:
    def __init__(self, configRef, workConfig, configSectionName, destinationImageDraw):
        self._load_filter_remapping(configRef, workConfig, configSectionName)
        self._load_blank_configs(workConfig, configSectionName, destinationImageDraw)
        self._load_overlay_configs(workConfig, configSectionName)

    def _load_config_value(self, workConfig, section, option, default, type_converter):
        try:
            if type_converter == bool:
                setattr(self, option, type_converter(workConfig.getboolean(section, option)))
            else:
                setattr(self, option, type_converter(workConfig.get(section, option)))
        except Exception as e:
            pieceLogger(f" ==> Config value not loaded: {option} ==> will be set to {default} \n  {e}", 1)
            setattr(self, option, default)

    # ---- dither remapping ------------

    def _load_filter_remapping(self, configRef, workConfig, configSectionName):
        self.configRef = configRef
        self._load_config_value(workConfig, configSectionName, "filterRemapping", False, bool)
        self._load_config_value(workConfig, configSectionName, "filterRemappingProb", 0.0, float)
        self._load_config_value(workConfig, configSectionName, "filterRemappingReappearProb", 0.10, float)
        self._load_config_value(workConfig, configSectionName, "filterRemapMinHoriSize", 1, int)
        self._load_config_value(workConfig, configSectionName, "filterRemapMaxHoriSize", 1, int)
        self._load_config_value(workConfig, configSectionName, "filterRemapMinVertSize", 1, int)
        self._load_config_value(workConfig, configSectionName, "filterRemapMaxVertSize", 1, int)
        self._load_config_value(workConfig, configSectionName, "filterRemapRangeY", 1, int)
        self._load_config_value(workConfig, configSectionName, "filterRemapRangeX", 1, int)
        self._load_config_value(workConfig, configSectionName, "contractXSpeed", 2, int)
        self._load_config_value(workConfig, configSectionName, "contractYSpeed", 2, int)
        self._load_config_value(workConfig, configSectionName, "expandXSpeed", 2, int)
        self._load_config_value(workConfig, configSectionName, "expandYSpeed", 2, int)

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

    def _load_blank_configs(self, workConfig, configSectionName, destinationImageDraw):
        self.useBlanks = workConfig.getboolean(configSectionName, "useBlanks", fallback=False)
        self.resetBlanksProb = float(workConfig.get(configSectionName, "resetBlanksProb", fallback="0.001"))
        self.blankColorAsColorProb = float(workConfig.get(configSectionName, "blankColorAsColorProb", fallback="0.5"))
        self.blanks_maxNumberOfDeadPixels = int(workConfig.get(configSectionName, "numberOfDeadPixels", fallback="1"))
        self.blanks_probabilityOfBlockBlanks = 0.0
        self.blanks_sizeTarget = [int(x) for x in workConfig.get(configSectionName, "sizeTarget", fallback="128,128").split(",")]
        self.blanks_colsRange = [int(x) for x in workConfig.get(configSectionName, "colsRange", fallback="32,256").split(",")]
        self.blanks_rowsRange = [int(x) for x in workConfig.get(configSectionName, "rowsRange", fallback="32,256").split(",")]
        self.blankPolyVariation = int(workConfig.get(configSectionName, "blankPolyVariation", fallback="10"))
        self.destinationImageDraw = destinationImageDraw
        self.blankColor = (0, 0, 0, 15)

        self.reset_poly_blanks()

    def _load_overlay_configs(self, workConfig, configSectionName):
        self.panelWidth = int(workConfig.get(configSectionName, "panelWidth", fallback="64"))
        self.panelHeight = int(workConfig.get(configSectionName, "panelHeight", fallback="32"))
        self.panelColumns = int(workConfig.get(configSectionName, "panelColumns", fallback="10"))
        self.panelRows = int(workConfig.get(configSectionName, "panelRows", fallback="10"))
        self.panelOverlayRange = [int(x) for x in workConfig.get(configSectionName, "panelOverlayRange", fallback="1,30").split(",")]
        self.panelOverlayChangeProb = float(workConfig.get(configSectionName, "panelOverlayChangeProb", fallback=".0003"))
        self.panelOverlayAmount = float(workConfig.get(configSectionName, "panelOverlayAmount", fallback=".1"))
        self.usingPanelOverlays = self.panelColumns != 0 and self.panelRows != 0

    def handleOverlayActions(self):
        """Handles filter remapping if enabled."""
        if random.random() < self.filterRemappingChangeProb and (self.use_filters and self.filterRemapping):
            self.remap_filter()

        if random.random() < self.resetBlanksProb and self.useBlanks:
            self.reset_poly_blanks()

        if self.useBlanks :
            self.draw_poly_blanks()
