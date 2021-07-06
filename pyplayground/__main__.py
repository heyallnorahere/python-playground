import os, sys
from pyplayground.tile_manager import TileDescriptor
import pygame, pygame.font, pygame.mixer, pygame.event
import pygame.locals as pygame_constants
from pyplayground import *
from pyplayground.components import SpriteComponent, TilesetComponent
if not pygame.font: print("fonts have been disabled; whoops")
if not pygame.mixer: print("sound has been disabled; whoops")
pygame.init()
window_size = (800, 600)
display = Display(window_size, "pyplayground window")
scene = Scene()
object = GameObject()
image = Image("assets/images/chrome.png", display)
object.add_component(SpriteComponent(image))
scene.add(object)
cell_size = (50, 50)
tileset = Image("assets/images/ground.png", display)
tile = GameObject((window_size[0], 50))
tile.pos = (0, window_size[1] - tile.size[1])
tile.add_component(TilesetComponent(tileset, cell_size, (1, 0)))
scene.add(tile)
manager = TileManager(display)
manager.load("assets/scenes/initial-scene.yml")
while True:
    for event in pygame.event.get():
        if event.type in (pygame_constants.QUIT, pygame_constants.KEYDOWN):
            sys.exit()
    scene.update()
    manager.update()
    scene.render(display)
    manager.render(display)
    display.update()