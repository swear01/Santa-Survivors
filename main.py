import pygame
import pygame_gui
from pygame_gui.core import ObjectID
from pygame.locals import * # CONSTS
import sys
from bin.player import Player
from bin.weapon import Weapon
from bin.enemy import Enemy
from bin.config import *
from bin.backend import Backend


pygame.init()
 

clock = pygame.time.Clock()

screen = pygame.display.set_mode((width, height))
manager = pygame_gui.UIManager((width,height))
for theme_file_path in theme_paths:
    manager.get_theme().load_theme(theme_file_path)
    
backend = Backend()

player = Player(pos=(200,200))
players = pygame.sprite.Group()
players.add(player)
player.weapons.append(Weapon('test', player=player, b_amt=7))
player.weapons.append(Weapon('autoaim', player=player, b_speed=125, b_hp=2))

#gui init
xp_bar_width = width-2*xp_bar_margin
xp_bar = pygame_gui.elements.UIStatusBar(relative_rect=pygame.Rect(xp_bar_margin,xp_bar_margin,xp_bar_width,20), manager=manager,
    sprite=player, follow_sprite=False, anchors={'top':'top', 'left':'left', 'right':'right'},
    percent_method=player.get_xp_percent ,object_id=ObjectID('#xp_bar','@player_bar'))

xp_bar.status_text = lambda : f'Level {player.level}'

# level_text = pygame_gui.elements.UILabel(relative_rect=pygame.Rect(5,2,50,16), text='init',
#     manager=manager, parent_element=xp_bar,
#     anchors={'top':xp_bar, 'left':xp_bar}
# )

hp_bar = pygame_gui.elements.UIStatusBar(relative_rect=(0,0,51,10), manager=manager,
    sprite=player, follow_sprite=True, anchors={'centerx':'left'},
    percent_method=player.get_health_percent, object_id=ObjectID('#hp_bar','@player_bar'))

bullets, enemies, drops = pygame.sprite.Group(), pygame.sprite.Group(), pygame.sprite.Group()
enemy_timer = enemy_cooldown
clock.tick() ##init call
while True:
    for event in pygame.event.get():
        manager.process_events(event=event)
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN:
            if event.key == K_p :
                backend.paused = not backend.paused
              
    dt = clock.tick(FPS)/1000
    if backend.paused : dt = 0  


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

    enemy_timer-= 1*dt
    if enemy_timer <= 0 : 
        enemy_timer = enemy_cooldown
        enemies.add(Enemy.spawn_enemy(player=player))


    #update position
    player.update(dt) 
    for bullet in bullets:
        bullet.update(dt)
    for enemy in enemies:
        drops.add(enemy.update(dt))
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
    
