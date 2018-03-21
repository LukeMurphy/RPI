#!/usr/bin/env python2.7
import RPi.GPIO as GPIO
import sys, getopt, os, io
import time
import subprocess

GPIO.setmode(GPIO.BCM)

# GPIO 18 set up as input. It is pulled up to stop false signals
GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def __main__():
	print("Started testing GPIO for off signal")
	try:
		GPIO.wait_for_edge(18, GPIO.FALLING)
		print("shutting down!")
		time.sleep(.1)
		try:
			print("shutdown call")
			#os.system("/home/pi/Documents/RPI/cntrlscripts/shutdown.sh")
			subprocess.call(['/home/pi/Documents/RPI/cntrlscripts/shutdown.sh'])
		except OSError:
			print(OSError)
			subprocess.call(['/home/pi/RPI/cntrlscripts/shutdown.sh'])
			#os.system("/home/pi/RPI/cntrlscripts/shutdown.sh")
	except KeyboardInterrupt:
		GPIO.cleanup()       # clean up GPIO on CTRL+C exit
	GPIO.cleanup()           # clean up GPIO on normal exit




