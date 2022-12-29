import pygame
import pygame_gui
from pygame_gui.core import ObjectID
from pygame.locals import * # CONSTS
import sys
from bin.config import *

pygame.init() #place here or get error.
screen = pygame.display.set_mode((width, height))

from bin.player import Player
from bin.weapon import Weapon
from bin.enemy import Spawner
from bin.backend import Backend
from bin.huds import Huds
from bin.ui import *


 

clock = pygame.time.Clock()
manager = pygame_gui.UIManager((width,height))
for theme_file_path in theme_paths:
    manager.get_theme().load_theme(theme_file_path)

backend = Backend()

def gaming():
    time_elapsed = 0
    player = Player(pos=(200,200))
    players = pygame.sprite.Group()
    players.add(player)
    player.weapons.append(Weapon('test', player=player, b_amt=7))
    player.weapons.append(Weapon('autoaim', player=player, b_speed=125, b_hp=2))

    # level_text = pygame_gui.elements.UILabel(relative_rect=pygame.Rect(5,2,50,16), text='init',
    #     manager=manager, parent_element=xp_bar,
    #     anchors={'top':xp_bar, 'left':xp_bar}
    # )

    bullets, enemies, drops = pygame.sprite.Group(), pygame.sprite.Group(), pygame.sprite.Group()
    spawner = Spawner()
    huds = Huds(manager, width, height, player)
    clock.tick() ##init call

    while True:
        for event in pygame.event.get():
            manager.process_events(event=event)
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_p and not backend.paused:
                    backend.paused = True
                    ui_reload = 1
                    ui_cooldown = 1
                    resume_game =  pygame_gui.elements.UITextBox(html_text="resume",relative_rect=pygame.Rect((0,150), (100, 50)),
                            manager=manager,anchors={'centerx': 'centerx'},object_id=ObjectID(class_id='@selected'))
                    settings =  pygame_gui.elements.UITextBox(html_text="settings",relative_rect=pygame.Rect((0,225), (100, 50)),
                            manager=manager,anchors={'centerx': 'centerx'},object_id=ObjectID(class_id='@selected'))
                    quit_game =  pygame_gui.elements.UITextBox(html_text="quit",relative_rect=pygame.Rect((0,300), (100, 50)),
                            manager=manager,anchors={'centerx': 'centerx'},object_id=ObjectID(class_id='@selected'))
                    pause = [resume_game,settings,quit_game]
                    selected = 0
                    ds = 0

                if backend.paused:
                    if event.key == K_UP and selected>0:
                        selected-=1
                    if event.key == K_DOWN and selected<len(pause)-1:
                        selected+=1
                    if event.key == K_RETURN:
                        if pause[selected] == resume_game:
                            for option in pause:
                                option.kill()
                            backend.paused = False
                        else:
                            if pause[selected] == settings:
                                chosen = 'settings'
                            if pause[selected] == quit_game:
                                chosen = 'main_page'
                            for option in pause:
                                option.kill()
                                xp_bar.kill()
                                hp_bar.kill()
                            backend.paused = False
                            return chosen,False

        dt = clock.tick(FPS)/1000
        ds = dt*3

        if backend.paused : 
            dt = 0
            ui_reload -= ds
            if ui_reload <= 0:
                pause[selected].visible = 0
                ui_reload += ui_cooldown
            else:
                pause[selected].visible = 1
            for i in range(len(pause)):
                if i == selected:
                    pass
                else:
                    pause[i].visible = 1
                    
        time_elapsed += dt
        player.time_elapsed = time_elapsed


        keys = pygame.key.get_pressed()
        if keys[K_a] and not keys[K_d]:
            player.move('left', dt)
        if keys[K_d] and not keys[K_a]:
            player.move('right', dt)
        if keys[K_s] and not keys[K_w]:
            player.move('down', dt)
        if keys[K_w] and not keys[K_s]:
            player.move('up', dt)
        
        for weapon in player.weapons:
            weapon.reload -= 1*dt
            if weapon.reload <= 0:
                weapon.reload += weapon.cooldown
                bullets.add(weapon.shoot(player.rect.center, enemies))


        enemies.add(spawner.spawn(time_elapsed, dt, player, 5))


        #update position
        player.update(dt) 
        huds.update(time_elapsed)
        for bullet in bullets:
            bullet.update(dt)
        for enemy in enemies:
            drops.add(enemy.update(time_elapsed, dt))
        for drop in drops:
            drop.update(dt)

        #collision code
        b_e_collide = pygame.sprite.groupcollide(bullets, enemies, False, False)

        for bullet, hit_enemies in b_e_collide.items():
            for enemy in hit_enemies: #bullet will have at least 1 health
                if enemy.hp == 0 :              
                    continue
                enemy.hp -= bullet.atk
                bullet.hp -= 1 


                if bullet.hp <= 0 : break

        enemies_atked = pygame.sprite.spritecollide(player, enemies, dokill=False)

        for enemy in enemies_atked:
            player.hp -= enemy.atk
            enemy.avoid()
            
        drops_absorbed = pygame.sprite.spritecollide(player, drops, dokill=False)
        
        for drop in drops_absorbed:
            drop.absorbed()

        # gui updates
        # level_text.set_text(f'{player.level} Levels')

        manager.update(dt)

        # draw zone
        screen.fill('#000000')
        bullets.draw(screen)
        drops.draw(screen)
        enemies.draw(screen)
        players.draw(screen) #player is always at the top
        manager.draw_ui(screen)

        pygame.display.flip()


        #print(clock.get_fps(), len(enemies), len(bullets))
    


while True:
    if backend.main_page:
        next_stage,backend.main_page = main_page(screen,manager)
    if backend.start_game:
        next_stage,backend.start_game = gaming()
    if next_stage == 'main_page':
        backend.main_page = True
    elif next_stage == 'start':
        backend.start_game = True