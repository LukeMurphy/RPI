#!/bin/bash
#sudo python /Users/lamshell/Documents/Dev/RPI/player.py studio-mac ./ configs/"$@".cfg & 
if [ "$2" == "b" ]; then 
echo
else
ps -ef | pgrep Python | xargs sudo kill -9; 
fi
echo
echo 
sudo python3 player.py -mname studio-mac -path ./ -cfg "$1.cfg"& 
