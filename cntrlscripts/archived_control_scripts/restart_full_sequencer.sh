#
ps -ef | pgrep python | xargs sudo kill -9;
sleep 1
/usr/bin/python3 /home/daemon57/Documents/RPI/sequence-player.py -mname d57 -path /home/daemon57/Documents/RPI -cfg prod/seq-humaniti-1.cfg "$@"
