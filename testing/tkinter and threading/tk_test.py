# Import Module
from tkinter import *
import time
import threading

# Create Object
root = Tk()

global t1

# Set geometry
root.geometry("400x400")

# use threading



# Python program creating
# three threads
 
 
# counts from 1 to 9
def func(number):
	print(threading.active_count())

	for i in range(1, 10):
		time.sleep(2)
		print('Thread ' + str(number) + ': prints ' + str(number*i))
 
# creates 3 threads

def threadingAction():
	for i in range(0, 3):
		t = threading.Thread(target=func, args=(i,))
		t.start()


# work function
def work():

	print("sleep time start")

	for i in range(10):
		print(i)
		time.sleep(3)

	print("sleep time stop")

# Create Button
Button(root,text="Click Me",command = threadingAction).pack()

# Execute Tkinter
root.mainloop()
