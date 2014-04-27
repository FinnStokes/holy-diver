import bisect

import pygame
from pygame.locals import *

import resources

class Layers():
    def __init__(self, densities, depths):
        assert(len(densities) == len(depths))
        self.densities = densities
        self.depths = depths
        self.colors = [pygame.Color('cyan'), pygame.Color('red'), pygame.Color('yellow'), pygame.Color('green'), pygame.Color('blue')]
        self.filenames = ["RedRipple.png","YellowDiamonds.png","GreenStripe.png","BlueTartan.png"]

    def __len__(self):
        return len(self.densities)

    def density(self, top, bottom):
        itop = bisect.bisect_left(self.depths,top)
        ibot = bisect.bisect_left(self.depths,bottom)
        if itop >= len(self.densities):
            itop = len(self.densities) - 1
        if ibot >= len(self.densities):
            ibot = len(self.densities) - 1
        if itop == ibot:
            return self.densities[itop]
        else:
            rho = self.densities[itop] * (self.depths[itop] - top) * 1.0 / (bottom - top)
            for i in xrange(itop+1, ibot):
                print(i)
                rho += self.densities[i] * (self.depths[i] - self.depths[i-1]) * 1.0 / (bottom - top)
            rho += self.densities[ibot] * (bottom - self.depths[ibot-1]) * 1.0 / (bottom - top)
            return rho

    def draw(self, surface):
        rect = surface.get_rect()
        rect.height = self.depths[0]
        rect.top = 0
        pygame.draw.rect(surface, self.colors[0], rect)

        for i in xrange(1,len(self.depths)):
            rect.height = self.depths[i] - self.depths[i-1]
            rect.top = self.depths[i-1]
            tile,square = resources.load_png(self.filenames[i-1])
            numtilesY = rect.height/square.height+1
            numtilesX = rect.width/square.width+1

            for jy in xrange(0,numtilesY):
                for jx in xrange(0,numtilesX):
                    xplace = jx*86
                    yplace = rect.top + jy*86
                    surface.blit(tile,(xplace,yplace))