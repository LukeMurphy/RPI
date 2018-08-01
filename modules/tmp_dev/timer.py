import time
import random
import math

import sys
import threading
from time import sleep
import _thread
from threading import Timer


#from _thread import Timer

"Timer utiltiy"
class TimerClass:


	complete =  False
	tDelta = 0
	timeTrigger = False
	t1 = 0

	## "Public" variables that can be set
	randomSteps = True
	steps = 100
	tLimit = 10
	tLimitBase = 10


	def __init__(self): 
		self.t1 = time.time()
		self.timeTrigger = False

	
	def checkTime(self):
		t = time.time()
		self.tDelta = (t - self.t1)
		if self.tDelta > self.tLimit :
			self.complete = True	


	def timeOut(self, t , callBack = None) :
		self.complete = False
		self.t1 = time.time()
		tLimit = t


def looper(arg, delta):
    while 1:
        print (arg)
        try:
            time.sleep(delta)
        except:
            continue

def fcu():
	print("hi")


'''
t1  = threading.Thread.__init__(looper('foo',1))
t2 = threading.Thread.__init__(looper('bar',.5))
t2.start()
t1.start()
'''

t = Timer(3.0, fcu)
t.start()