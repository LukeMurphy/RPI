#!/bin/sh
echo "\n*************"
# Pull the local value -- not totatlly safe if it gets overriden with something wrong or unsafe...
localWorkValue=$(cat "${localMachine}Documents/remotemngr/local-work.txt")
localBrightnessValue=$(cat "${localMachine}Documents/remotemngr/local-brightness.txt")

path="${localMachine}Documents/RPI/"

# set the remote to be a default
workToPlay=$(curl -s -m 10 -A "Mozilla/5.0 (Windows NT 5.1; rv:21.0) Gecko/20130401 Firefox/21" "${piecePath}local-work.txt")
workBrightnessControl=$(curl -s -m 10 -A "Mozilla/5.0 (Windows NT 5.1; rv:21.0) Gecko/20130401 Firefox/21" "${piecePath}local-brightness.txt")
# status=$?

# MUST DO THIS TO LINUX MACHINE FOR SHUTDOWN TO WORK
# sudo visudo
# user_name ALL=(ALL) NOPASSWD: /sbin/poweroff, /sbin/reboot, /sbin/shutdown

runScript=0
player="player.py"
# if curl is ok, set the remote value

if [ $1 = "startup" ] || [ $1 = "cron" ]; then
    echo "OK -- CHECKINGs..."
    echo "-----------------------"
    echo "local work:" $localWorkValue
    echo "Local brightness:" $localBrightnessValue
    echo "-----------------------"
    echo "Remote work:" $workToPlay
    echo "Remote brightness:" $workBrightnessControl
    configToUse=$localWorkValue
    brightnessConfig=$localBrightnessValue

    if [ $brightnessConfig = '' ]; then
        brightnessConfig = 1
    fi


    sub="--manifest.cfg"
    if [ $1 = 'startup' ]; then
        runScript=1
        case "$configToUse" in
                *"$sub"*)
                player="sequencer.v2.py"
                echo "MATCH";;
                *)
                echo "NO MATCH"
                ;;
        esac
        execString="${path}${player} -mname ${machine} -path ${path} -cfg ${configToUse} -brightnessOverride ${brightnessConfig}"
    fi


    if [ $workToPlay != $localWorkValue ] || [ $workBrightnessControl != $localBrightnessValue ]; then
        if [ $workToPlay = 'Shutdown' ]; then
            echo "==>shutting down <=="
            ps -ef | pgrep -f player.py | xargs kill -9
            # echo "x" > $controlPath"localWorkValue.cfg"
            # echo "50" > $controlPath"localBrightnessValue.cfg"
            echo admin000 | sudo -S shutdown -h now
        fi
        if [ $workToPlay = 'Restart' ]; then
            echo "==>restarting <=="
            ps -ef | pgrep -f player.py | xargs kill -9
            # echo "x" > $controlPath"localWorkValue.cfg"
            # echo "50" > $controlPath"localBrightnessValue.cfg"
            echo admin000 | sudo -S shutdown -r now
        fi
        if [ $workToPlay = 'update' ]; then
            echo "==> RUN UPDATE <=="
            ps -ef | pgrep -f player.py | xargs kill -9
            git -C $path pull
            # echo "x" > $controlPath"localWorkValue.cfg"
            # echo "50" > $controlPath"localBrightnessValue.cfg"
        fi
        if [ $workToPlay != 'update' ]; then
            echo "==> NOT THE SAME or STARTING UP"
            echo $workToPlay >$controlPath"localWorkValue.cfg"
            echo $workBrightnessControl >$controlPath"localBrightnessValue.cfg"
            configToUse=$remotevalue
            brightnessConfig=$workBrightnessControl
            ps -ef | pgrep -f player.py | xargs kill -9
            if [ $configToUse == *"--manifest"* ]; then
                player="sequence-player.py"
            fi
            execString="${path}${player} -mname ${machine} -path ${path} -cfg ${configToUse} -brightnessOverride ${brightnessConfig}"
            # config=$remotevalue
            runScript=1
        fi
    fi
    if [ $runScript -eq 1 ]; then
        echo "==> Will run:"
        echo $execString
        echo "\n\n"
        # export DISPLAY=:0; /usr/bin/python3 $execString&
        python3 $execString &
    fi
fi
