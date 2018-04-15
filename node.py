import pyglet, random, math


class Node():

    def __init__(self):
        self.b = 0
        self.parents = []
        self.children = []

    def add_parent(self, parent):
        self.parents.append(parent)

    def add_children(self, child):
        self.children.append(child)
