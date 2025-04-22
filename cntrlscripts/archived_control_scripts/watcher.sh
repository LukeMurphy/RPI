#!/usr/bin/env bash
# usage: watch [command] [sleep duration]

t1=$(date -r "./configs/$1.cfg" +%s)
change=0
echo $t1
#echo "$1"


ps -ef | pgrep -f  player.py | xargs sudo kill -9;
setsid sudo python /home/pi/RPI/sequenceplayer.py "$@"
sudo python3 player.py -mname studio-mac -path ./ -cfg "$1.cfg"& 

  	
while change==0
do 
  t2=$(date -r "./configs/$1.cfg" +%s)
  if [ "$t2" != "$t1" ]
  then 
  	echo "CHANGED"
  	change=1
  	t1=$(date -r "./configs/$1.cfg" +%s)
  	ps -ef | pgrep -f  player.py | xargs sudo kill -9;
  	setsid sudo python /home/pi/RPI/sequenceplayer.py "$@"
  	sudo python3 player.py -mname studio-mac -path ./ -cfg "$1.cfg"& 
  	#break
  fi
  sleep ${2:-1}
done