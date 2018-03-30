#!/bin/bash
ps -eaf | pgrep Python | xargs sudo kill;
sleep 1
sudo shutdown -r now
