#!/usr/bin/python
import numpy as np
import matplotlib.pyplot as plt
N = 5
# The golden ratio
phi = (1.0+np.sqrt(5.0))/2
# angle increment
theta0 = np.pi/5
LEFT = 0
RIGHT = 1
# fill plot a pentagon with center at (Xorig, Yorig) and orientation theta
def pentagon (Xorig, Yorig, theta):
    Ind = np.arange(N+1)
    X = np.cos(Ind*2*np.pi/N+theta)+Xorig
    Y = np.sin(Ind*2*np.pi/N+theta)+Yorig
    plt.fill(X, Y, 'r-')
# At each step three edges are generated
# and two recursive calls are made
def stepSplit (previousPoint, previousTurn, theta, nIter):
    if nIter == 0:
        return
    if previousTurn == RIGHT:
        # Turn left 
        theta = theta+theta0
    elif previousTurn == LEFT:
        # turn right 
        theta = theta-theta0
    nextPoint = previousPoint + phi*np.array([np.cos(theta), np.sin(theta)])
    X, Y = zip(previousPoint, nextPoint)
    pentagon (nextPoint[0], nextPoint[1], theta)
    # Update
    previousPoint[:] = nextPoint[:]
    # Bifurcation
    # Turn left 
    theta1 = theta+theta0

    nextPoint = previousPoint + phi*np.array([np.cos(theta1), np.sin(theta1)])
    X, Y = zip(previousPoint, nextPoint)
    pentagon (nextPoint[0], nextPoint[1], theta1)
    stepSplit(nextPoint, LEFT, theta1, nIter-1)

    # Turn right 
    theta1 = theta-theta0
    nextPoint = previousPoint + phi*np.array([np.cos(theta1), np.sin(theta1)])
    X, Y = zip(previousPoint, nextPoint)
    pentagon (nextPoint[0], nextPoint[1], theta1)
    stepSplit(nextPoint, RIGHT, theta1, nIter-1)

# fill plot pentagons
# Central pentagon
pentagon (0.0, 0.0, 0.0)
for i in [1, 3, 5, 7, 9]:
    stepSplit (np.array([0.0, 0.0]), -1, i*theta0, 5)

for i in [0, 2, 4, 6, 8]:
    theta = i*np.pi/5
    x0 = phi*(1.0+2*np.cos(np.pi/5))*np.cos(theta)
    y0 = phi*(1.0+2*np.cos(np.pi/5))*np.sin(theta)
    pentagon (x0, y0, theta0)
    stepSplit (np.array([x0, y0]), -1, theta, 4)

plt.axes().set_aspect ('equal')
plt.axis('off')
plt.savefig("pentagonLattice4.png", bbox_inches='tight')
plt.show()