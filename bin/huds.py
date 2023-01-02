from configparser import ConfigParser, ExtendedInterpolation

import pygame
import pygame_gui
from pygame.locals import *  # CONSTS
from pygame_gui.core import ObjectID

config = ConfigParser(interpolation=ExtendedInterpolation())
config.read('./data/config/huds.ini')

class Weapon_icon():
    def __init__(self,screen,weapon,number):
        self.screen = screen
        self.x = [int(x) for x in config['weapon_icon']['x'].split('\n')][number]
        self.y = int(config['weapon_icon']['y'])
        self.width = int(config['weapon_icon']['width'])
        self.height = int(config['weapon_icon']['height'])
        self.name = 'weapon_icon'
        if weapon != "weapon_icon":
            self.image = pygame.transform.scale(weapon.image,(self.width,self.height))
        else:
            self.image = pygame.image.load(config['weapon_icon']['img_dir']).convert_alpha()
            self.image = pygame.transform.scale(self.image,(self.width,self.height))
        
    def show(self,screen):
        screen.blit(self.image,(self.x,self.y))

class Buff_icon():
    def __init__(self,screen,buff,number):
        self.screen = screen
        self.x = [int(x) for x in config['buff_icon']['x'].split('\n')][number]
        self.y = int(config['buff_icon']['y'])
        self.width = int(config['buff_icon']['width'])
        self.height = int(config['buff_icon']['height'])
        if buff != "buff_icon":
            self.image = pygame.transform.scale(self.image,(self.width,self.height))
        else:
            self.image = pygame.image.load(config['buff_icon']['img_dir']).convert_alpha()
            self.image = pygame.transform.scale(self.image,(self.width,self.height))
        
    def show(self,screen):
        screen.blit(self.image,(self.x,self.y))

class Huds:
    def __init__(self, screen, manager, width, height, player):
        self.manager = manager
        self.player = player
        self.screen = screen
        xp_bar_width = width-2*int(config['xp_bar']['margin'])
        
        self.xp_bar = pygame_gui.elements.UIStatusBar(
            relative_rect=pygame.Rect(
                int(config['xp_bar']['margin']),int(config['xp_bar']['margin']),xp_bar_width,int(config['xp_bar']['height'])), 
            manager=manager,
            sprite=player, follow_sprite=False, anchors={'top':'top', 'left':'left'},
            percent_method=player.get_xp_percent ,object_id=ObjectID('#xp_bar','@player_bar'))
        self.xp_bar.status_text = lambda : f'Level {player.level}'
            
        self.hp_bar = pygame_gui.elements.UIStatusBar(relative_rect=(0,0,player.width,int(config['hp_bar']['height'])), 
            manager=manager,
            sprite=player, follow_sprite=True, anchors={},
            percent_method=player.get_health_percent, object_id=ObjectID('#hp_bar','@player_bar'))

        self.timer = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect(0,0,int(config['timer']['width']),int(config['timer']['height'])),
            anchors={'centerx':'centerx','top_target':self.xp_bar}, text = '00 : 00', manager=manager,
            object_id=ObjectID('#guide_text')
            )

        self.kill_counter = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect(-250,0,int(config['kill_counter']['width']),int(config['kill_counter']['height'])),
            anchors={'right':'right','top_target':self.xp_bar}, text = 'kills:0', manager=manager,
            object_id=ObjectID('#guide_text')
            )
        self.weapon_icons = [Weapon_icon(screen,'weapon_icon',0), Weapon_icon(screen,'weapon_icon',1), Weapon_icon(screen,'weapon_icon',2), Weapon_icon(screen,'weapon_icon',3)]
        self.buff_icons = [Buff_icon(screen,'buff_icon',0), Buff_icon(screen,'buff_icon',1), Buff_icon(screen,'buff_icon',2), Buff_icon(screen,'buff_icon',3)]
        self.weapons = 0
        self.buffs = 0
        #self.timer.set_text_scale(1)
        
        
    def update(self, time_elapsed,kill_counts):
        self.timer.set_text(f'{(int(time_elapsed // 60)):02d} : {(int(time_elapsed) % 60):02d}')
        self.kill_counter.set_text(f'kills:{kill_counts}')
        if self.weapons < len(self.player.weapons):
            self.weapon_icons[self.weapons] = Weapon_icon(self.screen,self.player.weapons[self.weapons],self.weapons)
            self.weapons += 1

    def kill(self):
        self.timer.kill()
        self.hp_bar.kill()
        self.xp_bar.kill()
        self.kill_counter.kill()
       
    def draw(self,screen):
            for icon in self.weapon_icons:
                icon.show(screen)
            for icon in self.buff_icons:
                icon.show(screen)

