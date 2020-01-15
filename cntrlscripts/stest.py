#!/usr/bin/env python2.7
import getopt
import io
import os
import subprocess
import sys
import time

import RPi.GPIO as GPIO

#GPIO.setmode(GPIO.BCM)

# GPIO 18 set up as input. It is pulled up to stop false signals
#GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_UP)
#GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def callBack(arg):
	print("shutting down CALLLED!")
	try:
		print("shutdown call")
		# os.system("/home/pi/Documents/RPI/cntrlscripts/shutdown.sh")
		subprocess.call(["/home/pi/Documents/RPI/cntrlscripts/shutdown.sh"])
	except OSError:
		print(OSError)
		subprocess.call(["/home/pi/Documents/RPI/cntrlscripts/shutdown.sh"])
		# os.system("/home/pi/RPI/cntrlscripts/shutdown.sh")

def __main__():
	print("Started testing GPIO for off signal")


GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.add_event_detect(18, GPIO.FALLING, callback=callBack, bouncetime=10)