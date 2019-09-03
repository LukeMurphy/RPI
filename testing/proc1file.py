import random
import threading
import time

xpos = 0
delay = 0.2
clr = "yellow"


def proc1():
	while True:
	    drawRef.rectangle((xpos, 0, 250, 500), fill="red")
	    drawRef.rectangle(
	        (
	            xpos,
	            0,
	            xpos + round(random.uniform(10, 100)),
	            round(random.uniform(10, 200)),
	        ),
	        fill=clr,
	    )
	    time.sleep(delay)
