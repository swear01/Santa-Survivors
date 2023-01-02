import sys

import pygame
import pygame_gui
from pygame.locals import *  # CONSTS
from pygame_gui.core import ObjectID

from bin.config import *

pygame.init() #place here or get error.
screen = pygame.display.set_mode((width, height))

from bin.backend import Backend
from bin.background import Background
from bin.enemy import Spawner
from bin.huds import Huds
from bin.player import Player
from bin.ui import *
from bin.weapon import weapon_list
from configparser import ConfigParser, ExtendedInterpolation

bgm_and_sounds_config = ConfigParser(interpolation=ExtendedInterpolation())
bgm_and_sounds_config.read('./data/config/bgm_and_sounds.ini')

clock = pygame.time.Clock()
manager = pygame_gui.UIManager((width,height))
for theme_file_path in theme_paths:
    manager.get_theme().load_theme(theme_file_path)

backend = Backend()
background = Background()
bgm = pygame.mixer.music.load(bgm_and_sounds_config['bgm']['dir'])
player_hurt = pygame.mixer.Sound(bgm_and_sounds_config['player_hurt']['dir'])
player_hurt.set_volume(0.4)
player_die = pygame.mixer.Sound(bgm_and_sounds_config['player_die']['dir'])
player_die.set_volume(0.6)

pygame.mixer.music.play(-1)#表示音樂撥放幾次
pygame.mixer.music.set_volume(0.4)

def gaming(selected_character):
    time_elapsed = 0
    bullets, enemies, enemy_bullets, drops = pygame.sprite.Group(), pygame.sprite.Group(), pygame.sprite.Group(), pygame.sprite.Group()
    player = Player(selected_character,(width/2, height/2), backend, weapon_list, enemies)
    players = pygame.sprite.Group(player)
    r,g,b = 128,128,128 #for game over animation

    spawner = Spawner(player)
    huds = Huds(screen,manager, width, height, player)

    while True:
        for event in pygame.event.get():
            manager.process_events(event=event)
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_p and not backend.paused and not backend.upgrade_menu or backend.upgrade:
                    backend.paused = True
                    pause = Pause(screen,backend)
                if backend.paused:
                    backend.game_over = pause.choose(event)
                if backend.upgrade_menu:
                    upgrade.choose(event)
                    # for weapon in player.weapons:
                    #     print(weapon.name,weapon.level)
                    # for buff in player.buffs:
                    #     print(buff.name,buff.level)


        dt = clock.tick(FPS)/1000

        # gui updates
        if backend.paused:
            dt = 0
            pause.show()
        if backend.upgrade_menu:
            dt = 0
            upgrade.show()

        time_elapsed += dt
        #player.time_elapsed = time_elapsed



        keys = pygame.key.get_pressed()

        enemies.add(spawner.spawn(time_elapsed, dt))


        #update position
        player.update(keys ,time_elapsed, dt) #include moves
        player.shift_pos(background,(width, height), bullets, enemies, enemy_bullets, drops)
        
        huds.update(time_elapsed,player.enemy_killed)
        for weapon in player.weapons:
            bullets.add(weapon.update(dt))
        for bullet in bullets:
            bullet.update(dt)
        for enemy in enemies:
            enemy_bullets.add(enemy.update(time_elapsed, dt))
            drops.add(enemy.if_death())

        for enemy_bullet in enemy_bullets:
            enemy_bullet.update(time_elapsed, dt)
            enemy_bullet.if_death()
        for drop in drops:
            drop.update(dt)

        if dt != 0 : #dt = 0 , no collision

            #collision code
            b_e_collide = pygame.sprite.groupcollide(bullets, enemies, False, False)

            for bullet, hit_enemies in b_e_collide.items():
                for enemy in hit_enemies: #bullaet may have 0 hp
                    if bullet.hp <= 0 : break
                    if enemy.hp <= 0 :    
                        enemy.death()          
                        continue
                    enemy.hp -= bullet.atk*player.ratio['atk']
                    bullet.hp -= 1 
                    # if type(bullet) == Deer_antler_bullet or type(bullet) == Igloo_shelter :
                    #     enemy.avoid()

            for enemy1, enemy2s in pygame.sprite.groupcollide(enemies,enemies, False, False, pygame.sprite.collide_circle_ratio(0.5)).items():
                for enemy2 in enemy2s:
                    if enemy1 == enemy2 : continue
                    drct = enemy1.pos - enemy2.pos
                    if not norm(drct) : continue
                    drct = drct/norm(drct)*2.5
                    enemy1.pos += drct
                    enemy2.pos -= drct
                    

            enemies_atked = pygame.sprite.spritecollide(player, enemies, dokill=False)
            enemies_atked += pygame.sprite.spritecollide(player, enemy_bullets, dokill=False)

            for enemy in enemies_atked:
                if not pygame.sprite.collide_mask(player, enemy) : continue
                player.hp -= enemy.atk
                player_hurt.play()
                enemy.avoid()
                
            drops_absorbed = pygame.sprite.spritecollide(player, drops, dokill=False)
            
            for drop in drops_absorbed:
                drop.absorbed()


        manager.update(dt)
        # draw at last/ player is always on the top
        backend.draw(screen,background,drops,enemy_bullets,enemies,bullets,huds,players)
        manager.draw_ui(screen)

        if backend.upgrade:
            dt = 0
            upgrade = Upgrade(screen,manager,player,backend)
            upgrade.draw()
            backend.upgrade = False
            backend.upgrade_menu = True

        if backend.upgrade_menu:
            dt = 0
            upgrade.draw()

        if backend.paused:
            pause.draw()
        
        if backend.game_over:
            pygame.mixer.music.stop()
            dt = 0
            ds = clock.get_time()
            r,g,b = r-ds*0.1,g-ds*0.1,b-ds*0.1
            player_die.play()
            if r <= 0:
                screen.fill((0,0,0))
                huds.kill()
                backend.game_over = False
                return "game_over", player.enemy_killed, False
            else:
                screen.fill((r,g,b))
        pygame.display.flip()


        #print(clock.get_fps(), len(enemies), len(bullets))
    

clock.tick()#init call
while True:
    if not pygame.mixer.music.get_busy():
        pygame.mixer.music.play(-1)#表示音樂撥放幾次
        pygame.mixer.music.set_volume(0.4)
    if backend.main_page:
        next_stage,backend.main_page = main_page(screen,manager,clock)
    elif backend.tutorial:
        next_stage,backend.tutorial = tutorial(screen,manager,clock)
    elif backend.select_character:
        next_stage, backend.selected_character, backend.select_character = select_role(screen,manager,clock)
    elif backend.start_game:
        next_stage, enemy_killed,backend.start_game = gaming(backend.selected_character)
    elif backend.game_over:
        next_stage,backend.game_over = game_over(screen,manager,clock, enemy_killed)

    if next_stage == 'main_page':
        backend.main_page = True
    elif next_stage == 'tutorial':
        backend.tutorial = True
    elif next_stage == 'select_character':
        backend.select_character = True
    elif next_stage == 'start':
        backend.start_game = True
    elif next_stage == 'game_over':
        backend.game_over = True
