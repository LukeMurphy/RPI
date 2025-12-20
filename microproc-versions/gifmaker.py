import os
import imageio.v3 as imageio

import re

_nsre = re.compile('([0-9]+)')
def natural_sort_key(s):
    return [int(text) if text.isdigit() else text.lower()
            for text in re.split(_nsre, s)] 
def convert(str):
    return int("".join(re.findall("\d*", str)))

png_dir = '/Users/lamshell/Downloads/sequence/'
images = []

listOfFiles = sorted(os.listdir(png_dir), key=natural_sort_key)

for file_name in listOfFiles :
    if file_name.endswith('.png'):
        file_path = os.path.join(png_dir, file_name)
        images.append(imageio.imread(file_path))

listOfFiles = sorted(os.listdir(png_dir), key=natural_sort_key, reverse=True)

for file_name in listOfFiles :
    if file_name.endswith('.png'):
        file_path = os.path.join(png_dir, file_name)
        images.append(imageio.imread(file_path))

# Make it pause at the end so that the viewers can ponder
# for _ in range(10):
#     images.append(imageio.imread(file_path))


# imageio.mimsave('/Users/lamshell/Downloads/movie.gif', images)
imageio.imwrite('/Users/lamshell/Downloads/movie.gif', images, fps=60, duration=0)