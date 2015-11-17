if [ "$1" == "plane" ]; then 
	sudo python /home/pi/RPI1/plane-scroller.py
elif [ "$1" == "wb" ]; then 
	sudo python /home/pi/RPI1/whiteboardscroller.py
else
	sudo python /home/pi/RPI1/sequence.py "$@"
fi
