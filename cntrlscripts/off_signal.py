#Checks for off signal
import urllib2
#import httplib2
from subprocess import call
import sys, os

urlToCheck = "http://192.168.0.4/projects/rpi-controls/banner-status.cfg"
#resp, content = httplib2.Http().request(urlToCheck)

def checker() :
	res  = urllib2.urlopen(urlToCheck).read()
	if(res) == "off" :
		# Turn off any running scripts and then shutdown
		os.system("/home/pi/RPI/cntrlscripts/off_signal.sh")
	if(res) == "anim" :
		os.system("/home/pi/RPI/cntrlscripts/off_restarts.sh")
	if(res) == "signage" :
		os.system("/home/pi/RPI/cntrlscripts/off_restartsigns.sh")

checker()