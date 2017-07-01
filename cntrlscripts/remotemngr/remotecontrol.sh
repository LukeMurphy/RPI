#!/bin/sh

## Set crontab -e to */1 * * * * /Documents/RPI/cntrlscripts/remotemngr/remotecontrol.sh

startingup="0"
if [ $# -ne 0 ]
    then
    if test $1 = "startup"
    then
        startingup="1"
    fi
fi

# Changes based on machine setup
#path="/home/lukr/Documents/RPI/"
path="/Users/lukemurphy/Documents/DEVTEMP/RPI/"
configGroup="configs/p4-4x4/"
machine="daemon4"

# Pull the local value -- not totatlly safe if it gets overriden with something wrong or unsafe...
localvalue=$(cat $path"cntrlscripts/remotemngr/localvalue.cfg")

# set the remote to be a default
remotevalue=$localvalue
remotecurlvalue=$(curl -s -m 10 -A "Mozilla/5.0 (Windows NT 5.1; rv:21.0) Gecko/20130401 Firefox/21" "http://www.lukelab.com/projects/rpi-controls/")
status=$?

echo $status
# if curl is ok, set the remote value
if [ $status -eq 0 ]
then
        echo "OK -- CHANGING..."
        remotevalue=$remotecurlvalue
        echo $remotevalue
fi

# choose the piece to play
if [ $remotevalue != $localvalue ] || [ "$startingup" -eq "1" ] ; then

    echo "NOT THE SAME or STARTING UP"
    echo $remotevalue > $path"cntrlscripts/remotemngr/localvalue.cfg"

    ps -ef | pgrep python | xargs kill -9;

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

    if test  $remotevalue = "machine"
    then
        config="machine.cfg"
    fi

    if test  $remotevalue = "hang"
    then
        config="hang.cfg"
    fi

    if test  $remotevalue = "stroop2"
    then
        config="stroop2.cfg"
    fi

    if test  $remotevalue = "XOs"
    then
        config="XOs.cfg"
    fi    

    if test  $remotevalue = "counter"
    then
        config="counter.cfg"
    fi

    execString=$path"player.py "$machine" "$path" "$path$configGroup$config
    #echo $execString

    DISPLAY=:0 python $execString&
fi
