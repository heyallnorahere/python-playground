from pyplayground.gameobject import GameObject
from pyplayground.display import Display
class Scene():
    def __init__(self):
        self.children = list[GameObject]()
    def add(self, object: GameObject):
        self.children.append(object)
    def update(self):
        for child in self.children:
            child.update()
    def render(self, display: Display):
        for child in self.children:
            child.render(display)
        pass
