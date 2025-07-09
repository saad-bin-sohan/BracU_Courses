from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random
import time
import math

W_width, W_height = 500, 500
bg_color = "white"
rain_color = (1.0, 0.65, 0.0)
angle = 0

class Raindrop:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speed = 3.0

    def update(self):
        global angle
        self.x += self.speed * math.sin(math.radians(angle))
        self.y -= self.speed * math.cos(math.radians(angle))
        if self.y < 140 or self.check_collision_with_house():
            self.reset()
    def reset(self):
        self.y = 500
        self.x = random.uniform(-1000, 1000)

    def check_collision_with_house(self):
        left_roof_slope = (300 - 200) / (250 - 50)
        right_roof_slope = (300 - 200) / (250 - 450)
        left_roof_intercept = 300 - left_roof_slope * 250
        right_roof_intercept = 300 - right_roof_slope * 250
        
        y_left_roof = left_roof_slope * self.x + left_roof_intercept
        y_right_roof = right_roof_slope * self.x + right_roof_intercept

        return self.y <= y_left_roof if self.x < 250 else self.y <= y_right_roof

raindrops = []

def generate_raindrops():
    global raindrops
    for y in range(500, 0, -25):
        for x in range(-500, 500, 10):
            if not (50 <= x <= 450 and 30 <= y <= 200):
                raindrops.append(Raindrop(x, y))

last_drop_time = time.time()
time_interval = 1.0

def iterate():
    glViewport(0, 0, 500, 500)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0.0, 500, 0.0, 500, 0.0, 1.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

def show_screen():
    global bg_color
    if bg_color == "white":
        glClearColor(1.0, 1.0, 1.0, 1.0)
    else:
        glClearColor(0.0, 0.0, 0.0, 1.0)
    
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    iterate()
    draw_house()
    draw_circle(165, 65, 3)
    update_raindrops()
    draw_raindrops()
    glutSwapBuffers()

def draw_house():
    glLineWidth(30)
    glBegin(GL_LINES)
    glColor3f(1.0, 0.65, 0.0)
    glVertex2f(50, 200)
    glVertex2f(250, 300)
    glVertex2f(250, 300)
    glVertex2f(450, 200)
    glVertex2f(52, 200)
    glVertex2f(448, 200)
    glVertex2f(80, 200)
    glVertex2f(80, 30)
    glVertex2f(418, 200)
    glVertex2f(418, 30)
    glVertex2f(72, 30)
    glVertex2f(426, 30)
    glEnd()
    glLineWidth(2)
    glBegin(GL_LINES)
    glVertex2f(127, 30)
    glVertex2f(127, 120)
    glVertex2f(177, 30)
    glVertex2f(177, 120)
    glVertex2f(127, 120)
    glVertex2f(176, 120)
    glEnd()
    glLineWidth(2)
    glBegin(GL_LINES)
    glVertex2f(280, 150)
    glVertex2f(330, 150)
    glVertex2f(280, 150)
    glVertex2f(280, 100)
    glVertex2f(280, 100)
    glVertex2f(330, 100)
    glVertex2f(330, 150)
    glVertex2f(330, 100)
    glEnd()
    glLineWidth(1)
    glBegin(GL_LINES)
    glVertex2f(280, 125)
    glVertex2f(330, 125)
    glVertex2f(305, 150)
    glVertex2f(305, 100)
    glEnd()

def draw_circle(x, y, radius):
    num_segments = 2000
    theta = 2 * math.pi / num_segments

    glColor3f(1.0, 0.65, 0.0)
    glBegin(GL_TRIANGLES)
    for i in range(num_segments):
        angle1 = i * theta
        angle2 = (i + 1) * theta
        cx1 = radius * math.cos(angle1)
        cy1 = radius * math.sin(angle1)
        cx2 = radius * math.cos(angle2)
        cy2 = radius * math.sin(angle2)
        glVertex2f(x, y)
        glVertex2f(x + cx1, y + cy1)
        glVertex2f(x + cx2, y + cy2)
    glEnd()

def update_raindrops():
    global raindrops, last_drop_time, time_interval
    current_time = time.time()
    if current_time - last_drop_time > time_interval:
        last_drop_time = current_time

    for raindrop in raindrops:
        raindrop.update()

def draw_raindrops():
    global angle
    glLineWidth(1)
    glColor3f(1.0, 0.65, 0.0)
    glBegin(GL_LINES)
    for raindrop in raindrops:
        glVertex2f(raindrop.x, raindrop.y)
        
        end_x = raindrop.x + 10 * math.sin(math.radians(angle))
        end_y = raindrop.y - 10 * math.cos(math.radians(angle))
        glVertex2f(end_x, end_y)
    glEnd()

def key_listener(key, x, y):
    global bg_color
    if key == b'w':
        bg_color = "white"
    elif key == b'b':
        bg_color = "black"
    glutPostRedisplay()

def special_key_listener(key, x, y):
    global angle
    if key == GLUT_KEY_LEFT:
        angle -= 1
    elif key == GLUT_KEY_RIGHT:
        angle += 1
    glutPostRedisplay()

glutInit()
glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)
glutInitWindowSize(W_width, W_height)
glutInitWindowPosition(0, 0)
wind = glutCreateWindow(b"Rain, Rain, don't go away!")
glutDisplayFunc(show_screen)
glutIdleFunc(show_screen)
glutKeyboardFunc(key_listener)
glutSpecialFunc(special_key_listener)
generate_raindrops()
glutMainLoop()
