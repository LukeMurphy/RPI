import os
import subprocess
import sys
import tkinter as tk
from tkinter import *
from tkmacosx import Button


commadStringPyth = "python3 /Users/lamshell/Documents/Dev/RPI/player.py -path /Users/lamshell/Documents/Dev/RPI/ -mname studio -cfg "
commadStringMultiPyth = "python3 /Users/lamshell/Documents/Dev/RPI/multiplayer.py -path /Users/lamshell/Documents/Dev/RPI/ -mname studio -cfg "
commadStringProc = ""
JavaAppRunning = ""


actionDict1 = [


	{"_____________________________________________": ""},
	{" ": ""},
	{"--- Left wall: Door Insert --------": "p4-4x3-panel/composition-door.cfg"},
	{"_____________________________________________": ""},
	{" ": ""},
	{"--- Small Unsettled Abstraction --------": "p4-1x4-cube/panel-test.cfg"},
	
	{"_____________________________________________": ""},
	{" ": ""},
	{"--- ** Police Line 1 --------": "p10-line/static-1.cfg"},
	{"--- Police Line 2 --------": "p10-line/flow-1.cfg"},
	{"--- Police Line 3 --------": "p10-line/flow-2.cfg"},

	{"_____________________________________________": ""},
	{" ": ""},
	{"--- Rough Line --------": "p4-1x4-cube/diagnostics-single-line.cfg"},

	#{" ": ""},
	#{"--- Right wall panels: Bridge - Inset": "p4-4x3-panel/composition-panel.cfg"},
	{"_____________________________________________": ""},
	{" ": ""},
	{"--- Ladder - Interchange (Java)": "/Users/lamshell/Dropbox/Dev/Processing/production/Player/application.macosx/Player.app"},

	{"_____________________________________________": ""},
	{" ": ""},
	{"--- Two poles - Rural Lights": "p4-3x8-informal/mono-flavin.cfg"},
	#{"--- WALKING ": "p4-3x8-informal/img-hub3-walk.cfg"},
	#{"--- CLOUDS ": "p4-3x8-informal/img-hub3-clouds.cfg"},


	{" ": ""},
	{"_____________________________________________": ""},
	{" ": ""},
	{"--- The Problem With Dot Paintings 2": "p4-3x8-informal/spots2.cfg"},
	{"--- The Problem With Dot Paintings 1": "p4-3x8-informal/spots.cfg"},
	{"3x8 Informal : Patched Rothko": "p4-3x8-informal/mono-rothko.cfg"},
	{"3x8 Informal : TWO FLOW": "multi/manifest-3x8-informal.cfg"},
	{"3x8 Informal : FAst Flames": "p4-3x8-informal/fast-flames-2.cfg"},
	{"3x8 Informal : Gradients": "p4-3x8-informal/gradients.cfg"},
	{"3x8 Informal : Log Cabin Quilt": "p4-3x8-informal/quilt.cfg"},
	{"3x8 Informal : Quilt Polys": "p4-3x8-informal/quilt-polys.cfg"},
	{"3x8 Informal : Quilt Triangles": "p4-3x8-informal/quilt-triangles-b.cfg"},
	{"3x8 Informal : Quilt Stars": "p4-3x8-informal/quilt-stars.cfg"},
	{"3x8 Informal : Squares": "p4-3x8-informal/quilt-squares.cfg"},
	{"3x8 Informal : Squares Plane": "p4-3x8-informal/quilt-squares-plane.cfg"},
	{"3x8 Informal : THRow Multi": "multi/throw-quilt.cfg"},

	#{"_____________________________________________": ""},
	#{" ": ""},
	#{"--- Upset Cube  - GlitchBox": "p4-4x4/cube-screenproject.cfg"},
	#{"--- Upset Cube - Box Lights": "p4-4x4/dot-grid-4x6.cfg"},
	#{" ": ""},

	#{"_____________________________________________": ""},
	
	#{" ": ""},

	#{"_____________________________________________": ""},
	

	{"_____________________________________________": ""},
	{" ": ""},
	{"--- Inset frame: small p3": "staging/p3-inset-compositions.cfg"},
	{"--- Inset frame oblong p4": "staging/p4-inset-compositions-2.cfg"},
	


	#{"--- Road Sign tree-armature tourmanline": "p4-4x4/sign-tourmaline-b.cfg"},


]

actionDict2 = [


	{"_____________________________________________": ""},
	{" ": ""},
	{"--- P10 - arbor-vitae-blue": "multi/manifest-p10-1.cfg"},
	{"--- P10 - arbor-vitae-flow": "p10/arbor-vitae-flow.cfg"},
	{"--- P10 - arbor-vitae-1 - flames": "p10/arbor-vitae-1.cfg"},
	{"--- P10 - arbor-vitae-1 - flames2": "p10/arbor-vitae-2.cfg"},

	{"_____________________________________________": ""},
	{" ": ""},
	{"--- Trap Prop  p10-frame - algoflames": "p4-6x1-firestick/p10-algoflames-rbg.cfg"},
	{"--- Trap Prop  p10-frame - tourmalines": "p4-6x1-firestick/p10-doorframe-tourmaline.cfg"},
	{"--- Trap Prop  p10-frame - tourmalines -b": "p4-6x1-firestick/p10-doorframe-tourmaline-b.cfg"},

	{"_____________________________________________": ""},

	{"_____________________________________________": ""},
	{" ": ""},
	#{" ": ""},
	{"==== BUNDLE FLOOR ====": ""},
	{"--- P10 BUNDLE PILE - Flow": "p10/bundle-scroller-flow.cfg"},
	{"--- P10 BUNDLE PILE - Flow": "p10/plank-scroller-flow.cfg"},
	{"--- P10 BUNDLE PILE - Flow": "p10/plank-scroller-flow.cfg"},
	{"--- P10 Bundle  - AlgoFlames Pink": "p10/plank-algoflames-2.cfg"},
	{"--- P10 BUNDLE PILE - Tourmaline": "p10/bundle-collage-tourmaline.cfg"},
	{".  .  .  .  .  .  .  .  .  .  .  .  .": ""},
	{"P10 BUNDLE PILE - leaning lights": "p10/bundle-leaninglights-2.cfg"},
	{"P10 BUNDLE PILE - AlgoFlames c": "p10/bundle-algofall-2.14.cfg"},
	{"P10 BUNDLE PILE - AlgoFlames": "p10/bundle-algoflames-1.cfg"},
	{"P10 BUNDLE PILE - AlgoFlames b": "p10/bundle-algoflames-2.cfg"},
	{" ": ""},


	{" ": ""},
	{"Java - Impression": "/Users/lamshell/Dropbox/Dev/Processing/production/Impression/application.macosx/Impression.app"},
	{"Java - partial plinth Gray Glory": "grayburst.app"},
	{"Java - DotGridTiles": "/Users/lamshell/Documents/Dev/RPI/altproduction/DotGridTiles.app"},
	{"Java - Afer Images": "/Users/lamshell/Documents/Dev/RPI/altproduction/concentrics/ConcentricAfterImagesAll.app"},

	{"_____________________________________________": ""},
	{"SCREEN TEST ": "screens/test-448x320.cfg"},
	{"SCREEN TEST @x=100 y=100": "screens/test-448x320b.cfg"},
	{"SCREEN TEST P8": "screens/p8-448x320b.cfg"},
	{"SCREEN TEST P10": "screens/p10-192x128.cfg"},
	{"Police Line P8 ": "p10-line/p8-static-1.cfg"},


	{" " :''},
	#{"FirePike" :'p4-4x4/newfire.cfg'},


	# {" " :''},
	# {"* P4 3x8 p4-3x8-informal - disturbed " :'p3-2x4/marquee2.cfg'},
	# {"------------------------------" :''},
	# {"Pencil Tower: Sun Bolts" :'p10-twr4/6x4-sunbolts.cfg'},
	# {" " :''},
	# {"------------------------------" :''},
	# {"* Short Tower: monument-to-the-glitch" :'p4-4x8-3x-short-tower/diagnostics.cfg'},
	# {"Short Tower: clown" :'p4-4x8-3x-short-tower/quilt.cfg'},
	# {"Short Tower: quilt" :'p4-4x8-3x-short-tower/quilt-log-cabin.cfg'},
	# {" " :''},
	# {"---------- FLOOR - FIREPLCE ----------" :''},
	# {"* To Fro: Algoflames2" :'p4-4x6/algoflames2.cfg'},
	# {"To Fro: Algoflames" :'p4-5x6-tofro/algoflames.cfg'},
	# {"To Fro: Betes.2" :'p4-5x6-tofro/betes.cfg'},
	# {"To Fro: Afer Images" :'concentrics/ConcentricAfterImagesAll.app'},
	# {" " :''},
	#{"--- LEFT WALL ----": ""},
	#{"--- Tower w. Bump Collage": "p4-5x8/bump-collage.cfg"},
	#{" ": ""},
	#{"-------- Firestick on FLOOR  -------------": ""},	
	#{"--- p4-6x1-firestick - Honly Tonk box lights": "p4-6x1-firestick/dot-grid.cfg"},
	#{"p4-6x1-firestick - leaninglights": "p4-6x1-firestick/leaninglights-3.cfg"},
	#{"p4-6x1-firestick - algoflames": "p4-6x1-firestick/bundle-algoflames-1.cfg"},
	#{"p4-6x1-firestick - AfterImages": "concentrics/ConcentricAfterImagesAll.app"},
	#{"Upset Cube  - AlgoFlames Pink": "p4-4x4/cube-algoflames-2.cfg"},
	#{"Upset Cube  - AlgoFlames Pink-2": "p4-4x4/cube-algoflames-3.cfg"},
	#{"Material Compositions": "p4-4x4/cube-compositions.cfg"},
	#{"Pixel Shack": "p4-4x4/pixel-shack-4x6.cfg"},
	#{"Pixel Shack - AlgoFlames": "p4-4x4/pixel-shack-algoflames-1b.cfg"},
	#{"--- Inset frame: inset collage 2": "p4-2x2/compositions-2-hub.cfg"},
	#{"--- Small Inset frame: inset collage 3": "p3-2x4/diagnostics.cfg"},
	#{"Inset frame: light grid": "p4-2x2/dot-grid.cfg"},
	#{"Inset frame: inset collage 3": "p4-2x2/compositions-3-hub.cfg"},
	#{"Inset frame: compositions 1": "p4-2x2/compositions-hub.cfg"},
	# {"Wall Hanging: Patched MonoChrome" :'p4-3x8-informal/mono.cfg'},
	# {"Wall Hanging: Patched Yellow" :'p4-3x8-informal/mono-rothko-yellow.cfg'},
	#{".  .  .  .  .  .  .  .  .  .  .  .  .": ""},
	#{"Wall Hanging: Compositions": "p4-3x8-informal/compositions.cfg"},
	#{"Wall Hanging: compositions a": "p4-3x8-informal/compositions.cfg"},
	#{"Wall Hanging: compositions b": "p4-3x8-informal/compositions.cfg"},
	#{".  .  .  .  .  .  .  .  .  .  .  .  .": ""},
	#{".  .  .  .  .  .  .  .  .  .  .  .  .": ""},
	#{"Vert Bars - gray": "p4-5x8/mono-lights-gray.cfg"},
	# {"Square - mono-flavin" :'p4-3x8-informal/mono-flavin.cfg'},
	#{".  .  .  .  .  .  .  .  .  .  .  .  .": ""},
	#{"Wall Hanging: Signage": "p4-3x8-informal/signage.cfg"},
	#{"Wall Hanging: Propagation": "p4-3x8-informal/Propagation.cfg"},
	#{".  .  .  .  .  .  .  .  .  .  .  .  .": ""},
	


	#{"-------- FLOOR - FIREPLCE ------": ""},
	#{"--- pile: Algoflames2.3": "p4-6x8/algofall-2.3.cfg"},
	#{".  .  .  .  .  .  .  .  .  .  .  .  .": ""},
	#{"pile: Algoflames2.2": "p4-6x8/algofall-2.2.cfg"},
	#{"pile: Algoflames2.1": "p4-6x8/algofall-2.1.cfg"},
	#{"pile: Algoflames2.14": "p4-6x8/algofall-2.14.cfg"},
	#{"pile: Algoflames-6": "p4-6x8/algofall6.cfg"},
	#{"pile: Algoflames-6a": "p4-6x8/algofall6a.cfg"},
	#{"pile: image-particles": "p4-6x8/image-particles.cfg"},




	#{"--- Square - mono-flavin" :'p4-4x8/mono-flavin.cfg'},
	#{"--- Square - mono-rothko" :'p4-4x8/mono-rothko.cfg'},
	#{"--- Square scroller": "p4-4x6/scroller-b.cfg"},
	#{"--- Square scroller": "multi/pixel-shack-4x6.cfg"},
	#{"Wall Hanging: Squares": "p4-3x8-informal/quilt-squares.cfg"},
	# {"Square - quilt" :'p4-4x8/quilt-log-cabin.cfg'},
	# {" " :''},
	# {"Square - ICE" :'p4-4x8/square.cfg'},
	# {"Square - ICE - 2" :'p4-4x8/square-ice-2.cfg'},
	#{"Square - pattern-pent" :'p4-4x8/pattern-pent.cfg'},
	#{"Square - mono-flavin-skew" :'p4-4x8/mono-flavin-2.cfg'},
	# {" " :''},
	 #{"Square - marquee a" :'p4-4x8/square-marquee-a.cfg'},
	 
	 #{"Square - marquee b" :'p4-4x8/square-marquee-b.cfg'},
	 #{"Square - marquee c" :'p4-4x8/square-marquee-c.cfg'},
	# {"Square - Collage" :'p4-4x8/square-collage.cfg'},
	# {"Square - Fludd" :'p4-4x8/square-fludd.cfg'},
	# {"Square - RUG" :'p4-4x8/square-rug.cfg'},
	# {" " :''},
	# {"---------- TEST WALL --------------" :''},
	# {"* P3 Wall w. removal: marquee2 - disturbed " :'p3-2x4/marquee2.cfg'},
	# {"* P3 Wall w. removal: cubes - blur" :'p3-2x4/p3-2x6-squares.cfg'},
	# {" " :''},
	# {"P3 Wall w. removal: cubes-b" :'p3-2x4/p3-2x6-squares-b.cfg'},
	# {"P3 Wall w. removal: triangles " :'p3-2x4/p3-2x6.cfg'},
	# {"P3 Wall w. removal: marquee2c - concentric " :'p3-2x4/marquee2c.cfg'},
	# {" " :''},
	# {"P3 sqr w. shift: marquee2b " :'p3-2x4/marquee2b.cfg'},
	# {" " :''},
	# {".  .  .  .  .  .  .  .  .  .  .  .  ." :''},
	# {"ARC - BENT GLITCH" :'p4-1xn-arc/bentglitch.cfg'},
	# {"Arc: Afer Pink" :'concentrics/ConcentricAfterImagesArc.app'},
	# {" " :''},
	#{" ": ""},


	#{"Tower w. Bump Collage2": "p4-5x8/bump-collage2.cfg"},
	#{"Alt Flames": "p4-6x8/alt-flames.cfg"},
	# {"Tower w. Bump Flames" :'p4-5x8/bump-fire.cfg'},
	# {"Tower w. Bump Glitch" :'p4-5x8/bump-glitch.cfg'},
	# {"Tower w. Bump Diagnostics" :'p4-5x8/bump-diagnostics.cfg'},
	#{"Falling Stairs - flames": "p4-2xsteps/algoflames.cfg"},
	#{"Falling Stairs - ice": "p4-2xsteps/algofall.cfg"},
	# {" " :''},
	# {"Three Way Leaning Lights" :'p4-6x8/leaninglights.cfg'},
	# {"Alt Flames" :'p4-6x8/alt-flames.cfg'},
	#{"-------- LEFT / WEST WALL  -------------": ""},
	#{"--- 4x6 bnd: Leaning lights": "p4-4x6-bent-lean/leaninglights-3.cfg"},
	#{"--- TWO FLOW bend": "multi/manifest-4x6.cfg"},
	#{"4x6 bend: Algoflames2.3": "p4-4x6-bent-lean/algofall-2.3.cfg"},
	#{"4x6 bnd: Afer Images": "concentrics/ConcentricAfterImagesAll.app"},
	#{" ": ""},

	#{"-------- NORTH WALL  -------------": ""},
	#{"--- P10 Dangler Torumaline": "p10/dangler-tourmaline.cfg"},
	#{"--- P10 Dangler Flow": "p10/dangler-flow.cfg"},

	#{" ": ""},

	#{"--- P10 Branch: Afer Images": "concentrics/ConcentricAfterImagesAll.app"},
	#{".  .  .  .  .  .  .  .  .  .  .  .  .": ""},
	#{"--- P10 Branch - Collage branch": "p10/collage-lines-1.cfg"},
	#{"P10 Branch - Collage branch 2": "p10/collage-lines-1a.cfg"},
	#{"P10 Branch - Collage branch inv": "p10/collage-lines-2.cfg"},
	#{"P10 Branch - Tourmaline": "p10/collage-tourmaline.cfg"},
	#{".  .  .  .  .  .  .  .  .  .  .  .  .": ""},
	#{"P10 Branch - Glitch": "p10/glitch-screen.cfg"},
	#{"P10 Branch - Algoflames-b": "p10/algoflames-1b.cfg"},
	#{"P10 Branch - Collage": "p10/collage-1.cfg"},

	# {" " :''},
	# {"--------- FLOOR PILE -----------" :''},
	# {"* 3 PILE - compositions" :'p4-3x8-pile/leaninglights-3.cfg'},
	# {"3 PILE - flames" :'p4-3x8-pile/alt-flames-2b.cfg'},

	# {"-------- TABLE -------------" :''},
	# {"Oblong Fire" :'p4-1x4-cube/algoflames.cfg'},
	# {"Oblong Fire 2" :'p4-1x4-cube/algoflames2.cfg'},
	# {"X Pile Quilt" :'p4-2x4/quiltx.cfg'},
	# {"X Pile square-polys" :'p4-2x4/square-polys.cfg'},
	# {"X Pile marquee" :'p4-2x4/marquee2.cfg'},
	# {"X Pile Compositions" :'p4-2x4/compositions.cfg'},
	# {"Wall Hanging: Fludd" :'p4-3x8-informal/fluddc.cfg'},
	# {"* Wall Hanging 3x7: Fludd Factory" :'p4-3x7-informal/fluddc.cfg'},
	# {"* Wall Hanging 3x7: Patched Rothko" :'p4-3x7-informal/mono-rothko.cfg'},
	# {"* Wall Hanging 3x7: Star Quilt" :'p4-3x7-informal/quilt-stars.cfg'},
	# {"* Wall Hanging 3x7: Tri Quilt" :'p4-3x7-informal/quilt-triangles-b.cfg'},
	# {"* Wall Hanging 3x7: Signage Abstraction" :'p4-3x7-informal/signage.cfg'},
	# {".  .  .  .  .  .  .  .  .  .  .  .  ." :''},
	# {" " :''},
	# {"Wall Hanging: FLAG" :'p4-3x8-informal/flag.cfg'},
	# {" " :''},
	# {"3rd Gen Tatlin" :'p4-7x4/mono-flavin2.cfg'},
	# {"Marquee" :'p4-7x4/marquee-b.cfg'},
	# {"Aym Shift: Conveyor" :'p4-10x2-asymshift/screenmedium.cfg'},
	# {"Aym Shift: Flow" :'p4-10x2-asymshift/flow.cfg'},
	# {"Aym Shift: Repeater" :'p4-10x2-asymshift/repeater-cloud.cfg'},
	# {" " :''},
	# {"-------- LEFT WALL -------------" :''},
	# {"* Wall Compositions" :'p4-5x8/compositions.cfg'},
	# {"* Vert Bars - gray" :'p4-5x8/mono-lights-gray.cfg'},
	# {"Vert Bars - yellow" :'p4-5x8/mono-lights-yellow.cfg'},
	# {"Horizontal Bars" :'p4-5x8/mono-lights-h.cfg'},
	# {" " :''},
	# {"3 PILE - movement" :'p4-3x8-pile/square-ice-2.cfg'},
	# {"P10 BUNDLE PILE - leaning pattern" :'p10/bundle-lines-2.cfg'},

	#{"-------- PLANK AND DOOR  -------------": ""},
	#{"--- P10 Plank-Door - Tourmanline": "p10/plank-tourmaline.cfg"},
	#{".  .  .  .  .  .  .  .  .  .  .  .  .": ""},
	#{"P10 Plank-Door - AlgoFlames": "p10/plank-algoflames-1b.cfg"},
	#{"P10 Plank-Door - movement": "p10/plank-movement-2.cfg"},
	#{"P10 Plank-Door - glitch": "p10/plank-glitch.cfg"},
	# {"P10 Plank-Door - gradients" :'p10/plank-gradients.cfg'},
	# {"P10 Plank-Door - collage" :'p10/plank-collage-1.cfg'},
	# {"* Tower: Monument to the Glitch" :'p4-7x8-tower/screen.cfg'},
	# {"* Pencil Tower: Monument to the Glitch" :'p10-twr4/6x4-monument-to-the-glitch.cfg'},
	# {"* Pencil Tower: Tourmaline" :'p10-twr4/6x4-tourmaline.cfg'},
	# {"* Pencil Tower: Afer Images" :'concentrics/ConcentricAfterImagesAll.app'},
	#{"--- Bad flare - mono-flavin-b" :'p4-4x4/mono-flavin-b.cfg'},
	#{"--- Afer Images": "concentrics/ConcentricAfterImagesAll.app"},
	#{"--- Pixel Shack": "p4-4x6/pixel-shack-4x6-b.cfg"},

	#{" ": ""},
	#{"--------- FLOOR -----------": ""},
	#{"Broken Sqr in Oblong - mono-flavin" :'p4-4x4/mono-flavin.cfg'},
	#{"Broken Sqr in Oblong - collage" :'p4-4x4/collage.cfg'},
	#{"Broken Sqr in Oblong - bluefire" :'p4-4x4/bluefire.cfg'},
	#{"--- P10 Plank-Door - AlgoFlames Pink": "p10/plank-algoflames-2.cfg"},
	#{"--- RIGHT WALL -------------": ""},
	#{"--------- Partial Plinth -----------" :''},



]


def verify():
	# print("==>",Lb.curselection())
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

		if JavaAppRunning != '' :
			os.system("ps -ef | pgrep -f " + JavaAppRunning + " | xargs sudo kill -9;")

		configSelected = a[1]
		configToRun = configSelected[list(configSelected.keys())[0]]
		execute(configToRun)


def stopAll():
	# print("Tkinter is easy to use!")
	os.system("ps -ef | pgrep -f player | xargs sudo kill -9;")


root = tk.Tk()
#frame = tk.Frame(root, bg="darkgray")
#frame.pack(padx=1, pady=1)
# width x height x X x Y
root.geometry("%dx%d+%d+%d" % (680, 740, 1200, 100))

Lb1 = Listbox(root, width=33, height=42)
Lb2 = Listbox(root, width=32, height=42)

for i, item in enumerate(actionDict1):
	Lb1.insert(END, " " + list(item.keys())[0])


for i, item in enumerate(actionDict2):
	Lb2.insert(END, " " + list(item.keys())[0])

#Lb1.pack(side=tk.LEFT, padx=0, ipadx=10)
#Lb2.pack(side=tk.LEFT, ipadx=10, expand=0)
Lb1.place(bordermode=OUTSIDE, x=2, y=2)
Lb2.place(bordermode=OUTSIDE, x=300, y=2)

topBtnPlace = 400
leftBtnPlace = 560

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



root.mainloop()




