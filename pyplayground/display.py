import pygame, pygame.display
class Display:
    def __init__(self, size: pygame.Vector2, title: str):
        self.display = pygame.display.set_mode(size)
        pygame.display.set_caption(title)
    def create_surface(self, size: pygame.Vector2 = None):
        surface = pygame.Surface(self.display.get_size())
        return surface.convert(self.display)
    def update(self):
        pygame.display.update()