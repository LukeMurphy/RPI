if [ $1 = "1" ]; then
    echo "==>starting "
    exec /home/daemon104/Documents/electron-quick-start-linux-x64/electron-quick-start
    ps -ef | pgrep -f player.py | xargs kill -9;
fi

if [ $1 = "2" ]; then
    echo "==>starting "
    /usr/bin/python3 /home/daemon104/Documents/RPI/player.py -cfg prod/p4-6x8-paintings.cfg
    ps -ef | pgrep -f electron | xargs kill -9;
fi