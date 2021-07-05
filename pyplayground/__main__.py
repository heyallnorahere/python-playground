import os, sys
import pygame, pygame.font, pygame.mixer, pygame.display, pygame.event
from pygame.locals import *
from pyplayground import *
if not pygame.font: print("fonts have been disabled; whoops")
if not pygame.mixer: print("sound has been disabled; whoops")
pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("pygame testapp")
background = pygame.Surface(screen.get_size())
scene = Scene()
scene.add_child(GameObject())
while True:
    for event in pygame.event.get():
        if event.type in (QUIT, KEYDOWN):
            sys.exit()
    scene.update()