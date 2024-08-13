# Generic classes for adding config info and managing timing for
# animation vs simple delays in loops etc

import argparse
import math
import random
import time
import types

class Holder:
    def __init__(self, *args, **kwargs):
        if args != None:
            self.config = args


class Director:
    """docstring for Director"""
    
    # slotRate is the period between events
    # this is just an interval timer but the main
    # interate function has a delay set in the config - usually about .02 seconds
    # so every .02 seconds this class instance is checked to see if the interval 
    # of time that equals the "slotRate" has been passed, and if it has, the 
    # class sets the advance to True and the calling function has to reset the
    # advance to False

    slotRate = .5

    def __init__(self, config):
        super(Director, self).__init__()
        self.config = config
        self.tT = time.time()

    def checkTime(self):
        if (time.time() - self.tT) >= self.slotRate:
            self.tT = time.time()
            self.advance = True
        else:
            self.advance = False

    def next(self):
        self.checkTime()