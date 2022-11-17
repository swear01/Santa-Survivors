import pygame
from pygame.locals import * # CONSTS
import sys
from bin.player import Player
from bin.weapon import Weapon
from bin.enemy import Enemy
from bin.config import *


pygame.init()
 

clock = pygame.time.Clock()

screen = pygame.display.set_mode((width, height))

player = Player(pos=(200,200))
players = pygame.sprite.Group()
players.add(player)
player.weapons.append(Weapon('test', player=player, b_amt=7))
player.weapons.append(Weapon('autoaim', player=player, b_speed=125, b_hp=2))

bullets, enemies = pygame.sprite.Group(), pygame.sprite.Group()
enemy_timer = enemy_cooldown
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()


    keys = pygame.key.get_pressed()
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
            weapon.reload += weapon.cooldown
            bullets.add(weapon.shoot(player.rect.center, enemies))

    enemy_timer-=1
    if enemy_timer <= 0 : 
        enemy_timer = enemy_cooldown
        enemies.add(Enemy.spawn_enemy(player=player))


    #update position
    player.update() 
    for bullet in bullets:
        bullet.update()
    for enemy in enemies:
        enemy.update()    

    #collision code
    b_e_collide = pygame.sprite.groupcollide(bullets, enemies, False, False)

    for bullet, hit_enemies in b_e_collide.items():
        for enemy in hit_enemies: #bullet will have at least 1 health
            if enemy.hp == 0 : continue
            enemy.hp -= bullet.atk
            bullet.hp -= 1 

            if bullet.hp <= 0 : break



    # draw zone
    screen.fill('#000000')
    bullets.draw(screen)
    enemies.draw(screen)
    players.draw(screen) #player is always at the top

    pygame.display.flip()

    clock.tick(fps)

    print(clock.get_fps(), len(enemies), len(bullets))
    
