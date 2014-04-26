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
        self.image, self.rect = resources.load_png('diver.png')
        screen = pygame.display.get_surface()
        self.area = screen.get_rect()
        self.layers = layers
        self.side = side
        if self.side == "right":
            self.image = pygame.transform.flip(self.image, True, False)
        self.speed = 1.0
        self.density = 2.5
        self.input = input.Input()
        self.drag = 3.6
        self.velocity = 0
        self.position = self.rect.center
        self.lives = 3
        self.reinit()

    def reinit(self):
        if self.side == "left":
            self.rect.midleft = self.area.midleft
        elif self.side == "right":
            self.rect.midright = self.area.midright
        self.velocity = 0
        self.position = self.rect.center

    def update(self):
        movepos = [0,0]
        if self.input.up:
            self.density -= self.speed / 60.0
        if self.input.down:
            self.density += self.speed / 60.0

        if self.density < self.layers.densities[0]:
            self.density = self.layers.densities[0]
        elif self.density > self.layers.densities[-1]:
            self.density = self.layers.densities[-1]

        self.velocity += physics.GRAVITY / 60.0 * (self.density - self.layers.density(self.rect.top, self.rect.bottom)) / self.density
        self.velocity *= 1 - self.drag / 60.0
        if abs(self.velocity) < 1:
            self.velocity = 0
        self.position = (self.position[0], self.position[1] + self.velocity / 60.0)
        self.rect.center = self.position

    def markHits(self, torpedos):
        if pygame.sprite.spritecollide(self,torpedos,1):
            self.lives -= 1
            print("Player side "+self.side+" lost life. "+str(self.lives)+" remaining")
