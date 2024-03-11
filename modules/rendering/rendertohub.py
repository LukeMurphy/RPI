import random
import threading
import datetime
import time

import tkinter as tk
import os

from modules.filters import *
from PIL import (
    Image,
    ImageChops,
    ImageDraw,
    ImageEnhance,
    ImageFilter,
    ImageFont,
    ImageTk,
)

# from tkVideoPlayer import TkinterVideo
# from Tkinter import *
# import tkMessageBox
# import PIL.Image
# import PIL.ImageTk
# import gc, os

"""""" """""" """""" """""" """""" """""" """""" """""" """""" """""" ""

global root
global work, config
memoryUsage = 0
debug = False
counter = 0

canvasOffsetX = 4
canvasOffsetY = 7
buff = 8


"""""" """""" """""" """""" """""" """""" """""" """""" """""" """""" ""
def update_duration():
	""" updates the duration after finding the duration """
	duration = config.videoplayer.video_info()["duration"]
	loc = config.videoplayer.current_duration()
	if loc > 40:
		config.videoplayer.seek(0)


def setUp(config):
    # global root, canvasOffsetX, canvasOffsetY, buff, config
    gc.enable()

    config.imageArrayForSaving = []
    config.frameCount = 0
    config.frameCountLimit = 2

    if config.MID == "studio-mac":
        config.path = "./"
        windowOffset = [1900, 20]
        windowOffset = [2560, 24]
        windowOffset = [config.windowXOffset, config.windowYOffset]
        # windowOffset = [4,45]
    else:
        windowOffset = [-1, 13]
        windowOffset = [config.windowXOffset, config.windowYOffset]

    # -----> this is somewhat arbitrary - just to get the things aligned
    # after rotation
    # if(config.rotation == 90) : canvasOffsetY = -25

    root = tk.Tk()
    w = config.windowWidth + buff
    h = config.windowHeight + buff
    x = windowOffset[0]
    y = windowOffset[1]

    config.screenPositionX = x
    config.screenPositionY = y

    root.overrideredirect(False)

    try:
        if config.useDrawingPoints == True:
            # screen_width = root.winfo_screenwidth()
            # screen_height = root.winfo_screenheight()
            # root.geometry("%dx%d+%d+%d" % (600, round(.9*screen_height), round(3*screen_width/4), round(0*screen_height/3)))
            root.geometry("%dx%d+%d+%d" % (w, h, x, y))
        else:
            root.geometry("%dx%d+%d+%d" % (w, h, x, y))
    except Exception as e:
        root.geometry("%dx%d+%d+%d" % (w, h, x, y))
        print(str(e))

    # root.protocol("WM_DELETE_WINDOW", on_closing)

    # Button(root, text="Quit", command=root.quit).pack(side="bottom")
    root.lift()

    config.root = root

    cnvs = tk.Canvas(
        root,
        width=config.screenWidth + buff,
        height=config.screenHeight + buff,
        border=0,cursor="none"
    )
    config.cnvs = cnvs
    config.cnvs.create_rectangle(
        0, 0, config.screenWidth + buff, config.screenHeight + buff, fill="black"
    )
    # config.cnvs.pack()
    config.cnvs.place(
        bordermode="outside",
        width=config.screenWidth + buff,
        height=config.screenHeight + buff,
    )

    # cnvs2 = tk.Canvas(root, width=config.screenWidth + buff, height=config.screenHeight + buff, border=-4)
    # config.cnvs2 = cnvs2
    # config.cnvs2.create_rectangle(0, 0, config.screenWidth + buff, config.screenHeight + buff, fill="black")
    # config.cnvs2.pack()
    # config.cnvs2.place(bordermode='outside', width=config.screenWidth + buff, height=config.screenHeight + buff, x=config.screenWidth + 2)

    # tempImage = PIL.ImageTk.PhotoImage(config.renderImageFull)
    tempImage = ImageTk.PhotoImage(config.renderImageFull)
    config.cnvs._image_id = config.cnvs.create_image(
        canvasOffsetX, canvasOffsetY, image=tempImage, anchor="nw", tag="mainer"
    )

    # config.cnvs.update()
    # config.cnvs.update_idletasks()

    config.torqueAngle = 0

    # videoplayer = TkinterVideo(master=root, scaled=True)
    # videoplayer.load("/Users/lamshell/Desktop/Untitled.mov")
    # videoplayer.place(bordermode="ignore", width=360, height=160,x=10,y=10)
    # videoplayer.play()  # play the video
    # config.videoplayer = videoplayer

    root.after(100, startWork)
    root.call("wm", "attributes", ".", "-topmost", "1")
    root.mainloop()


"""""" """""" """""" """""" """""" """""" """""" """""" """""" """""" ""


def on_closing():
    global root
    return True


"""""" """""" """""" """""" """""" """""" """""" """""" """""" """""" ""

def writeImage(baseName, renderImage):
    # baseName = "outputquad3/comp2_"
    fn = baseName+".png"
    renderImage.save(fn)
        
        
def startWork(*args):
    # global config, work, root, counter
    global counter

    # Putting the animation on its own thread
    # Still throws and error when manually closed though...

    try:
        t = threading.Thread.__init__(work.runWork())
        t.start()
    except tk.TclError as details:
        print(details)
        pass
        exit()

    # work.runWork()


"""""" """""" """""" """""" """""" """""" """""" """""" """""" """""" ""


def updateCanvas():
    # global canvasOffsetX, canvasOffsetY, root, counter, buff
    global counter
    # For testing ...
    # draw1  = ImageDraw.Draw(config.renderImageFull)
    # draw1.rectangle((xOffset+32,yOffset,xOffset + 32 + 32, yOffset +32), fill=(255,100,0))
    counter += 1
    if counter > 1000:
        # print(gc.get_count())
        # I don't know if this really really helps
        gc.collect()
        counter = 0

    # This significantly helped performance !!
    config.cnvs.delete("main")
    config.cnvs._image_tk = PIL.ImageTk.PhotoImage(config.renderImageFull)
    config.cnvs._image_id = config.cnvs.create_image(
        canvasOffsetX,
        canvasOffsetY,
        image=config.cnvs._image_tk,
        anchor="nw",
        tag="main",
    )
    config.cnvs.update()
    
    # update_duration()
    
    

    # config.cnvs2.delete("main")
    # config.cnvs2._image_tk = PIL.ImageTk.PhotoImage(config.renderImageFull)
    # config.cnvs2._image_id = config.cnvs2.create_image(canvasOffsetX -4, canvasOffsetY, image=config.cnvs2._image_tk, anchor='nw', tag="main")
    # config.cnvs2.update()

    # This *should* be more efficient
    # config.cnvs.update_idletasks()
    # root.update()

    ############################################################
    ######  Check if config file has changed and reload    #####
    ############################################################

    if config.checkForConfigChanges == True:
        currentTime = time.time()
        f = os.path.getmtime(config.fileName)
        f2 = os.path.getmtime(config.path + "pieces/" + config.work + ".py")
        config.delta = currentTime - f
        config.delta2 = currentTime - f2

        if config.delta <= 1 or config.delta2 <= 1:
            if config.reloadConfig == False:
                print("** LAST MODIFIED DELTA: " + str(config.delta) + " **")
                print("** LAST MODIFIED DELTA: " +
                      str(config.initialArgs) + " **")
                # commadStringPyth = "python3 /Users/lamshell/Documents/Dev/RPI/player.py -path /Users/lamshell/Documents/Dev/RPI/ -mname studio -cfg "

                if config.doFullReloadOnChange == True:
                    os.system(
                        config.path + '/cntrlscripts/restart_player_dev.sh' + ' ' + config.initialArgs + "&")
                # commadStringPyth = ""
                # os.system(commadStringPyth + config.initialArgs + "&")

                else:
                    config.doingReload = True
                    # NEED TO PASS BACK THIS CONFIG TO THE RELOAD ... otherwise loses reference
                    config.loadFromArguments(True, config)
            config.reloadConfig = True
        else:
            config.reloadConfig = False

        if config.delta2 <= 1:
            commadStringPyth = "python3 /Users/lamshell/Documents/Dev/LEDELI/RPI/player.py -mname studio -cfg "
            # os.system("ps -ef | pgrep -f player | xargs sudo kill -9;")
            # os.system(commadStringPyth + config.fileNameRaw + "&")


"""""" """""" """""" """""" """""" """""" """""" """""" """""" """""" ""


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
    # global memoryUsage
    # global config, debug

    # Render to canvas
    # This needs to be optomized !!!!!!

    if config.forceBGSwap == True:
        data = numpy.array(imageToRender)

        try:
            im_rgb = data[:, :, [0, 2, 1, 3]]
        except Exception as e:
            im_rgb = data[:, :, [0, 2, 1]]

        data2 = numpy.array(im_rgb)

        imageToRender = Image.fromarray(data2)

    if config.rotation != 0:
        if config.fullRotation == True:
            # This rotates the image that is painted i.e. after pasting-in the image sent
            config.renderImageFull = config.renderImageFull.rotate(
                -config.rotation, expand=False
            )
        else:
            # This rotates the image sent to be rendered
            imageToRender = imageToRender.rotate(-config.rotation, expand=True)
            # imageToRender = ImageChops.offset(imageToRender, -40, 40)

    try:
        config.renderImageFull.paste(
            imageToRender, (xOffset, yOffset), imageToRender)

    except:
        config.renderImageFull.paste(imageToRender, (xOffset, yOffset))

    # config.drawBeforeConversion()

    # config.renderImageFull.paste(config.renderImageFull2)

    config.renderImageFull = config.renderImageFull.convert("RGB")
    config.renderDraw = ImageDraw.Draw(config.renderImageFull)

    # config.renderImageFull = ImageChops.offset(config.renderImageFull, 40, 40)

    # For planes, only this works - has to do with transparency of repeated pasting of
    # PNG's I think
    # newimage = Image.new('RGBA', config.renderImageFull.size)
    # newimage.paste(config.renderImageFull, (0, 0))
    # config.renderImageFull =  newimage.convert("RGB")

    # enhancer = ImageEnhance.Brightness(config.renderImageFull)
    # config.renderImageFull = enhancer.enhance(.75)

    if config.useFilters == True:

        if config.filterRemap == True:
            config.tempImage = config.renderImageFull.copy()
            config.tempImage = ditherFilter(
                config.tempImage, xOffset, yOffset, config)
            crop = config.tempImage.crop(config.remapImageBlockSection)
            crop = crop.convert("RGBA")
            if config.ditherFilterBrightness != 1.0:
                crop = ImageEnhance.Brightness(crop).enhance(
                    config.ditherFilterBrightness
                )
            config.renderImageFull.paste(
                crop, config.remapImageBlockDestination, crop)
        else:
            config.renderImageFull = ditherFilter(
                config.renderImageFull, xOffset, yOffset, config
            )

    if config.usePixelSort == True and config.pixelSortRotatesWithImage == True:
        if random.random() < config.pixelSortAppearanceProb:
            config.renderImageFull = pixelSort(config.renderImageFull, config)

    if config.rotation != 0:
        if config.rotationTrailing or config.fullRotation:
            # This rotates the image that is painted back to where it was
            # basically same thing as rotating the image to be pasted in
            # except in some cases, more trailing is created
            config.renderImageFull = config.renderImageFull.rotate(
                config.rotation)

    # ---- Pixel Sort Type Effect ---- #
    if config.usePixelSort and config.pixelSortRotatesWithImage == False:
        if random.random() < config.pixelSortAppearanceProb:
            config.renderImageFull = pixelSort(config.renderImageFull, config)

            # crop = config.renderImageFull.crop()
            # crop = crop.convert("RGBA")
            # crop =  pixelSort(crop, config)
            # config.renderImageFull = config.renderImageFull.convert("RGBA")
            # config.renderImageFull.paste(crop)

    # ---- Remap sections of image to accommodate odd panels ---- #
    if config.remapImageBlock == True:
        crop = config.renderImageFull.crop(config.remapImageBlockSection)
        if config.remapImageBlockSectionRotation != 0:
            crop = crop.convert("RGBA")
            crop = crop.rotate(config.remapImageBlockSectionRotation)
        crop = crop.convert("RGBA")
        config.renderImageFull.paste(
            crop, config.remapImageBlockDestination, crop)

    if config.remapImageBlock2 == True:
        crop = config.renderImageFull.crop(config.remapImageBlockSection2)
        if config.remapImageBlockSection2Rotation != 0:
            crop = crop.convert("RGBA")
            crop = crop.rotate(config.remapImageBlockSection2Rotation)
        crop = crop.convert("RGBA")
        config.renderImageFull.paste(
            crop, config.remapImageBlockDestination2, crop)

    if config.remapImageBlock3 == True:
        crop = config.renderImageFull.crop(config.remapImageBlockSection3)
        if config.remapImageBlockSection3Rotation != 0:
            crop = crop.convert("RGBA")
            crop = crop.rotate(config.remapImageBlockSection3Rotation)
        crop = crop.convert("RGBA")
        config.renderImageFull.paste(
            crop, config.remapImageBlockDestination3, crop)

    if config.remapImageBlock4 == True:
        crop = config.renderImageFull.crop(config.remapImageBlockSection4)
        if config.remapImageBlockSection4Rotation != 0:
            crop = crop.convert("RGBA")
            crop = crop.rotate(config.remapImageBlockSection4Rotation)
        crop = crop.convert("RGBA")
        config.renderImageFull.paste(
            crop, config.remapImageBlockDestination4, crop)

    if config.remapImageBlock5 == True:
        crop = config.renderImageFull.crop(config.remapImageBlockSection5)
        if config.remapImageBlockSection5Rotation != 0:
            crop = crop.convert("RGBA")
            crop = crop.rotate(config.remapImageBlockSection5Rotation)
        crop = crop.convert("RGBA")
        config.renderImageFull.paste(
            crop, config.remapImageBlockDestination5, crop)

    if config.remapImageBlock6 == True:
        crop = config.renderImageFull.crop(config.remapImageBlockSection6)
        if config.remapImageBlockSection6Rotation != 0:
            crop = crop.convert("RGBA")
            crop = crop.rotate(config.remapImageBlockSection6Rotation)
        crop = crop.convert("RGBA")
        config.renderImageFull.paste(
            crop, config.remapImageBlockDestination6, crop)

    if config.remapImageBlock7 == True:
        crop = config.renderImageFull.crop(config.remapImageBlockSection7)
        if config.remapImageBlockSection7Rotation != 0:
            crop = crop.convert("RGBA")
            crop = crop.rotate(config.remapImageBlockSection7Rotation)
        crop = crop.convert("RGBA")
        config.renderImageFull.paste(
            crop, config.remapImageBlockDestination7, crop)

    # ---- Overall image blurring  ---- #
    if config.useBlur == True:
        # config.renderImageFull = config.renderImageFull.filter(ImageFilter.GaussianBlur(radius=config.sectionBlurRadius))

        crop = config.renderImageFull.crop(config.blurSection)
        destination = (config.blurXOffset, config.blurYOffset)
        crop = crop.convert("RGBA")
        crop = crop.filter(ImageFilter.GaussianBlur(
            radius=config.sectionBlurRadius))
        config.renderImageFull.paste(crop, destination, crop)

    if config.renderDiagnostics == True:
        config.renderDiagnosticsCall()

    try:
        if config.useLastOverlay == True:
            config.renderDrawOver.rectangle(
                config.lastOverlayBox, fill=config.lastOverlayFill, outline=None)
            # config.renderDrawOver.rectangle(config.lastOverlayBox, fill=(255,0,0,255), outline=None)
            if config.lastOverlayBlur > 0:
                config.renderImageFullOverlay = config.renderImageFullOverlay.filter(
                    ImageFilter.GaussianBlur(radius=config.lastOverlayBlur))
            config.renderImageFull.paste(
                config.renderImageFullOverlay, (0, 0), config.renderImageFullOverlay)
    except Exception as e:
        print(e)

    if config.overallResize == True :
        # Testing a pseudo version of LED matrix display
        # Sharpening kernel
        kernel = [-1, -1, -1,
            -1,  9, -1,
            -1, -1, -1]
        kernel_filter = ImageFilter.Kernel((3, 3), kernel, scale=1, offset=0)

        iTemp = config.renderImageFull.copy()
        factor = 3
        (width, height) = (iTemp.width * factor, iTemp.height * factor)
        iTemp = iTemp.resize((width, height))
        # Sharpen the image
        # iTemp = iTemp.filter(kernel_filter)
        iTemp = iTemp.filter(ImageFilter.SHARPEN)
        iTemp = iTemp.filter(ImageFilter.SHARPEN)
        config.renderImageFull.paste(iTemp, (0,0))


    if config.outputMode == 'gif':
        config.frameCount += 1
        if config.frameCount >= config.frameCountLimit:
            config.imageArrayForSaving.append(config.renderImageFull)
            config.frameCount = 0

        if len(config.imageArrayForSaving) > 500:
            ts = time.time()
            st = datetime.datetime.fromtimestamp(
                ts).strftime("%Y-%m-%d--%H-%M-%S")
            # name = config.work + "_" + st + "_video.avi"
            # /Users/lamshell/Documents/Dev/RPI/build/
            name = "" + st + ".gif"
            config.imageArrayForSaving[0].save(
                name, save_all=True, append_images=config.imageArrayForSaving[1:], optimize=True, duration=.5, loop=0)
            config.imageArrayForSaving = []
            
    if config.saveToFile == True :
        config.topDirector.checkTime()
        if config.topDirector.advance == True :
            currentTime = time.time()
            baseName = config.outPutPath + str(currentTime)
            writeImage(baseName, renderImage=config.renderImageFull)


    



    if updateCanvasCall:
        updateCanvas()

    # mem = int(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)/1024/1024
    # if mem > memoryUsage and debug :
    #     memoryUsage = mem
    #     print 'Memory usage: %s (mb)' % str(memoryUsage)


"""""" """""" """""" """""" """""" """""" """""" """""" """""" """""" ""
# Might be used at some point


def remappingFunctionTemp():
    for i in range(0, 4):
        # Map the one below to the next set of 4
        pix = 16
        colWidth = 128
        row = i
        cropRow = i * 2 + 1

        remapImageBlockSection = (
            0, cropRow * pix, colWidth, cropRow * pix + pix)
        remapImageBlockDestination = (colWidth, row * 16)
        crop = config.renderImageFull.crop(remapImageBlockSection)
        crop = crop.convert("RGBA")
        config.renderImageFull.paste(crop, remapImageBlockDestination, crop)
        # Move a row "up"

        remapImageBlockSection = (
            0,
            (cropRow - 1) * pix,
            colWidth,
            (cropRow - 1) * pix + pix,
        )
        remapImageBlockDestination = (0, (row) * pix)
        crop = config.renderImageFull.crop(remapImageBlockSection)
        crop = crop.convert("RGBA")
        config.renderImageFull.paste(crop, remapImageBlockDestination, crop)


def drawBeforeConversion():
    return True


"""""" """""" """""" """""" """""" """""" """""" """""" """""" """""" ""
