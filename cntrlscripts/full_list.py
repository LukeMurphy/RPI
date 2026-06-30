import os
import subprocess
import json
import select
import datetime
import sys
import threading
import time
from multiprocessing import Manager


import tkinter as tk
from tkinter import Listbox
from tkinter import Scrollbar
from tkinter import Text
from tkinter import Button
from tkinter import END
from tkinter import OUTSIDE
from tkinter import RIGHT
from tkinter import BOTH
from tkinter import font

# import tkmacosx
from tkmacosx import Button

# Tracks running piece processes: config_path -> subprocess.Popen
running_procs = {}

_defaultClr = "#5d7982"
_defaultClr = "#029eed"
_stopAndRun = "#0277ed"
_quitClr = "#74144c"
_stopAllClr = "#9e1b67"

_prodColor = "#85f3d6"
_stagingColor = "#fafad3"
_devFormsClr = "#3bdde2"
_devClr = "#cef7f8"
_devFormsClr = "#79fcf3"
_devOnDeckClr = "#ccFF00"
_screenGridClr = "#eeeeee"
_reference = "#adc4fd"


class bcolors:
    HEADER = "\033[95m"
    OKBLUE = "\033[94m"
    OKGREEN = "\033[92m"
    WARNING = "\033[93m"
    FAIL = "\033[95m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"


"""Summary

Attributes:
    actionDict1 (TYPE): Description
    actionDict2 (TYPE): Description
    commadStringMultiPyth (str): Description
    commadStringProc (str): Description
    commadStringPyth (str): Description
    JavaAppRunning (str): Description
    ListBoxOfConfigs (TYPE): Description
    leftBtnPlace (int): Description
    quitbutton (TYPE): Description
    root (TYPE): Description
    scrollbar (TYPE): Description
    slogan (TYPE): Description
    sortbutton (TYPE): Description
    sortDefault (int): Description
    topBtnPlace (int): Description
"""

commadStringProc = ""
JavaAppRunning = ""
configPath = "/Users/lamshell/Documents/Dev/LEDELI/RPI/configs/"


actionDict1 = [
    # {"--- Police Line 2 --------": "p10-line/flow-1.cfg"},
    {"SCREEN TEST ": "screens/test-448x320.cfg"},
]

actionDict2 = [
    {"SCREEN TEST ": "screens/test-448x320.cfg"},
]


def verify():
    # print("==>",Lb.curselection())
    global actionDict1
    process = False
    configSelected = None
    if list(ListBoxOfConfigs.curselection()):
        selection = ListBoxOfConfigs.curselection()[0]
        configSelected = actionDict1[selection]
        process = True
    # elif len(list(Lb2.curselection())) > 0:
    #     selection = Lb2.curselection()[0]
    #     configSelected = actionDict2[selection]
    #     process = True
    return (process, configSelected)


'''
# --------------------------------------------------------------------- #
from multiprocessing.managers import BaseManager

class _SharedList:
    def __init__(self):
        self._data = []

    def get_all(self):
        # print(f"[server] get_all id(self)={id(self)} data={self._data}", flush=False)
        return list(self._data)
    
    def append(self, item):
        self._data.append(item)
        print(f"[server] append id(self)={id(self)} data now={self._data}", flush=True)

    def setListValue(self, item):
        self._data.append(item)
        print(f"[server] append id(self)={id(self)} data now={self._data}", flush=True)

    def clear(self):
        self._data.clear()

class _SharedDict:
    def __init__(self):
        self._data = {}

    def get_all(self):
        return dict(self._data)

    def set(self, key, value):
        print(f"..[server] setting {key} {value}")
        self._data[key] = value

    def get(self, key, default=None):
        return self._data.get(key, default)

    def clear(self):
        self._data.clear()

_shared_state = _SharedList()
_shared_dict = _SharedDict()

def _shared_dict_factory():
    return _shared_dict

def _shared_list_factory():
    return _shared_state

class localManager(BaseManager):
    pass

localManager.register('sharedlist', callable=_shared_list_factory, exposed=['get_all', 'append', 'clear','setListValue'])
localManager.register('shareddict', callable=_shared_dict_factory, exposed=['get_all', 'set', 'get', 'clear'])

manager = localManager(address=('127.0.0.1', 50000), authkey=b'secret')
_manager_server = manager.get_server()

threading.Thread(target=_manager_server.serve_forever, daemon=True).start()
manager.connect()

_sharedlist = manager.sharedlist()
_sharedlist.append("SERVER_INIT")

_shareddict = manager.shareddict()

_shareddict.set("bg", "")
_shareddict.set("cmd", "")
_shareddict.set("p1Change", False)
_shareddict.set("p2Change", False)
_shareddict.set("p3Change", False)
_shareddict.set("p4Change", False)

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


# def poll_pieces():
#     # print("polling...")
#     # print(running_procs.items())
#     for cfg, proc in list(running_procs.items()):
#         # log_message(proc.stdout)
#         if proc.poll() is not None:
#             log_message(f"[stopped] {cfg.split(configPath)[1]}")
#             del running_procs[cfg]
#             continue
#         ready, _, _ = select.select([proc.stdout], [], [], 0)
#         if ready:
#             line = proc.stdout.readline()
#             if line:
#                 log_message(f"[piece] {line.rstrip()}")
    # root.after(100, poll_pieces)




def send_typed_message():
    raw = MsgEntry.get().strip()
    # if not raw:
    #     return
    # try:
    #     msg = json.loads(raw)
    # except json.JSONDecodeError:
    #     msg = {"cmd": raw}
    # send_to_piece(msg)
    # MsgEntry.delete(0, END)

    # _sharedlist.append(raw)
    # print(f"[sent] {raw} → list now: {_sharedlist.get_all()}", flush=True)

    if raw in ["red","rnd"] :
        _shareddict.set("bg", raw)
    if raw in ["reset"] :
        _shareddict.set("p1Change", False)
        _shareddict.set("p2Change", False)
        _shareddict.set("p3Change", False)
        _shareddict.set("p4Change", False)
        _shareddict.set("bg", "")

# --------------------------------------------------------------------- #
'''
def log_message(text):
    print(f">> {text}")
    # MsgLog.config(state="normal")
    # MsgLog.insert(END, text + "\n")
    # MsgLog.see(END)
    # MsgLog.config(state="disabled")


def execute(configToRun):
    log_message(f"{bcolors.WARNING}")
    log_message("\n\n---------------------------------------------------------------------------------------")
    log_message("full_list.py app window is calling this to run: ")
    log_message(configToRun.split(configPath)[1])

    global JavaAppRunning
    base = "/Users/lamshell/Documents/Dev/LEDELI/RPI/"
    cfg_rel = configToRun.split(configPath)[1]

    if ".cfg" in configToRun:
        if "multi" in configToRun:
            log_message("MULTIPLAYER STARTING >>>\n")
            cmd = ["python3", "-u", base + "multiplayer.py", "-path", base, "-mname", "studio", "-cfg", cfg_rel]
        elif "--manifest" in configToRun:
            cmd = ["python3", "-u", base + "sequencer.v2.py", "-path", base, "-mname", "studio", "-cfg", cfg_rel]
            log_message(" ".join(cmd))
        else:
            cmd = ["python3", "-u", base + "player.py", "-path", base, "-mname", "studio", "-cfg", cfg_rel]


        # with Manager() as manager:
        #     shared_list = manager.list()
        #     shared_dict = manager.dict()

        # proc = subprocess.Popen(cmd, 
        #                         stdin=subprocess.PIPE, 
        #                         stdout=subprocess.PIPE, 
        #                         stderr=subprocess.STDOUT, 
        #                         text=True, 
        #                         bufsize=1)

        proc = subprocess.Popen(cmd, text=True, bufsize=1)
        running_procs[configToRun] = proc
        log_message(f"[started] {cfg_rel}")

        # --- old os.system launches ---
        # if "multi" in configToRun:
        #     commadStringMultiPyth = "python3 /Users/lamshell/Documents/Dev/LEDELI/RPI/multiplayer.py -path /Users/lamshell/Documents/Dev/LEDELI/RPI/ -mname studio -cfg "
        #     os.system(commadStringMultiPyth + configToRun.split(configPath)[1] + "&")
        # if "--manifest" in configToRun:
        #     commadStringSeqPyth = "python3 /Users/lamshell/Documents/Dev/LEDELI/RPI/sequencer.v2.py -path /Users/lamshell/Documents/Dev/LEDELI/RPI/ -mname studio -cfg "
        #     print(commadStringSeqPyth + configToRun.split(configPath)[1] + "&")
        #     os.system(commadStringSeqPyth + configToRun.split(configPath)[1] + "&")
        # else:
        #     commadStringPyth = "python3 /Users/lamshell/Documents/Dev/LEDELI/RPI/player.py -path /Users/lamshell/Documents/Dev/LEDELI/RPI/ -mname studio -cfg "
        #     os.system(commadStringPyth + configToRun.split(configPath)[1] + "&")

    elif ".app" in configToRun:
        os.system(f"open {commadStringProc}{configToRun.split(configPath)[1]}")
        JavaAppRunning = configToRun.split(configPath)[1]

    print(f"---------------------------------------------------------------------------------------\n\n\n{bcolors.ENDC}")


def action():
    a = verify()
    if a[0]:
        # os.system('ps -ef | pgrep -f player | xargs sudo kill -9;')
        configSelected = a[1]
        configToRun = configSelected[list(configSelected.keys())[0]]
        execute(configToRun)


def action2():
    global JavaAppRunning
    a = verify()
    if a[0]:
        os.system("ps -ef | pgrep -f player | xargs sudo kill -9;")
        os.system("ps -ef | pgrep -f Player | xargs sudo kill -9;")

        if JavaAppRunning != "":
            os.system(f"ps -ef | pgrep -f {JavaAppRunning} | xargs sudo kill -9;")

        configSelected = a[1]
        configToRun = configSelected[list(configSelected.keys())[0]]
        execute(configToRun)


def clear():
    Txt.delete("1.0", "1.20")


def stopAll():
    # print("Tkinter is easy to use!")
    os.system("ps -ef | pgrep -f player | xargs sudo kill -9;")
    os.system("ps -ef | pgrep -f sequencer | xargs sudo kill -9;")


def sortByDate():
    filterText = Txt.get("1.0", "end-1c")
    getAllConfigFiles(True, False, filterText)


def sortByFolder():
    filterText = Txt.get("1.0", "end-1c")
    getAllConfigFiles(False, False, filterText)


def sortByFolderAndDate():
    getAllConfigFiles(False, True)


def openFile():
    a = verify()
    if a[0]:
        # os.system('ps -ef | pgrep -f player | xargs sudo kill -9;')
        configSelected = a[1]
        # os.system("open " + "configs/" + configSelected[list(configSelected.keys())[0]])
        os.system(f"open {configSelected[list(configSelected.keys())[0]]}")


def ondeck(arg, _dateSort=True, _subsortDate=True):
    getAllConfigFiles(dateSort=_dateSort, subsortDate=_subsortDate, filterText=arg)


def returnFirstElement(arg):
    return arg[0]


# Generate list of configs:


def returnSecondElement(arg):
    return arg[1]


def getAllConfigFiles(dateSort=False, subsortDate=False, filterText=""):
    global actionDict1, ListBoxOfConfigs, configPath

    fullList = _get_config_files(configPath, filterText)

    if dateSort:
        fullList.sort(key=returnSecondElement, reverse=True)
    else:
        fullList.sort(key=returnFirstElement, reverse=False)

    actionDict1 = _create_action_dict(fullList, dateSort, configPath)

    ListBoxOfConfigs.delete(0, END)
    for item in actionDict1:
        _update_listbox(ListBoxOfConfigs, item)


def _get_config_files(configPath, filterText):
    fullList = []
    filterResults = len(filterText) > 1
    for root, dirs, files in os.walk(configPath, topdown=False):
        for name in files:
            fullPath = os.path.join(root, name)
            if name.endswith(".cfg") and not name.endswith(".py") and name != ".DS_Store":
                res = os.stat(fullPath)
                if "asset_configs" not in fullPath and "/marks" not in fullPath and "/textures" not in fullPath and "/colors" not in fullPath and "/disturbances" not in fullPath:
                    if not filterResults and "non_working" not in fullPath:
                        fullList.append((fullPath, res.st_mtime, name))
                    elif name.find(filterText) > 0 or fullPath.find(filterText) > 0:
                        if filterText == "non_working" and "non_working" in fullPath or "non_working" not in fullPath:
                            fullList.append((fullPath, res.st_mtime, name))
    return fullList


def _create_action_dict(fullList, dateSort, configPath):
    actionDict = [{"": ""}]
    lastDir = ""
    for f in fullList:
        if f:
            tsTxt = datetime.datetime.fromtimestamp(f[1]).strftime("%Y-%m-%d [%H:%M]")
            currentDir = os.path.dirname(f[0].split(configPath)[1]).lstrip("/")
            if currentDir != lastDir and not dateSort:
                actionDict.append({"": ""})
                lastDir = currentDir
            actionDict.append({f"{tsTxt}\t{f[2]}\t\t [{currentDir}]": f[0]})
            # actionDict.append({f"{tsTxt}\t\t{currentDir} \t\t\t\t \t\t\t\t{f[2]}": f[0]})
        else:
            actionDict.append({"": ""})
    return actionDict


def _update_listbox(ListBoxOfConfigs, item):
    ListBoxOfConfigs.insert(END, f" {list(item.keys())[0]}")
    key = list(item.keys())[0]
    ListBoxOfConfigs.itemconfig(END, bg=_prodColor if "prod" in key else "white")
    ListBoxOfConfigs.itemconfig(END, bg=_stagingColor if "staging" in key else None)
    ListBoxOfConfigs.itemconfig(END, bg=_devClr if "dev/" in key else None)
    ListBoxOfConfigs.itemconfig(END, bg=_devFormsClr if "forms" in key else None)
    ListBoxOfConfigs.itemconfig(END, bg=_devOnDeckClr if "dev_ondeck" in key else None)
    ListBoxOfConfigs.itemconfig(END, bg=_screenGridClr if "screen_grid" in key else None)
    ListBoxOfConfigs.itemconfig(END, bg=_reference if "reference-configs" in key else None)


# -------------------------------- #
# Setup the TKINTER window
root = tk.Tk()
# frame = tk.Frame(root, bg="darkgray")
# frame.pack(padx=1, pady=1)
# width x height x X x Y

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

root.geometry(
    "%dx%d+%d+%d"
    % (
        960,
        320,
        # round(screen_height * 0.6),
        round(screen_width - 970),
        round(1 * screen_height / 2),
    )
)
def_font = tk.font.nametofont("TkDefaultFont")
def_font.config(size=12)
root.config(bg="white")

# -------------------------------- #
# Setup the main listBox widget
ListBoxOfConfigs = Listbox(root, width=110, height=42, bg="white", foreground="black", bd=False)

# for item in actionDict1:
    # ListBoxOfConfigs.insert(END, f" {list(item.keys())[0]}")
    # ListBoxOfConfigs.itemconfig(END, {"bg": "red"})

ListBoxOfConfigs.place(bordermode=OUTSIDE, x=2, y=14)

# -------------------------------- #
scrollbar = Scrollbar(root)
scrollbar.pack(side=RIGHT, fill=BOTH)
ListBoxOfConfigs.config(yscrollcommand=scrollbar.set)
scrollbar.config(command=ListBoxOfConfigs.yview)

topBtnPlace = 8
leftBtnPlace = 830

# sort by directory is 1 sort all by date is 0
sortDefault = 1

# -------------------------------- #
slogan = Button(root,text="Stop & Run",width=120,bg=_stopAndRun,fg="white",borderless=1,command=action2,
)
slogan.place(bordermode=OUTSIDE, x=leftBtnPlace, y=topBtnPlace)

# -------------------------------- #
slogan = Button(root, text="Run", width=120, bg=_stopAndRun, fg="white", borderless=1, command=action)
slogan.place(bordermode=OUTSIDE, x=leftBtnPlace, y=topBtnPlace + 25)

# -------------------------------- #
openbutton = Button(root,text="Open",width=120,bg=_defaultClr,fg="white",borderless=1,command=openFile,
)
openbutton.place(bordermode=OUTSIDE, x=leftBtnPlace, y=topBtnPlace + 50)

# -------------------------------- #
sortbutton1 = Button(root,text="Sort By Date",width=120,bg=_defaultClr,fg="white",borderless=1,command=sortByDate,
)
sortbutton1.place(bordermode=OUTSIDE, x=leftBtnPlace, y=topBtnPlace + 75)

# -------------------------------- #
sortbutton2 = Button(root,text="Sort by Folder",width=120,bg=_defaultClr,fg="white",borderless=1,command=sortByFolder,
)
sortbutton2.place(bordermode=OUTSIDE, x=leftBtnPlace, y=topBtnPlace + 100)

sortbutton3 = Button(root,text="Sort by Folder+",width=120,bg=_defaultClr,fg="white",borderless=1,command=sortByFolderAndDate,
)
sortbutton3.place(bordermode=OUTSIDE, x=leftBtnPlace, y=topBtnPlace + 150)
# -------------------------------- #
# -------------------------------- #
ondeckButton = Button(root, text="non-working", width=120, bg=_devOnDeckClr, fg="#000000", borderless=1, command=lambda: ondeck("non_working"))
ondeckButton.place(bordermode=OUTSIDE, x=leftBtnPlace, y=topBtnPlace + 125)

ondeckButton = Button(root, text="Staging", width=120, bg=_stagingColor, fg="#000000", borderless=1, command=lambda: ondeck("staging"))
ondeckButton.place(bordermode=OUTSIDE, x=leftBtnPlace, y=topBtnPlace + 150)

prodButton = Button(root, text="Production", width=120, bg=_prodColor, fg="#000000", borderless=1, command=lambda: ondeck("prod"))
prodButton.place(bordermode=OUTSIDE, x=leftBtnPlace, y=topBtnPlace + 175)

devButton = Button(root, text="Dev", width=120, bg=_devClr, fg="#000000", borderless=1, command=lambda: ondeck("dev"))
devButton.place(bordermode=OUTSIDE, x=leftBtnPlace, y=topBtnPlace + 200)

refButton = Button(root, text="Reference", width=120, bg=_reference, fg="#000000", borderless=1, command=lambda: ondeck("reference", False))
refButton.place(bordermode=OUTSIDE, x=leftBtnPlace, y=topBtnPlace + 225)

# -------------------------------- #
slogan = Button(root,text="Stop All",width=120,bg=_stopAllClr,fg="white",borderless=1,command=stopAll,
)
slogan.place(bordermode=OUTSIDE, x=leftBtnPlace, y=topBtnPlace + 250)

# -------------------------------- #
quitbutton = Button(root, text="QUIT", width=120, bg=_quitClr, fg="white", borderless=1, command=quit)
quitbutton.place(bordermode=OUTSIDE, x=leftBtnPlace, y=topBtnPlace + 275)


# -------------------------------- #
# Filter text box
Txt = Text(root, height=1, width=32, bg="white", fg="black", bd=False, padx=4, pady=4)
Txt.place(bordermode=OUTSIDE, x=2, y=2)
clearButton = Button(root,text="Clear",width=120,bg=_defaultClr,fg="white",borderless=True,command=clear,
)
clearButton.place(bordermode=OUTSIDE, x=280, y=2)

# -------------------------------- #



'''
# -------------------------------- #
# Message log + send box (below the main list)
# MsgLog = Text(root, height=5, width=110, bg="#111111", fg="#00ff88", bd=False, padx=4, pady=4, state="disabled")
# MsgLog.place(bordermode=OUTSIDE, x=2, y=530)

MsgEntry = tk.Entry(root, width=20, bg="#222222", fg="white", bd=False)
MsgEntry.place(bordermode=OUTSIDE, x=420, y=5)
MsgEntry.bind("<Return>", lambda _e: send_typed_message())

sendButton = Button(root, text="Send", width=80, bg=_defaultClr, fg="white", borderless=1, command=send_typed_message)
sendButton.place(bordermode=OUTSIDE, x=600, y=5)
'''





# sort by date = True,
getAllConfigFiles(True, True)

# -------------------------------- #
# root.after(200, poll_pieces)
root.mainloop()
