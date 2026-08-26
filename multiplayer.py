#!/usr/bin/python
# Two instance player

"""
p4-3x8-informal/quilt-triangles-b
p4-3x8-informal/quilt
"""

import argparse
import configparser
import os
import sys
import threading
import time

from PIL import Image, ImageTk
from matplotlib.pyplot import pie

from modules import configuration, player_module
from modules.configuration import bcolors
from modules.configuration import pieceLogger
from modules import rendering
from modules.rendering import appWindow, renderClass


# Create a blank dummy object container for now
# config = type('', (object,), {})()

##########################################################################
#
#
# -------   Reads configuration files and sets defaults
# -------   Piece is initiated by command line: e.g.
# sudo python /Users/lamshell/Documents/Dev/LED-MATRIX-RPI/RPI/player.py studio-mac ./ configs/fludd.cfg &
#
#
##########################################################################
def callbacker(arg):
	pieceLogger(arg)


###
"""
# Expects 3 arguments:
# 		name-of-machine
#       the local path
# 		the config file to load
args = sys.argv
pieceLogger("Arguments passed to player.py:")
pieceLogger(args)
"""
def loadFromArguments(masterConfig, reloading=False):

	if reloading == False:
		# loads the manifest of pieces and their locations in the window
		loadTheConfig(masterConfig)

		# Set up the app window
		workWindow = appWindow.AppWindow(masterConfig)
		workWindow.setUp()

		# set up the common renderer -- i.e. everything renders here
		# but really there should be more than one renderImageFull ....
		workWindow.renderer = renderClass.CanvasElement(workWindow.root, masterConfig)
		workWindow.renderer.masterConfig = masterConfig
		workWindow.renderer.canvasXPosition = 0
		workWindow.renderer.delay = 1
		workWindow.renderer.setUpCanvas(workWindow.root)
		workWindow.renderer.setUp()
		workWindow.players = []

	else:
		#### TO BE IMPLEMENTED - NEED TO KILL ALL THE THREADS AND THEN
		#### RELOAD WINDOW ETC
		pieceLogger(">> reloading: ")

	for i in range(0, len(masterConfig.workSets)):
		workDetails = masterConfig.workSets[i]

		pieceLogger(">> CREATING Player: " + str(i),3)
		cfgToFetch = masterConfig.workConfigParser.get(workDetails, "cfg")
		canvasOffsetX = int(
			masterConfig.workConfigParser.get(workDetails, "canvasOffsetX")
		)
		canvasOffsetY = int(
			masterConfig.workConfigParser.get(workDetails, "canvasOffsetY")
		)
		canvasRotation = float(
			masterConfig.workConfigParser.get(workDetails, "canvasRotation")
		)
		workArgument = masterConfig.path + "/configs/" + cfgToFetch  # + ".cfg"

		## Load the piece's config file
		workConfigParser = configparser.ConfigParser()
		workConfigParser.read(workArgument)

		## Create blank config object for this work
		workObject = configuration.ArtWorkConfig(workArgument)
		workObject.workId = i
		workObject.standAlone = False
		workObject.doingReload = False
		workObject.brightnessOverride = None
		workObject.isRunning = True
		workObject.reloadConfig = False
		workObject.checkForConfigChanges = False
		workObject.useDrawingPoints = False
		workObject.startTime = time.time()
		workObject.currentTime = time.time()

		## Set up the per-piece renderer (writes to workObject.renderImageFull,
		## does NOT touch the Tk canvas — that's handled by startWindowUpdater)
		workObject.renderer = renderClass.CanvasElement(workWindow.root, masterConfig)
		workObject.renderer.config = workObject
		workObject.renderer.setUp()

		try:
			randomChange = masterConfig.workConfigParser.getboolean(workDetails, "randomChange")
		except Exception as e:
			pieceLogger(str(e))
			randomChange = True

		workObject.renderer.config.randomChange = randomChange

		if randomChange == False:
			workObject.renderer.config.canvasOffsetX = canvasOffsetX
			workObject.renderer.config.canvasOffsetY = canvasOffsetY
			workObject.renderer.config.canvasRotation = canvasRotation
		else:
			workObject.renderer.config.canvasOffsetX = 0
			workObject.renderer.config.canvasOffsetY = 0
			workObject.renderer.config.canvasRotation = 0

		workObject.renderer.config.canvasOffsetX_init = canvasOffsetX
		workObject.renderer.config.canvasOffsetY_init = canvasOffsetY
		workObject.renderer.config.canvasRotation_init = canvasRotation

		## Force a fresh module import for each slot so two slots using the same piece
		## type get independent module globals (config, workConfig, particle arrays, etc.)
		workName = workConfigParser.get("displayconfig", "work")
		moduleKey = f"pieces.{workName}"
		if moduleKey in sys.modules:
			del sys.modules[moduleKey]

		## Configure and initialize the piece module (calls main(run=False) internally)
		## standAlone=False prevents renderAsAnimationWindow from opening its own Tk window
		player_module.configure(workObject, workConfigParser)

		## Override render to use CanvasElement (writes to renderImageFull only)
		## rather than the standalone render.py which would try to update a Tk canvas
		workObject.render = workObject.renderer.render

		## Double-buffer: after each complete render (post-ditherFilter), snapshot
		## renderImageFull into renderImageFull_ready. The compositor reads the ready
		## copy so it never sees a mid-render or pre-filter frame.
		workObject.renderImageFull_ready = workObject.renderImageFull.copy()
		_orig_render = workObject.render
		def _make_snapshotting_render(orig, work):
			def _render(imageToRender, xOffset, yOffset, *args, **kwargs):
				orig(imageToRender, xOffset, yOffset, *args, **kwargs)
				work.renderImageFull_ready = work.renderImageFull.copy()
			return _render
		

		workObject.render = _make_snapshotting_render(_orig_render, workObject)
		workObject.updateCanvas = lambda: None
		workObject.drawBeforeConversion = lambda: None
		try:
			workObject.callBack = player_module.work.callBack
			# comment: 
		except Exception as e:
			pieceLogger(e)
			workObject.callBack = lambda: None
		# end try

		workWindow.players.append(workObject)

		startWorkThread(workObject, i)

	pieceLogger(">> ")

	## Resize the root window to match the manifest's screenWidth/screenHeight
	buff = 4
	workWindow.root.geometry(
		f"{masterConfig.screenWidth + buff}x{masterConfig.screenHeight + buff}"
		f"+{masterConfig.windowXOffset}+{masterConfig.windowYOffset}"
	)

	startWindowUpdater(workWindow)
	workWindow.run()


def runWork(work):
	pieceLogger(f">> runWork starting for work {work.workId}")
	# note all the pieces need to have a runWork() function ....
	work.workRefForSequencer.runWork()


def startWindowUpdater(workWindow):
	"""Schedules canvas compositing on the Tk main thread via root.after."""
	mc = workWindow.masterConfig
	mc.sendMessage = False

	# Create the canvas image once; itemconfig updates it in-place to avoid the
	# blank gap that delete+create_image would cause between frames.
	_blank = Image.new("RGBA", (mc.screenWidth, mc.screenHeight), (0, 0, 0, 255))
	_initial_tk = ImageTk.PhotoImage(_blank)
	workWindow.renderer.cnvs._image_tk = _initial_tk
	_image_id = workWindow.renderer.cnvs.create_image(0, 0, image=_initial_tk, anchor="nw")

	def updateLoop():

		try:
			composite = Image.new("RGBA", (mc.screenWidth, mc.screenHeight), (0, 0, 0, 255))
			for work in workWindow.players:
				if work.workId == 0 and mc.sendMessage :
					mc.sendMessage = False
					work.callBack(f"FROM {work.workId}")
				try:
					# Read the ready buffer — always a complete post-filter frame
					src = work.renderImageFull_ready.copy().convert("RGBA")
					if work.canvasRotation != 0:
						src = src.rotate(-work.canvasRotation, expand=True)
					composite.paste(src, (work.canvasOffsetX + 3, work.canvasOffsetY +3), src)
				except Exception:
					pass

			img_tk = ImageTk.PhotoImage(composite)
			workWindow.renderer.cnvs._image_tk = img_tk
			workWindow.renderer.cnvs.itemconfig(_image_id, image=img_tk)

		except Exception as e:
			pieceLogger(f">> updateLoop error: {e}", 1)
		delay_ms = max(1, int(mc.repaintDelay * 1000))
		workWindow.root.after(delay_ms, updateLoop)
	workWindow.root.after(100, updateLoop)


def startWorkThread(work, i):
	pieceLogger(">> startWorkThread THREAD STARTING " + str(i))
	work.running = True
	thrd = threading.Thread(target=runWork, kwargs=dict(work=work))
	thrd.daemon = True
	masterConfig.threads.append(thrd)
	thrd.start()

##########################################################################


"""
example:
python player.py -cfg p4-6x5/stroop2
python player.py -mname daemon3 -path ./ -cfg p4-6x5/stroop2&
"""

def loadTheConfig(masterConfig):
	parser = argparse.ArgumentParser(description="Process")
	parser.add_argument("-mname", type=str, default="local", help="machine name (optional)")
	parser.add_argument("-path", type=str, default="./", help="directory (optional)")
	parser.add_argument(
		"-cfg",
		type=str,
		required=True,
		help="Config File - just need sub-folder and name - e.g. p4-6x5/repeater.cfg",
	)
	parser.add_argument(
		"-brightnessOverride",
		type=int,
		help="brightness param to override the config value (optional)",
	)
	args = parser.parse_args()

	pieceLogger(">>  Config Arguments --> " + str(args) + " **")

	# """
	# config.MID = args[1]
	# config.path = args[2]
	# argument = args[3]
	# """

	masterConfig.MID = args.mname
	masterConfig.path = args.path
	masterConfig.windowConfig = masterConfig.path + "/configs/" + args.cfg

	masterConfig.startTime = time.time()
	masterConfig.currentTime = time.time()
	masterConfig.reloadConfig = False
	masterConfig.doingReload = False
	masterConfig.checkForConfigChanges = False
	masterConfig.loadFromArguments = loadFromArguments
	masterConfig.fileName = masterConfig.windowConfig
	masterConfig.brightnessOverride = None

	# Optional 4th argument to override the brightness set in the
	# config
	if args.brightnessOverride != None:
		brightnessOverride = args.brightnessOverride
		masterConfig.brightness = float(float(brightnessOverride) / 100)
		masterConfig.brightnessOverride = float(float(brightnessOverride) / 100)

	f = os.path.getmtime(masterConfig.windowConfig)
	masterConfig.delta = int((masterConfig.startTime - f))
	pieceLogger(">> LAST MODIFIED DELTA: " + str(masterConfig.delta))

	configure(masterConfig)


def configure(masterConfig):
	pieceLogger(">>  Multiplayer running loadTheConfig **")
	
	masterConfig.workConfigParser = configparser.ConfigParser()
	masterConfig.workConfigParser.read(masterConfig.windowConfig)

	# Get the list of pieces and where the configs for each one is located
	masterConfig.workSets = list(
		map(
			lambda x: x,
			masterConfig.workConfigParser.get("worksList", "works").split(","),
		)
	)
	masterConfig.screenHeight = int(
		masterConfig.workConfigParser.get("worksList", "screenHeight")
	)
	masterConfig.screenWidth = int(
		masterConfig.workConfigParser.get("worksList", "screenWidth")
	)
	masterConfig.canvasOffsetX = int(
		masterConfig.workConfigParser.get("worksList", "canvasOffsetX")
	)
	masterConfig.canvasOffsetY = int(
		masterConfig.workConfigParser.get("worksList", "canvasOffsetY")
	)
	masterConfig.windowXOffset = int(
		masterConfig.workConfigParser.get("worksList", "windowXOffset")
	)
	masterConfig.windowYOffset = int(
		masterConfig.workConfigParser.get("worksList", "windowYOffset")
	)

	try:
		masterConfig.repaintDelay = float(
			masterConfig.workConfigParser.get("worksList", "repaintDelay")
		)
	except Exception as e:
		pieceLogger(str(e))
		masterConfig.repaintDelay = 0.01
	
	try:
		masterConfig.useFilters = masterConfig.workConfigParser.getboolean("worksList", "useFilters")
	except Exception as e:
		pieceLogger(str(e))
		masterConfig.useFilters = False

	
	try:
		masterConfig.useBlur = masterConfig.workConfigParser.getboolean("worksList", "useBlur")
		masterConfig.blurXOffset = int(masterConfig.workConfigParser.get("worksList", "blurXOffset"))
		masterConfig.blurYOffset = int(masterConfig.workConfigParser.get("worksList", "blurYOffset"))
		masterConfig.blurSectionWidth = int(
			masterConfig.workConfigParser.get("worksList", "blurSectionWidth")
		)
		masterConfig.blurSectionHeight = int(
			masterConfig.workConfigParser.get("worksList", "blurSectionHeight")
		)
		masterConfig.sectionBlurRadius = int(
			masterConfig.workConfigParser.get("worksList", "sectionBlurRadius")
		)
		masterConfig.blurSection = (
			masterConfig.blurXOffset,
			masterConfig.blurYOffset,
			masterConfig.blurXOffset + masterConfig.blurSectionWidth,
			masterConfig.blurYOffset + masterConfig.blurSectionHeight,
		)
	except Exception as e:
		pieceLogger(str(e))
		masterConfig.useBlur = False


##########################################################################
pieceLogger(">>  Multiplayer running loadFromArguments **")

masterConfig = configuration.ArtWorkConfig()
masterConfig.path = "."
masterConfig.checkForConfigChanges = True
masterConfig.threads = []


def main():
	loadFromArguments(masterConfig)


# Kick off .......
if __name__ == "__main__":
	main()
