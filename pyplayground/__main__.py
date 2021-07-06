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