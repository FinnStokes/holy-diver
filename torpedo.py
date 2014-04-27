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
        screen = pygame.display.get_surface()
        self.area = screen.get_rect()
        self.layers = layers
        self.dragy = 3.6
        self.dragx = 0.06
        self.reinit(velocity,density,player)

    def reinit(self, velocity, density, player):
        self.velocity = velocity
        self.density = density
        self.side = player.side
        if self.side == "left":
            self.rect.midbottom = player.rect.bottomright
        elif self.side == "right":
            self.rect.midbottom = player.rect.bottomleft
        self.position = self.rect.center

    def update(self, dt):
        self.velocity[1] += physics.GRAVITY * dt * (self.density - self.layers.density(self.rect.top, self.rect.bottom)) / self.density
        self.velocity[0] *= 1 - self.dragx * dt
        self.velocity[1] *= 1 - self.dragy * dt
        if abs(self.velocity[0]) < 10*dt + 0.02: # Magic numbers determined by experimentation. Stops oscillations.
            self.velocity[0] = 0
        if abs(self.velocity[1]) < 10*dt + 0.02:
            self.velocity[1] = 0
        self.position = (self.position[0] + self.velocity[0] * dt, self.position[1] + self.velocity[1] * dt)
        self.rect.center = self.position

