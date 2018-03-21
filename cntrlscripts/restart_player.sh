#
ps -eaf | pgrep python | xargs sudo kill;
sleep 3
sudo python3 /home/pi/RPI/player.py &