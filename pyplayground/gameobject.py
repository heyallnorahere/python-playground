from pygame import *
from pyplayground.display import Display
class GameObject:
    def __init__(self):
        self.pos = Vector2(0, 0)
        self.children = []
        self.components = []
    def add_component(self, component):
        self.components.append(component)
    def add_child(self, child):
        self.children.append(child)
    def update(self):
        for component in self.components:
            component.update(self)
        for child in self.children:
            child.update()
    def render(self, display: Display):
        for component in self.components:
            component.render(self, display)