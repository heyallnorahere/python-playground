import os, sys
import pygame, pygame.font, pygame.mixer, pygame.display, pygame.event
from pygame.locals import *
from pyplayground import *
import pyplayground
class TestComponent:
    def update(self, object: pyplayground.GameObject):
        print("({}, {})".format(object.pos.x, object.pos.y))
    def render(self, object: pyplayground.GameObject, display: pyplayground.Display):
        pass
if not pygame.font: print("fonts have been disabled; whoops")
if not pygame.mixer: print("sound has been disabled; whoops")
pygame.init()
display = pyplayground.Display((800, 600), "pygame testapp")
scene = Scene()
object = GameObject()
object.add_component(TestComponent())
scene.add(object)
while True:
    for event in pygame.event.get():
        if event.type in (QUIT, KEYDOWN):
            sys.exit()
    scene.update()
    scene.render(display)