#!/usr/bin/python

import os
import sys
import getopt
import time
import configparser
from modules import configuration
from modules.configuration import bcolors
from modules import player
import argparse

workconfig = configparser.ConfigParser()

'''
example:

python player.py -cfg p4-6x5/stroop2
python player.py -mname daemon3 -path ./ -cfg p4-6x5/stroop2&
'''

parser = argparse.ArgumentParser(description='Process')
parser.add_argument('-mname', type=str, default="local", help='machine name (optional)')
parser.add_argument('-path', type=str, default="./", help='directory (optional)')
parser.add_argument('-cfg', type=str, required=True, help='Config File - just need sub-folder and name - e.g. p4-6x5/repeater.cfg')
parser.add_argument('-brightnessOverride', type=int, help='brightness param to override the config value (optional)')
args = parser.parse_args()

print("** " + str(args) + " **")


# Create a blank dummy object container for now
#config = type('', (object,), {})()

##########################################################################
#
#
# -------   Reads configuration files and sets defaults
# -------   Piece is initiated by command line: e.g.
# sudo python /Users/lamshell/Documents/Dev/LED-MATRIX-RPI/RPI/player.py studio-mac ./ configs/fludd.cfg &
#
#
##########################################################################

def loadFromArguments(reloading=False, config = None):
	#global config, workconfig, path, tempImage, threads, thrd


	print(bcolors.OKBLUE + "\n>> ** RELOADING: " + str(reloading) + bcolors.ENDC)

	if(reloading == False):
		try:
			###
			# Expects 3 arguments:
			#		name-of-machine
			#       the local path
			#		the config file to load
			'''
			args = sys.argv
			print("Arguments passed to player.py:")
			print(args)
			'''
			config = configuration.Config()

			# Load the default work

			if(args.cfg != None):

				'''
				config.MID = args[1]
				config.path = args[2]
				argument = args[3]
				'''

				config.MID = args.mname
				config.path = args.path

				argument = config.path + "/configs/" + args.cfg  # + ".cfg"

				workconfig.read(argument)

				config.startTime = time.time()
				config.currentTime = time.time()
				config.reloadConfig = False
				config.doingReload = False
				config.checkForConfigChanges = False
				config.loadFromArguments = loadFromArguments
				config.fileName = argument
				config.brightnessOverride = None

				# Optional 4th argument to override the brightness set in the
				# config
				if(args.brightnessOverride != None):
					brightnessOverride = args.brightnessOverride
					config.brightness = float(float(brightnessOverride) / 100)
					config.brightnessOverride = float(
						float(brightnessOverride) / 100)

				f = os.path.getmtime(argument)
				config.delta = int((config.startTime - f))
				print(bcolors.OKGREEN + "** " + str(argument) +  " --> LAST MODIFIED DELTA: " +  str(config.delta) + " **" + bcolors.ENDC)
			else:
				# Machine ID
				config.MID = baseconfig.MID
				# Default Work Instance ID
				config.WRKINID = baseconfig.WRKINID
				# Default Local Path
				config.path = baseconfig.path
				print(bcolors.WARNING + "** Loading " + config.path + '/configs/pieces/' + config.WRKINID + ".cfg" + " to run. **" + bcolors.ENDC)
				workconfig.read(config.path + '/configs/pieces/' + config.WRKINID + ".cfg")

			player.configure(config, workconfig)

		except getopt.GetoptError as err:
			# print help information and exit:
			print("Error:" + str(err))
	else:
		print("\n** RELOADING NOW: " + config.fileName)
		workconfig.read(config.fileName)
		player.configure(config, workconfig)


''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''


def main():
	global config, threads
	loadFromArguments()
	'''
	# Threading now handled by renderer - e.g. see modules/rendertohub.py
	thrd = threading.Thread(target=configure)
	threads.append(thrd)
	thrd.start()
	'''

# Kick off .......
if __name__ == "__main__":
	main()
