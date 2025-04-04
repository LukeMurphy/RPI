#!/bin/sh
# MUST DO THIS TO LINUX MACHINE FOR SHUTDOWN TO WORK
# sudo visudo
# user_name ALL=(ALL) NOPASSWD: /sbin/poweroff, /sbin/reboot, /sbin/shutdown
configGroup=""
machine="local"

# local machine
localMachine="/home/daemon102/"

# Remote path to check
piecePath="https://lukelab.com/projects/rpi-controls/p3-informal-abstraction/"

pathToMain="${localMachine}Documents/RPI/cntrlscripts/remotemngr/main.sh"
. "${pathToMain}"