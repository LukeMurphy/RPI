#!/bin/sh
# Changes based on machine setup
path="/home/daemon8/Documents/RPI/"
configGroup="configs/p4-4x4/"
machine="daemon8"
pieceFileName="http://www.lukelab.com/projects/rpi-controls/daemon8-status.cfg"
brightnessFile="http://www.lukelab.com/projects/rpi-controls/daemon8-controlstatus.cfg"

## Set crontab -e to */1 * * * * /Documents/RPI/cntrlscripts/remotemngr/remotecontrol.sh
DIR="${BASH_SOURCE%/*}"
if [[ ! -d "$DIR" ]]; then DIR="$PWD"; fi
. "$DIR/main.sh"
