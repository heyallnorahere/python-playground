import os, sys
import pygame, pygame.font, pygame.mixer, pygame.event
from pygame.locals import *
from pyplayground import *
from pyplayground.components import SpriteComponent
if not pygame.font: print("fonts have been disabled; whoops")
if not pygame.mixer: print("sound has been disabled; whoops")
pygame.init()
display = Display((800, 600), "pygame testapp")
scene = Scene()
object = GameObject()
object.add_component(SpriteComponent(Image("assets/images/chrome.png", display), (100, 100)))
scene.add(object)
while True:
    for event in pygame.event.get():
        if event.type in (QUIT, KEYDOWN):
            sys.exit()
    scene.update()
    scene.render(display)
    display.update()