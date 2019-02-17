import tkinter as tk
import sys
import os
import subprocess
from tkinter import *

commadStringPyth = 'python3 /Users/lamshell/Documents/Dev/RPI/player.py -path /Users/lamshell/Documents/Dev/RPI/ -mname studio -cfg '
commadStringProc = '/Users/lamshell/Documents/Dev/RPI/altproduction/'


actionDict1 = [
	{" " :''},
	{"-------- WALL -------------" :''},
	#{"------------------------------" :''},
	{"* Wall Hanging: Fludd" :'p4-3x8-informal/fluddc.cfg'}, 
	{"* Wall Hanging: Signage" :'p4-3x8-informal/signage.cfg'}, 
	{"* Wall Hanging: Compositions" :'p4-3x8-informal/compositions.cfg'}, 
	{"* Wall Hanging: Patched Rothko" :'p4-3x8-informal/mono-rothko.cfg'},
	{" " :''},
	#{"------------------------------" :''},
	#{" " :''},
	{"Wall Hanging: Patched MonoChrome" :'p4-3x8-informal/mono.cfg'},
	{"Wall Hanging: Patched Yellow" :'p4-3x8-informal/mono-rothko-yellow.cfg'},
	{"Wall Hanging: Quilt Polys" :'p4-3x8-informal/quilt-polys.cfg'}, 
	{"Wall Hanging: Quilt Triangles" :'p4-3x8-informal/quilt-triangles-b.cfg'}, 
	{"Wall Hanging: Quilt Stars" :'p4-3x8-informal/quilt-stars.cfg'}, 
	{"Wall Hanging: Squares" :'p4-3x8-informal/quilt-squares.cfg'}, 
	{"Wall Hanging: Propagation" :'p4-3x8-informal/Propagation.cfg'},
	{"Wall Hanging: Afer Images" :'concentrics/ConcentricAfterImagesAll.app'},
	{"Wall Hanging: FLAG" :'p4-3x8-informal/flag.cfg'},
	{" " :''},


	
	#{"-------- BENT WALL -------------" :''},
	#{"Aym Shift: Conveyor" :'p4-10x2-asymshift/screenmedium.cfg'},
	#{"Aym Shift: Flow" :'p4-10x2-asymshift/flow.cfg'},
	#{"Aym Shift: Repeater" :'p4-10x2-asymshift/repeater-cloud.cfg'},
	#{" " :''},


	{"--------- TOWERS -----------" :''},
	{"* Tower: Monument to the Glitch" :'p4-7x8-tower/screen.cfg'},
	{"* Pencil Tower: Monument to the Glitch" :'p10-twr4/6x4-monument-to-the-glitch.cfg'},
	{"* Pencil Tower: Tourmaline" :'p10-twr4/6x4-tourmaline.cfg'},
	{" " :''},
	#{"------------------------------" :''},
	#{"Pencil Tower: Sun Bolts" :'p10-twr4/6x4-sunbolts.cfg'},
	{"Pencil Tower: Afer Images" :'concentrics/ConcentricAfterImagesAll.app'},
	{" " :''},

	{"---------- FLOOR - FIREPLCE ----------" :''},
	{"* To Fro: Algoflames" :'p4-5x6-tofro/algoflames.cfg'},
	{"To Fro: Betes.2" :'p4-5x6-tofro/betes.cfg'},
	#{"To Fro: Afer Images" :'concentrics/ConcentricAfterImagesAll.app'},
	{" " :''},

	]

actionDict2 = [
	{" " :''},
	{"--------- FLOOR MAT -----------" :''},
	{"* Square - mono-flavin" :'p4-4x8/mono-flavin.cfg'},
	{" " :''},
	{"Square - marquee a" :'p4-4x8/square-marquee-a.cfg'},
	{"Square - marquee b" :'p4-4x8/square-marquee-b.cfg'},
	{"Square - marquee c" :'p4-4x8/square-marquee-c.cfg'},
	{" " :''},
	{"Square - ICE" :'p4-4x8/square.cfg'},
	{"Square - ICE - 2" :'p4-4x8/square-ice-2.cfg'},
	{"Square - pattern-pent" :'p4-4x8/pattern-pent.cfg'},
	{"Square - mono-rothko" :'p4-4x8/mono-rothko.cfg'},
	{"Square - Collage" :'p4-4x8/square-collage.cfg'},
	{"Square - Fludd" :'p4-4x8/square-fludd.cfg'},
	{"Square - RUG" :'p4-4x8/square-rug.cfg'},


	{" " :''},
	{"---------- TEST WALL --------------" :''},
	{"* P3 Wall w. removal: marquee2 - disturbed " :'p3-2x4/marquee2.cfg'},
	{"* P3 Wall w. removal: cubes - blur" :'p3-2x4/p3-2x6-squares.cfg'},
	{" " :''},
	{"P3 Wall w. removal: cubes-b" :'p3-2x4/p3-2x6-squares-b.cfg'},
	{"P3 Wall w. removal: triangles " :'p3-2x4/p3-2x6.cfg'},
	{"P3 Wall w. removal: marquee2c - concentric " :'p3-2x4/marquee2c.cfg'},
	{" " :''},

	#{"P3 sqr w. shift: marquee2b " :'p3-2x4/marquee2b.cfg'},

	{" " :''},
	{"-------- TABLE -------------" :''},
	{"Oblong Fire" :'p4-1x4-cube/algoflames.cfg'},
	{"Oblong Fire 2" :'p4-1x4-cube/algoflames2.cfg'},
	#{"X Pile Quilt" :'p4-2x4/quiltx.cfg'},
	#{"X Pile square-polys" :'p4-2x4/square-polys.cfg'},
	#{"X Pile marquee" :'p4-2x4/marquee2.cfg'},
	#{"X Pile Compositions" :'p4-2x4/compositions.cfg'},


	{" " :''},
	#{"------------------------------" :''},
	#{"ARC - BENT GLITCH" :'p4-1xn-arc/bentglitch.cfg'},
	#{"Arc: Afer Pink" :'concentrics/ConcentricAfterImagesArc.app'},




	]

def verify():
	#print("==>",Lb.curselection())
	process = False
	configSelected = None
	if len(list(Lb1.curselection())) > 0 :
		selection  = (Lb1.curselection()[0])
		configSelected  = actionDict1[selection];
		process = True
	elif len(list(Lb2.curselection())) > 0 :
		selection  = (Lb2.curselection()[0])
		configSelected  = actionDict2[selection];
		process = True
	return (process, configSelected)


def execute(configToRun) :
	if ".cfg" in configToRun :
		os.system(commadStringPyth + configToRun + '&')
	elif ".app" in configToRun :
		os.system('open ' + commadStringProc + configToRun)
	
	

def action():
	a = verify()
	if a[0] == True:
		#os.system('ps -ef | pgrep -f player | xargs sudo kill -9;')
		configSelected = a[1]
		configToRun = configSelected[list(configSelected.keys())[0]]
		execute(configToRun)


def action2():
	a = verify()
	if a[0] == True:
		os.system('ps -ef | pgrep -f player | xargs sudo kill -9;')
		configSelected = a[1]
		configToRun = configSelected[list(configSelected.keys())[0]]
		execute(configToRun)



def stopAll():
	#print("Tkinter is easy to use!")
	os.system('ps -ef | pgrep -f player | xargs sudo kill -9;')

root = tk.Tk()
frame = tk.Frame(root)
frame.pack(padx=10,pady=10)
root.geometry('%dx%d+%d+%d' % (740, 690, 1000, 100))

Lb1 = Listbox(frame, width = 26, height = 38) 
Lb2 = Listbox(frame, width = 33, height = 38) 

for i, item in enumerate(actionDict1):
	Lb1.insert(END, " " + list(item.keys())[0])


for i, item in enumerate(actionDict2):
	Lb2.insert(END, " " + list(item.keys())[0])

Lb1.pack(side=tk.LEFT,padx=10,ipadx=10 )
Lb2.pack(side=tk.LEFT,ipadx=10,expand=0  )



button = tk.Button(frame, text="QUIT", bg="black", fg="red", command=quit)
button.pack(side=tk.BOTTOM, padx=2)

slogan = tk.Button(frame,text="Run",fg="Red", command=action)
slogan.pack(side=tk.BOTTOM,padx=2)

slogan = tk.Button(frame,text="Stop All",fg="blue", command=stopAll)
slogan.pack(side=tk.BOTTOM,padx=2)

slogan = tk.Button(frame,text="Stop & Run",fg="blue", command=action2)
slogan.pack(side=tk.BOTTOM,padx=2)




root.mainloop()






