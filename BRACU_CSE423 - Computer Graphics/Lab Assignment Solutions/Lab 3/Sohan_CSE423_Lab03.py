from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random
import math
import os

shooter_x = 0
shooter_radius = 20
projectiles = []
falling_circles = []
score = 0
game_over = False
paused = False
missed_circles = 0
max_lives = 3
lives = max_lives
misfires = 0
max_misfires = 3
is_paused = False
circle_radius = 15

last_score = score
last_lives = lives
last_misfires = misfires

buttons = {
    "restart": (-450, 240, -150, 310),
    "pause": (-150, 240, 150, 310),
    "exit": (150, 240, 450, 310)
}

def draw_circle(xc, yc, r):
    x = 0
    y = r
    d = 1 - r
    draw_symmetric_points(xc, yc, x, y)
    while x < y:
        if d < 0:
            d = d + 2 * x + 3
        else:
            d = d + 2 * (x - y) + 5
            y -= 1
        x += 1
        draw_symmetric_points(xc, yc, x, y)

def draw_symmetric_points(xc, yc, x, y):
    glBegin(GL_POINTS)
    glVertex2f(xc + x, yc + y)
    glVertex2f(xc - x, yc + y)
    glVertex2f(xc + x, yc - y)
    glVertex2f(xc - x, yc - y)
    glVertex2f(xc + y, yc + x)
    glVertex2f(xc - y, yc + x)
    glVertex2f(xc + y, yc - x)
    glVertex2f(xc - y, yc - x)
    glEnd()

def draw_line(x0, y0, x1, y1):
    dx = abs(x1 - x0)
    dy = abs(y1 - y0)
    sx = 1 if x0 < x1 else -1
    sy = 1 if y0 < y1 else -1
    err = dx - dy
    while True:
        glBegin(GL_POINTS)
        glVertex2f(x0, y0)
        glEnd()
        if x0 == x1 and y0 == y1:
            break
        e2 = 2 * err
        if e2 > -dy:
            err -= dy
            x0 += sx
        if e2 < dx:
            err += dx
            y0 += sy

def draw_arrow():
    draw_line(-375, 275, -345, 290)
    draw_line(-375, 275, -345, 260)
    draw_line(-345, 275, -320, 275)

def draw_pause():
    draw_line(-30, 260, -30, 290)
    draw_line(-10, 260, -10, 290)

def draw_play():
    draw_line(-20, 260, 0, 275)
    draw_line(0, 275, -20, 290)
    draw_line(-20, 290, -20, 260)

def draw_x():
    draw_line(250, 260, 290, 290)
    draw_line(250, 290, 290, 260)

def draw_shooter():
    global shooter_x, shooter_radius
    glColor3f(0.0, 1.0, 0.0)
    draw_circle(shooter_x, -250, shooter_radius)

def draw_projectiles():
    global projectiles
    glColor3f(1.0, 1.0, 0.0)
    for projectile in projectiles:
        draw_circle(projectile[0], projectile[1], 5)

def draw_falling_circles():
    global falling_circles
    glColor3f(1.0, 0.0, 0.0)
    for circle in falling_circles:
        draw_circle(circle[0], circle[1], circle_radius)

def render_text(x, y, text):
    glRasterPos2f(x, y)
    for ch in text:
        glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(ch))

def display_score_life():
    global score, lives, misfires, last_score, last_lives, last_misfires
    glColor3f(1.0, 1.0, 1.0)
    render_text(-300, 230, f"Score: {score}  Lives: {lives}  Misfires: {misfires}")
    if score != last_score or lives != last_lives or misfires != last_misfires:
        print(f"Score: {score}, Lives: {lives}, Misfires: {misfires}")
        last_score = score
        last_lives = lives
        last_misfires = misfires

def draw_buttons():
    glColor3f(0.0, 0.0, 0.0)
    glBegin(GL_QUADS)
    glVertex2f(-450, 240)
    glVertex2f(-150, 240)
    glVertex2f(-150, 310)
    glVertex2f(-450, 310)
    glEnd()
    glBegin(GL_QUADS)
    glVertex2f(-150, 240)
    glVertex2f(150, 240)
    glVertex2f(150, 310)
    glVertex2f(-150, 310)
    glEnd()
    glBegin(GL_QUADS)
    glVertex2f(150, 240)
    glVertex2f(450, 240)
    glVertex2f(450, 310)
    glVertex2f(150, 310)
    glEnd()
    glColor3f(0.0, 1.0, 1.0)
    draw_arrow()
    glColor3f(1.0, 0.6, 0.0)
    if not is_paused:
        draw_pause()
    else:
        draw_play()
    glColor3f(1.0, 0.0, 0.0)
    draw_x()

def mouse_click(button, state, x, y):
    global game_over, paused, score, lives, misfires, falling_circles, projectiles, is_paused
    if state == GLUT_DOWN:
        world_x = (x / 800.0) * 800 - 400
        world_y = ((600 - y) / 600.0) * 600 - 300
        if buttons["restart"][0] <= world_x <= buttons["restart"][2] and buttons["restart"][1] <= world_y <= buttons["restart"][3]:
            score = 0
            lives = max_lives
            misfires = 0
            game_over = False
            falling_circles.clear()
            projectiles.clear()
            is_paused = False
            print("Starting Over")
        elif buttons["pause"][0] <= world_x <= buttons["pause"][2] and buttons["pause"][1] <= world_y <= buttons["pause"][3]:
            is_paused = not is_paused
        elif buttons["exit"][0] <= world_x <= buttons["exit"][2] and buttons["exit"][1] <= world_y <= buttons["exit"][3]:
            print(f"Goodbye! Final Score: {score}")
            os._exit(0)

def keypress(key, x, y):
    global shooter_x, projectiles, game_over, misfires
    if game_over or is_paused:
        return
    if key == b'a' and shooter_x > -380:
        shooter_x -= 10
    elif key == b'd' and shooter_x < 380:
        shooter_x += 10
    elif key == b' ' and not game_over:
        projectiles.append([shooter_x, -230])

def is_overlapping(new_circle, existing_circles):
    for circle in existing_circles:
        if math.hypot(new_circle[0] - circle[0], new_circle[1] - circle[1]) < 2 * circle_radius:
            return True
    return False

def update(value):
    global projectiles, falling_circles, score, game_over, missed_circles, lives, misfires, is_paused
    if game_over or is_paused:
        glutTimerFunc(50, update, 0)
        return
    for circle in falling_circles:
        circle[1] -= 3
        if circle[1] < -300:
            falling_circles.remove(circle)
            missed_circles += 1
            lives -= 1
            if lives == 0:
                game_over = True
        if math.hypot(circle[0] - shooter_x, circle[1] + 250) < shooter_radius + circle_radius:
            game_over = True
    for projectile in projectiles:
        projectile[1] += 10
        if projectile[1] > 300:
            projectiles.remove(projectile)
            misfires += 1
            if misfires >= max_misfires:
                game_over = True
    for circle in falling_circles:
        for projectile in projectiles:
            if math.hypot(circle[0] - projectile[0], circle[1] - projectile[1]) < 20:
                falling_circles.remove(circle)
                projectiles.remove(projectile)
                score += 1
                misfires = 0
                break
    if random.random() < 0.01:
        new_circle = [random.randint(-380, 380), 300]
        if not is_overlapping(new_circle, falling_circles):
            falling_circles.append(new_circle)
    glutTimerFunc(50, update, 0)
    glutPostRedisplay()

def display():
    global score, game_over, lives, misfires
    glClear(GL_COLOR_BUFFER_BIT)
    draw_shooter()
    draw_projectiles()
    draw_falling_circles()
    draw_buttons()
    display_score_life()
    if game_over:
        glColor3f(1.0, 0.0, 0.0)
        render_text(-50, 100, f"Game Over! Final Score: {score}")
        print(f"Game Over! Final Score: {score}")
        if lives == 0:
            render_text(-150, 50, "You lost as three circles crossed the bottom boundary.")
            print("You lost as three circles crossed the bottom boundary.")
        elif misfires >= max_misfires:
            render_text(-100, 50, "You lost due to three misfires.")
            print("You lost due to three misfires.")
        else:
            render_text(-150, 50, "A circle hit your shooter!")
            print("A circle hit your shooter!")
        falling_circles.clear()
        projectiles.clear()
    glutSwapBuffers()

def init():
    glClearColor(0.0, 0.0, 0.0, 1.0)
    glColor3f(1.0, 1.0, 1.0)
    glPointSize(2.0)
    gluOrtho2D(-400, 400, -300, 300)

def main():
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)
    glutInitWindowSize(800, 600)
    glutInitWindowPosition(100, 100)
    glutCreateWindow(b"Shoot The Circles!")
    init()
    glutDisplayFunc(display)
    glutKeyboardFunc(keypress)
    glutMouseFunc(mouse_click)
    glutTimerFunc(50, update, 0)
    glutMainLoop()

main()
