import os
from os import listdir
from os.path import isfile, join, isdir
from os import walk
import datetime
import subprocess
import sys
import tkinter as tk
from tkinter import *
import tkmacosx
from tkmacosx import Button

# from tk import Button

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
    if len(list(ListBoxOfConfigs.curselection())) > 0:
        selection = ListBoxOfConfigs.curselection()[0]
        configSelected = actionDict1[selection]
        process = True
    # elif len(list(Lb2.curselection())) > 0:
    #     selection = Lb2.curselection()[0]
    #     configSelected = actionDict2[selection]
    #     process = True
    return (process, configSelected)


def execute(configToRun):

    commadStringPyth = "python3 /Users/lamshell/Documents/Dev/LEDELI/RPI/player.py -path /Users/lamshell/Documents/Dev/LEDELI/RPI/ -mname studio -cfg "
    commadStringMultiPyth = "python3 /Users/lamshell/Documents/Dev/LEDELI/RPI/multiplayer.py -path /Users/lamshell/Documents/Dev/LEDELI/RPI/ -mname studio -cfg "
    commadStringSeqPyth = "python3 /Users/lamshell/Documents/Dev/LEDELI/RPI/sequencer.v2.py -path /Users/lamshell/Documents/Dev/LEDELI/RPI/ -mname studio -cfg "

    print("--------------------------------------------")
    print("--------------------------------------------")
    print(configToRun.split(configPath)[1])
    print("--------------------------------------------")
    print("--------------------------------------------")
    """Summary

	Args:
	    configToRun (TYPE): Description
	"""
    global JavaAppRunning
    if ".cfg" in configToRun:
        if "multi" in configToRun:
            print("MULTIPLAYER STARTING >>>\n")
            os.system(commadStringMultiPyth +
                      configToRun.split(configPath)[1] + "&")
        if "--manifest" in configToRun:
            print(commadStringSeqPyth + configToRun.split(configPath)[1] + "&")
            os.system(commadStringSeqPyth +
                      configToRun.split(configPath)[1] + "&")
        else:
            os.system(commadStringPyth +
                      configToRun.split(configPath)[1] + "&")
    elif ".app" in configToRun:
        os.system("open " + commadStringProc +
                  configToRun.split(configPath)[1])
        JavaAppRunning = configToRun.split(configPath)[1]


def action():
    a = verify()
    if a[0] == True:
        # os.system('ps -ef | pgrep -f player | xargs sudo kill -9;')
        configSelected = a[1]
        configToRun = configSelected[list(configSelected.keys())[0]]
        execute(configToRun)


def action2():
    global JavaAppRunning
    a = verify()
    if a[0] == True:
        os.system("ps -ef | pgrep -f player | xargs sudo kill -9;")
        os.system("ps -ef | pgrep -f Player | xargs sudo kill -9;")

        if JavaAppRunning != "":
            os.system("ps -ef | pgrep -f " + JavaAppRunning +
                      " | xargs sudo kill -9;")

        configSelected = a[1]
        configToRun = configSelected[list(configSelected.keys())[0]]
        execute(configToRun)

def clear() :
    T.delete('1.0', '1.20')

def stopAll():
    # print("Tkinter is easy to use!")
    os.system("ps -ef | pgrep -f player | xargs sudo kill -9;")


def sortByDate():
    filterText = (T.get("1.0", "end-1c"))
    getAllConfigFiles(True, False, filterText)


def sortByFolder():
    filterText = (T.get("1.0", "end-1c"))
    getAllConfigFiles(False, False, filterText)


def sortByFolderAndDate():
    getAllConfigFiles(False, True)


def openFile():
    a = verify()
    if a[0] == True:
        # os.system('ps -ef | pgrep -f player | xargs sudo kill -9;')
        configSelected = a[1]
        # os.system("open " + "configs/" + configSelected[list(configSelected.keys())[0]])
        os.system("open " + configSelected[list(configSelected.keys())[0]])


def returnFirstElement(l):
    return l[0]

# Generate list of configs:


def returnSecondElement(l):
    return l[1]


def getAllConfigFiles(dateSort=False, subsortDate=False, filterText = ""):

    global actionDict1, ListBoxOfConfigs
    global configPath
    # arr = os.listdir(configPath)
    # Sort the directories by name
    # arr.sort(reverse=False)
    fullList = []
    actionDict1 = []
    
    filterResults = False
    if len(filterText) > 1 :
        filterResults = True
        
    for root, dirs, files in os.walk(configPath, topdown=False):
        for name in files:
            fullPath = os.path.join(root, name)
            if name.find(".cfg") > 0 and name.find(".py") == -1 and name.find(".DS_Store") == -1:
                res = os.stat(fullPath)
                
                if filterResults == False :
                    fullList.append((os.path.join(root, name), res.st_mtime, name))
                if filterResults == True :
                    if name.find(filterText) > 0 or fullPath.find(filterText) > 0:
                        fullList.append((os.path.join(root, name), res.st_mtime, name))


    # Sort the configs by date descending
    if dateSort == True:
        fullList.sort(key=returnSecondElement, reverse=True)
    else:
        fullList.sort(key=returnFirstElement, reverse=False)

    lastDir = ""
    fName = ""

    actionDict1.append({"": ""})

    for f in fullList:
        fName = f[0].split(configPath)[1].split('/')[0]
        if len(f) > 0:
            tsTxt = datetime.datetime.fromtimestamp(f[1]).strftime("%Y-%m-%d [%H:%M]")
            tsTxtVals = tsTxt.split(" ")
            
            # and dateSort != True
            currentDir = f[0].split(configPath)[1].split('/')[0]
            currDirLevel2 = f[0].split(configPath)[1].split('/')[1]
            if currDirLevel2.find(".cfg") <= 0 :
                    currentDir = currentDir + "/" + currDirLevel2
            if currentDir != lastDir and dateSort == False :
                actionDict1.append({"": ""})
                lastDir = currentDir

            actionDict1.append({tsTxt + "\t\t" + f[0].split(f[2])[0].split(configPath)[1]  + " \t\t\t\t \t\t\t\t" + f[2]: f[0]})
        else:
            actionDict1.append({"": ""})

    ListBoxOfConfigs.delete(0, END)
    for i, item in enumerate(actionDict1):
        # print(list(item.keys())[0])
        ListBoxOfConfigs.insert(END, " " + list(item.keys())[0])
        ListBoxOfConfigs.itemconfig(END, bg = "#ffeeea" if list(item.keys())[0].find("prod/") > 0 else "white" )
        ListBoxOfConfigs.itemconfig(END, bg = "#58fc00" if list(item.keys())[0].find("dev_forms/") > 0 else None )
        ListBoxOfConfigs.itemconfig(END, bg = "#58fcbd" if list(item.keys())[0].find("dev/") > 0 else None )
        ListBoxOfConfigs.itemconfig(END, bg = "#eeeeee" if list(item.keys())[0].find("screen_grid") > 0 else None )


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
        760,
        round(screen_height * 0.6),
        round(screen_width -800),
        round(1 * screen_height / 2),
    )
)
def_font = tk.font.nametofont("TkDefaultFont")
def_font.config(size=12)
root.config(bg="white")

# -------------------------------- #
# Setup the main listBox widget
ListBoxOfConfigs = Listbox(root, width=90, height=42, bg="white", foreground="black", bd = False)

for i, item in enumerate(actionDict1):
    ListBoxOfConfigs.insert(END, " " + list(item.keys())[0])
    ListBoxOfConfigs.itemconfig(END, {"bg" : 'red'} )

ListBoxOfConfigs.place(bordermode=OUTSIDE, x=2, y=14)

# -------------------------------- #
scrollbar = Scrollbar(root)
scrollbar.pack(side=RIGHT, fill=BOTH)
ListBoxOfConfigs.config(yscrollcommand=scrollbar.set)
scrollbar.config(command=ListBoxOfConfigs.yview)

topBtnPlace = 8
leftBtnPlace = 630

# sort by directory is 1 sort all by date is 0
sortDefault = 1

# -------------------------------- #
slogan = Button(
    root,
    text="Stop & Run",
    width=120,
    bg="#497faa",
    fg="white",
    borderless=1,
    command=action2,
)
slogan.place(bordermode=OUTSIDE, x=leftBtnPlace, y=topBtnPlace)

# -------------------------------- #
slogan = Button(
    root, text="Run", width=120, bg="#497faa", fg="white", borderless=1, command=action
)
slogan.place(bordermode=OUTSIDE, x=leftBtnPlace, y=topBtnPlace + 25)

# -------------------------------- #
openbutton = Button(
    root, text="Open", width=120, bg="#497faa", fg="white", borderless=1, command=openFile
)
openbutton.place(bordermode=OUTSIDE, x=leftBtnPlace, y=topBtnPlace + 50)

# -------------------------------- #
sortbutton1 = Button(
    root,
    text="Sort By Date",
    width=120,
    bg="#497faa",
    fg="white",
    borderless=1,
    command=sortByDate,
)
sortbutton1.place(bordermode=OUTSIDE, x=leftBtnPlace, y=topBtnPlace + 100)

# -------------------------------- #
sortbutton2 = Button(
    root,
    text="Sort by Folder",
    width=120,
    bg="#497faa",
    fg="white",
    borderless=1,
    command=sortByFolder,
)
sortbutton2.place(bordermode=OUTSIDE, x=leftBtnPlace, y=topBtnPlace + 125)

# sortbutton3 = Button(
#     root,
#     text="Sort by Folder+",
#     width=120,
#     bg="#497faa",
#     fg="white",
#     borderless=1,
#     command=sortByFolderAndDate,
# )
# sortbutton3.place(bordermode=OUTSIDE, x=leftBtnPlace, y=topBtnPlace + 150)
# -------------------------------- #
slogan = Button(
    root,
    text="Stop All",
    width=120,
    bg="#497faa",
    fg="white",
    borderless=1,
    command=stopAll,
)
slogan.place(bordermode=OUTSIDE, x=leftBtnPlace, y=topBtnPlace + 175)

# -------------------------------- #
quitbutton = Button(
    root, text="QUIT", width=120, bg="#497faa", fg="white", borderless=1, command=quit
)
quitbutton.place(bordermode=OUTSIDE, x=leftBtnPlace, y=topBtnPlace + 200)

# -------------------------------- #
# Filter text box
T = Text(root, height = 1, width = 32, bg="white", fg="black", bd=False, padx=4, pady =4)
T.place(bordermode=OUTSIDE, x=2, y=2)
clearButton = Button(
    root, text="Clear", width=120, bg="#497faa", fg="white", borderless=True, command=clear
)
clearButton.place(bordermode=OUTSIDE, x=280, y=2)


# -------------------------------- #
# sort by date = True,  
getAllConfigFiles(True, True)

# -------------------------------- #
root.mainloop()
