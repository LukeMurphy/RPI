import datetime
import gc
import os
import random
import time

import numpy
import pygame
from PIL import Image, ImageDraw, ImageEnhance, ImageFilter

from modules.configuration import pieceLogger
from modules.filters import colorSeparator, ditherFilter, pixelSort

# Pygame equivalent of modules/rendering/render.py -- same PIL-based effects
# pipeline, but windowing/display goes through pygame instead of tkinter.
#
# The original tkinter render loop is (accidentally) single-threaded: it
# calls work.runWork() synchronously from a root.after() callback, and it is
# config.cnvs.update() -- called every frame from inside that call stack --
# that actually pumps Tk's event loop. This module mirrors that structure so
# all pygame calls happen on the same (main) thread, which pygame requires.

# ----------------------------------------- #

global screen
global work, config
memoryUsage = 0
debug = False
counter = 0

canvasOffsetX = 4
canvasOffsetY = 7
buff = 8


# ----------------------------------------- #


def setUp(config):
    pieceLogger(" >> ** Setting up the pygame window and rendering\n", 3)
    gc.enable()

    global screen

    config.imageArrayForSaving = []
    config.frameCount = 0
    config.frameCountLimit = 2

    windowOffset = [config.windowXOffset, config.windowYOffset]
    w = config.windowWidth + buff
    h = config.windowHeight + buff
    x, y = windowOffset

    config.screenPositionX = x
    config.screenPositionY = y

    # pygame/SDL has no direct equivalent of Tk's geometry() call -- window
    # position has to be requested before the display is created.
    os.environ["SDL_VIDEO_WINDOW_POS"] = f"{x},{y}"

    pygame.init()
    # pygame.display.set_caption(getattr(config, "work", "player"))
    pygame.display.set_caption((f"PyG - {config.work}: {config.fileNameRaw}"))
    pygame.mouse.set_visible(False)

    flags = pygame.NOFRAME if config.noWindowChrome else 0
    screen = pygame.display.set_mode((w, h), flags)
    screen.fill((0, 0, 0))
    pygame.display.flip()

    config.screen = screen
    config.torqueAngle = 0
    config.clock = pygame.time.Clock()

    startWork()


# ----------------------------------------- #


def on_closing():
    return True


# ----------------------------------------- #


def writeImage(baseName, renderImage):
    fn = f"{baseName}.png"
    renderImage.save(fn)


def startWork(*args):
    global counter
    try:
        work.runWork()
    except Exception as e:
        pieceLogger(str(e))


# ----------------------------------------- #


def _handleEvents():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            config.isRunning = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                config.isRunning = False
            elif event.key == pygame.K_SPACE and config.saveToFile:
                config.spaceBarAction()
                saveImageToFile()


def updateCanvas():
    global counter
    counter += 1
    if counter > 1000:
        gc.collect()
        counter = 0

    _handleEvents()

    if not config.isRunning:
        pygame.quit()
        return

    img = config.renderImageFull
    if img.mode != "RGBA":
        img = img.convert("RGBA")
    surf = pygame.image.frombuffer(img.tobytes(), img.size, "RGBA")
    screen.fill((0, 0, 0))
    screen.blit(surf, (canvasOffsetX, canvasOffsetY))
    pygame.display.flip()
    config.clock.tick(60)

    ############################################################
    ######  Check if config file has changed and reload    #####
    ############################################################

    if config.checkForConfigChanges:
        relaunchOnChange(config)


# TODO Rename this here and in `updateCanvas`
def relaunchOnChange(config):
    currentTime = time.time()
    configurationDirectory = os.path.dirname(config.fileName)

    files = [f for f in os.listdir(f"{configurationDirectory}")
             if os.path.isfile(os.path.join(f"{configurationDirectory}", f))
             ]

    f2 = os.path.getmtime(f"{config.path}pieces/{config.work}.py")

    fileHasChanged = False
    for f in files:
        fModTime = os.path.getmtime(f"{configurationDirectory}/{f}")
        _delta = currentTime - fModTime
        if _delta <= 1:
            fileHasChanged = True

    config.delta = currentTime - f2

    if config.delta <= 1 or fileHasChanged:
        if not config.reloadConfig:
            pieceLogger(f" >> ** LAST MODIFIED DELTA: {str(config.delta)} **")
            pieceLogger(f" >> ** LAST MODIFIED DELTA: {str(config.initialArgs)} **")

            if config.doFullReloadOnChange:
                os.system(config.path + "/cntrlscripts/restart_player_dev.sh" + " " + config.initialArgs + "&")
            else:
                config.doingReload = True
                config.loadFromArguments(True, config)
        config.reloadConfig = True
    else:
        config.reloadConfig = False


# ----------------------------------------- #


def _applyColorSep(xOffset=0, yOffset=0):
    _colorSep(xOffset, yOffset)


def _colorSep(xOffset=0, yOffset=0):
    _tempImage = config.renderImageFull.copy()
    _tempImage = colorSeparator(_tempImage, xOffset, yOffset, config)
    _remapImageBlockSection = (100, 50, 300, 200)
    _remapImageBlockDestination = (100, 50)
    crop = _tempImage.crop(_remapImageBlockSection)
    crop = crop.convert("RGBA")
    _f = crop.filter(ImageFilter.DETAIL)
    config.renderImageFull.paste(_f, _remapImageBlockDestination, _f)


# ----------------------------------------- #


def _applyDitherFilter(xOffset, yOffset):
    if not config.useFilters:
        return
    if config.filterRemap:
        _ditherReMapPrep(xOffset, yOffset)
    else:
        config.renderImageFull = ditherFilter(config.renderImageFull, xOffset, yOffset, config)


def _ditherReMapPrep(xOffset, yOffset):
    config.tempImage = config.renderImageFull.copy()
    config.tempImage = ditherFilter(config.tempImage, xOffset, yOffset, config)
    crop = config.tempImage.crop(config.remapImageBlockSection)
    crop = crop.convert("RGBA")
    if config.ditherFilterBrightness != 1.0:
        crop = ImageEnhance.Brightness(crop).enhance(config.ditherFilterBrightness)
    config.renderImageFull.paste(crop, config.remapImageBlockDestination, crop)


def _reMapBlock(sectionName):
    _name = "remapImageBlock"
    _num = sectionName.split(_name)[1]
    _section = config.__getattribute__(f"{_name}Section{_num}")
    _sectionDestination = config.__getattribute__(f"{_name}Destination{_num}")
    _sectionRotation = config.__getattribute__(f"{_name}Section{_num}Rotation")

    crop = config.renderImageFull.crop(_section)
    if _sectionRotation != 0:
        crop = crop.convert("RGBA")
        crop = crop.rotate(_sectionRotation, resample=Image.NEAREST, expand=1)
    crop = crop.convert("RGBA")
    config.renderImageFull.paste(crop, _sectionDestination, crop)


def _reMapBlockShift(sectionName):
    _name = sectionName
    _section = config.__getattribute__(f"{_name}Section")
    _nonsection = config.__getattribute__(f"{_name}StableSection")
    _sectionDestination = config.__getattribute__(f"{_name}Destination")

    crop = config._imageToRender.crop(_section)
    noncrop = config._imageToRender.crop(_nonsection)
    crop = crop.convert("RGBA")
    config.renderImageFull.paste(noncrop, (0, 0), noncrop)
    config.renderImageFull.paste(crop, _sectionDestination, crop)


def _doReMappingBlocks():
    if config.remapImageBlock:
        _reMapBlock("remapImageBlock")

    if config.remapImageBlock2:
        _reMapBlock("remapImageBlock2")

    if config.remapImageBlock3:
        _reMapBlock("remapImageBlock3")

    if config.remapImageBlock4:
        _reMapBlock("remapImageBlock4")

    if config.remapImageBlock5:
        _reMapBlock("remapImageBlock5")

    if config.remapImageBlock6:
        _reMapBlock("remapImageBlock6")

    if config.remapImageBlock7:
        _reMapBlock("remapImageBlock7")

    if config.remapImageBlockShift:
        _reMapBlockShift("remapImageBlockShift")
        if config.remapImageBlockShift2:
            _reMapBlockShift("remapImageBlockShift2")
        if config.remapImageBlockShift3:
            _reMapBlockShift("remapImageBlockShift3")
        if config.remapImageBlockShift4:
            _reMapBlockShift("remapImageBlockShift4")
        if config.remapImageBlockShift5:
            _reMapBlockShift("remapImageBlockShift5")
        if config.remapImageBlockShift6:
            _reMapBlockShift("remapImageBlockShift6")


def _blurringCall():
    if not config.useBlur:
        return

    config._render_crop = config.renderImageFull.crop(config.blurSection)
    config._render_destination = (config.blurXOffset, config.blurYOffset)
    config._render_crop = config._render_crop.convert("RGBA")
    config._render_crop = config._render_crop.filter(ImageFilter.GaussianBlur(radius=config.sectionBlurRadius))
    config.renderImageFull.paste(config._render_crop, config._render_destination, config._render_crop)


def _lastOverLay():
    try:
        if config.useLastOverlay:
            config.renderDrawOver.rectangle(config.lastOverlayBox, fill=config.lastOverlayFill, outline=None)
            if config.lastOverlayBlur > 0:
                config.renderImageFullOverlay = config.renderImageFullOverlay.filter(ImageFilter.GaussianBlur(radius=config.lastOverlayBlur))
            config.renderImageFull.paste(config.renderImageFullOverlay, (0, 0), config.renderImageFullOverlay)
    except Exception as e:
        pieceLogger(f"[renderpygame.py:_lastOverLay] >> {e}")


def _overallResize():
    if not config.overallResize:
        return

    iTemp = config.renderImageFull.copy()
    factor = 3
    (width, height) = (iTemp.width * factor, iTemp.height * factor)
    iTemp = iTemp.resize((width, height))
    iTemp = iTemp.filter(ImageFilter.SHARPEN)
    iTemp = iTemp.filter(ImageFilter.SHARPEN)
    config.renderImageFull.paste(iTemp, (0, 0))


def _saveToFileCall():
    if config.outputMode == "gif":
        config.frameCount += 1
        if config.frameCount >= config.frameCountLimit:
            config.imageArrayForSaving.append(config.renderImageFull)
            config.frameCount = 0

        if len(config.imageArrayForSaving) > 500:
            ts = time.time()
            st = datetime.datetime.fromtimestamp(ts).strftime("%Y-%m-%d--%H-%M-%S")
            name = f"{st}.gif"
            config.imageArrayForSaving[0].save(
                name,
                save_all=True,
                append_images=config.imageArrayForSaving[1:],
                optimize=True,
                duration=0.5,
                loop=0,
            )
            config.imageArrayForSaving = []

    if config.saveToFile:
        config.topDirector.checkTime()
        if config.topDirector.advance:
            saveImageToFile()


def _forceBlueGreenSwap(imageToRender):
    if not config.forceBGSwap:
        return
    data = numpy.array(imageToRender)
    try:
        im_rgb = data[:, :, [0, 2, 1, 3]]
    except Exception as e:
        pieceLogger(e)
        im_rgb = data[:, :, [0, 2, 1]]

    data2 = numpy.array(im_rgb)
    imageToRender = Image.fromarray(data2)
    return imageToRender


def _renderDiagnostics():
    if not config.renderDiagnostics:
        return
    config.renderDiagnosticsCall()


def render(
    imageToRender,
    xOffset,
    yOffset,
    w=128,
    h=64,
    nocrop=False,
    overlayBottom=False,
    updateCanvasCall=True,
):
    if config.remapImageBlockShift:
        config._imageToRender = imageToRender.copy()

    if imageToRender.mode == "RGB":
        imageToRender = imageToRender.convert("RGBA")

    if config.forceBGSwap:
        imageToRender = _forceBlueGreenSwap(imageToRender)

    if config.rotation != 0:
        if config.fullRotation:
            config.renderImageFull = config.renderImageFull.rotate(-config.rotation, expand=False)
        else:
            imageToRender = imageToRender.rotate(-config.rotation, expand=True)

    if config.remapImageBlockShift and config.rotation != 0:
        config._imageToRender = config._imageToRender.rotate(-config.rotation, expand=True)

    try:
        if not config.remapImageBlockShift:
            config.renderImageFull.paste(imageToRender, (xOffset, yOffset), imageToRender)

    except Exception as e:
        pieceLogger(e)
        config.renderImageFull.paste(imageToRender, (xOffset, yOffset))

    if config.convertRenderImageFullToRGB:
        config.renderImageFull = config.renderImageFull.convert("RGB")
    config.renderDraw = ImageDraw.Draw(config.renderImageFull)

    if config.applyDitherBeforeRemapping:
        _applyDitherFilter(xOffset, yOffset)

    if config.usePixelSort and config.pixelSortRotatesWithImage and random.SystemRandom().random() < config.pixelSortAppearanceProb:
        config.renderImageFull = pixelSort(config.renderImageFull, config)

    if config.rotation != 0 and (config.rotationTrailing or config.fullRotation):
        config.renderImageFull = config.renderImageFull.rotate(config.rotation)

    # ---- Pixel Sort Type Effect ---- #
    if config.usePixelSort and not config.pixelSortRotatesWithImage and random.SystemRandom().random() < config.pixelSortAppearanceProb:
        config.renderImageFull = pixelSort(config.renderImageFull, config)

    # ---- Remap sections of image to accommodate odd panels ---- #
    _doReMappingBlocks()

    if not config.applyDitherBeforeRemapping:
        _applyDitherFilter(xOffset, yOffset)

    # ---- Overall image blurring  ---- #
    _blurringCall()
    _renderDiagnostics()
    _lastOverLay()
    _overallResize()
    _saveToFileCall()

    if updateCanvasCall:
        updateCanvas()


# ----------------------------------------- #


def drawBeforeConversion():
    return True


def saveImageToFile():
    pieceLogger(" >> Saving image to file")
    currentTime = time.time()
    baseName = config.outPutPath + str(currentTime)
    _temp = config.renderImageFull.copy()
    _img = _temp.crop((config.saveFileCropFromLeft, config.saveFileCropFromTop, config.windowWidth, config.windowHeight))
    _img = _img.convert("RGBA")
    writeImage(baseName, renderImage=_img)


# ----------------------------------------- #
