from Tkinter import *


def run():
	root = Tk()
	w = 600
	h = 500
	foo = Canvas(root, width=w, height=h)
	foo.pack()
	global data
	data = {}
	data["foo"] = foo
	data["w"] = w
	data["h"] = h
	init()
	timerFired()
	root.mainloop()


def init():
	global data
	data["squareColor"] = "blue"
	data["squareLeft"] = 50
	data["squareTop"] = 50
	data["squareSize"] = 50
	data["counter"] = 0
	data["goingR"] = True
	data["goingD"] = False


def timerFired():
	global data
	foo = data["foo"]
	doTimerFired()
	redrawAll()
	delay = 10
	foo.after(delay, timerFired)


def doTimerFired():
	global data
	if data["goingR"]:
	    if data["squareLeft"] + data["squareSize"] > data["w"]:
	        data["goingR"] = False
	    else:
	        moveRight()
	else:
	    if data["squareLeft"] < 0:
	        data["goingR"] = True
	    else:
	        moveLeft()
	if data["goingD"]:
	    if data["squareTop"] + data["squareSize"] > data["h"]:
	        data["goingD"] = False
	    else:
	        moveDown()
	else:
	    if data["squareTop"] < 0:
	        data["goingD"] = True
	    else:
	        moveUp()


def moveLeft():
	global data
	data["squareLeft"] -= 5


def moveRight():
	global data
	data["squareLeft"] += 5


def moveUp():
	global data
	data["squareTop"] -= 5


def moveDown():
	global data
	data["squareTop"] += 5


def redrawAll():
	global data
	data["foo"].delete(ALL)
	data["foo"].create_rectangle(
	    data["squareLeft"],
	    data["squareTop"],
	    data["squareLeft"] + data["squareSize"],
	    data["squareTop"] + data["squareSize"],
	    fill=data["squareColor"],
	)


run()
