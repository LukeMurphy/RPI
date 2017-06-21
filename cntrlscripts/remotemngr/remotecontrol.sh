#!/bin/sh
#!/bin/bash
# Remote reader
path="/home/lukr/Documents/RPI/"
configGroup="configs/p4-4x4/"
machine="daemon4"

remotevalue=$(curl -A "Mozilla/5.0 (Windows NT 5.1; rv:21.0) Gecko/20130401 Firefox/21" "http://www.lukelab.com/projects/rpi-controls/daemon4-status.cfg")
localvalue=$(cat /home/lukr/Documents/RPI/cntrlscripts/remotemngr/localvalue.cfg)
echo $remotevalue
echo $localvalue
if [ $remotevalue != $localvalue ]
then
    echo "NOT THE SAME"
    echo -n $remotevalue > /home/lukr/Documents/RPI/cntrlscripts/remotemngr/localvalue.cfg

    ps -ef | pgrep python | xargs sudo kill -9;

    if test $remotevalue = "fludd"
    then
        config="fludd.cfg"
    fi

    if test  $remotevalue = "marquee"
    then
        config="marquee.cfg"
    fi

    if test  $remotevalue = "repaint"
    then
        config="repaint.cfg"
    fi

    if test  $remotevalue = "flames"
    then
        config="img-hub.cfg"
    fi

    execString=$path"player.py "$machine" "$path" "$path$configGroup$config
    echo $execString

    DISPLAY=:0 python $execString&
fi
