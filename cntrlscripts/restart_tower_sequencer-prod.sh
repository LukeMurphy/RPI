#
ps -ef | pgrep python | xargs kill -9;
sleep 1
/usr/bin/python3 /home/daemon63/Documents/RPI/sequence-player.py -mname d63 -path /home/daemon63/Documents/RPI/ -cfg prod/seq-tower-line--manifest.cfg "$@"
