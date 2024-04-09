import argparse
import math
import random
import time
import types
import noise
from modules import colorutils

# Doing this because choosing from HSL or HSV ranges and then excluding certain ranges
# was becoming awkward 
# Middle English awkeward in the wrong direction, from awke turned the wrong way, from Old Norse ǫfugr; akin to Old High German abuh turned the wrong way

# ------- use this way :
 
# paletteList = (workConfig.get("noisescroller", "paletteSets")).split(",")
# config.palette = Palette(paletteList, workConfig)
# barColor = config.palette.chooseFromPalette(100,config.brightness)

# ------- in config file in primary piece-section, declare palettes to be used
# paletteSets = pal-yellows,pal-pinks

# ------- Add colors as HSL ranges 

# [pal-reds]
# hMin = 0
# hMax = 20
# sMin = .8
# sMax = 1.0
# lMin = .20
# lMax = .5

# [pal-pinks]
# hMin = 330
# hMax = 350
# sMin = 1.0
# sMax = 1.0
# lMin = .25
# lMax = .4

# [pal-rose]
# hMin = 340
# hMax = 345
# sMin = .90
# sMax = 1.0
# lMin = .2
# lMax = .5

# [pal-yellows]
# hMin = 37
# hMax = 58
# sMin = .8
# sMax = 1.0
# lMin = .40
# lMax = .5

class Palette :
    
    def __init__(self, paletteList, configRef):
        
        self.paletteRangeList = []
        self.confifRef = configRef

        for p in paletteList :
            hMin = float(self.confifRef.get(p, "hMin"))
            hMax = float(self.confifRef.get(p, "hMax"))
            sMin = float(self.confifRef.get(p, "sMin"))
            sMax = float(self.confifRef.get(p, "sMax"))
            lMin = float(self.confifRef.get(p, "lMin"))
            lMax = float(self.confifRef.get(p, "lMax"))
            
            self.paletteRangeList.append([hMin,hMax,sMin,sMax,lMin,lMax])
            
        # print(self.paletteRangeList)
        
    def chooseFromPalette(self,a,brtns) :
        i = math.floor(random.uniform(0, len(self.paletteRangeList)))
        hslRange = self.paletteRangeList[i]
        color = colorutils.getRandomColorHSL(hslRange[0],hslRange[1],hslRange[2],hslRange[3],hslRange[4],hslRange[5],0,0,a,brtns)
        return color
    
    
        
        
        
            
            
        

