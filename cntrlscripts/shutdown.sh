#!/bin/bash
echo "Shutting Down Python scripts"
ps -eaf | pgrep python | xargs sudo kill -9;
sleep 1
echo "Doing shutdown / halt"
sudo shutdown -h now
