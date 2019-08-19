import tkinter as tk
import sys
import os
import subprocess
from tkinter import *

commadStringPyth = 'python3 /Users/lamshell/Documents/Dev/RPI/player.py -path /Users/lamshell/Documents/Dev/RPI/ -mname studio -cfg '
commadStringMultiPyth = 'python3 /Users/lamshell/Documents/Dev/RPI/multiplayer.py -path /Users/lamshell/Documents/Dev/RPI/ -mname studio -cfg '
commadStringProc = '/Users/lamshell/Documents/Dev/RPI/altproduction/'


actionDict1 = [

	#{" " :''},


	{" " :''},
	{"-------- NORTH WALL  -------------" :''},
	{"P10 Branch - Glitch" :'p10/glitch-screen.cfg'},
	{"P10 Branch - Algoflames-b" :'p10/algoflames-1b.cfg'},
	{"P10 Branch - Collage" :'p10/collage-1.cfg'},
	{"* P10 Branch - Collage branch" :'p10/collage-lines-1.cfg'},
	{"* P10 Branch - Collage branch 2" :'p10/collage-lines-1a.cfg'},
	{"* P10 Branch - Collage branch inv" :'p10/collage-lines-2.cfg'},
	{"* P10 Branch - Tourmaline" :'p10/collage-tourmaline.cfg'},
	{"* P10 Branch: Afer Images" :'concentrics/ConcentricAfterImagesAll.app'},


	#{" " :''},
	#{"* P4 3x8 p4-3x8-informal - disturbed " :'p3-2x4/marquee2.cfg'},


	#{"------------------------------" :''},
	#{"Pencil Tower: Sun Bolts" :'p10-twr4/6x4-sunbolts.cfg'},
	#{" " :''},
	#{"------------------------------" :''},
	#{"* Short Tower: monument-to-the-glitch" :'p4-4x8-3x-short-tower/diagnostics.cfg'},
	#{"Short Tower: clown" :'p4-4x8-3x-short-tower/quilt.cfg'},
	#{"Short Tower: quilt" :'p4-4x8-3x-short-tower/quilt-log-cabin.cfg'},


	#{" " :''},
	#{"---------- FLOOR - FIREPLCE ----------" :''},
	#{"* To Fro: Algoflames2" :'p4-4x6/algoflames2.cfg'},
	#{"To Fro: Algoflames" :'p4-5x6-tofro/algoflames.cfg'},
	#{"To Fro: Betes.2" :'p4-5x6-tofro/betes.cfg'},
	#{"To Fro: Afer Images" :'concentrics/ConcentricAfterImagesAll.app'},
	#{" " :''},

	{" " :''},
	{"---------- FLOOR - FIREPLCE ----------" :''},
	{"* pile: Algoflames2.2" :'p4-6x8/algofall-2.2.cfg'},
	{"pile: Algoflames2.1" :'p4-6x8/algofall-2.1.cfg'},
	{"pile: Algoflames2.14" :'p4-6x8/algofall-2.14.cfg'},
	{"pile: Algoflames-6" :'p4-6x8/algofall6.cfg'},
	{"pile: Algoflames-6a" :'p4-6x8/algofall6a.cfg'},
	{"pile: image-particles" :'p4-6x8/image-particles.cfg'},

	#{" " :''},


	{" " :''},
	{"-------- RIGHT WALL -------------" :''},
	{"* Wall Hanging: Patched Rothko" :'p4-3x8-informal/mono-rothko.cfg'},
	{"* Wall Hanging: Compositions" :'p4-3x8-informal/compositions.cfg'}, 
	{"* Wall Hanging: compositions a" :'p4-3x8-informal/compositions.cfg'}, 
	{"* Wall Hanging: compositions b" :'p4-3x8-informal/compositions.cfg'}, 
	{"------------------------------" :''},
	{"Wall Hanging: Quilt Polys" :'p4-3x8-informal/quilt-polys.cfg'}, 
	{"Wall Hanging: Quilt Triangles" :'p4-3x8-informal/quilt-triangles-b.cfg'}, 
	{"Wall Hanging: Quilt Stars" :'p4-3x8-informal/quilt-stars.cfg'}, 
	{"Wall Hanging: Squares" :'p4-3x8-informal/quilt-squares.cfg'}, 
	{"Wall Hanging: THRow Multi" :'multi/throw-quilt.cfg'}, 
	{"------------------------------" :''},
	{"Wall Hanging: Gradients" :'p4-3x8-informal/gradients.cfg'}, 
	{"Wall Hanging: TWO FLOW" :'multi/manifest-3x8-informal.cfg'}, 

	{"------------------------------" :''},
	{"Wall Hanging: Signage" :'p4-3x8-informal/signage.cfg'}, 
	{"Wall Hanging: Patched MonoChrome" :'p4-3x8-informal/mono.cfg'},
	{"Wall Hanging: Patched Yellow" :'p4-3x8-informal/mono-rothko-yellow.cfg'},
	{"Wall Hanging: Propagation" :'p4-3x8-informal/Propagation.cfg'},
	{"Wall Hanging: Afer Images" :'concentrics/ConcentricAfterImagesAll.app'},
	{"------------------------------" :''},
	{"* Vert Bars - gray" :'p4-5x8/mono-lights-gray.cfg'},
	{"Square - mono-flavin" :'p4-3x8-informal/mono-flavin.cfg'},
	]

actionDict2 = [

	{" " :''},
	#{"--------- FLOOR PILE -----------" :''},
	#{"* 3 PILE - compositions" :'p4-3x8-pile/leaninglights-3.cfg'},
	#{"3 PILE - flames" :'p4-3x8-pile/alt-flames-2b.cfg'},

	
	{" " :''},
	{"-------- BUNDLE FLOOR  -------------" :''},
	{"P10 BUNDLE PILE - AlgoFlames" :'p10/bundle-algoflames-1.cfg'},
	{"P10 BUNDLE PILE - AlgoFlames b" :'p10/bundle-algoflames-2.cfg'},
	{"* P10 BUNDLE PILE - AlgoFlames c" :'p10/bundle-algofall-2.14.cfg'},
	#{"3 PILE - movement" :'p4-3x8-pile/square-ice-2.cfg'},
	{"* P10 BUNDLE PILE - Flow" :'p10/bundle-scroller-flow.cfg'},
	{"P10 BUNDLE PILE - Tourmaline" :'p10/bundle-collage-tourmaline.cfg'},
	{"P10 BUNDLE PILE - leaning lights" :'p10/bundle-leaninglights-2.cfg'},
	{"P10 BUNDLE PILE - leaning pattern" :'p10/bundle-lines-2.cfg'},


	{" " :''},
	{"-------- PLANK AND DOOR  -------------" :''},
	{"P10 Plank-Door - AlgoFlames" :'p10/plank-algoflames-1b.cfg'},
	{"P10 Plank-Door - movement" :'p10/plank-movement-2.cfg'},
	{"* P10 Plank-Door - gradients" :'p10/gradients.cfg'},
	{"* P10 Plank-Door - collage" :'p10/plank-collage-1.cfg'},
	{"* P10 Plank-Door - glitch" :'p10/plank-glitch.cfg'},
	{"* P10 Plank-Door - Tourmanline" :'p10/plank-tourmaline.cfg'},
	{"* P10 BUNDLE PILE - Flow" :'p10/plank-scroller-flow.cfg'},


	#{"* Tower: Monument to the Glitch" :'p4-7x8-tower/screen.cfg'},
	#{"* Pencil Tower: Monument to the Glitch" :'p10-twr4/6x4-monument-to-the-glitch.cfg'},
	#{"* Pencil Tower: Tourmaline" :'p10-twr4/6x4-tourmaline.cfg'},
	#{"* Pencil Tower: Afer Images" :'concentrics/ConcentricAfterImagesAll.app'},



	{" " :''},
	{"-------- TABLE -------------" :''},
	{"Oblong Fire" :'p4-1x4-cube/algoflames.cfg'},
	{"Oblong Fire 2" :'p4-1x4-cube/algoflames2.cfg'},
	#{"X Pile Quilt" :'p4-2x4/quiltx.cfg'},
	#{"X Pile square-polys" :'p4-2x4/square-polys.cfg'},
	#{"X Pile marquee" :'p4-2x4/marquee2.cfg'},
	#{"X Pile Compositions" :'p4-2x4/compositions.cfg'},

	#{"Wall Hanging: Fludd" :'p4-3x8-informal/fluddc.cfg'}, 
	#{"* Wall Hanging 3x7: Fludd Factory" :'p4-3x7-informal/fluddc.cfg'},
	#{"* Wall Hanging 3x7: Patched Rothko" :'p4-3x7-informal/mono-rothko.cfg'},
	#{"* Wall Hanging 3x7: Star Quilt" :'p4-3x7-informal/quilt-stars.cfg'},
	#{"* Wall Hanging 3x7: Tri Quilt" :'p4-3x7-informal/quilt-triangles-b.cfg'},
	#{"* Wall Hanging 3x7: Signage Abstraction" :'p4-3x7-informal/signage.cfg'},
	#{"------------------------------" :''},
	#{" " :''},
	#{"Wall Hanging: FLAG" :'p4-3x8-informal/flag.cfg'},
	#{" " :''},



	#{"3rd Gen Tatlin" :'p4-7x4/mono-flavin2.cfg'},
	#{"Marquee" :'p4-7x4/marquee-b.cfg'},
	#{"Aym Shift: Conveyor" :'p4-10x2-asymshift/screenmedium.cfg'},
	#{"Aym Shift: Flow" :'p4-10x2-asymshift/flow.cfg'},
	#{"Aym Shift: Repeater" :'p4-10x2-asymshift/repeater-cloud.cfg'},
	#{" " :''},
	#{"-------- LEFT WALL -------------" :''},
	#{"* Wall Compositions" :'p4-5x8/compositions.cfg'},
	#{"* Vert Bars - gray" :'p4-5x8/mono-lights-gray.cfg'},
	#{"Vert Bars - yellow" :'p4-5x8/mono-lights-yellow.cfg'},
	#{"Horizontal Bars" :'p4-5x8/mono-lights-h.cfg'},
	#{" " :''},



	{" " :''},
	{"--------- FLOOR -----------" :''},
	{"* Tower w. Bump Collage" :'p4-5x8/bump-collage.cfg'},
	{"* Tower w. Bump Collage2" :'p4-5x8/bump-collage2.cfg'},
	{"* Alt Flames" :'p4-6x8/alt-flames.cfg'},
	
	#{"Tower w. Bump Flames" :'p4-5x8/bump-fire.cfg'},
	#{"Tower w. Bump Glitch" :'p4-5x8/bump-glitch.cfg'},
	#{"Tower w. Bump Diagnostics" :'p4-5x8/bump-diagnostics.cfg'},


	{" " :''},
	{"* Falling Stairs - flames" :'p4-2xsteps/algoflames.cfg'},
	{"* Falling Stairs - ice" :'p4-2xsteps/algofall.cfg'},
	{" " :''},
	{"* Three Way Leaning Lights" :'p4-6x8/leaninglights.cfg'},
	{"* Alt Flames" :'p4-6x8/alt-flames.cfg'},
	{" " :''},


	
	
	{" " :''},
	#{"--------- ROUND CORNER -----------" :''},
	#{"Square - mono-flavin" :'p4-4x8/mono-flavin.cfg'},
	#{"Square - quilt" :'p4-4x8/quilt-log-cabin.cfg'},
	#{" " :''},
	#{"Square - ICE" :'p4-4x8/square.cfg'},
	#{"Square - ICE - 2" :'p4-4x8/square-ice-2.cfg'},
	#{"Square - pattern-pent" :'p4-4x8/pattern-pent.cfg'},
	#{"Square - mono-rothko" :'p4-4x8/mono-rothko.cfg'},

	
	#{" " :''},
	#{"Square - marquee a" :'p4-4x8/square-marquee-a.cfg'},
	#{"Square - marquee b" :'p4-4x8/square-marquee-b.cfg'},
	#{"Square - marquee c" :'p4-4x8/square-marquee-c.cfg'},
	#{"Square - Collage" :'p4-4x8/square-collage.cfg'},
	#{"Square - Fludd" :'p4-4x8/square-fludd.cfg'},
	#{"Square - RUG" :'p4-4x8/square-rug.cfg'},

	
	#{" " :''},
	#{"---------- TEST WALL --------------" :''},
	
	#{"* P3 Wall w. removal: marquee2 - disturbed " :'p3-2x4/marquee2.cfg'},
	#{"* P3 Wall w. removal: cubes - blur" :'p3-2x4/p3-2x6-squares.cfg'},
	#{" " :''},
	#{"P3 Wall w. removal: cubes-b" :'p3-2x4/p3-2x6-squares-b.cfg'},
	#{"P3 Wall w. removal: triangles " :'p3-2x4/p3-2x6.cfg'},
	#{"P3 Wall w. removal: marquee2c - concentric " :'p3-2x4/marquee2c.cfg'},
	#{" " :''},

	#{"P3 sqr w. shift: marquee2b " :'p3-2x4/marquee2b.cfg'},



	#{" " :''},
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
		if "multi" in configToRun:
			os.system(commadStringMultiPyth + configToRun + '&')
		else:
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
frame = tk.Frame(root, bg="blue")
frame.pack(padx=1,pady=1)
# width x height x X x Y
root.geometry('%dx%d+%d+%d' % (680, 740, 100, 100))

Lb1 = Listbox(frame, width = 26, height = 48) 
Lb2 = Listbox(frame, width = 33, height = 48) 

for i, item in enumerate(actionDict1):
	Lb1.insert(END, " " + list(item.keys())[0])


for i, item in enumerate(actionDict2):
	Lb2.insert(END, " " + list(item.keys())[0])

Lb1.pack(side=tk.LEFT,padx=0,ipadx=10 )
Lb2.pack(side=tk.LEFT,ipadx=10,expand=0  )



button = tk.Button(frame, text="QUIT", bg="blue", fg="red", highlightbackground='blue',command=quit)
button.pack(side=tk.BOTTOM, padx=2)

slogan = tk.Button(frame,text="Run",bg="Red", highlightbackground='blue', command=action)
slogan.pack(side=tk.BOTTOM,padx=2)

slogan = tk.Button(frame,text="Stop All",bg="blue", highlightbackground='blue', command=stopAll)
slogan.pack(side=tk.BOTTOM,padx=2)

slogan = tk.Button(frame,text="Stop & Run", bg="blue", highlightbackground='blue', command=action2)
slogan.pack(side=tk.BOTTOM,padx=2)




root.mainloop()






