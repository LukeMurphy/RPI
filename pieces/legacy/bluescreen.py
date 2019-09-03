import math
import random
import time

# ################################################## #


def test():
	global config
	config.actions.explosion()


def draw():
	global config
	config.image = config.Image.new("RGBA", (config.actualScreenWidth, 32))
	config.draw = config.ImageDraw.Draw(config.image)
	config.draw.rectangle(
		(0, 0, config.actualScreenWidth, 32), fill=(0, 0, int(255 * config.brightness))
	)
	config.id = config.image.im.id
	config.matrix.SetImage(config.id, 1, 1)
	# time.sleep(int(random.uniform(.1,4)))

	if random.random() > 0.8:
		config.image = config.image.rotate(int(random.uniform(-5, 5)))
	config.id = config.image.im.id
	config.matrix.SetImage(config.id, 0, 0)
	x = 10 + int(random.random() * config.actualScreenWidth)
	config.matrix.SetImage(config.id, 0, 0)
	config.actions.drawBlanks()

	for n in range(0, 25):
		if random.random() > 0.8:
			config.matrix.SetImage(config.id, 0, 0)
			if random.random() > 0.8:
				config.actions.setBlanks()
				config.actions.drawBlanks()
		if random.random() > 0.8:
			config.actions.drawBlanks()
		y = 10 + int(random.random() * 31)
		config.matrix.SetPixel(
			x, y, int(220 * config.brightness), int(120 * config.brightness), 0
		)
		time.sleep(0.25)
