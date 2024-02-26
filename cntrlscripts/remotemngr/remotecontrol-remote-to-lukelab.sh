#!/bin/sh
configGroup=""
machine="local"

# Where the player and configs all live -- changes based on machine setup
path="/home/daemon90/Documents/RPI/"
path="/Users/lamshell/Documents/Dev/LEDELI/RPI/"

# Where the control scripts live
controlPath="/home/daemon90/Documents/remotemngr/"
controlPath="/Users/lamshell/Documents/Dev/LEDELI/RPI/cntrlscripts/remotemngr/"

# Local file with name of cfg file to check and update
localConfigNameFile="/home/daemon90/Documents/remotemngr/localvalue.cfg"
localConfigNameFile="/Users/lamshell/Documents/Dev/LEDELI/RPI/cntrlscripts/remotemngr/localvalue.cfg"

# Local file with the brightness override
localControlConfigFileName="/home/daemon90/Documents/remotemngr/localvaluecontrol.cfg"
localControlConfigFileName="/Users/lamshell/Documents/Dev/LEDELI/RPI/cntrlscripts/remotemngr/localvaluecontrol.cfg"

# Remote file to check
pieceFileName="https://lukelab.com/projects/rpi-controls/local-status.cfg"

# Remote brightness file to check
brightnessFile="https://lukelab.com/projects/rpi-controls/local-controlstatus.cfg"
# . /home/daemon90/Documents/remotemngr/main.sh
. /Users/lamshell/Documents/Dev/LEDELI/RPI/cntrlscripts/remotemngr/main.sh