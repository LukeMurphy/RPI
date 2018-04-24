#!/bin/bash
ps -ef | pgrep python | xargs sudo kill -9;
#sudo python /Users/lamshell/Documents/Dev/RPI/player.py studio-mac ./ configs/"$@".cfg & 
sudo python3 player.py -mname studio-mac -path ./ -cfg "$@.cfg"& 
