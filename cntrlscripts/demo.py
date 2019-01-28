import tkinter as tk
import sys
import os
import subprocess
from tkinter import *

commadStringPyth = 'python3 /Users/lamshell/Documents/Dev/RPI/player.py -path /Users/lamshell/Documents/Dev/RPI/ -mname studio -cfg '
commadStringProc = '/Users/lamshell/Documents/Dev/RPI/altproduction/'


actionDict = [
	{"Wall Hanging: Quilt Polys" :'p4-3x8-informal/quilt-polys.cfg'}, 
	{"Wall Hanging: Quilt Triangles" :'p4-3x8-informal/quilt-triangles-b.cfg'}, 
	{"Wall Hanging: Quilt Stars" :'p4-3x8-informal/quilt-star.cfg'}, 
	#{"------------------------------" :''},
	{" " :''},
	{"Wall Hanging: Fludd" :'p4-3x8-informal/fluddc.cfg'}, 
	{"Wall Hanging: Signage" :'p4-3x8-informal/signage.cfg'}, 
	{"Wall Hanging: Patched MonoChrome" :'p4-3x8-informal/mono.cfg'},
	{"Wall Hanging: Patched Rothko" :'p4-3x8-informal/mono-rothko.cfg'},
	{"Wall Hanging: Patched Yellow" :'p4-3x8-informal/mono-rothko-yellow.cfg'},
	#{"------------------------------" :''},
	{" " :''},
	{"Wall Hanging: Propagation" :'p4-3x8-informal/Propagation.cfg'},
	{"Wall Hanging: Afer Images" :'concentrics/ConcentricAfterImagesAll.app'},
	{"Wall Hanging: FLAG" :'p4-3x8-informal/flag.cfg'},


	#{"------------------------------" :''},
	#{"Angle Quilt Small" :'p4-1x4-cube/l-quilt.cfg'},

	
	{"------------------------------" :''},
	{"Aym Shift: Conveyor" :'p4-10x2-asymshift/screenmedium.cfg'},
	{"Aym Shift: Flow" :'p4-10x2-asymshift/flow.cfg'},
	{"Aym Shift: Repeater" :'p4-10x2-asymshift/repeater-cloud.cfg'},


	{"------------------------------" :''},
	{"Tower: Monument to the Glitch" :'p4-7x8-tower/screen.cfg'},
	
	{"------------------------------" :''},
	{"Pencil Tower: Monument to the Glitch" :'p10-twr4/6x4-monument-to-the-glitch.cfg'},
	{"Pencil Tower: Sun Bolts" :'p10-twr4/6x4-sunbolts.cfg'},
	{"Pencil Tower: Tourmaline" :'p10-twr4/6x4-tourmaline.cfg'},
	{"Pencil Tower: Afer Images" :'concentrics/ConcentricAfterImagesAll.app'},


	{"------------------------------" :''},
	{"X Pile Quilt" :'p4-2x4/quiltx.cfg'},
	{"X Pile square-polys" :'p4-2x4/square-polys.cfg'},
	{"X Pile marquee" :'p4-2x4/marquee2.cfg'},


	
	{"------------------------------" :''},
	{"Arc: Afer Pink" :'concentrics/ConcentricAfterImagesArc.app'},



	
	{"------------------------------" :''},
	{"To Fro: Betes.2" :'p4-5x6-tofro/betes.cfg'},
	{"To Fro: Algoflames" :'p4-5x6-tofro/algoflames.cfg'},
	{"To Fro: Afer Images" :'concentrics/ConcentricAfterImagesAll.app'},
	{" " :''},





	]


def action():
	#print("==>",Lb.curselection())

	if len(list(Lb.curselection())) > 0 :
		selection  = (Lb.curselection()[0])
		os.system('ps -ef | pgrep -f player | xargs sudo kill -9;')
		configSelected  = actionDict[selection];
		configToRun = configSelected[list(configSelected.keys())[0]]

		if ".cfg" in configToRun :
			os.system(commadStringPyth + configToRun + '&')
		elif ".app" in configToRun :
			os.system('open ' + commadStringProc + configToRun)



def stopAll():
	#print("Tkinter is easy to use!")
	os.system('ps -ef | pgrep -f player | xargs sudo kill -9;')

root = tk.Tk()
frame = tk.Frame(root)
frame.pack(padx=10,pady=10)
root.geometry('%dx%d+%d+%d' % (300, 640, 1600, 100))

Lb = Listbox(frame, width = 40, height = 35) 


for i,item in enumerate(actionDict):
    Lb.insert(END, list(item.keys())[0])

Lb.pack(fill=BOTH, expand=1)

button = tk.Button(frame, text="QUIT", bg="black", fg="red", command=quit)
button.pack(side=tk.LEFT)

slogan = tk.Button(frame,text="Run",fg="Red", command=action)
slogan.pack(side=tk.LEFT)

slogan = tk.Button(frame,text="Stop All",fg="blue", command=stopAll)
slogan.pack(side=tk.LEFT)


root.mainloop()






