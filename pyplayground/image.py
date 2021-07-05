import pygame.image
from pyplayground.display import Display
class Image:
    def __init__(self, file_path: str, display: Display):
        temp_surface = pygame.image.load(file_path)
        if display == None:
            self.surface = temp_surface.convert()
        else:
            self.surface = temp_surface.convert(display.display)