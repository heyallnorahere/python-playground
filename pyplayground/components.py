from pyplayground import *
import pygame, pygame.transform
class SpriteComponent:
    def __init__(self, image: Image):
        self.image = image
    def update(self, object: GameObject):
        pass
    def render(self, object: GameObject, display: Display):
        display.display.blit(pygame.transform.scale(self.image.surface, object.size), object.pos)
class TilesetComponent:
    def __init__(self, tileset: Image, cell_size: pygame.Vector2 = (50, 50), tile: tuple[int, int] = [0, 0]):
        self.tileset = tileset
        self.cell_size = cell_size
        self.tile = tile
    def update(self, object: GameObject):
        pass
    def render(self, object: GameObject, display: Display):
        source_clip = pygame.Rect(
            self.cell_size[0] * self.tile[0], self.cell_size[1] * self.tile[1],
            self.cell_size[0], self.cell_size[1]
        )
        temp_surface = pygame.Surface(self.cell_size)
        temp_surface.blit(self.tileset.surface, (0, 0), source_clip)
        display.display.blit(pygame.transform.scale(temp_surface, object.size), object.pos)