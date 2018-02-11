#!/bin/sh
# Changes based on machine setup
path="/home/lukr/Documents/RPI/"
configGroup="configs/p4-4x4/"
machine="daemon4"
pieceFileName="http://www.lukelab.com/projects/rpi-controls/lukr-status.cfg"
brightnessFile="http://www.lukelab.com/projects/rpi-controls/lukr-controlstatus.cfg"

## Set crontab -e to */1 * * * * /Documents/RPI/cntrlscripts/remotemngr/remotecontrol.sh
DIR="${BASH_SOURCE%/*}"
if [[ ! -d "$DIR" ]]; then DIR="$PWD"; fi
. "$DIR/main.sh"
#. "/home/lukr/Documents/RPI/cntrlscripts/remotemngr/main.sh"
