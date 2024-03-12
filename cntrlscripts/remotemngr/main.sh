#!/bin/sh
# Pull the local value -- not totatlly safe if it gets overriden with something wrong or unsafe...
localvalue=$(cat $localConfigNameFile)
localvalueControl=$(cat $localControlConfigFileName)

# set the remote to be a default
remotevalue=$(curl -s -m 10 -A "Mozilla/5.0 (Windows NT 5.1; rv:21.0) Gecko/20130401 Firefox/21" $pieceFileName)
remotevalueControl=$(curl -s -m 10 -A "Mozilla/5.0 (Windows NT 5.1; rv:21.0) Gecko/20130401 Firefox/21" $brightnessFile)
# status=$?


# MUST DO THIS TO LINUX MACHINE FOR SHUTDOWN TO WORK
# sudo visudo
# user_name ALL=(ALL) NOPASSWD: /sbin/poweroff, /sbin/reboot, /sbin/shutdown

echo "\n*************"
echo $1
#echo $2
echo $localConfigNameFile
echo $localvalue
echo $remotevalue
echo $controlPath
echo "*************\n"

runScript=0
player="player.py"
# if curl is ok, set the remote value

if [ $1 =  "startup" ] || [ $1 = "cron" ]
then
                echo "OK -- CHECKINGs..."
                echo "local value:" $localvalue
                echo "Local brightness:" $localvalueControl
                echo "Remote value:" $remotevalue
                echo "Remote brightness:" $remotevalueControl
        configToUse=$localvalue
        brightnessConfig=$localvalueControl
    if [ $1 = 'startup' ]
    then
    runScript=1
    if [ $configToUse = *"--manifest"* ]
    then player="sequencer.v2.py" 
    fi
    execString=$path$player" -mname "$machine" -path "$path" -cfg "$configToUse" -brightnessOverride "$brightnessConfig
    fi

    if [ $remotevalue != $localvalue ] || [ $remotevalueControl != $localvalueControl ]
    then
        if [ $remotevalue = 'Shutdown' ]
        then
            echo "==>shutting down <=="
            ps -ef | pgrep -f player.py | xargs kill -9;
            echo "x" > $controlPath"localvalue.cfg"
            echo "50" > $controlPath"localvaluecontrol.cfg"
            echo admin000 | sudo -S shutdown -h now
        fi
        if [ $remotevalue = 'update' ]
        then
            echo "==> RUN UPDATE <=="
            ps -ef | pgrep -f player.py | xargs kill -9;
            git -C $path pull
            echo "x" > $controlPath"localvalue.cfg"
            echo "50" > $controlPath"localvaluecontrol.cfg"
        fi
        if [ $remotevalue != 'update' ]
        then
            echo "==> NOT THE SAME or STARTING UP"
            echo $remotevalue > $controlPath"localvalue.cfg"
            echo $remotevalueControl > $controlPath"localvaluecontrol.cfg"
            configToUse=$remotevalue
            brightnessConfig=$remotevalueControl
            ps -ef | pgrep -f player.py | xargs kill -9;
            if [ $configToUse == *"--manifest"* ]
            then player="sequence-player.py"
            fi
            execString=$path$player" -mname "$machine" -path "$path" -cfg "$configToUse" -brightnessOverride "$brightnessConfig
            # config=$remotevalue
            runScript=1
        fi
    fi
    if [ $runScript -eq 1 ]
    then
        echo "==> Will run:"
        echo $execString
        echo "\n\n"
        # export DISPLAY=:0; /usr/bin/python3 $execString&
        python3 $execString&
    fi
fi