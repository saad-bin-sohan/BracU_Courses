from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random
import time
from math import cos, sin, pi

class Point:
    def __init__(self, x, y, color, speed):
        self.x = x
        self.y = y
        self.color = color
        self.speed = speed
        self.dx = random.choice([-1, 1]) * speed
        self.dy = random.choice([-1, 1]) * speed
        self.blink_timer = 0.0
        self.is_blinking = False

    def update(self, delta_time):
        self.x += self.dx * delta_time
        self.y += self.dy * delta_time

        if self.x < -1.0:
            self.x = -1.0
            self.dx *= -1
        elif self.x > 1.0:
            self.x = 1.0
            self.dx *= -1
        if self.y < -1.0:
            self.y = -1.0
            self.dy *= -1
        elif self.y > 1.0:
            self.y = 1.0
            self.dy *= -1

        if self.is_blinking:
            self.blink_timer += delta_time
            if self.blink_timer >= 1.0:
                self.is_blinking = False
                self.blink_timer = 0.0

    def draw(self):
        if self.is_blinking:
            glColor3fv([0.0, 0.0, 0.0])
        else:
            glColor3fv(self.color)
        self.draw_circle(self.x, self.y, 0.02)

    def draw_circle(self, x, y, radius):
        glBegin(GL_TRIANGLE_FAN)
        glVertex2f(x, y)
        for i in range(361):
            angle = 2 * pi * i / 360
            glVertex2f(x + radius * cos(angle), y + radius * sin(angle))
        glEnd()

class Box:
    def __init__(self):
        self.points = []
        self.is_frozen = False

    def add_point(self, x, y):
        if not self.is_frozen:
            color = (random.uniform(0.7, 1.0), random.uniform(0.7, 1.0), random.uniform(0.7, 1.0))
            speed = 0.1
            self.points.append(Point(x, y, color, speed))

    def update(self, delta_time):
        if not self.is_frozen:
            for point in self.points:
                point.update(delta_time)

    def draw(self):
        for point in self.points:
            point.draw()

    def handle_mouse_button(self, button, state, x, y):
        if not self.is_frozen:
            if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
                for point in self.points:
                    point.is_blinking = True
            elif button == GLUT_RIGHT_BUTTON and state == GLUT_DOWN:
                normalized_x = (x / glutGet(GLUT_WINDOW_WIDTH)) * 2 - 1
                normalized_y = 1 - (y / glutGet(GLUT_WINDOW_HEIGHT)) * 2
                self.add_point(normalized_x, normalized_y)

def display():
    glClear(GL_COLOR_BUFFER_BIT)
    box.draw()
    glutSwapBuffers()

def handle_key(key, x, y):
    if key == b' ':
        box.is_frozen = not box.is_frozen
    elif key == b'\x1b':
        glutLeaveMainLoop()
    glutPostRedisplay()

def special_key_listener(key, x, y):
    if key == GLUT_KEY_UP:
        for point in box.points:
            point.dx *= 1.1
            point.dy *= 1.1
    elif key == GLUT_KEY_DOWN:
        for point in box.points:
            point.dx *= 0.9
            point.dy *= 0.9

def idle():
    global last_time
    current_time = time.time()
    delta_time = current_time - last_time
    last_time = current_time
    box.update(delta_time)
    glutPostRedisplay()

def reshape(width, height):
    glViewport(0, 0, width, height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(-1.0, 1.0, -1.0, 1.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

global box
global last_time
glutInit()
glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)
glutInitWindowSize(800, 800)
glutCreateWindow("Moving Points")
glutDisplayFunc(display)
glutIdleFunc(idle)
glutReshapeFunc(reshape)
glutMouseFunc(lambda button, state, x, y: box.handle_mouse_button(button, state, x, y))
glutKeyboardFunc(handle_key)
glutSpecialFunc(special_key_listener)

glClearColor(0.0, 0.0, 0.0, 1.0)

box = Box()

last_time = time.time()

glutMainLoop()
