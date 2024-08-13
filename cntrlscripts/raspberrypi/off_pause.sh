#
ps aux | grep sequence | awk '{print $2}' | xargs sudo kill -9;
