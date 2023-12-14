#!/bin/sh
# Changes based on machine setup
path="/Users/lamshell/Documents/Dev/LEDELI/RPI/"
configGroup=""
machine="local"
pieceFileName="http://localhost:8888/projects/rpi-controls/local-status.cfg"
brightnessFile="http://localhost:8888/projects/rpi-controls/local-controlstatus.cfg"
pieceFileName="https://lukelab.com/projects/rpi-controls/local-status.cfg"
brightnessFile="https://lukelab.com/projects/rpi-controls/local-controlstatus.cfg"

## Set crontab -e to */1 * * * * /Documents/RPI/cntrlscripts/remotemngr/remotecontrol.sh
DIR="${BASH_SOURCE%/*}"
if [[ ! -d "$DIR" ]]; then DIR="$PWD"; fi
. "$DIR/main.sh"
#. $path"/cntrlscripts/remotemngr/main.sh"