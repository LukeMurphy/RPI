#!/bin/bash
if [ "$1" == "image" ]; then 
	setsid sudo python /home/pi/RPI/image-scroller.py "$@" ; 
elif [ "$1" == "wb" ]; then 
	setsid sudo python /home/pi/RPI/whiteboardscroller.py ; 
else 
	setsid sudo python /home/pi/RPI/sequence.py "$@" ; 
fi
