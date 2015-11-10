#!/usr/bin/python

#import modules

from modules import utils, actions,machine,scroll,user,bluescreen ,loader, squares
import Image
import ImageDraw
import time
import random
from rgbmatrix import Adafruit_RGBmatrix
import datetime
import ImageFont
import textwrap
import math

# ################################################### #

#matrix = Adafruit_RGBmatrix(32, 4)
#image = Image.new("RGBA", (128, 32))
#draw  = ImageDraw.Draw(image)
#id = image.im.id
#matrix.SetImage(id, 0, 0)


matrix = Adafruit_RGBmatrix(32, 8)



config = utils
config.matrix = matrix
#config.id = id
#config.draw = draw
#config.image = image
config.Image = Image
config.ImageDraw = ImageDraw
config.ImageFont = ImageFont
config.imageTop = Image.new("RGBA", (256, 64))
config.imageBottom = Image.new("RGBA", (256, 64))

config.actions = actions
action = actions
action.config = config

scroll = scroll
scroll.config = config

user = user
user.config = config

imgLoader = loader
imgLoader.config = config

concentric = squares
concentric.config = config
concentric.colorSwitch = False


def seq2() :
	n = 0
	while (n<2):
		msg = 'Infinite beatitude of existence! It is; and there is nothing else beside It. It fills all Space, and what It fills, It is. What It thinks, that It utters; and what It utters, that It hears; and It itself is Thinker, Utterer, Hearer, Thought, Word, Audition; it is the One, and yet the All in All. Ah, the happiness, ah, the happiness of Being! Ah, the joy, ah, the joy of Thought! What can It not achieve by thinking! Its own Thought coming to Itself, suggestive of its disparagement, thereby to enhance Its happiness! Sweet rebellion stirred up to result in triumph! Ah, the divine creative power of the All in One! Ah, the joy, the joy of Being! Me me me I mine mine mine is'
		msg = "TEST-1234567890****"
		scroll.scrollMessage(msg, True, False, "Bottom")
		n+=1
		
seq2()


