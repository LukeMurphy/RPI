#Checks for off signal
import urllib2
#import httplib2
from subprocess import call
import sys, os

urlToCheck = "http://192.168.1.124/projects/rpi-controls/banner-status-4.cfg"
#resp, content = httplib2.Http().request(urlToCheck)

def checker() :
	res  = urllib2.urlopen(urlToCheck).read()
	if(res == "off") :
		# Turn off any running scripts and then shutdown
		os.system("/home/pi/RPI/cntrlscripts/off_signal.sh")
	elif(res == "pause") :
		os.system("/home/pi/RPI/cntrlscripts/off_pause.sh")
	elif(res != "") :
		action = "/home/pi/RPI/cntrlscripts/off_restarts.sh " + res
		os.system(action)

checker()
