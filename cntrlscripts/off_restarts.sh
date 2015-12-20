#
ps -eaf | pgrep python | xargs sudo kill
sleep 1
sudo python /home/pi/RPI/sequence.py seq "$@"
