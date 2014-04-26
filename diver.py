import math

import pygame
from pygame.locals import *

import resources
import input

class Diver(pygame.sprite.Sprite):
    """A player controlled submersible"""

    def __init__(self, side):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = resources.load_png('diver.png')
        screen = pygame.display.get_surface()
        self.area = screen.get_rect()
        self.side = side
        if self.side == "right":
            self.image = pygame.transform.flip(self.image, True, False)
        self.speed = 180.0
        self.diagonal_speed = self.speed
        self.input = input.Input()
        self.reinit()

    def reinit(self):
        if self.side == "left":
            self.rect.midleft = self.area.midleft
        elif self.side == "right":
            self.rect.midright = self.area.midright

    def update(self):
        movepos = [0,0]
        if self.input.left:
            movepos[0] -= 1
        if self.input.right:
            movepos[0] += 1
        if self.input.up:
            movepos[1] -= 1
        if self.input.down:
            movepos[1] += 1

        if movepos[0] != 0 and movepos[1] != 0:
            movepos[0] *= self.diagonal_speed / 60.0
            movepos[1] *= self.diagonal_speed / 60.0
        else:
            movepos[0] *= self.speed / 60.0
            movepos[1] *= self.speed / 60.0

        newpos = self.rect.move(movepos)
        if self.area.contains(newpos):
            self.rect = newpos
