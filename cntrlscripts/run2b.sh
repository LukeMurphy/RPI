#!/bin/bash
#ps -ef | pgrep Python | xargs sudo kill -9;
sudo python /Users/lamshell/Documents/Dev/RPI/player.py studio-mac ./ configs/"$@".cfg & 
