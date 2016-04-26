#!/bin/bash
if [ "$1" != "" ]; then 
	setsid sudo python /home/pi/RPI/sequenceplayer.py "$@" & 
else 
	setsid sudo python /home/pi/RPI/player.py&
fi