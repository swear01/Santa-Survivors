import pygame
from pygame.locals import * # CONSTS
import sys
from bin.player import Player
from bin.weapon import Weapon, Bullet
from config import *


pygame.init()
 

clock = pygame.time.Clock()

screen = pygame.display.set_mode((width, height))

player = Player(pos=(200,200))
players = pygame.sprite.Group()
players.add(player)
player.weapons.append(Weapon('test'))

bullets = pygame.sprite.Group()

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()


    keys = pygame.key.get_pressed()
    print(player.rect.center)
    if keys[K_a] and not keys[K_d]:
        player.move('left')
    if keys[K_d] and not keys[K_a]:
        player.move('right')
    if keys[K_s] and not keys[K_w]:
        player.move('down')
    if keys[K_w] and not keys[K_s]:
        player.move('up')
    
    for weapon in player.weapons:
        weapon.reload -= 1/fps
        if weapon.reload <= 0:
            weapon.reload+= weapon.cooldown
            weapon.shoot(player.rect.center)



            


        

    screen.fill('#000000')
    players.draw(screen)


    pygame.display.flip()

    clock.tick(fps)
    
