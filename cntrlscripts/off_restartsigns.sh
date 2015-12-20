#
ps -eaf | pgrep python | xargs sudo kill
sleep 1
/home/pi/RPI/cntrlscripts/run.sh blend
