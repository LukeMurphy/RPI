if [ "$1" == "plane" ]; then 
	sudo python /home/pi/RPI/plane-scroller.py
elif [ "$1" == "wb" ]; then 
	sudo python /home/pi/RPI/whiteboardscroller.py
else
	sudo python /home/pi/RPI/sequence.py "$@"
fi

