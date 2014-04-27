import math

import pygame
from pygame.locals import *

import physics
import resources
import scorepanel

class Diver(pygame.sprite.Sprite):
    """A player controlled submersible"""

    def __init__(self, side, layers):
        pygame.sprite.Sprite.__init__(self)
        self.side = side
        self.base, self.frame = resources.load_png('diver_'+self.side+'_blank.png')
        self.frame.width /= len(layers) - 1
        self.rect = self.frame.copy()
        screen = pygame.display.get_surface()
        self.area = screen.get_rect()
        self.layers = layers
        self.speed = 1.0
        self.drag = 3.6
        self.loadTime = 500.0
        self.scorepanel = scorepanel.Scorepanel(side)
        self.lives = 3
        self.reinit()

    def reinit(self):
        if self.side == "left":
            self.rect.midleft = self.area.midleft
        elif self.side == "right":
            self.rect.midright = self.area.midright
        self.velocity = 0
        self.position = self.rect.center
        self.timer = 0
        self.density = 2.5
        self.torpedo = 3
        self.frame.left = 0
        self.image = self.base.subsurface(self.frame)

    def update(self, dt):
        self.velocity += physics.GRAVITY * dt * (self.density - self.layers.density(self.rect.top, self.rect.bottom)) / self.density
        self.velocity *= 1 - self.drag * dt
        if abs(self.velocity) < 10*dt + 0.02: # Magic numbers determined by experimentation. Stops oscillations.
            self.velocity = 0
        self.position = (self.position[0], self.position[1] + self.velocity * dt)
        self.rect.center = self.position
        self.frame.left = (self.torpedo) * self.frame.width
        self.image = self.base.subsurface(self.frame)

    def up(self):
        self.density -= 1.0
        if self.density < self.layers.densities[0] + 0.5:
            self.density = self.layers.densities[0] + 0.5

    def down(self):
        self.density += 1.0
        if self.density > self.layers.densities[-1] - 0.5:
            self.density = self.layers.densities[-1] - 0.5

    def torpedoUp(self):
        self.torpedo -= 1
        if self.torpedo < 0:
            self.torpedo = 0

    def torpedoDown(self):
        self.torpedo += 1
        if self.torpedo > len(self.layers) - 2:
            self.torpedo = len(self.layers) - 2

    def torpedoDensity(self):
        if self.torpedo >= 0:
            return self.layers.densities[self.torpedo] + 0.5
        else:
            return 0

    def markHit(self):
        self.lives -= 1
        self.scorepanel.setLife(self.lives)
