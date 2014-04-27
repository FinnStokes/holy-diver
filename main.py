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
    screenRect = screen.get_rect()

    # Initialise game objects
    layers = world.Layers([1, 2, 3, 4, 5], [100,200,400,500,600])
    player1 = diver.Diver("right", layers)
    player2 = diver.Diver("left", layers)
    
    # Initialise sprites
    playersprite = pygame.sprite.Group((player1,player2))
    scoresprite = pygame.sprite.Group((player1.scorepanel,player2.scorepanel))
    torpedos1 = pygame.sprite.Group()
    torpedos2 = pygame.sprite.Group()
    torpedoPool = []

    def newTorpedo(velocity, player):
        density = player.torpedoDensity()
        if len(torpedoPool) == 0:
            return torpedo.Torpedo(velocity,density,player,layers)
        else:
            t = torpedoPool.pop()
            t.reinit(velocity,density,player)
            return t

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

    # Initialise torpedo timers
    torp1timer = 0
    torp2timer = 0

    timer = pygame.time.get_ticks() + 1500

    while 1:
        # Make sure game doesn't run at more than 60 frames per second
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == QUIT:
                return
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    return
                if event.key == K_o:
                    player1.input.up = True
                    player1.setBuoyant()
                elif event.key == K_l:
                    player1.input.down = True
                    player1.setBuoyant()
                elif event.key == K_i:
                    player1.torpedoUp()
                elif event.key == K_k:
                    player1.torpedoDown()
                elif event.key == K_w:
                    player2.input.up = True
                    player2.setBuoyant()
                elif event.key == K_s:
                    player2.input.down = True
                    player2.setBuoyant()
                elif event.key == K_q:
                    player2.torpedoUp()
                elif event.key == K_a:
                    player2.torpedoDown()
            elif event.type == KEYUP:
                if event.key == K_o:
                    player1.input.up = False
                elif event.key == K_l:
                    player1.input.down = False
                elif event.key == K_w:
                    player2.input.up = False
                elif event.key == K_s:
                    player2.input.down = False

        t = pygame.time.get_ticks()
        if t - timer >= 2000:
            torpedos1.add(newTorpedo([-600,0],player1))
            torpedos2.add(newTorpedo([600,0],player2))
            timer += 2000

        screen.blit(background, (0,0))

        torpedos1.update()
        torpedos2.update()

        delete = [t for t in torpedos1 if not t.rect.colliderect(screenRect)]
        for t in delete:
            torpedoPool.append(t)
            torpedos1.remove(t)
        delete = [t for t in torpedos2 if not t.rect.colliderect(screenRect)]
        for t in delete:
            torpedoPool.append(t)
            torpedos2.remove(t)

        playersprite.update()

        collisions = pygame.sprite.spritecollide(player1,torpedos2,1)
        if collisions:
            torpedoPool.extend(collisions)
            player1.markHit()

        collisions = pygame.sprite.spritecollide(player2,torpedos1,1)
        if collisions:
            torpedoPool.extend(collisions)
            player2.markHit()

        torpedos1.draw(screen)
        torpedos2.draw(screen)
        playersprite.draw(screen)
        scoresprite.draw(screen)

        pygame.display.flip()

if __name__ == '__main__': main()
