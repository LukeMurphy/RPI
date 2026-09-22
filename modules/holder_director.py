# Generic classes for adding config info and managing timing for
# animation vs simple delays in loops etc
import time, random

from modules.configuration import pieceLogger


class Holder:
    def __init__(self, *args, **kwargs):
        if args is not None:
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

    slotRate = 0.5
    baseSlotRate = 0.5
    actionDelay = 0.5
    loopDelay = 0.03
    redrawSpeed = 0.02
    advance = False
    minslotRate = 0.5
    maxslotRate = 0.5
    timingVariability = 0.25

    def __init__(self, config):
        super(Director, self).__init__()
        self.config = config
        self.tT = time.time()

    def setSlotTimeRange(self, setBase = False):
        if setBase :
            self.baseSlotRate = self.slotRate
        self.minslotRate = self.baseSlotRate * (1.0 - self.timingVariability)
        self.maxslotRate = self.baseSlotRate * (1.0 + self.timingVariability)
        self.slotRate = self.randomRange(self.minslotRate, self.maxslotRate, True)
        # pieceLogger(f"New slotRate {self.slotRate}")

    def reset(self):
        self.advance = False
        self.tT = time.time()
        print(f"[holder_director.py: Director.reset] >> New rate: {self.slotRate}")

    def checkTime(self):
        if (time.time() - self.tT) >= self.slotRate:
            self.tT = time.time()
            self.advance = True
        else:
            self.advance = False

    def next(self):
        self.checkTime()

    def randomRange(self, a, b, rounded=False):
        if not rounded:
            return random.uniform(a, b)
        else:
            return round(random.uniform(a, b))
