
'''
data = numpy.array(imageToRender)

try :
	im_rgb = data[:, :, [0, 2, 1, 3]]
except Exception as e :
	im_rgb = data[:, :, [0, 2, 1]]

data2 = numpy.array(im_rgb)

imageToRender = Image.fromarray(data2)
'''

from PIL import Image
import numpy as np

arr = np.zeros([150, 250, 4], dtype=np.uint8)

arr[:, :50] = [255, 128, 0, 255]

arr[:, 100:220] = [0, 0, 255, 100]

img = Image.fromarray(arr)

# img.show()

img.save("RGBA_image.png")
'''

data = [1,2,3,4,5,6,7,8,9]
print(data)

d2 = data[1:]
print(d2)

d2 = data[:2]
print(d2)

d2 = data[::2]
print(d2)

d2 = data[::-1]
print(d2)

d2 = data[::-3]
print(d2)

datax = np.array([ [ 1,  2,  3,  4], [ 5,  6,  7,  8], [ 9, 10, 11, 12], [13, 14, 15, 16] ])

d2 = datax[1:2, ::2]
print(d2)

d2 = datax[1:2, [0,2,1]]
print(d2)

d2 = datax[:, [0,2,1]]
print(d2)
'''
