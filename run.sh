#echo "$@"
if [ "$@" == "plane" ]; then 
	sudo python plane-scroller.py
elif [ "$@" == "wb" ]; then 
	sudo python whiteboardscroller.py
else
	sudo python sequence.py "$@"
fi
