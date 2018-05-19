#
ps -eaf | pgrep Python | xargs sudo kill -9;
sleep 3
sudo python3 /home/pi/RPI/player.py &