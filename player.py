# Attributes:
#     args (TYPE): Description
#     parser (TYPE): Description
#     workconfig (TYPE): Description
# """

import argparse
import configparser
import getopt
import os
import time
import sys

from configs import defaultpiece
from modules import configuration, player_module
from modules.configuration import bcolors
from modules.configuration import pieceLogger

# from PIL import (
# 	Image,
# 	ImageChops,
# 	ImageDraw,
# 	ImageEnhance,
# 	ImageFilter,
# 	ImageFont,
# 	ImageOps,
# )


workconfig = configparser.ConfigParser()

"""

Command line start of any piece:
example:

python player.py -cfg p4-6x5/stroop2
python player.py -mname daemon3 -path ./ -cfg p4-6x5/stroop2&

python3 player.py -path ./ -cfg __in_progress/p8_particles_sparkles&

"""

parser = argparse.ArgumentParser(description="Process")
parser.add_argument("-mname", type=str, default="local", help="machine name (optional)")
parser.add_argument("-path", type=str, default="./", help="directory (optional)")
# parser.add_argument('-cfg', type=str, required=True,
# help='Config File - just need sub-folder and name
# - e.g. p4-6x5/repeater.cfg')
parser.add_argument(
    "-cfg",
    type=str,
    required=True,
    help="Config File - just need sub-folder and name - e.g. p4-6x5/repeater.cfg",
)
parser.add_argument(
    "-brightnessOverride",
    type=float,
    required=False,
    help="brightness param to override the config value (optional)",
)
args = parser.parse_args()


pieceLogger("Inital Player Arguments: \n" + str(args),3)




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


def loadFromArguments(reloading=False, config=None):
    """Summary

    Args:
        reloading (bool, optional): Description
        config (None, optional): Description
    """
    # global config, workconfig, path, tempImage, threads, thrd

    pieceLogger(f"** RELOADING: {str(reloading)}", 3)

    if reloading is False:
        try:
            _initializeConfiguration(loadFromArguments)
        except getopt.GetoptError as err:
            # print help information and exit:
            print(f"Error:{str(err)}")
    else:
        pieceLogger("\n** RELOADING NOW: " + config.fileName, 3)
        workconfig.read(config.fileName)
        player_module.configure(config, workconfig)



def _initializeConfiguration(loadFromArguments):
    ###
    # Expects 3 arguments:
    # 		name-of-machine
    #       the local path
    # 		the config file to load

    # args = sys.argv
    # print("Arguments passed to player.py:")
    # print(args)

    config = configuration.ArtWorkConfig("BASE PLAYER CONFIGS")
    config.startTime = time.time()
    config.currentTime = time.time()
    config.doingReload = False
    config.brightnessOverride = None
    config.standAlone = True
    config.isRunning = True

    config.reloadConfig = False
    config.checkForConfigChanges = False
    # Load the default work

    if args.cfg is not None:
        _parseArgs(config, loadFromArguments)
    else:
        _printConfigsLoaded(config)
    # ****************************************** #
    # Sets off the piece based on loading the intitail configs #
    # ****************************************** #

    player_module.configure(config, workconfig)


def _printConfigsLoaded(config):
    # Machine ID
    config.MID = "local"
    # Default Work Instance ID
    config.WRKINID = defaultpiece.defaultPieceToRun
    # Default Local Path
    config.path = "/Users/lamshell/Documents/Dev/LEDELI/RPI/"
    pieceLogger(f"** Loading {config.path}configs/{config.WRKINID}.cfg to run. **\n",3)
    workconfig.read(f"{config.path}configs/{config.WRKINID}.cfg")
    print(f"{bcolors.OKBLUE}** ")
    for c in workconfig:
        print(c)
        for a in workconfig[c]:
            print("\t" + str(a) + ":  " + str(workconfig.get(c, a)))
    print(f"**{bcolors.ENDC}")


def _parseArgs(config, loadFromArguments):
    """
    config.MID = args[1]
    config.path = args[2]
    argument = args[3]
    """
    config.initialArgs = args.cfg
    config.MID = args.mname
    config.path = args.path

    # Automating the config path a bit better
    # assumes that if no -path is specified, it defaults to ./ so 
    # just to be sure get the abs path
    if config.path == './' :
        # config.path = os.getcwd() + "/"
        config.path = __file__.replace('player.py','')+ "/"


    argument = f"{config.path}/configs/{args.cfg}"
    workconfig.read(argument)

    config.loadFromArguments = loadFromArguments
    config.fileName = argument
    config.fileNameRaw = args.cfg


    # Optional 4th argument to override the brightness set in the
    # config
    # code frome web overrides come in as xx/100
    if args.brightnessOverride is not None:
        _brightnessOverrideConfigs(config)

    f = os.path.getmtime(argument)
    config.delta = int((config.startTime - f))
    config.deltaWorkFile = int((config.startTime - f))


    print(f"{bcolors.OKBLUE}---------------------------------------------------------------------------------------")
    print ("script: sys.argv[0] is", repr(sys.argv[0]))
    print ("script: __file__ is", repr(__file__))
    print ("script: cwd is", repr(os.getcwd()))
    print ("config: path  is", repr(args.path))
    print ("config: path  is", args.path)
    print("-cfg argument: is", argument)
    print("Last Modified Delta: is", config.delta)
    print(f"---------------------------------------------------------------------------------------{bcolors.ENDC}")



def _brightnessOverrideConfigs(config):
    brightnessOverride = args.brightnessOverride
    _brightnessOverride = float(brightnessOverride)
    if _brightnessOverride > 2.0 :
        _brightnessOverride /= 100
    config.brightness = _brightnessOverride
    config.brightnessOverride = _brightnessOverride
    # y = 0.3215x2 + 0.0092x + 0.6742
    config.ditherfilterbrightness = 0.3215 * config.brightness * config.brightness + .0092 * config.brightness + 0.6742


def main():

    loadFromArguments()
    # """
    # # Threading now handled by renderer - e.g. see modules/render.py
    # thrd = threading.Thread(target=configure)
    # threads.append(thrd)
    # thrd.start()
    # """

# Kick off .......
if __name__ == "__main__":
    main()