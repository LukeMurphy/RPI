# Source - https://stackoverflow.com/a/58528177
# Posted by John, modified by community. See post 'Timeline' for change history
# Retrieved 2026-06-28, License - CC BY-SA 4.0

#!/usr/bin/env python3

from socketserver import UnixStreamServer, StreamRequestHandler, ThreadingMixIn
import os
import time

try:
    os.unlink("/tmp/my_socket") 
    # comment: 
except Exception as e:
    print(e)
# end try

class Handler(StreamRequestHandler):
    def handle(self):
        # while True:
        print(self.rfile.readlines())
        msg = self.rfile.readline().strip()
        # _l = self.rfile.readlines()
        # for l in _l :
        #     print(f"lines: {l}")
        if msg:
            print(f"\nData Recieved from client is: {msg}")
        # else:
        #     return
        time.sleep(1)

class ThreadedUnixStreamServer(ThreadingMixIn, UnixStreamServer):
    pass

with ThreadedUnixStreamServer('/tmp/my_socket', Handler) as server:
    server.serve_forever()
