import pyplayground
from pygame import *
class GameObject:
    def __init__(self):
        self.pos = Vector2(0, 0)
        self.children = []
    def add_child(self, child):
        self.children.append(child)
    def update(self):
        # this base function does not operate on its own; it simply updates its children. to use it in a child class, call super().update() at the end.
        for child in self.children:
            child.update()
