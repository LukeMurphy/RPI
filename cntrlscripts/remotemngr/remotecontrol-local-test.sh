#!/bin/sh
# Changes based on machine setup
path="/Users/lamshell/Documents/Dev/LEDELI/RPI/cntrlscripts/remotemngr/"
configGroup=""
machine="local"
pieceFileName="/Documents/RPI/cntrlscripts/remotemngr/localvalue.cfg"
brightnessFile="/Documents/RPI/cntrlscripts/remotemngr/localvaluecontrol"


## Set crontab -e to */1 * * * * /Documents/RPI/cntrlscripts/remotemngr/remotecontrol.sh
# DIR="${BASH_SOURCE%/*}"
# if [[ ! -d "$DIR" ]]; then DIR="$PWD"; fi
# . "$DIR/main.sh"
#. $path"/cntrlscripts/remotemngr/main.sh" 

pieceFileName="https://lukelab.com/projects/rpi-controls/p3-informal-abstraction/local-status.cfg"

# Remote brightness file to check
brightnessFile="https://lukelab.com/projects/rpi-controls/p3-informal-abstraction/local-controlstatus.cfg"

. /Users/lamshell/Documents/Dev/LEDELI/RPI/cntrlscripts/remotemngr/main.sh