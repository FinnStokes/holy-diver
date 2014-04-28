import pygame
from pygame.locals import *

import resources

class Scorepanel(pygame.sprite.Sprite):
    """Manages the score panel"""

    def __init__(self, side, faction):
        pygame.sprite.Sprite.__init__(self)
        self.side = side
        self.base, self.frame = resources.load_png('score_'+self.side+'_'+faction+'.png')
        self.frame.width /= 4
        self.rect = self.frame.copy()
        screen = pygame.display.get_surface()
        self.area = screen.get_rect()
        self.reinit()

    def reinit(self):
        if self.side == "left":
            self.rect.topleft = self.area.topleft
        elif self.side == "right":
            self.rect.topright = self.area.topright
        self.position = self.rect.center
        self.frame.left = 0
        self.image = self.base.subsurface(self.frame)

    def setLife(self,life):
        if life > 3:
            print("Invalid life (" + str(life) + ") for " + self.side + " player.")
            life = 3
        elif life < 0:
            print("Invalid life (" + str(life) + ") for " + self.side + " player.")
            life = 0
        self.frame.left = (3-life) * self.frame.width
        self.image = self.base.subsurface(self.frame)
