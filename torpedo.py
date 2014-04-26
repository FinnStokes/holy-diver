import math

import pygame
from pygame.locals import *

import physics
import resources

class Torpedo(pygame.sprite.Sprite):
    """A torpedo with some fixed density experiencing buoyancy"""

    def __init__(self, velocity, density, player, layers):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = resources.load_png('torpedo.png')
        self.rect.midbottom = player.rect.bottomright
        self.position = self.rect.center
        screen = pygame.display.get_surface()
        self.area = screen.get_rect()
        self.velocity = velocity
        self.density = density
        self.layers = layers
        self.dragy = 3.6
        self.dragx = 0.06

    def update(self):
        self.velocity[1] += physics.GRAVITY / 60.0 * (self.density - self.layers.density(self.rect.top, self.rect.bottom)) / self.density
        self.velocity[0] *= 1 - self.dragx / 60.0
        self.velocity[1] *= 1 - self.dragy / 60.0
        self.position = (self.position[0] + self.velocity[0] / 60.0, self.position[1] + self.velocity[1] / 60.0)
        self.rect.center = self.position

