from math import *
from pyglet.gl import *
import random
import time

#count = 0
#t0 = 0
#t1 = 0
#t2 = 0
#t3 = 0

CIRCLES = 5000
NUM_POINTS = 40

window = pyglet.window.Window(800, 600)
batch = pyglet.graphics.Batch()

cos_value = [cos(radians(float(i)/NUM_POINTS * 360)) for i in range(NUM_POINTS)]
sin_value = [sin(radians(float(i)/NUM_POINTS * 360)) for i in range(NUM_POINTS)]

class Circle():

    def __init__(self, center_x, center_y, radius, color, batch):
        # first get all verteces of the circle
        self.center = (center_x, center_y)
        self.radius = radius
        vertices = self._pos_vertices()
        self.num_verts = len(vertices) // 2
        colors = self._color_vertices(color)
        self.vertex_list = batch.add(self.num_verts, pyglet.gl.GL_TRIANGLE_STRIP, None,
                                     ('v2f', vertices),
                                     ('c3B', colors))

    def _pos_vertices(self):
        #global t2, t3
        x = (self.radius*cos_value[i] + self.center[0] for i in range(NUM_POINTS))
        y = (self.radius*sin_value[i] + self.center[1] for i in range(NUM_POINTS))
        #t22 = time.time()
        circle_verts = list(zip(x,y))
        #t2 += time.time() - t22
        #t33 = time.time()
        verts = list()
        verts.extend(2 * (self.center[0], self.center[1]))
        for v1, v2 in zip(circle_verts[0:-1:2], circle_verts[1::2]):
            verts += v1
            verts += v2
            verts += (self.center[0], self.center[1])
        verts.extend(2 * circle_verts[0])
        #t3 += time.time() - t33
        return verts

    def _color_vertices(self, color):
        colors = self.num_verts * color
        return colors

    def set_position(self, x, y):
        #global t0, t1
        #t00 = time.time()
        self.center = (x, y)
        new_verts = self._pos_vertices()
        #t0 += time.time() - t00
        #t11 = time.time()
        self.vertex_list.vertices = new_verts
        #t1 += time.time() - t11

    def delete(self):
        self.vertex_list.delete()

def makeCircles(number, center_x, center_y, radius, batch):
    color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
    circles = []
    for i in range(number):
        circles.append(Circle(random.randint(0,800), random.randint(0,600), radius, color, batch))
    return circles

circles = makeCircles(CIRCLES, random.randint(0,800), random.randint(0,600), 20, batch)

@window.event
def on_draw():
    glClear(pyglet.gl.GL_COLOR_BUFFER_BIT)
    batch.draw()

    #GL_TRIANGLE_STRIP global count, t0, t1, t2, t3
    #count += 1
    #if count % 10 == 0:
    #    print('------------------------------------')
    #    print("CALC    ", t0)
    #    print("ADD VERT", t1)
    #    print("VERT 1  ", t2)
    #    print("VERT 2  ", t3)
    #    t0 = 0
    #    t1 = 0
    #    t2 = 0
    #    t3 = 0
    fps_display.draw()

fps_display = pyglet.clock.ClockDisplay()

def update(dt):
    for circle in circles:
        circle.set_position(random.randint(0,800), random.randint(0,600))

pyglet.clock.schedule_interval(update, 0.01)

pyglet.app.run()
