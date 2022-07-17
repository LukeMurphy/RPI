#
echo "*****************************"
echo "*****************************"
echo "*****************************"
echo "*****************************"
echo "*****************************"
echo "*****************************"
echo "*****************************"
echo "*****************************"
echo "*****************************"
echo "*****************************"
echo "*****************************"
echo "*****************************"
echo "*****************************"
echo "*****************************"
echo "*****************************"

ps -ef | pgrep -f player | xargs sudo kill -9;
ps -ef | pgrep -f player | xargs sudo kill -9;
sleep 1

#python3 /Users/lamshell/Documents/Dev/RPI/sequence-player.py -mname d57 -path /Users/lamshell/Documents/Dev/RPI/ -cfg __in_progress/industrial-incandescent--manifest.cfg
/usr/bin/python3 /home/daemon40/Documents/RPI/sequence-player.py -mname d40 -path /home/daemon40/Documents/RPI -cfg prod/industrial-incandescent--manifest.cfg "$@"
