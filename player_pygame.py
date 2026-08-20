# Attributes:
#     args (TYPE): Description
#     parser (TYPE): Description
#     workconfig (TYPE): Description
#
# Pygame-windowed variant of player.py.
#
# Identical command-line interface and config loading to player.py -- the
# only difference is that it forces `rendering = pygame` in the loaded
# config, regardless of what the .cfg file specifies, so the piece is
# displayed through modules/rendering/renderpygame.py (a pygame window)
# instead of modules/rendering/render.py (a tkinter window).
#
# Pieces themselves (e.g. pieces/particles.py) don't need a separate
# version to run under pygame -- they only draw into a PIL image and call
# config.render(...), never touching the windowing toolkit directly. That
# call is wired to the pygame renderer here instead of the tkinter one.

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

workconfig = configparser.ConfigParser()

"""
Command line start of any piece, windowed via pygame instead of tkinter:
example:

python player_pygame.py -cfg p4-6x5/stroop2
python player_pygame.py -mname daemon3 -path ./ -cfg p4-6x5/stroop2&
"""

##########################################################################

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
    type=float,
    required=False,
    help="brightness param to override the config value (optional)",
)
args = parser.parse_args()


pieceLogger("[player_pygame] >> Inital Player Arguments: \n" + str(args), 3)

##########################################################################
#
# -------   Reads configuration files and sets defaults
# -------   Piece is initiated by command line, windowed via pygame
#
##########################################################################


def _forcePygameRendering(workconfig):
    if not workconfig.has_section("displayconfig"):
        workconfig.add_section("displayconfig")
    workconfig.set("displayconfig", "rendering", "pygame")


def loadFromArguments(reloading=False, config=None):
    """
    Args:
        reloading (bool, optional): Description
        config (None, optional): Description
    """
    pieceLogger(f" >> ** RELOADING: {str(reloading)}", 3)

    if reloading is False:
        try:
            _initializeConfiguration(loadFromArguments)
        except getopt.GetoptError as err:
            pieceLogger(f" >> Error:{str(err)}")
    else:
        pieceLogger("\n >>** RELOADING NOW: " + config.fileName, 3)
        workconfig.read(config.fileName)
        _forcePygameRendering(workconfig)
        player_module.configure(config, workconfig)


def _initializeConfiguration(loadFromArguments):
    ###
    # Expects 3 arguments:
    # 		name-of-machine
    #       the local path
    # 		the config file to load

    config = configuration.ArtWorkConfig("BASE PLAYER CONFIGS")

    if args.cfg is not None:
        _parseArgs(config, loadFromArguments)
    else:
        _pieceLoggerConfigsLoaded(config)

    _forcePygameRendering(workconfig)

    # ****************************************** #
    # Sets off the piece based on loading the intitail configs #
    # ****************************************** #

    player_module.configure(config, workconfig)


def _pieceLoggerConfigsLoaded(config):
    # Machine ID
    config.MID = "local"
    # Default Work Instance ID
    config.WRKINID = defaultpiece.defaultPieceToRun
    # Default Local Path
    config.path = "/Users/lamshell/Documents/Dev/LEDELI/RPI/"
    pieceLogger(f" >> ** Loading {config.path}configs/{config.WRKINID}.cfg to run. **\n", 3)
    workconfig.read(f"{config.path}configs/{config.WRKINID}.cfg")
    pieceLogger(f"{bcolors.OKBLUE}")
    for c in workconfig:
        pieceLogger(f" >> {c}")
        for a in workconfig[c]:
            pieceLogger(f" >> \t {a} : {workconfig.get(c, a)}")
    pieceLogger(f"{bcolors.ENDC}")


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
    if config.path == './':
        config.path = __file__.replace('player_pygame.py', '') + "/"

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

    pieceLogger(f" >> {bcolors.OKBLUE}---------------------------------------------------------------------------------------")
    pieceLogger(" >> script: sys.argv[0] is", repr(sys.argv[0]))
    pieceLogger(" >> script: __file__ is", repr(__file__))
    pieceLogger(" >> script: cwd is", repr(os.getcwd()))
    pieceLogger(" >> config: path  is", repr(args.path))
    pieceLogger(" >> config: path  is", args.path)
    pieceLogger(" >> -cfg argument: is", argument)
    pieceLogger(" >> Last Modified Delta: is", config.delta)
    pieceLogger(f" >> ---------------------------------------------------------------------------------------{bcolors.ENDC}")


def _brightnessOverrideConfigs(config):
    brightnessOverride = args.brightnessOverride
    _brightnessOverride = float(brightnessOverride)
    if _brightnessOverride > 2.0:
        _brightnessOverride /= 100
    config.brightness = _brightnessOverride
    config.brightnessOverride = _brightnessOverride
    # y = 0.3215x2 + 0.0092x + 0.6742
    config.ditherfilterbrightness = 0.3215 * config.brightness * config.brightness + .0092 * config.brightness + 0.6742


def main():
    loadFromArguments()


# Kick off .......
if __name__ == "__main__":
    main()
