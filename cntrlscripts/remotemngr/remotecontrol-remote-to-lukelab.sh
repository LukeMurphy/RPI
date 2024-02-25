#!/bin/sh
configGroup=""
machine="local"

# Where the player and configs all live -- changes based on machine setup
path="/Users/lamshell/Documents/Dev/LEDELI/RPI/"

# Local file with name of cfg file to check and update
localConfigNameFile="/Users/lamshell/Documents/Dev/LEDELI/RPI/cntrlscripts/remotemngr/localvalue.cfg"

# Local file with the brightness override
localControlConfigFileName="/Users/lamshell/Documents/Dev/LEDELI/RPI/cntrlscripts/remotemngr/localvaluecontrol.cfg"

# Remote file to check
pieceFileName="https://lukelab.com/projects/rpi-controls/local-status.cfg"

# Remote brightness file to check
brightnessFile="https://lukelab.com/projects/rpi-controls/local-controlstatus.cfg"

## Set crontab -e to */1 * * * * /Documents/RPI/cntrlscripts/remotemngr/remotecontrol.sh
DIR="${BASH_SOURCE%/*}"
if [[ ! -d "$DIR" ]]; then DIR="$PWD"; fi
. "$DIR/main.sh"
#. $path"/cntrlscripts/remotemngr/main.sh"