#
ps -eaf | pgrep python | xargs sudo kill;
sleep 3
sudo python /home/pi/RPI/player.py &