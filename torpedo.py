import math

import pygame
from pygame.locals import *

import physics
import resources

class Torpedo(pygame.sprite.Sprite):
    """A torpedo with some fixed density experiencing buoyancy"""

    def __init__(self, velocity, player, layers):
        pygame.sprite.Sprite.__init__(self)
        self.baseR = [None, None, None]
        self.baseL = [None, None, None]
        files = ['torpedo_slow.png','torpedo_med.png','torpedo_fast.png']
        for i in xrange(len(files)):
            self.baseR[i], self.rect = resources.load_png(files[i])
            self.baseL[i] = pygame.transform.flip(self.baseR[i],True,False)
        self.coloursR, self.rect = resources.load_png('torpedo_colours.png')
        self.coloursL = pygame.transform.flip(self.coloursR,True,False)
        mask, self.rect = resources.load_png('torpedo.png')
        self.frame = self.rect.copy()
        self.maskR = pygame.mask.from_surface(mask)
        self.maskL = pygame.mask.from_surface(pygame.transform.flip(mask,True,False))
        screen = pygame.display.get_surface()
        self.area = screen.get_rect()
        self.layers = layers
        self.dragy = 3.6
        self.dragx = 0.06
        self.framerate = 60.0
        self.reinit(velocity,player)

    def reinit(self, velocity, player):
        self.player = player
        self.locked = True
        self.power = 0
        self.velocity = velocity
        self.mode = -1
        self.density = 0
        self.side = self.player.side
        if self.side == "left":
            self.base = self.baseL
            self.mask = self.maskL
            self.colours = self.coloursL
        elif self.side == "right":
            self.base = self.baseR
            self.mask = self.maskR
            self.colours = self.coloursR
        self.position = self.rect.center
        self.time = 0.0
        self.frame.left = 0
        self.image = self.base[self.power].subsurface(self.frame)

    def update(self, dt):
        if self.locked:
            self.rect.bottom = self.player.rect.bottom
            if self.side == "left":
                self.rect.right = self.player.rect.right - 15
            elif self.side == "right":
                self.rect.left = self.player.rect.left + 15
            self.position = self.rect.center
            if self.mode != self.player.torpedo:
                self.mode = self.player.torpedo
                if self.mode >= 0:
                    self.density = self.layers.densities[self.mode] + 0.5
                    rect = self.frame.copy()
                    if self.side == "left":
                        rect.left = (len(self.layers) - self.mode - 2) * rect.width
                    elif self.side == "right":
                        rect.left = self.mode * rect.width
                    colour = self.colours.subsurface(rect)
                    for base in self.base:
                        for i in xrange(3):
                            rect.left = i*rect.width
                            base.blit(colour, rect)
                else:
                    self.density = 0
        else:
            self.velocity[1] += physics.GRAVITY * dt * (self.density - self.layers.density(self.rect.top, self.rect.bottom)) / self.density
            self.velocity[0] *= 1 - self.dragx * dt
            self.velocity[1] *= 1 - self.dragy * dt
            if abs(self.velocity[0]) < 10*dt + 0.02: # Magic numbers determined by experimentation. Stops oscillations.
                self.velocity[0] = 0
            if abs(self.velocity[1]) < 10*dt + 0.02:
                self.velocity[1] = 0
            self.position = (self.position[0] + self.velocity[0] * dt, self.position[1] + self.velocity[1] * dt)
        self.rect.center = self.position
        self.time += dt
        frame = int(self.time * self.framerate) % 3
        self.frame.left = frame * self.frame.width
        self.image = self.base[self.power].subsurface(self.frame)
