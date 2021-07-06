import pygame, pygame.time, pygame.transform
from pyplayground.display import Display
from pyplayground.image import Image
from pyplayground.gameobject import GameObject
from math import floor
import os.path
import yaml
class Animation:
    def __init__(self, sprites: pygame.Surface, sprite_width: int, fps: float):
        self.frames = list[pygame.Surface]()
        self.playing = False
        self.looping = False
        self.time_offset = 0
        self.current_frame = 0
        self.fps = fps
        frame_count = floor(sprites.get_width() / sprite_width)
        height = sprites.get_height()
        surface_size = (sprite_width, height)
        for frame in range(frame_count):
            frame_data = pygame.Surface(surface_size)
            blit_area = pygame.Rect(
                frame * sprite_width, 0,
                sprite_width, height
            )
            frame_data.blit(sprites, (0, 0), blit_area)
            self.frames.append(frame_data)
    def update(self):
        if self.playing:
            current_animation_time = (pygame.time.get_ticks() / 1000) - self.time_offset
            current_frame = floor(self.fps * current_animation_time)
            if current_frame > len(self.frames) and not self.looping:
                self.stop()
                return
            self.current_frame = current_frame % len(self.frames)
    def play(self, loop: bool = False):
        self.playing = True
        self.looping = loop
        self.current_frame = 0
        self.time_offset = pygame.time.get_ticks() / 1000
    def stop(self):
        self.playing = False
        self.current_frame = 0
class AnimatedSpriteComponent:
    def __init__(self, animations: list[Animation], idle_animation: int = 0):
        self.animations = animations
        self.idle_index = idle_animation
        self.current_animation = self.idle_index
        self.animations[self.idle_index].play(True)
    def create_from_yaml(name: str, display: Display):
        stub = os.path.join("assets", "spritesheets", name)
        data = None
        with open(stub + ".yml", "r") as stream:
            try:
                data = yaml.load(stream, Loader=yaml.Loader)
                stream.close()
            except yaml.YAMLError as exc:
                print(exc)
        if data == None:
            print("Failed to load animation data; aborting...")
            exit(1)
        spritesheet = Image(stub + ".png", display)
        animations = list[Animation]()
        yaml_animations = data["animations"]
        for index in range(len(yaml_animations)):
            desc = yaml_animations[index]
            sprite_size = desc["sprite-size"]
            fps = desc["fps"]
            pixel_offset = desc["y-pixel-offset"]
            surface_size = (spritesheet.surface.get_width(), sprite_size[1])
            blit_clip = pygame.Rect(
                (0, pixel_offset),
                surface_size
            )
            surface = pygame.Surface(surface_size)
            surface.blit(spritesheet.surface, (0, 0), blit_clip)
            animations.append(Animation(surface, sprite_size[0], fps))
        idle_animation = data["idle"]
        return AnimatedSpriteComponent(animations, idle_animation)
    def play(self, index: int, loop: bool = False):
        if index == self.idle_index:
            self.idle()
            return
        self.animations[self.current_animation].stop()
        self.current_animation = index
        self.animations[self.current_animation].play(loop)
    def idle(self):
        if self.current_animation == self.idle_index:
            return
        self.animations[self.current_animation].stop()
        self.current_animation = self.idle_index
    def update(self, object: GameObject):
        for animation in self.animations:
            animation.update()
    def render(self, object: GameObject, display: Display):
        animation = self.animations[self.current_animation]
        frame = animation.frames[animation.current_frame]
        display.display.blit(pygame.transform.scale(frame, object.size), object.pos)