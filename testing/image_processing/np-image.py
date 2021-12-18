from PIL import Image
from PIL import ImageDraw, ImageFont, ImageTk
import numpy as np
import tkinter as tk
import random, time

testImage = 'img.jpg'
testImage = 'pattern-t4.jpg'
testImage = 'pattern-t2b.jpg'

im = Image.open(testImage)
#im = im.resize((256,256))
#im.show()


im2arr = np.array(im) # im2arr.shape: height x width x channel
arr2im = Image.fromarray(im2arr)
#arr2im.show()

im = np.array(Image.open(testImage))
#.resize(256, 256)
im_RGB = im // 2 * 22
'''

im_R = im.copy()
im_R[:, :, (1, 2)] = 0

im_G = im.copy()
im_G[:, :, (0, 2)] = 0

im_B = im.copy()
im_B[:, :, (0, 1)] = 0

im_RGB = np.concatenate((im_R, im_G, im_B), axis=1)
# im_RGB = np.hstack((im_R, im_G, im_B))
# im_RGB = np.c_['1', im_R, im_G, im_B]
'''

pil_img = Image.fromarray(im_RGB)
#pil_img.save('lena_numpy_split_color.png')
#pil_img.show()


class App():

	limUp = 100
	limDown = 1
	d = 1
	delta = 1

	dMult = 16
	d2 = 4
	delta2 = 10

	def __init__(self):
		#threading.Thread
		#threading.Thread.__init__(self)
		#self.start()
		pass

	def callback(self):
		self.root.quit()

	def run(self):
		self.root = tk.Tk()
		# self.root.protocol("WM_DELETE_WINDOW", self.callback)

		# label = Label(self.root, text="Hello World")
		# label.pack()

		#tk.Button(self.root, text="Quit", command=self.root.quit).pack()

		self.cnvs = tk.Canvas(self.root, width=256, height=256)
		self.cnvs.pack()
		self.cnvs.create_rectangle(0, 0, 200, 200, fill="blue")
		self.cnvs.update()
		#self.render()
		self.root.after(100, self.startWork)
		self.root.mainloop()

	def startWork(self):
		while True:
			#datab = self.data // self.d * self.dMult

			#datab = self.data * self.d
			datab = self.data
			datab = .50 * np.sin(10.0 * self.data + self.d/3) * self.data + self.data * 2.0

			self.limUp = 512
			datab = np.roll(datab, int(self.d), (0))


			#datab = datab[:, :, [0, 2, 1]]
			a.renderImageFull = Image.fromarray(datab.astype('uint8'))
			#a.renderImageFull.convert('RGBA')
			self.render()
			self.d += self.delta

			if self.d >= self.limUp or self.d <= self.limDown :
				self.delta *= -1
				self.d2 += self.delta2
				if self.d2 >= 255 or self.d <= 1 :
					self.delta2 *= -1

			time.sleep(.02)


	def render(self):
		self.cnvs.delete("main1")
		self.cnvs._image_tk = ImageTk.PhotoImage(self.renderImageFull)
		self.cnvs._image_id = self.cnvs.create_image(
			0,
			0,
			image=self.cnvs._image_tk,
			anchor="nw",
			tag="main1",
		)
		self.cnvs.update()

'''
'''
a = App()#im.resize(512, 512)
a.data = np.array(im)
a.run()




