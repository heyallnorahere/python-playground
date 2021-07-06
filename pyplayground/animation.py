import pygame, pygame.time
from pyplayground.display import Display
from pyplayground.image import Image
from pyplayground.gameobject import GameObject
from math import floor
class Animation:
    def __init__(self, sprites: Image, sprite_width: int, fps: float):
        self.frames = list[pygame.Surface]()
        self.playing = False
        self.looping = False
        self.time_offset = 0
        self.current_frame = 0
        self.fps = fps
        frame_count = floor(sprites.surface.get_width() / sprite_width)
        height = sprites.surface.get_height()
        surface_size = (sprite_width, height)
        for frame in range(frame_count):
            frame_data = pygame.Surface(surface_size)
            blit_area = pygame.Rect(
                frame * sprite_width, 0,
                sprite_width, height
            )
            frame_data.blit(sprites.surface, (0, 0), blit_area)
            self.frames.append(frame_data)
    def update(self):
        if self.playing:
            current_animation_time = (pygame.time.get_ticks() / 100) - self.time_offset
            self.current_frame = floor(self.fps * current_animation_time)
            if self.current_frame > len(self.frames):
                self.current_frame = 0
                if not self.looping:
                    self.playing = False
    def play(self, loop: bool = False):
        self.playing = True
        self.looping = loop
        self.current_frame = 0
    def stop(self):
        self.playing = False
        self.current_frame = 0
class AnimatedSpriteComponent:
    def __init__(self, animations: list[Animation], idle_animation: int = 0):
        self.animations = animations
        self.idle = idle_animation