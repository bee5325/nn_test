from math import *
from pyglet.gl import *
import random
import time

pyglet.options['debug_gl'] = False

CIRCLES = 10000
NUM_POINTS = 100
t0 = 0
t1 = 0
t2 = 0

window = pyglet.window.Window(800, 600)
batch = pyglet.graphics.Batch()

def getPoints(center_x, center_y, radius, color):
    # first get all verteces of the circle
    global t0, t1, t2
    t00 = time.time()
    circle_verts = list()
    for i in range(NUM_POINTS):
        angle = radians(float(i)/NUM_POINTS * 360.0)
        x = radius*cos(angle) + center_x
        y = radius*sin(angle) + center_y
        circle_verts.append((x,y))
    # wrap around
    circle_verts.append(circle_verts[0])
    t0 += time.time() - t00
    t11 = time.time()
    # then get verteces of triangles needed
    verts = list()
    colors = list()
    for v1, v2 in zip(circle_verts[0:-1], circle_verts[1:]):
        verts += v1
        verts += v2
        verts += center_x, center_y
        colors += 3 * color
    t1 += time.time() - t11
    return (verts, colors)

def makeCircle(center_x, center_y, radius, color, batch):
    # first get all verteces of the circle
    global t0, t1, t2
    t00 = time.time()
    circle_verts = list()
    for i in range(NUM_POINTS):
        angle = radians(float(i)/NUM_POINTS * 360.0)
        x = radius*cos(angle) + center_x
        y = radius*sin(angle) + center_y
        circle_verts.append((x,y))
    # wrap around
    circle_verts.append(circle_verts[0])
    t0 += time.time() - t00
    t11 = time.time()
    # then get verteces of triangles needed
    verts = list()
    colors = list()
    for v1, v2 in zip(circle_verts[0:-1], circle_verts[1:]):
        verts += v1
        verts += v2
        verts += center_x, center_y
        colors += 3 * color
    t1 += time.time() - t11
    t22 = time.time()
    circle = batch.add(NUM_POINTS * 3, pyglet.gl.GL_TRIANGLES, None,
              ('v2f', verts),
              ('c3B', colors))
    t2 += time.time() - t22
    return circle

def makeCircles(number, center_x, center_y, radius, color, batch):
    color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
    verts = []
    colors = []
    for i in range(number):
        v, c = getPoints(random.randint(0,800), random.randint(0,600), 20, color)
        verts.extend(v)
        colors.extend(c)
    global t2
    t22 = time.time()
    circles = batch.add(len(verts)//2, pyglet.gl.GL_TRIANGLES, None,
                        ('v2f', verts),
                        ('c3B', colors))
    t2 = time.time() - t22
    return circles
    #circles.append(makeCircle(random.randint(0,800), random.randint(0,600), 20, color, batch))

color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
circles = makeCircles(CIRCLES, random.randint(0,800), random.randint(0,600), 20, color, batch)
#circles = []
#color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
#for i in range(10000):
#    circles.append(makeCircle(random.randint(0,800), random.randint(0,600), 20, color, batch))
print(t0)
print(t1)
print(t2)

@window.event
def on_draw():
    glClear(pyglet.gl.GL_COLOR_BUFFER_BIT)
    batch.draw()
    fps_display.draw()

fps_display = pyglet.clock.ClockDisplay()

def update(dt):
    global circles
    circles.delete()
    circles = makeCircles(CIRCLES, random.randint(0,800), random.randint(0,600), 20, color, batch)

pyglet.clock.schedule_interval(update, 0.01)

pyglet.app.run()
