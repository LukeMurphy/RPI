#
ps aux | grep sequence | awk '{print $2}' | xargs sudo kill -9;
sleep 1
sudo python /home/pi/RPI/sequence.py seq "$@"
