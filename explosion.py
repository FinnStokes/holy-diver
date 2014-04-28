import math

import pygame
from pygame.locals import *

import resources

class Explosion(pygame.sprite.Sprite):
    """An explosion resulting from a torpedo hitting a submarine"""

    def __init__(self, position):
        pygame.sprite.Sprite.__init__(self)
        self.base, self.rect = resources.load_png('EXPLOSION.png')
        self.rect.width /= 5
        self.time = 0.0
        self.frame = self.rect.copy()
        self.rect.center = position
        self.framerate = 60

    def update(self, dt):
        self.time += dt
        frame = int(self.time * self.framerate)
        if frame > 4:
            frame = 4
        self.frame.left = frame * self.frame.width
        self.image = self.base.subsurface(self.frame)
