if [ "$1" == "image" ]; then 
	sudo python /home/pi/RPI/image-scroller.py "$@"
elif [ "$1" == "wb" ]; then 
	sudo python /home/pi/RPI/whiteboardscroller.py
else
	sudo python /home/pi/RPI/sequence.py "$@"
fi

