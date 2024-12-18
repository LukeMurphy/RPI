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
import platform

from configs import defaultpiece
from modules import configuration, player
from modules.configuration import bcolors

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
    type=int,
    required=False,
    help="brightness param to override the config value (optional)",
)
args = parser.parse_args()


print(bcolors.OKBLUE)
print("--------------------------------")
print("Inital Player Arguments: \n" + str(args))
print("--------------------------------")
print(bcolors.ENDC)



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

    print(bcolors.OKBLUE + "** RELOADING: " + str(reloading) + bcolors.ENDC)

    if reloading is False:
        try:
            ###
            # Expects 3 arguments:
            # 		name-of-machine
            #       the local path
            # 		the config file to load

            # args = sys.argv
            # print("Arguments passed to player.py:")
            # print(args)

            config = configuration.Config()
            config.startTime = time.time()
            config.currentTime = time.time()
            config.reloadConfig = False
            config.doingReload = False
            config.checkForConfigChanges = False
            config.brightnessOverride = None
            config.standAlone = True
            config.isRunning = True

            # Load the default work

            if args.cfg is not None:

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
                    

                argument = config.path + "/configs/" + args.cfg  # + ".cfg"
                workconfig.read(argument)

                config.loadFromArguments = loadFromArguments
                config.fileName = argument
                config.fileNameRaw = args.cfg


                # Optional 4th argument to override the brightness set in the
                # config
                if args.brightnessOverride != None:
                    brightnessOverride = args.brightnessOverride
                    config.brightness = float(float(brightnessOverride) / 100)
                    config.brightnessOverride = float(float(brightnessOverride) / 100)

                f = os.path.getmtime(argument)
                config.delta = int((config.startTime - f))
                config.deltaWorkFile = int((config.startTime - f))
                print(bcolors.OKGREEN)
                
                print("-----------------------------------------")
                print ("script: sys.argv[0] is", repr(sys.argv[0]))
                print ("script: __file__ is", repr(__file__))
                print ("script: cwd is", repr(os.getcwd()))
                print ("config: path  is", repr(args.path))
                print ("config: path  is", args.path)
                print ("-cfg argument: is", str(argument))
                print ("Last Modified Delta: is", str(config.delta))
                print("-----------------------------------------" + bcolors.ENDC)
                
            else:
                # Machine ID
                config.MID = "local"
                # Default Work Instance ID
                config.WRKINID = defaultpiece.defaultPieceToRun
                # Default Local Path
                config.path = "/Users/lamshell/Documents/Dev/LEDELI/RPI/"
                print(
                    bcolors.WARNING
                    + "** Loading "
                    + config.path
                    + "configs/"
                    + config.WRKINID
                    + ".cfg"
                    + " to run. **"
                    + bcolors.ENDC
                )
                workconfig.read(config.path + "configs/" + config.WRKINID + ".cfg")
                print(bcolors.OKGREEN + "** ")
                for c in workconfig:
                    print(c)
                    for a in workconfig[c]:
                        print("\t" + str(a) + ":  " + str(workconfig.get(c, a)))
                print("**" + bcolors.ENDC)

            # ****************************************** #
            # Sets off the piece based on loading the intitail configs #
            # ****************************************** #

            player.configure(config, workconfig)

        except getopt.GetoptError as err:
            # print help information and exit:
            print("Error:" + str(err))
    else:
        print("\n** RELOADING NOW: " + config.fileName)
        workconfig.read(config.fileName)
        player.configure(config, workconfig)


# """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" ""


def main():

    loadFromArguments()
    # """
    # # Threading now handled by renderer - e.g. see modules/rendertohub.py
    # thrd = threading.Thread(target=configure)
    # threads.append(thrd)
    # thrd.start()
    # """


# Kick off .......
if __name__ == "__main__":
    main()
