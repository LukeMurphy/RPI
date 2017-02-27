#!/usr/bin/env python2.7
import RPi.GPIO as GPIO
import sys, getopt, os
import ConfigParser, io
import time

GPIO.setmode(GPIO.BCM)

# GPIO 18 set up as input. It is pulled up to stop false signals
GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def __main__():
	print("started testing")
	try:
		GPIO.wait_for_edge(18, GPIO.FALLING)
		print("shutting down!")
		time.sleep(1)
		os.system("/home/pi/RPI/cntrlscripts/shutdown.sh")
	except KeyboardInterrupt:
		GPIO.cleanup()       # clean up GPIO on CTRL+C exit
	GPIO.cleanup()           # clean up GPIO on normal exit

