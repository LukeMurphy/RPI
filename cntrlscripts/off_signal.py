#Checks for off signal
import urllib2
import sys, getopt, os
import ConfigParser, io

#import httplib2
from subprocess import call

baseconfig = ConfigParser.ConfigParser()
baseconfig.read('/home/pi/RPI/config.cfg')

base = baseconfig.get("config", 'controlUrl')
unit = baseconfig.get("config", 'unitNumber')

urlToCheck = base + "/banner-status-"+unit+".cfg"
confirmUrl = base + "/confirm.php?rpiunit=" + unit
#resp, content = httplib2.Http().request(urlToCheck)


# --------------------------------------------------------------#
# TODO Need to alert somehow that the connection is not working

def checker() :
	global urlToCheck, confirmUrl, base
	offAction = "/home/pi/RPI/cntrlscripts/off_signal.sh"
	pauseAction = "/home/pi/RPI/cntrlscripts/off_pause.sh"
	restartAction = "/home/pi/RPI/cntrlscripts/off_restarts.sh "
	reboot = "/home/pi/RPI/cntrlscripts/reboot.sh"
	#print("checking ==> " + urlToCheck + " " + confirmUrl + " " + base)

	try:
		res  = urllib2.urlopen(urlToCheck).read()
		confirm = urllib2.urlopen(confirmUrl).read()
		#print(res)

		if(res == "off") :
			# Turn off any running scripts and then shutdown
			os.system(offAction)
		elif(res == "pause") :
			os.system(pauseAction)
		elif(res == "reboot") :
			os.system(reboot)
		elif(res != "nochange" and res != "") :
			action = restartAction + res
			os.system(action)

	except Exception, e:
		res = "nochange"
		print(e)


checker()
