# Source - https://stackoverflow.com/a/58528177
# Posted by John, modified by community. See post 'Timeline' for change history
# Retrieved 2026-06-28, License - CC BY-SA 4.0

#!/usr/bin/env python3

import socket
import sys 
import time

with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as client:
    client.connect("/tmp/my_socket")
    client.send(b"Client 1: hi\n")
    time.sleep(1)
    client.close()
