import subprocess
import json
import threading
import time
import random
from multiprocessing import Manager
from multiprocessing.managers import BaseManager



# --------------------------------------------------------------------- #
class localManager(BaseManager):
    pass

class _SharedList:
    def __init__(self):
        self._data = []

    def get_all(self):
        # print(f"[server] get_all id(self)={id(self)} data={self._data}", flush=False)
        return list(self._data)
    
    def append(self, item):
        self._data.append(item)
        # print(f"[server] append id(self)={id(self)} data now={self._data}", flush=True)

    def setListValue(self, item):
        self._data.append(item)
        # print(f"[server] append id(self)={id(self)} data now={self._data}", flush=True)

    def clear(self):
        self._data.clear()

class _SharedDict:
    def __init__(self):
        self._data = {}

    def get_all(self):
        return dict(self._data)

    def set(self, key, value):
        # print(f">> [server] _SharedDict.set() called {key} {value}")
        self._data[key] = value

    def get(self, key, default=None):
        return self._data.get(key, default)

    def clear(self):
        self._data.clear()

class SharedData:
    arbVar = "ok"

    def __init__(self):
        self._data = {}
    
    def publicAction(self):
        print(f"[server SharedData] called ok: {self.arbVar}")

def _shared_dict_factory():
    return _shared_dict

def _shared_list_factory():
    return _shared_state

def _sharedDatafactory():
    return _sharedData


# Tracks running piece processes: config_path -> subprocess.Popen
running_procs = {}
commadStringProc = ""
configPath = "/Users/lamshell/Documents/Dev/LEDELI/RPI/configs/"
_shared_state = _SharedList()
_shared_dict = _SharedDict()
_sharedData = SharedData()


localManager.register('sharedlist', callable=_shared_list_factory, exposed=['get_all', 'append', 'clear','setListValue'])
localManager.register('shareddict', callable=_shared_dict_factory, exposed=['get_all', 'set', 'get', 'clear'])
localManager.register('sharedData', callable=_sharedDatafactory, exposed=['publicAction'])

manager = localManager(address=('127.0.0.1', 50000), authkey=b'LEDDELI49')
_manager_server = manager.get_server()

threading.Thread(target=_manager_server.serve_forever, daemon=True).start()
manager.connect()

_sharedlist = manager.sharedlist()
_sharedlist.append("SERVER_INIT")

_shareddict = manager.shareddict()
_shareddict.set("p1-changed", False)
_shareddict.set("p2-changed", False)
_shareddict.set("p3-changed", False)
_shareddict.set("p4-changed", False)


# --------------------------------------------------------------------- #

def send_to_piece(msg: dict):
    if not running_procs:
        log_message("[no running pieces]")
        return
    for cfg, proc in list(running_procs.items()):
        if proc.poll() is None:
            proc.stdin.write(json.dumps(msg) + "\n")
            proc.stdin.flush()
            label = cfg.split(configPath)[1] if configPath in cfg else cfg
            log_message(f"[sent to {label}] {msg}")

def log_message(text):
    print(f">> {text}")

# def _resetPieces():
#     _shareddict.set("p1Change", False)
#     _shareddict.set("p2Change", False)
#     _shareddict.set("p3Change", False)
#     _shareddict.set("p4Change", False)
#     _shareddict.set("bg", "")


# def send_typed_message(raw):
#     raw = raw.strip()
#     _resetPieces()

#     if raw in ["red","rnd"] :
#         _shareddict.set("bg", raw)

#     if raw in ["reset"] :
#         _resetPieces()

# --------------------------------------------------------------------- #

def execute(configToRun):
    log_message("full_list.py app window is calling this to run: ")
    log_message(configToRun)

    base = "/Users/lamshell/Documents/Dev/LEDELI/RPI/"
    if "multi" in configToRun :
        cmd = ["python3", "-u", base + "multiplayer.py", "-path", base, "-mname", "studio", "-cfg", configToRun]
    else:
        cmd = ["python3", "-u", base + "player.py", "-path", base, "-mname", "studio", "-cfg", configToRun]

    proc = subprocess.Popen(cmd, text=True, bufsize=1)
    running_procs[configToRun] = proc
    log_message(f"[started] {configToRun}")


def main():
    cfgs = [
        "dev/p4-512px-in-parts/mngd_celestials-m-1.cfg"
        ,"dev/p4-512px-in-parts/mngd_celestials-m-2.cfg"
        ,"dev/p4-512px-in-parts/mngd_celestials-m-3.cfg"
        ,"dev/p4-512px-in-parts/mngd_celestials-m-4.cfg"
            ]
    # cfgs = ["dev/p4-512px-in-parts/multi-celestials.cfg"]
    
    # cfgs = [
    #     "dev/p4-512px-in-parts/hashing-marks-v3-m-1.cfg",
    #     "dev/p4-512px-in-parts/hashing-marks-v3-m-2.cfg",
    #     "dev/p4-512px-in-parts/hashing-marks-v3-m-3.cfg",
    #     "dev/p4-512px-in-parts/hashing-marks-v3-m-4.cfg"
    #         ]
    # cfgs = ["dev/p4-512px-in-parts/multi-hashing.cfg"]


    for cfg in cfgs :
        execute(cfg)

    while True:
        time.sleep(.3)

        # if random.random() < .02 :
        #     send_typed_message("rnd")


if __name__ == "__main__":
    main()




