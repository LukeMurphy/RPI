#
ps -eaf | pgrep python | xargs sudo kill;
sleep 1
sudo shutdown now