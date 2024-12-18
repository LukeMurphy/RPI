#!/bin/sh
configGroup=""
machine="local"

# Where the player and configs all live -- changes based on machine setup
path="/home/daemon102/Documents/RPI/"
# path="/Users/lamshell/Documents/Dev/LEDELI/RPI/"

# Where the control scripts live
controlPath="/home/daemon102/Documents/remotemngr/"
# controlPath="/Users/lamshell/Desktop/remotemngr/"

# Local file with name of cfg file to check and update
localConfigNameFile="/home/daemon102/Documents/remotemngr/localvalue.cfg"
# localConfigNameFile="/Users/lamshell/Desktop/remotemngr/localvalue.cfg"

# Local file with the brightness override
localControlConfigFileName="/home/daemon102/Documents/remotemngr/localvaluecontrol.cfg"
# localControlConfigFileName="/Users/lamshell/Desktop/remotemngr/localvaluecontrol.cfg"

# Remote file to check
pieceFileName="https://lukelab.com/projects/rpi-controls/p3-informal-abstraction/local-status.cfg"

# Remote brightness file to check
brightnessFile="https://lukelab.com/projects/rpi-controls/p3-informal-abstraction/local-controlstatus.cfg"

. /home/daemon102/Documents/remotemngr/main.sh
# . /Users/lamshell/Documents/Dev/LEDELI/RPI/cntrlscripts/remotemngr/main.sh