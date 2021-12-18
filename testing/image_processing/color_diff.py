from PIL import Image
import numpy as np
import math

im = np.array(Image.open('lena.jpg'))
im_R = np.array(Image.open('white.jpg'))

# im.shape[1]
print(im.shape)
rads = math.pi / im.shape[0]
for c in range(0, im.shape[0] - 3, 1):
	for r in range(0, im.shape[1] - 3, 3):
		rVal = round(abs(math.cos(c * rads * .5)) * r)
		cVal = round(abs(math.sin(r * rads * .75)) * c)
		#im_R[c,r] = im[cVal,rVal]

		rVal = im[c,r][0]
		gVal = im[c,r][1]
		bVal = im[c,r][2]

		im_R[c,r+0] = [rVal,0,0]
		im_R[c,r+1] = [0,gVal,0]
		im_R[c,r+2] = [0,0,bVal]





im_G = im.copy()
im_G[:, :, (0, 2)] = 0


im_B = im.copy()
im_B[:, :, (0, 1)] = 0

im_RGB = np.concatenate((im_R, im_G, im_B), axis=0)
#im_RGB = np.hstack((im_R, im_G, im_B))
#im_RGB = np.c_['1', im_R, im_G, im_B]

pil_img = Image.fromarray(im_RGB)
pil_img.save('lena_numpy_split_color.png')