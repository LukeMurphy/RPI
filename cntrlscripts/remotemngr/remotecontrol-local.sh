#!/bin/sh
# Changes based on machine setup
path="/Users/lamshell/Documents/Dev/RPI/"
configGroup="/p4-4x4/"
machine="local"
pieceFileName="http://lukelab/projects/rpi-controls/local-status.cfg"
brightnessFile="http://lukelab/projects/rpi-controls/local-controlstatus.cfg"

## Set crontab -e to */1 * * * * /Documents/RPI/cntrlscripts/remotemngr/remotecontrol.sh
DIR="${BASH_SOURCE%/*}"
if [[ ! -d "$DIR" ]]; then DIR="$PWD"; fi
. "$DIR/main.sh"
#. $path"/cntrlscripts/remotemngr/main.sh"