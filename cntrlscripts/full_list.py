"""Summary

Attributes:
    actionDict1 (TYPE): Description
    actionDict2 (TYPE): Description
    commadStringMultiPyth (str): Description
    commadStringProc (str): Description
    commadStringPyth (str): Description
    JavaAppRunning (str): Description
    Lb1 (TYPE): Description
    leftBtnPlace (int): Description
    quitbutton (TYPE): Description
    root (TYPE): Description
    scrollbar (TYPE): Description
    slogan (TYPE): Description
    sortbutton (TYPE): Description
    sortDefault (int): Description
    topBtnPlace (int): Description
"""
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


commadStringProc = ""
JavaAppRunning = ""
configPath = "/Users/lamshell/Documents/Dev/RPI/configs/"


actionDict1 = [
    # {"--- Police Line 2 --------": "p10-line/flow-1.cfg"},
    {"SCREEN TEST ": "screens/test-448x320.cfg"},
]

actionDict2 = [
    {"SCREEN TEST ": "screens/test-448x320.cfg"},
]


def verify():
    """Summary

    Returns:
        TYPE: Description
    """
    # print("==>",Lb.curselection())
    global actionDict1
    process = False
    configSelected = None
    if len(list(Lb1.curselection())) > 0:
        selection = Lb1.curselection()[0]
        configSelected = actionDict1[selection]
        process = True
    # elif len(list(Lb2.curselection())) > 0:
    #     selection = Lb2.curselection()[0]
    #     configSelected = actionDict2[selection]
    #     process = True
    return (process, configSelected)


def execute(configToRun):

    commadStringPyth = "python3 /Users/lamshell/Documents/Dev/RPI/player.py -path /Users/lamshell/Documents/Dev/RPI/ -mname studio -cfg "
    commadStringMultiPyth = "python3 /Users/lamshell/Documents/Dev/RPI/multiplayer.py -path /Users/lamshell/Documents/Dev/RPI/ -mname studio -cfg "
    commadStringSeqPyth = "python3 /Users/lamshell/Documents/Dev/RPI/sequence-player.py -path /Users/lamshell/Documents/Dev/RPI/ -mname studio -cfg "

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
    """Summary"""
    a = verify()
    if a[0] == True:
        # os.system('ps -ef | pgrep -f player | xargs sudo kill -9;')
        configSelected = a[1]
        configToRun = configSelected[list(configSelected.keys())[0]]
        execute(configToRun)


def action2():
    """Summary"""
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


def stopAll():
    """Summary"""
    # print("Tkinter is easy to use!")
    os.system("ps -ef | pgrep -f player | xargs sudo kill -9;")


def sortByDate():
    getAllConfigFiles(True)


def sortByFolder():
    getAllConfigFiles(False)


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
    """Summary

    Args:
        l (TYPE): Description

    Returns:
        TYPE: Description
    """
    return l[1]


def getAllConfigFiles(dateSort=False, subsortDate=False):
    """Summary

    Args:
        dateSort (bool, optional): Description
    """

    global actionDict1, Lb1
    global configPath
    # arr = os.listdir(configPath)
    # Sort the directories by name
    # arr.sort(reverse=False)
    fullList = []
    actionDict1 = []

    for root, dirs, files in os.walk(configPath, topdown=False):
        for name in files:
            fullPath = os.path.join(root, name)
            if name.find(".cfg") > 0 and name.find(".py") == -1 and name.find(".DS_Store") == -1:
                res = os.stat(fullPath)
                fullList.append((os.path.join(root, name), res.st_mtime))

    # for directory in arr:
    #     if (
    #         directory.find(".py") == -1
    #         and directory.find(".DS_Store") == -1
    #         and directory.find("_py") == -1
    #         and directory.find("LED") == -1
    #     ):
    #         subArr = os.listdir(configPath + directory)
    #         subDirectoryList = []

    #         if dateSort == False:
    #             subArr.sort(reverse=True)

    #         for file in subArr:
    #             if file.find(".DS_Store") == -1:
    #                 shortPath = directory + "/" + file
    #                 if os.path.isfile(configPath + shortPath):
    #                     res = os.stat(configPath + shortPath)
    #                     if dateSort == False:
    #                         subDirectoryList.append((shortPath, res.st_mtime))
    #                     else:
    #                         fullList.append((shortPath, res.st_mtime))

    #         if dateSort == False:
    #             # sorts by date within folder
    #             if subsortDate == True:
    #                 subDirectoryList.sort(key=returnSecondElement, reverse=True)
    #             else:
    #                 subDirectoryList.sort(reverse=False)
    #             fullList.extend(subDirectoryList)
    #             fullList.append({})

    # Sort the configs by date descending
    if dateSort == True:
        fullList.sort(key=returnSecondElement, reverse=True)
    else:
        fullList.sort(key=returnFirstElement, reverse=False)

    lastDir = ""
    fName = ""
    for f in fullList:
        fName = f[0].split(configPath)[1].split('/')[0]
        if len(f) > 0:
            tsTxt = datetime.datetime.fromtimestamp(
                f[1]).strftime("[%Y-%m-%d %H:%M]")
            
            # and dateSort != True
            if fName != lastDir :
                actionDict1.append({"": ""})

            lastDir = f[0].split(configPath)[1].split('/')[0]
            actionDict1.append(
                {tsTxt + "\t\t" + f[0].split(configPath)[1] + "     ": f[0]})
            # actionDict1.append({ "" + tsTxt  + "  " + f[0]  : f[0]})

        else:
            actionDict1.append({"": ""})

    Lb1.delete(0, END)
    for i, item in enumerate(actionDict1):
        Lb1.insert(END, " " + list(item.keys())[0])


root = tk.Tk()
# frame = tk.Frame(root, bg="darkgray")
# frame.pack(padx=1, pady=1)
# width x height x X x Y

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

root.geometry(
    "%dx%d+%d+%d"
    % (
        700,
        round(screen_height * 0.4),
        round(2 * screen_width / 3),
        round(2 * screen_height / 3),
    )
)

Lb1 = Listbox(root, width=70, height=32)


for i, item in enumerate(actionDict1):
    Lb1.insert(END, " " + list(item.keys())[0])


# Lb1.pack(side=tk.LEFT, padx=0, ipadx=10)
# Lb2.pack(side=tk.LEFT, ipadx=10, expand=0)
Lb1.place(bordermode=OUTSIDE, x=2, y=2)


scrollbar = Scrollbar(root)
scrollbar.pack(side=RIGHT, fill=BOTH)
Lb1.config(yscrollcommand=scrollbar.set)
scrollbar.config(command=Lb1.yview)

topBtnPlace = 8
leftBtnPlace = 540

# sort by directory is 1 sort all by date is 0
sortDefault = 1

slogan = Button(
    root,
    text="Stop & Run",
    width=120,
    bg="blue",
    fg="white",
    borderless=1,
    command=action2,
)
slogan.place(bordermode=OUTSIDE, x=leftBtnPlace, y=topBtnPlace)

slogan = Button(
    root, text="Run", width=120, bg="blue", fg="white", borderless=1, command=action
)
slogan.place(bordermode=OUTSIDE, x=leftBtnPlace, y=topBtnPlace + 25)

openbutton = Button(
    root, text="Open", width=120, bg="blue", fg="white", borderless=1, command=openFile
)
openbutton.place(bordermode=OUTSIDE, x=leftBtnPlace, y=topBtnPlace + 50)

sortbutton1 = Button(
    root,
    text="Sort By Date",
    width=120,
    bg="blue",
    fg="white",
    borderless=1,
    command=sortByDate,
)
sortbutton1.place(bordermode=OUTSIDE, x=leftBtnPlace, y=topBtnPlace + 100)

sortbutton2 = Button(
    root,
    text="Sort by Folder",
    width=120,
    bg="blue",
    fg="white",
    borderless=1,
    command=sortByFolder,
)
sortbutton2.place(bordermode=OUTSIDE, x=leftBtnPlace, y=topBtnPlace + 125)

# sortbutton3 = Button(
#     root,
#     text="Sort by Folder+",
#     width=120,
#     bg="blue",
#     fg="white",
#     borderless=1,
#     command=sortByFolderAndDate,
# )
# sortbutton3.place(bordermode=OUTSIDE, x=leftBtnPlace, y=topBtnPlace + 150)

slogan = Button(
    root,
    text="Stop All",
    width=120,
    bg="blue",
    fg="white",
    borderless=1,
    command=stopAll,
)
slogan.place(bordermode=OUTSIDE, x=leftBtnPlace, y=topBtnPlace + 175)

quitbutton = Button(
    root, text="QUIT", width=120, bg="blue", fg="white", borderless=1, command=quit
)
quitbutton.place(bordermode=OUTSIDE, x=leftBtnPlace, y=topBtnPlace + 200)

# sort by date = True,  
getAllConfigFiles(True, True)

root.mainloop()
