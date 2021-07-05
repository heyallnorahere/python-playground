import builtins
import os, sys
import pygame, pygame.font, pygame.mixer, pygame.display, pygame.event
from pygame.locals import *
import pyplayground
if not pygame.font: print("fonts have been disabled; whoops")
if not pygame.mixer: print("sound has been disabled; whoops")
pygame.init()
print("This is currently running in: {}".format(os.getcwd()))
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("pygame testapp")
background = pygame.Surface(screen.get_size())
scene = pyplayground.Scene()
scene.add_child(pyplayground.GameObject())
while True:
    for event in pygame.event.get():
        if event.type in (QUIT, KEYDOWN):
            sys.exit()
    scene.update()