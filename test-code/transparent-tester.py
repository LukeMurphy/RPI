# importing image object from PIL
import math
from PIL import Image, ImageDraw, ImageFilter

w, h = 220, 190
shape = [(40, 40), (w - 10, h - 10)]

# creating new Image object
img1 = Image.new("RGBA", (w, h))
img1Draw = ImageDraw.Draw(img1)  
img1Draw.rectangle((0,0,w,h), fill =(0,0,0,255))
img1Draw.rectangle(shape, fill =(255,0,0,255))
img1Draw.rectangle((0,0,100,100), fill =(0,0,255,115), outline=(0,255,0,100), width=10)
img1.save("test-image.png")

img2 = Image.new("RGBA", (w, h))
img2Draw = ImageDraw.Draw(img2)  
img2Draw.rectangle((50,50,140,140), fill =(0,0,255,115), outline=(0,255,0,100), width=20)

composite = Image.alpha_composite(img1, img2)
composite.save("test-image-composite.png")

mask = Image.new("L", (w,h), 0)
draw = ImageDraw.Draw(mask)
draw.ellipse((50, 50, 120, 120), fill=255)

img3 = Image.composite(composite, img1, mask)
img3.save("test-image-mask.png")

mask_blur = mask.filter(ImageFilter.GaussianBlur(10))
img4 = Image.composite(composite, img1, mask_blur)
img4.save("test-image-maskblur.png")