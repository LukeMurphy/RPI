from OpenGL import *
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *


x = 10.0

def myInit():
    glClearColor(1.0, 1.0, 0.0, 1.0)
    glColor3f(0.2, 0.5, 0.4)
    glPointSize(10.0)
    gluOrtho2D(0, 500, 0, 500)





glutInit()

def display():

    global x
    glClearColor(0.0, 0.0, 0.0, .150)

    glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)


    glBegin(GL_POINTS)
    glVertex2f(100, 100)
    glVertex2f(300, 200)
    glEnd()

    glColor3f(0.8, 0.5, 0.5)
    glBegin(GL_QUADS)
    glVertex2f(x, 100.0)
    glVertex2f(300.0 + x, 100.0)
    glVertex2f(300.0 + x, 200.0)
    glVertex2f(100.0 + x, 200.0)
    glEnd()

    glBegin(GL_TRIANGLE_STRIP)
    glVertex2f(100.0 + x, 210.0)
    glVertex2f(300.0 + x, 210.0)
    glVertex2f(300.0 + x, 310.0)
    glEnd()

    glFlush()

    x+=.10

    glutSwapBuffers()
    glutPostRedisplay()

def main():
    glutInitDisplayMode(GLUT_SINGLE | GLUT_RGB)
    glutInitWindowSize(500, 500)
    glutInitWindowPosition(1100, 100)
    glutCreateWindow("My OpenGL Code")
    myInit()
    glutDisplayFunc(display)
    glutMainLoop()

if __name__=='__main__':
    main()


