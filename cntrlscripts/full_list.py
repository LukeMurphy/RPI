import os
import datetime
import subprocess
import sys
import tkinter as tk
from tkinter import *
import tkmacosx
from tkmacosx import Button
#from tk import Button


commadStringPyth = "python3 /Users/lamshell/Documents/Dev/RPI/player.py -path /Users/lamshell/Documents/Dev/RPI/ -mname studio -cfg "
commadStringMultiPyth = "python3 /Users/lamshell/Documents/Dev/RPI/multiplayer.py -path /Users/lamshell/Documents/Dev/RPI/ -mname studio -cfg "
commadStringProc = ""
JavaAppRunning = ""


actionDict1 = [
	#{"--- Police Line 2 --------": "p10-line/flow-1.cfg"},
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
	if len(list(Lb1.curselection())) > 0:
		selection = Lb1.curselection()[0]
		configSelected = actionDict1[selection]
		process = True
	elif len(list(Lb2.curselection())) > 0:
		selection = Lb2.curselection()[0]
		configSelected = actionDict2[selection]
		process = True
	return (process, configSelected)


def execute(configToRun):
	global JavaAppRunning
	if ".cfg" in configToRun:
		if "multi" in configToRun:
			os.system(commadStringMultiPyth + configToRun + "&")
		else:
			os.system(commadStringPyth + configToRun + "&")
	elif ".app" in configToRun:
		os.system("open " + commadStringProc + configToRun)
		JavaAppRunning = configToRun


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

		if JavaAppRunning != '' :
			os.system("ps -ef | pgrep -f " + JavaAppRunning + " | xargs sudo kill -9;")

		configSelected = a[1]
		configToRun = configSelected[list(configSelected.keys())[0]]
		execute(configToRun)


def stopAll():
	# print("Tkinter is easy to use!")
	os.system("ps -ef | pgrep -f player | xargs sudo kill -9;")


def reSort():
	global sortDefault
	if sortDefault == 0 :
		sortDefault = 1
		getAllConfigFiles(False)
	else :
		sortDefault = 0
		getAllConfigFiles(True)


# Generate list of configs:
from os import listdir
from os.path import isfile, join
from os import walk

def returnSecondElement(l):
	return l[1]


def getAllConfigFiles(dateSort=False) :
	global actionDict1, Lb1
	configPath  = "/Users/lamshell/Documents/Dev/RPI/configs/"
	arr = os.listdir(configPath)
	fullList = []
	actionDict1 = []
	for d in arr :
		if d.find(".py") == -1 and d.find(".DS_Store") == -1 and d.find("_py") == -1 and d.find("LED") == -1:
			subArr = os.listdir(configPath + d)

			if dateSort == False: 
				subArr.sort()

			for f in subArr:
				if f.find(".DS_Store") == -1:
					shortPath = d + "/" + f
					res = os.stat(configPath + shortPath)
					fullList.append((shortPath,res.st_mtime))

			if dateSort == False: 
				fullList.append({})


	if dateSort == True : 
		fullList.sort(key=returnSecondElement, reverse=True)

	for f in fullList :
		if len(f) > 0 :
			tsTxt = datetime.datetime.fromtimestamp(f[1]).strftime('[%Y-%m-%d %H:%M]')
			actionDict1.append({ "" + tsTxt  + "  " + f[0]  : f[0]})
		else :
			actionDict1.append({ ""  : ""})


	Lb1.delete(0,END)
	for i, item in enumerate(actionDict1):
		Lb1.insert(END, " " + list(item.keys())[0])



root = tk.Tk()
#frame = tk.Frame(root, bg="darkgray")
#frame.pack(padx=1, pady=1)
# width x height x X x Y
root.geometry("%dx%d+%d+%d" % (600, 740, 1900, 100))

Lb1 = Listbox(root, width=60, height=42)


for i, item in enumerate(actionDict1):
	Lb1.insert(END, " " + list(item.keys())[0])


#Lb1.pack(side=tk.LEFT, padx=0, ipadx=10)
#Lb2.pack(side=tk.LEFT, ipadx=10, expand=0)
Lb1.place(bordermode=OUTSIDE, x=2, y=2)


scrollbar = Scrollbar(root)
scrollbar.pack(side = RIGHT, fill = BOTH)
Lb1.config(yscrollcommand = scrollbar.set) 
scrollbar.config(command = Lb1.yview) 

topBtnPlace = 8
leftBtnPlace = 440

sortDefault = 0

slogan = Button(
	root, text="Stop & Run", width = 120, bg='blue', fg='white', borderless=1, command=action2
)
slogan.place(bordermode=OUTSIDE, x=leftBtnPlace, y=topBtnPlace)

slogan = Button(
	root, text="Run", width = 120, bg='blue', fg='white', borderless=1, command=action
)
slogan.place(bordermode=OUTSIDE, x=leftBtnPlace, y=topBtnPlace+25)

slogan = Button(
	root, text="Stop All", width = 120, bg='blue', fg='white', borderless=1, command=stopAll
)
slogan.place(bordermode=OUTSIDE, x=leftBtnPlace, y=topBtnPlace+50)

quitbutton = Button(
	root, text="QUIT", width = 120, bg='blue', fg='white', borderless=1, command=quit
)
quitbutton.place(bordermode=OUTSIDE, x=leftBtnPlace, y=topBtnPlace+75)

sortbutton = Button(
	root, text="Re-Sort", width = 120, bg='blue', fg='white', borderless=1, command=reSort
)
sortbutton.place(bordermode=OUTSIDE, x=leftBtnPlace, y=topBtnPlace+100)


getAllConfigFiles(True)

root.mainloop()




