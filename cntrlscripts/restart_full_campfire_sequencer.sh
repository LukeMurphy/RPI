#
ps -ef | pgrep -f player.py | xargs kill -9;
sleep 1
python3 /Users/lamshell/Documents/Dev/LEDELI/RPI/sequence-player.py -mname d57 -path /Users/lamshell/Documents/Dev/RPI -cfg prod/seq-campfire-2.1.0.cfg "$@"
# /usr/bin/python3 /home/daemon60/Documents/RPI/sequence-player.py -mname d57 -path /home/daemon60/Documents/RPI -cfg prod/seq-campfire-2.1.0.cfg "$@"
