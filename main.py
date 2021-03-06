#!/usr/bin/env python2
#
# Holy Diver
# A two player competitive side-on shooter with buoyancy physics

import os

import pygame
from pygame.locals import *

import diver
import explosion
import resources
import torpedo
import world

def main():
    # Initialise constants
    leadTime = 2.0
    loadTime = 0.2
    thrustTime = 1.8
    torpedoTime = 2.0
    torpedoSpeed = 600

    # Initialise mixer
    pygame.mixer.pre_init(44100, -16, 2, 4096)

    # Initialise screen
    pygame.init()
    screen = pygame.display.set_mode((800,600))
    pygame.display.set_caption('Holy Diver')
    screenRect = screen.get_rect()
    
    # Initialise joysticks
    joysticks = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]
    map(lambda x: x.init(), joysticks)

    # Initialise game objects
    layers = world.Layers([1, 2, 3, 4, 5], [150,250,400,500,600])
    player1 = diver.Diver("right", "crescent", layers)
    player2 = diver.Diver("left", "cross", layers)
    
    # Initialise sounds
    pygame.mixer.init()
    bloopsound = resources.load_sound('bluop.wav')
    pewsound = resources.load_sound('PEW.wav')
    explodesound = resources.load_sound('PCHRR.wav')
    startsound = resources.load_sound('BADAM.wav')
    winsound = resources.load_sound('daDUN.wav')
    losesound = resources.load_sound('wawow.wav')

    pewChannel = pygame.mixer.find_channel()

    # Initialise sprites
    playersprite = pygame.sprite.Group((player1,player2))
    scoresprite = pygame.sprite.Group((player1.scorepanel,player2.scorepanel))
    torpedos1 = pygame.sprite.Group()
    torpedos2 = pygame.sprite.Group()
    torpedos = [None, None]
    torpedoPool = []
    explosions = pygame.sprite.Group()

    def newTorpedo(velocity, player):
        if len(torpedoPool) == 0:
            return torpedo.Torpedo(velocity,player,layers)
        else:
            t = torpedoPool.pop()
            t.reinit(velocity,player)
            return t

    # Fill background
    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill((0,0,0))
    layers.draw(background)

    splash, _ = resources.load_png("OpeningSplash.png")
    win_screen = {}
    win_screen['cross'], _ = resources.load_png("WinCross.png")
    win_screen['crescent'], _ = resources.load_png("WinCrescent.png")
    win_screen['draw'], _ = resources.load_png("Draw.png")

    # Blit everything to the screen
    screen.blit(background, (0, 0))
    pygame.display.flip()

    # Initialise clock
    clock = pygame.time.Clock()

    # Initialise torpedo timer
    timer = [-leadTime] # Length one array so it can be captured by closure

    def reset():
        player1.reinit()
        player2.reinit()
        torpedoPool.extend(torpedos1)
        torpedos1.empty()
        torpedoPool.extend(torpedos2)
        torpedos2.empty()
        explosions.empty()
        torpedos[0] = None
        torpedos[1] = None
        timer[0] = -leadTime

    state = "start"
    cinematic = False
    cin_timer = 0

    startsound.play()

    while 1:
        dt = clock.tick(1000) / 1000.0
        if state == "start":
            for event in pygame.event.get():
                if event.type == QUIT:
                    return
                elif event.type == KEYDOWN or event.type == JOYBUTTONDOWN:
                    state = "run"
            player1.setLife(3)
            player2.setLife(3)
            screen.blit(splash, (0,0))
        elif state == "run":
            if dt > 0.1:
                dt = 0.1

            if cinematic:
                cin_timer -= dt
                dt *= 0.05
                if cin_timer <= 0:
                    cinematic = False
                    reset()
                    if player2.lives <= 0:
                        if player1.lives > 0:
                            winner = player1.faction
                            winsound.play()
                            state = "end"
                        else:
                            winner = "draw"
                            losesound.play()
                            state = "end"
                    elif player1.lives <= 0:
                        winner = player2.faction
                        winsound.play()
                        state = "end"
                    continue
            else:
                mindist = 1000**2
                for t in torpedos1:
                    d = (t.rect.left - player2.rect.centerx - 23)**2 + (t.rect.centery - player2.rect.centery - 15)**2
                    if d < mindist:
                        mindist = d
                    d = (t.rect.left - player2.rect.centerx + 8)**2 + (t.rect.centery - player2.rect.centery - 15)**2
                    if d < mindist:
                        mindist = d
                for t in torpedos2:
                    d = (t.rect.right - player1.rect.centerx + 23)**2 + (t.rect.centery - player1.rect.centery - 15)**2
                    if d < mindist:
                        mindist = d
                    d = (t.rect.right - player1.rect.centerx - 8)**2 + (t.rect.centery - player1.rect.centery - 15)**2
                    if d < mindist:
                        mindist = d

                if mindist < 20**2:
                    dt *= 0.05
                elif mindist < 100**2:
                    dt *= 0.05 + 0.95 * (mindist - 20.0**2) / (100.0**2 - 20.0**2)

            for event in pygame.event.get():
                if event.type == QUIT:
                    return
                elif event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        reset()
                        state = "start"
                        continue
                    elif not cinematic:
                        if event.key == K_o:
                            player1.up()
                            #bloopsound.play()
                        elif event.key == K_l:
                            player1.down()
                            #bloopsound.play()
                        elif event.key == K_i:
                            player1.torpedoUp()
                        elif event.key == K_k:
                            player1.torpedoDown()
                        elif event.key == K_w:
                            player2.up()
                            #bloopsound.play()
                        elif event.key == K_s:
                            player2.down()
                            #bloopsound.play()
                        elif event.key == K_q:
                            player2.torpedoUp()
                        elif event.key == K_a:
                            player2.torpedoDown()
                elif event.type == JOYBUTTONDOWN:
                    if event.button == 6:
                        reset()
                        state = "start"
                        continue
                    elif not cinematic:
                        if event.joy == 0:
                            if event.button == 0:
                                player1.down()
                            elif event.button == 1:
                                player1.up()
                            elif event.button == 2:
                                player1.torpedoDown()
                            elif event.button == 3:
                                player1.torpedoUp()
                        elif event.joy == 1:
                            if event.button == 0:
                                player2.down()
                            elif event.button == 1:
                                player2.up()
                            elif event.button == 2:
                                player2.torpedoDown()
                            elif event.button == 3:
                                player2.torpedoUp()

            if not cinematic:
                timer[0] += dt

                if timer[0] >= loadTime or timer[0] < 0:
                    if torpedos[0] == None:
                        torpedos[0] = newTorpedo([-torpedoSpeed,0],player1)
                        torpedos1.add(torpedos[0])
                    if torpedos[1] == None:
                        torpedos[1] = newTorpedo([torpedoSpeed,0],player2)
                        torpedos2.add(torpedos[1])
                    if timer[0] >= thrustTime:
                        torpedos[0].power = 2
                        torpedos[1].power = 2
                        if not pewChannel.get_busy():
                            pewChannel.play(pewsound)
                        if timer[0] > torpedoTime:
                            torpedos[0].locked = False
                            torpedos[0] = None
                            torpedos[1].locked = False
                            torpedos[1] = None
                            timer[0] -= torpedoTime
                    elif timer[0] < 0:
                        torpedos[0].power = 0
                        torpedos[1].power = 0
                    else:
                        power = int((timer[0] - loadTime) * 2.0 / (thrustTime - loadTime))
                        torpedos[0].power = power
                        torpedos[1].power = power

            screen.blit(background, (0,0))

            torpedos1.update(dt)
            torpedos2.update(dt)

            delete = [t for t in torpedos1 if not t.rect.colliderect(screenRect)]
            for t in delete:
                torpedoPool.append(t)
                torpedos1.remove(t)
            delete = [t for t in torpedos2 if not t.rect.colliderect(screenRect)]
            for t in delete:
                torpedoPool.append(t)
                torpedos2.remove(t)

            playersprite.update(dt)

            collisions = pygame.sprite.spritecollide(player1,torpedos2,True,pygame.sprite.collide_mask)
            if collisions:
                for c in collisions:
                    explosions.add(explosion.Explosion(c.rect.midright))
                torpedoPool.extend(collisions)
                player1.markHit()
                if not cinematic:
                    explodesound.play()
                    cinematic = True
                    cin_timer = 2.0

            collisions = pygame.sprite.spritecollide(player2,torpedos1,True,pygame.sprite.collide_mask)
            if collisions:
                for c in collisions:
                    explosions.add(explosion.Explosion(c.rect.midleft))
                torpedoPool.extend(collisions)
                player2.markHit()
                if not cinematic:
                    explodesound.play()
                    cinematic = True
                    cin_timer = 2.0

            explosions.update(dt)

            playersprite.draw(screen)
            torpedos1.draw(screen)
            torpedos2.draw(screen)
            explosions.draw(screen)
            scoresprite.draw(screen)
        elif state == "end":
            for event in pygame.event.get():
                if event.type == QUIT:
                    return
                elif event.type == KEYDOWN or event.type == JOYBUTTONDOWN:
                    state = "start"
                    continue
            screen.blit(win_screen[winner], (0,0))

        pygame.display.flip()
if __name__ == '__main__': main()
