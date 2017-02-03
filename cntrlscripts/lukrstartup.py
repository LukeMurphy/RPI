#!/usr/bin/python
#import modules
#Checks for off signal
import urllib2
import sys, getopt, os
import ConfigParser, io
import time
#import httplib2
from subprocess import call

startupaction = "/home/lukr/Documents/RPI/cntrlscripts/lukrstartup.sh"
a="python /home/lukr/Documents/RPI/player.py RPI9 /home/lukr/Documents/RPI/ /home/lukr/Documents/RPI/configs/pb2.cfg&"
b="python /home/lukr/Documents/RPI/player.py RPI9 /home/lukr/Documents/RPI/ /home/lukr/Documents/RPI/configs/fludd.cfg&"
os.system(a)

time.sleep(1)

os.system(b)

