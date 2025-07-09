from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random

width, height = 800, 600
boat_x, boat_y = width // 2, 50
boat_speed = 20
diamond_x, diamond_y = random.randint(50, width - 50), height - 50
diamond_speed = 1
initial_diamond_speed = 1
speed_increment = 0.5
score = 0
is_playing = True
is_game_over = False

def write_pixel(x, y):
    glBegin(GL_POINTS)
    glVertex2i(int(x), int(y))
    glEnd()

def get_zone(dx, dy):
    if abs(dx) > abs(dy):
        if dx > 0:
            if dy > 0:
                return 0
            else:
                return 7
        else:
            if dy > 0:
                return 3
            else:
                return 4
    else:
        if dx > 0:
            if dy > 0:
                return 1
            else:
                return 6
        else:
            if dy > 0:
                return 2
            else:
                return 5

def convert_to_zone0(x, y, zone):
    if zone == 0:
        return x, y
    elif zone == 1:
        return y, x
    elif zone == 2:
        return y, -x
    elif zone == 3:
        return -x, y
    elif zone == 4:
        return -x, -y
    elif zone == 5:
        return -y, -x
    elif zone == 6:
        return -y, x
    elif zone == 7:
        return x, -y

def convert_from_zone0(x, y, zone):
    if zone == 0:
        return x, y
    elif zone == 1:
        return y, x
    elif zone == 2:
        return -y, x
    elif zone == 3:
        return -x, y
    elif zone == 4:
        return -x, -y
    elif zone == 5:
        return -y, -x
    elif zone == 6:
        return y, -x
    elif zone == 7:
        return x, -y

def draw_line(x1, y1, x2, y2):
    dx = x2 - x1
    dy = y2 - y1
    zone = get_zone(dx, dy)

    x1, y1 = convert_to_zone0(x1, y1, zone)
    x2, y2 = convert_to_zone0(x2, y2, zone)
    
    dx = abs(x2 - x1)
    dy = abs(y2 - y1)
    sx = 1 if x1 < x2 else -1
    sy = 1 if y1 < y2 else -1
    err = dx - dy

    while True:
        draw_x, draw_y = convert_from_zone0(x1, y1, zone)
        write_pixel(draw_x, draw_y)
        
        if x1 == x2 and y1 == y2:
            break
        e2 = 2 * err
        if e2 > -dy:
            err -= dy
            x1 += sx
        if e2 < dx:
            err += dx
            y1 += sy

def draw_boat(x, y):
    draw_line(x - 40, y, x + 40, y)
    draw_line(x - 40, y, x - 20, y - 20)
    draw_line(x + 40, y, x + 20, y - 20)
    draw_line(x - 20, y - 20, x + 20, y - 20)

def draw_diamond(x, y):
    draw_line(x, y + 20, x + 10, y)
    draw_line(x, y + 20, x - 10, y)
    draw_line(x - 10, y, x, y - 20)
    draw_line(x + 10, y, x, y - 20)

def draw_play_button(x, y):
    draw_line(x, y, x, y + 20)
    draw_line(x, y + 20, x + 15, y + 10)
    draw_line(x, y, x + 15, y + 10)

def draw_pause_button(x, y):
    draw_line(x, y, x, y + 20)
    draw_line(x + 10, y, x + 10, y + 20)

def draw_refresh_button(x, y):
    draw_line(x + 10, y + 5, x + 15, y + 10)
    draw_line(x + 15, y + 10, x + 10, y + 15)
    draw_line(x + 10, y + 15, x + 5, y + 10)
    draw_line(x + 5, y + 10, x + 10, y + 5)
    draw_line(x + 10, y + 5, x + 5, y + 10)
    draw_line(x + 10, y + 15, x + 15, y + 10)

def draw_cross_button(x, y):
    draw_line(x, y, x + 20, y + 20)
    draw_line(x, y + 20, x + 20, y)

def draw_text(string, x, y):
    glRasterPos2f(x, y)
    for char in string:
        glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(char))

def display():
    global diamond_y, diamond_x, score, is_playing, is_game_over, diamond_speed
    glClear(GL_COLOR_BUFFER_BIT)
    glColor3f(1.0, 1.0, 1.0)

    glColor3f(0.0, 0.0, 0.0)
    glRectf(50, height - 70, 70, height - 50)
    glRectf(width // 2 - 10, height - 70, width // 2 + 10, height - 50)
    glRectf(width - 70, height - 70, 70, height - 50)

    glColor3f(0.5, 1.0, 0.5)
    draw_refresh_button(50, height - 70)
    
    glColor3f(1.0, 0.65, 0.0)
    if is_playing and not is_game_over:
        draw_pause_button(width // 2 - 5, height - 70)
    else:
        draw_play_button(width // 2 - 10, height - 70)

    glColor3f(1.0, 0.0, 0.0)
    draw_cross_button(width - 70, height - 70)

    glColor3f(1.0, 0.65, 0.0)
    draw_boat(boat_x, boat_y)
    
    if is_playing and not is_game_over:
        diamond_y -= diamond_speed
        if diamond_y <= boat_y + 20 and abs(boat_x - diamond_x) <= 50:
            diamond_y = height - 50
            diamond_x = random.randint(50, width - 50)
            diamond_speed += speed_increment
            score += 1
        elif diamond_y <= 0:
            is_playing = False
            is_game_over = True

    glColor3f(1.0, 1.0, 1.0)
    draw_diamond(diamond_x, diamond_y)
    
    if is_game_over:
        draw_text(f"Game Over! Final Score: {score}", width // 2 - 80, height // 2)
    else:
        draw_text(f"Score: {score}", 10, 10)
    
    glFlush()

def keyboard(key, x, y):
    global is_playing
    if key == b'\x1b':
        is_playing = False
        global is_game_over
        is_game_over = True
    elif key == b'p' and not is_game_over:
        is_playing = not is_playing

def special_keys(key, x, y):
    global boat_x, is_playing
    if is_playing:
        if key == GLUT_KEY_LEFT:
            boat_x -= boat_speed
        elif key == GLUT_KEY_RIGHT:
            boat_x += boat_speed
        boat_x = max(40, min(width - 40, boat_x))
    glutPostRedisplay()

def mouse(button, state, x, y):
    global is_playing, diamond_x, diamond_y, score, is_game_over, diamond_speed, boat_x
    y = height - y

    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        if 50 <= x <= 70 and height - 70 <= y <= height - 50:
            is_playing = True
            score = 0
            diamond_y = height - 50
            diamond_x = random.randint(50, width - 50)
            diamond_speed = initial_diamond_speed
            boat_x = width // 2
            is_game_over = False
        elif width // 2 - 10 <= x <= width // 2 + 10 and height - 70 <= y <= height - 50:
            is_playing = not is_playing
        elif width - 70 <= x <= width - 50 and height - 70 <= y <= height - 50:
            is_playing = False
            is_game_over = True
    glutPostRedisplay()


glutInit()
glutInitDisplayMode(GLUT_SINGLE | GLUT_RGB)
glutInitWindowSize(width, height)
glutCreateWindow(b"Boat and Falling Diamond")
glClearColor(0.0, 0.0, 0.0, 1.0)
gluOrtho2D(0, width, 0, height)
glutDisplayFunc(display)
glutIdleFunc(display)
glutKeyboardFunc(keyboard)
glutSpecialFunc(special_keys)
glutMouseFunc(mouse)
glutMainLoop()