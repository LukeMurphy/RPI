#!/bin/bash
# Remote reader
path="/Users/lamshell/Documents/Dev/RPI/"
configGroup="configs/p4-4x4/"
machine="daemon4"

remotevalue=$(curl -A "Mozilla/5.0 (Windows NT 5.1; rv:21.0) Gecko/20130401 Firefox/21" "http://www.lukelab.com/projects/rpi-controls/daemon4-status.cfg")
localvalue=$(cat localvalue.cfg)
echo $remotevalue
echo $localvalue
if [ $remotevalue != $localvalue ] 
then
	echo "NOT THE SAME"
	echo -n $remotevalue > localvalue.cfg

	ps -ef | pgrep Python | xargs sudo kill -9;

	if [ $remotevalue == "fludd" ]
	then
		config="fludd.cfg"
	fi

	if [ $remotevalue == "marquee" ]
	then
		config="marquee.cfg"
	fi

	if [ $remotevalue == "repaint" ]
	then
		config="repaint.cfg"
	fi

	if [ $remotevalue == "flames" ]
	then
		config="img-hub.cfg"
	fi

	execString=$path"player.py "$machine" "$path" "$path$configGroup$config
	echo $execString

	python $execString&
 
fi
