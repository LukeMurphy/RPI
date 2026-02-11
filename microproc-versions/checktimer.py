import time
import random
import machine
import os
from interstate75 import Interstate75, DISPLAY_INTERSTATE75_64X64
i75 = Interstate75(display=DISPLAY_INTERSTATE75_64X64)
display = i75.display

def checkTime():
    hour  = time.localtime()[3]
    minute = time.localtime()[4]
    keepOn = False
    if hour >= 8 and hour <= 23 :
        keepOn = True
        
        
    if hour >= 1 and minute >= 3:
        keepOn = False
        
        
    if hour >= 1 and minute >= 11:
        keepOn = True
        
    # if random.random() < .05 :
        
    #     os.system('sudo reboot')
            
    return keepOn
