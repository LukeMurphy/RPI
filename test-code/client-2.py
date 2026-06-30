# Source - https://stackoverflow.com/a/58528177
# Posted by John, modified by community. See post 'Timeline' for change history
# Retrieved 2026-06-28, License - CC BY-SA 4.0

#!/usr/bin/env python3

import socket
import sys 
import time
import random
with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as client:
    client.connect("/tmp/my_socket")
    r = random.randint(1, 12)
    for i in range(r):
        msg = f"Client 2: hi {i}\n"
        client.send(msg.encode())
    time.sleep(1)
    client.close()
