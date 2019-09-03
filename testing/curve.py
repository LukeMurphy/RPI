import math

from PIL import Image, ImageDraw

image = Image.new("RGB", (1190, 841), "white")
draw = ImageDraw.Draw(image)
curve_smoothness = 100

# First, select start and end of curve (pixels)
curve_start = [(1, 1)]
curve_end = [(678, 128)]

# Second, split the path into segments
curve = []
for i in range(1, curve_smoothness, 1):
	split = (curve_end[0][0] - curve_start[0][0]) / curve_smoothness
	x = curve_start[0][0] + split * i
	curve.append(
	    (
	        x,
	        -7 * math.pow(10, -7) * math.pow(x, 3)
	        - 0.0011 * math.pow(x, 2)
	        + 0.235 * x
	        + 682.68,
	    )
	)

# Third, edit any other corners of polygon
other = [(1026, 721), (167, 688)]

# Finally, combine all parts of polygon into one list
xys = (
	curve_start + curve + curve_end + other
)  # putting all parts of the polygon together
draw.polygon(xys, fill=None, outline=256)

image.show()
