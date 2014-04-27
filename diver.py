import math

import pygame
from pygame.locals import *

import input
import physics
import resources

class Diver(pygame.sprite.Sprite):
    """A player controlled submersible"""

    def __init__(self, side, layers):
        pygame.sprite.Sprite.__init__(self)
        self.side = side
        self.base, self.frame = resources.load_png('diver_'+self.side+'.png')
        self.frame.width /= len(layers) + 1
        self.image = self.base.subsurface(self.frame)
        self.rect = self.frame.copy()
        screen = pygame.display.get_surface()
        self.area = screen.get_rect()
        self.layers = layers
        self.speed = 1.0
        self.input = input.Input()
        self.drag = 3.6
        self.loadTime = 500.0
        self.reinit()

    def reinit(self):
        if self.side == "left":
            self.rect.midleft = self.area.midleft
        elif self.side == "right":
            self.rect.midright = self.area.midright
        self.velocity = 0
        self.position = self.rect.center
        self.timer = 0
        self.lives = 3
        self.density = 2.5
        self.torpedo = -1

    def update(self):
        self.velocity += physics.GRAVITY / 60.0 * (self.density - self.layers.density(self.rect.top, self.rect.bottom)) / self.density
        self.velocity *= 1 - self.drag / 60.0
        if abs(self.velocity) < 1:
            self.velocity = 0
        self.position = (self.position[0], self.position[1] + self.velocity / 60.0)
        self.rect.center = self.position
        if self.input.fire:
            torpedoTime = pygame.time.get_ticks() - self.timer
            t = int(math.floor(torpedoTime/self.loadTime))
            if t > len(self.layers) - 2:
                t = len(self.layers) - 2
            if t != self.torpedo:
                self.torpedo = t
                self.frame.left = (t + 2) * self.frame.width
                self.image = self.base.subsurface(self.frame)
        elif self.torpedo != -1:
            self.torpedo = -1
            self.frame.left = 0
            self.image = self.base.subsurface(self.frame)

    def setBuoyant(self):
        if self.input.up:
            self.density -= 1.0
        if self.input.down:
            self.density += 1.0

        if self.density < self.layers.densities[0] + 0.5:
            self.density = self.layers.densities[0] + 0.5
        elif self.density > self.layers.densities[-1] - 0.5:
            self.density = self.layers.densities[-1] - 0.5

    def markHit(self):
        self.lives -= 1
        print("Player side "+self.side+" lost life. "+str(self.lives)+" remaining")

    def loadTorpedo(self):
        self.timer = pygame.time.get_ticks()
        self.torpedo = -1

    def torpedoDensity(self):
        if self.torpedo >= 0:
            return self.layers.densities[self.torpedo] + 0.5
        else:
            return 0
