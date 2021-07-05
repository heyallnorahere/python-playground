import os, sys
import pygame, pygame.font, pygame.mixer, pygame.event
from pygame.locals import *
from pyplayground import *
from pyplayground.components import SpriteComponent, TilesetComponent
if not pygame.font: print("fonts have been disabled; whoops")
if not pygame.mixer: print("sound has been disabled; whoops")
pygame.init()
display = Display((800, 600), "pygame testapp")
scene = Scene()
object = GameObject()
image = Image("assets/images/chrome.png", display)
object.add_component(SpriteComponent(image))
scene.add(object)
cell_size = (100, 100)
tile = GameObject(cell_size)
tile.pos = (100, 100)
tile.add_component(TilesetComponent(image, cell_size, (3, 2)))
scene.add(tile)
while True:
    for event in pygame.event.get():
        if event.type in (QUIT, KEYDOWN):
            sys.exit()
    scene.update()
    scene.render(display)
    display.update()