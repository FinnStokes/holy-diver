#!/usr/bin/env python2
#
# Holy Diver
# A two player competitive side-on shooter with buoyancy physics

import os

import pygame
from pygame.locals import *

import diver
import resources
import torpedo
import world

def main():
    # Initialise screen
    pygame.init()
    screen = pygame.display.set_mode((800,600))
    pygame.display.set_caption('Holy Diver')

    # Initialise game objects
    layers = world.Layers([1, 2, 3, 4], [150,300,450,600])
    player = diver.Diver("left")
    
    # Initialise sprites
    playersprite = pygame.sprite.Group(player)
    torpedos = pygame.sprite.Group()

    # Fill background
    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill((0,0,0))
    layers.draw(background)

    # Blit everything to the screen
    screen.blit(background, (0, 0))
    pygame.display.flip()

    # Initialise clock
    clock = pygame.time.Clock()

    while 1:
        # Make sure game doesn't run at more than 60 frames per second
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == QUIT:
                return
            elif event.type == KEYDOWN:
		if event.key == K_UP:
                    player.input.up = True
                elif event.key == K_DOWN:
                    player.input.down = True
		elif event.key == K_LEFT:
                    player.input.left = True
                elif event.key == K_RIGHT:
                    player.input.right = True
                elif event.key == K_SPACE:
                    torpedos.add(torpedo.Torpedo([10,0],2.5,player,layers))
            elif event.type == KEYUP:
		if event.key == K_UP:
                    player.input.up = False
                elif event.key == K_DOWN:
                    player.input.down = False
		elif event.key == K_LEFT:
                    player.input.left = False
                elif event.key == K_RIGHT:
                    player.input.right = False

        screen.blit(background, (0,0))

        torpedos.update()
        playersprite.update()
        torpedos.draw(screen)
        playersprite.draw(screen)

        pygame.display.flip()

if __name__ == '__main__': main()
