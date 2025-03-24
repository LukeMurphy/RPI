echo "==>shutting down <=="
ps -ef | pgrep -f player.py | xargs kill -9