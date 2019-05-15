#!/usr/bin/python

import os, getopt, sys, time
import configparser
from subprocess import call
from modules import configuration
from modules import player

global thrd, config


threads = []

workconfig = configparser.ConfigParser()

def loadFromArguments(reloading=False):
	global config, workconfig, path, tempImage, threads, thrd

	if(reloading == False) :
		try: 
			config = configuration

			'''
			config.MID = args[1]
			config.path = args[2]
			argument = args[3]
			'''

			config.MID = "dem0"
			config.path = "/users/lamshell/Documents/Dev/RPI"

			argument = config.path + "/configs/prod/p4-6x8-exp-repeater-cloud.cfg"
			
			workconfig.read(argument)

			config.startTime = time.time()
			config.currentTime = time.time()
			config.reloadConfig = False
			config.doingReload = False
			config.checkForConfigChanges =  False
			config.loadFromArguments = loadFromArguments
			config.fileName = argument
			config.brightnessOverride = None

			f = os.path.getmtime(argument)

			config.delta = int((config.startTime - f ))
			print (argument, "LAST MODIFIED DELTA: ", config.delta)

			player.configure(config, workconfig)

		except getopt.GetoptError as err:
			# print help information and exit:
			print ("Error:" + str(err))
	else :
		print("reloading: "+ config.fileName)
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
	
### Kick off .......
if __name__ == "__main__":
	main()
