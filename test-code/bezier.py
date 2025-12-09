# import matplotlib.pyplot as plt
# import matplotlib.path as mpath
# import matplotlib.patches as mpatches

# # Defining control points 
# verts = [(0, 0), (1, 1), (2, -1), (3, 0)]

# # Creating a Path object using Bezier curve
# path = mpath.Path(verts, [mpath.Path.MOVETO, mpath.Path.CURVE4, mpath.Path.CURVE4, mpath.Path.CURVE4])

# # Creating a patch representing the Bezier curve
# patch = mpatches.PathPatch(path, facecolor='none', lw=2)

# # Plotting the Bezier curve
# fig, ax = plt.subplots()
# ax.add_patch(patch)
# # Highlighting control points
# ax.scatter(*zip(*verts), c='red', marker='o')  
# ax.set_xlim(-1, 4)
# ax.set_ylim(-2, 2)
# plt.title('Simple Bezier Curve')
# plt.show()


from PIL import Image, ImageDraw
from bezier_interpolation import cubic_interpolation, quadratic_interpolation

# c_data = {"x": [1, 2, 3], "y": [-1, -5, 3]}
# c_data = list(zip(c_data["x"], c_data["y"]))
# c_interpolated_data = cubic_interpolation(c_data)
# print(c_interpolated_data)
# Returns: [[1, -1], [1.3, -3.3], [1.6 -5.6], [2, -5], [2.3, -4.3], [2.6, -0.6], [3, 3]]

q_data = [(10, 10), (20, 40), (30, 90)]
q_interpolated_data = quadratic_interpolation(q_data) * 10
# print(q_interpolated_data)
# Returns:  [[1, 1], [1.5, 2.5], [2, 4], [2.5, 5.5], [3, 9]]

_img = Image.new("RGBA", (800,800))

_imgDraw = ImageDraw.Draw(_img)

_plotDataX = q_interpolated_data[:,0].astype(float)
_plotDataY = q_interpolated_data[:,1].astype(float)
for pt in range(len(_plotDataX)-2) :

    _p1X = _plotDataX[pt]
    _p1Y = _plotDataY[pt]
    _p2X = _plotDataX[pt + 1]
    _p2Y = _plotDataY[pt + 1]

    _imgDraw.line((_p1X,_p1Y,_p2X,_p2Y), joint="curve", width= 2, fill=(255,0,0))

for pt in range(len(q_data)-2) :
    _imgDraw.line((q_data[pt],q_data[pt+1]), joint="curve", width= 2, fill=(255,0,0))


_img.show("Test")