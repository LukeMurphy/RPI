##convert-to-gif

from moviepy.editor import *


def convert() :
	clip = (VideoFileClip("Untitled.mpg").resize(.5))
	clip.write_gif("repeater.gif")


convert()