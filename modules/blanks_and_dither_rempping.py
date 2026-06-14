import random
from modules.configuration import bcolors, pieceLogger


def loadConfigValue(obj, workConfig, section, option, default, type_converter):
    try:
        if type_converter == bool:
            setattr(obj, option, type_converter(workConfig.getboolean(section, option)))
        else:
            setattr(obj, option, type_converter(workConfig.get(section, option)))
    except Exception as e:
        pieceLogger(f" ==> Config value not loaded: {option} ==> will be set to {default} \n  {e}", 1)
        setattr(obj, option, default)


# ---- dither remapping ------------


def loadFilterRemapping(config, workConfig, configSectionName):
    loadConfigValue(config, workConfig, configSectionName, "filterRemapping", False, bool)
    loadConfigValue(config, workConfig, configSectionName, "filterRemappingProb", 0.0, float)
    loadConfigValue(config, workConfig, configSectionName, "filterRemappingReappearProb", 0.10, float)
    loadConfigValue(config, workConfig, configSectionName, "filterRemapMinHoriSize", 1, int)
    loadConfigValue(config, workConfig, configSectionName, "filterRemapMaxHoriSize", 1, int)
    loadConfigValue(config, workConfig, configSectionName, "filterRemapMinVertSize", 1, int)
    loadConfigValue(config, workConfig, configSectionName, "filterRemapMaxVertSize", 1, int)
    loadConfigValue(config, workConfig, configSectionName, "filterRemapRangeY", 1, int)
    loadConfigValue(config, workConfig, configSectionName, "filterRemapRangeX", 1, int)
    loadConfigValue(config, workConfig, configSectionName, "contractXSpeed", 2, int)
    loadConfigValue(config, workConfig, configSectionName, "contractYSpeed", 2, int)
    loadConfigValue(config, workConfig, configSectionName, "expandXSpeed", 2, int)
    loadConfigValue(config, workConfig, configSectionName, "expandYSpeed", 2, int)

    config.filterRemappingChangeProb = config.filterRemappingProb
    config.filterRemapContracting = 0
    config.basefilterRemappingProb = config.filterRemappingProb


def expandFilterRemap(config):

    _pos = list(config.remapImageBlockSection)
    # pieceLogger(_pos)
    _pos[0] = max(_pos[0] - config.expandXSpeed, config.newFilterStartX)
    _pos[2] += config.expandXSpeed
    # _pos[1] -= 2
    # _pos[3] += 2
    # or _pos[1] <= (config.newFilterStartY)
    if _pos[0] <= (config.newFilterStartX):
        config.filterRemappingProb = config.basefilterRemappingProb
        config.remapImageBlockSection = (_pos[0], _pos[1], _pos[2], _pos[3])
        config.remapImageBlockDestination = [_pos[0], _pos[1]]
        config.filterRemapContracting = 1
        # pieceLogger(f"Expanidng done {config.newFilterStartX}")
        config.filterRemappingChangeProb = config.filterRemappingProb
    else:
        config.remapImageBlockSection = (_pos[0], _pos[1], _pos[2], _pos[3])
        config.remapImageBlockDestination = [_pos[0], _pos[1]]
        config.filterRemappingChangeProb = 1.0


def contractFilterRemap(config):
    _pos = list(config.remapImageBlockSection)
    # pieceLogger(_pos)
    # _pos[0] += config.contractXSpeed
    # _pos[2] -= config.contractXSpeed
    # _pos[1] += config.contractYSpeed
    _pos[3] -= config.contractYSpeed

    if _pos[0] >= _pos[2] or _pos[1] >= _pos[3]:
        config.filterRemappingProb = config.basefilterRemappingProb
        config.filterRemapContracting = 0
        config.remapImageBlockSection = (_pos[2], _pos[3], _pos[2], _pos[3])
        config.remapImageBlockDestination = [_pos[0], _pos[1]]
        # pieceLogger(f"contracting done {_pos} {config.filterRemapContracting} {config.filterRemappingProb}")
        config.filterRemappingChangeProb = config.filterRemappingReappearProb
    else:
        # pieceLogger(_pos)
        config.remapImageBlockSection = tuple(_pos)
        config.remapImageBlockDestination = [_pos[0], _pos[1]]
        config.filterRemappingChangeProb = 1.0


def remapFilter(config):
    """Remaps the filter block section."""
    config.filterRemap = True
    if config.filterRemappingProb != 1.0 and config.filterRemapContracting == 0:
        config.filterRemapContracting = 2
        config.newFilterStartX = round(random.uniform(0, config.filterRemapRangeX))
        config.newFilterStartY = round(random.uniform(0, config.filterRemapRangeY))
        config.newFilterEndX = round(random.uniform(config.filterRemapMinHoriSize, config.filterRemapMaxHoriSize))
        config.newFilterEndY = round(random.uniform(config.filterRemapMinVertSize, config.filterRemapMaxVertSize))
        config.remapImageBlockSection = (
            config.newFilterStartX + config.newFilterEndX,
            config.newFilterStartY,
            config.newFilterStartX + config.newFilterEndX,
            config.newFilterStartY + config.newFilterEndY,
        )
        # pieceLogger("Resetting to expand")
        # pieceLogger(f"{config.newFilterStartX} {config.newFilterStartY} {config.newFilterEndX + config.newFilterStartX} {config.newFilterEndY}")

    if config.filterRemapContracting == 1:
        # pieceLogger("Resetting to contract")
        contractFilterRemap(config)

    if config.filterRemapContracting == 2:
        expandFilterRemap(config)


# ---- blanks            ------------


def resetPolyBlanks(config):
    config.blanks_list = []
    config.blanks_numberOfDeadPixels = random.randint(1, config.blanks_maxNumberOfDeadPixels)

    for _ in range(config.blanks_numberOfDeadPixels):
        width1 = random.randint(config.blanks_colsRange[0], config.blanks_colsRange[1])
        height1 = random.randint(config.blanks_rowsRange[0], config.blanks_rowsRange[1])
        width2 = width1 + random.randint(-config.blankPolyVariation, config.blankPolyVariation)
        height2 = height1 + random.randint(-config.blankPolyVariation, config.blankPolyVariation)

        x0 = random.randint(0, config.blanks_sizeTarget[0])
        y0 = random.randint(0, config.blanks_sizeTarget[1])
        x1 = x0 + width1
        y1 = y0 + random.randint(-config.blankPolyVariation, config.blankPolyVariation)
        x2 = x1 + random.randint(-config.blankPolyVariation, config.blankPolyVariation)
        y2 = y1 + height1
        x3 = x2 - width2
        y3 = y2 + random.randint(-config.blankPolyVariation, config.blankPolyVariation)

        _poly = ((x0, y0), (x1, y1), (x2, y2), (x3, y3), (x0, y0))

        config.blanks_list.append(_poly)


def drawPolyBlanks(config, _drawRef):
    for p in range(config.blanks_numberOfDeadPixels):
        _poly = config.blanks_list[p]
        _drawRef.polygon(_poly, fill=config.blankColor)


def loadBlankConfigs(config, workConfig, configSectionName, destinationImageDraw):
    config.resetBlanksProb = config.bg_dropHueMax = float(workConfig.get(configSectionName, "resetBlanksProb", fallback="0.001"))
    config.blankColorAsColorProb = float(workConfig.get(configSectionName, "blankColorAsColorProb", fallback="0.5"))
    config.blanks_maxNumberOfDeadPixels = int(workConfig.get(configSectionName, "numberOfDeadPixels", fallback="1"))
    config.blanks_probabilityOfBlockBlanks = 0.0
    config.blanks_sizeTarget = [int(x) for x in workConfig.get(configSectionName, "sizeTarget", fallback="128,128").split(",")]
    config.blanks_colsRange = [int(x) for x in workConfig.get(configSectionName, "colsRange", fallback="32,256").split(",")]
    config.blanks_rowsRange = [int(x) for x in workConfig.get(configSectionName, "rowsRange", fallback="32,256").split(",")]
    config.blankPolyVariation = int(workConfig.get(configSectionName, "blankPolyVariation", fallback="10"))
    config.destinationImageDraw = destinationImageDraw
    config.blankColor = (0,0,0,15)

    resetPolyBlanks(config)

    # badpixels.numberOfDeadPixels = int(workConfig.get(configSectionName, "numberOfDeadPixels", fallback="1"))
    # badpixels.probabilityOfBlockBlanks = 0.0
    # badpixels.sizeTarget = [int(x) for x in workConfig.get(configSectionName, "sizeTarget", fallback=f"{config.drawingWidth},{config.drawingHeight}").split(",")]
    # badpixels.colsRange = [int(x) for x in workConfig.get(configSectionName, "colsRange", fallback="32,256").split(",")]
    # badpixels.rowsRange = [int(x) for x in workConfig.get(configSectionName, "rowsRange", fallback="32,256").split(",")]


def loadOverlayConfigs(config, workConfig, configSectionName):
    config.panelWidth = int(workConfig.get(configSectionName, "panelWidth", fallback="64"))
    config.panelHeight = int(workConfig.get(configSectionName, "panelHeight", fallback="32"))
    config.panelColumns = int(workConfig.get(configSectionName, "panelColumns", fallback="10"))
    config.panelRows = int(workConfig.get(configSectionName, "panelRows", fallback="10"))
    config.panelOverlayRange = [int(x) for x in workConfig.get(configSectionName, "panelOverlayRange", fallback="1,30").split(",")]
    config.panelOverlayChangeProb = float(workConfig.get(configSectionName, "panelOverlayChangeProb", fallback=".0003"))
    config.panelOverlayAmount = float(workConfig.get(configSectionName, "panelOverlayAmount", fallback=".1"))
    config.usingPanelOverlays = True
    if config.panelColumns == 0 or config.panelRows == 0:
        config.usingPanelOverlays = False


def handleOverlayActions(config):
    """Handles filter remapping if enabled."""
    # print(f"config.useFilters {config.useFilters}  config.filterRemapping {config.filterRemapping} config.filterRemappingProb {config.filterRemappingProb}")
    if random.random() < config.filterRemappingChangeProb and (config.useFilters and config.filterRemapping):
        remapFilter(config)

    if random.random() < config.resetBlanksProb:
        # badpixels.setBlanksOnScreen(config)
        resetPolyBlanks(config)

    drawPolyBlanks(config, config.destinationImageDraw)

    # if random.random() < config.panelOverlayChangeProb:
    #     setPanelOverlays()
# drawPolyBlanks(config.destinationImageDraw)
# handleFilterRemapping()
