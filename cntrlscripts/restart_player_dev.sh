#
ps -ef | pgrep -f player | xargs sudo kill -9;
ps -ef | pgrep -f player | xargs sudo kill -9;
sleep .5
python3 ~/Documents/Dev/LEDELI/RPI/player.py -mname studio -path ~/Documents/Dev/LEDELI/RPI/ -cfg "$@"