from pyplayground import *
from pygame import Vector2, Surface, Rect
import pygame.transform
class SpriteComponent:
    def __init__(self, image: Image, size: Vector2):
        self.image = image
        self.size = size
    def update(self, object: GameObject):
        pass
    def render(self, object: GameObject, display: Display):
        display.display.blit(pygame.transform.scale(self.image.surface, self.size), object.pos)