ps -ef | pgrep -f player | xargs sudo kill -9;
sleep .5
echo "\n"
echo "---------------------------------------------------\n"
echo "restart_player_dev.sh is Calling Restart of Player\n"
echo "---------------------------------------------------\n"
echo "\n"
python3 ~/Documents/Dev/LEDELI/RPI/player.py -mname studio -path ~/Documents/Dev/LEDELI/RPI/ -cfg "$@"
exit