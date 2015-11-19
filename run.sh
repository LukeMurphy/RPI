if [ "$1" == "plane" ]; then 
	sudo python /home/pi/RPI3/plane-scroller.py
elif [ "$1" == "wb" ]; then 
	sudo python /home/pi/RPI3/whiteboardscroller.py
else
	sudo python /home/pi/RPI3/sequence.py "$@"
fi
