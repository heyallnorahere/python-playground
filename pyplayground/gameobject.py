from pyplayground.display import Display
class GameObject:
    def __init__(self, size: tuple[int, int] = (100, 100)):
        self.pos = (0, 0)
        self.size = size
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
    def get_component(self, component_class: type):
        for component in self.components:
            if component.__class__ == component_class:
                return component
        return None
    def render(self, display: Display):
        for component in self.components:
            component.render(self, display)