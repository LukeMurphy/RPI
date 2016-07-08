#!/bin/bash
if [ "$1" != "" ]; then 
	setsid sudo python /home/pi/RPI/sequenceplayer.py "$@" & 
else 
	setsid sudo python /home/pi/RPI/player.py RPI9 ./ configs/studio/h-hat-base-1.1.cfg&
fi