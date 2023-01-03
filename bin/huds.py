from configparser import ConfigParser, ExtendedInterpolation

import pygame
import pygame_gui
from pygame.locals import *  # CONSTS
from pygame_gui.core import ObjectID

config = ConfigParser(interpolation=ExtendedInterpolation())
config.optionxform = str
config.read('./data/config/huds.ini')

class Weapon_icon():
    def __init__(self,screen,manager,player,weapon,number):
        self.screen = screen
        self.player = player
        self.number = number
        self.x = [int(x) for x in config['weapon_icon']['x'].split('\n')][number]
        self.y = int(config['weapon_icon']['y'])
        self.width = int(config['weapon_icon']['width'])
        self.height = int(config['weapon_icon']['height'])
        self.name = 'weapon_icon'
        if weapon != "weapon_icon":
            if weapon.name == 'LED' or weapon.name == 'led' or self.name == 'led':
                self.led = pygame.image.load(config['led']['img_dir']).convert_alpha()
                self.image = pygame.transform.scale(self.led,(self.width,self.height))
            else:
                self.image = pygame.transform.scale(weapon.image,(self.width,self.height))
        else:
            self.image = pygame.image.load(config['weapon_icon']['img_dir']).convert_alpha()
            self.image = pygame.transform.scale(self.image,(self.width,self.height))
        if number <= len(player.weapons)-1:
            self.level = player.weapons[number].level
            self.level_text = pygame_gui.elements.UILabel(relative_rect=pygame.Rect(self.x-10,self.y+27,50,30),
                text = f'lv.{self.level+1}', manager=manager,object_id=ObjectID('#level_text'))

    def show(self,screen):
        screen.blit(self.image,(self.x,self.y))
    
    def update(self):
        if self.level_text.text[3:] != 'MAX':
            if int(self.level_text.text[3:])-1 < self.player.weapons[self.number].level:
                self.level_text.set_text(f'lv.{int(self.player.weapons[self.number].level) + 1}')
            if int(self.level_text.text[3:]) == self.player.weapons[self.number].max_level+1:
                self.level_text.set_text(f'lv.MAX')

    def kill(self):
        self.level_text.kill()
        

class Buff_icon():
    def __init__(self,screen,manager,player,buff,number):
        self.screen = screen
        self.player = player
        self.number = number
        self.x = [int(x) for x in config['buff_icon']['x'].split('\n')][number]
        self.y = int(config['buff_icon']['y'])
        self.width = int(config['buff_icon']['width'])
        self.height = int(config['buff_icon']['height'])
        self.name = 'weapon_icon'
        if buff != "buff_icon":
            self.image = pygame.transform.scale(buff.image,(self.width,self.height))
        else:
            self.image = pygame.image.load(config['buff_icon']['img_dir']).convert_alpha()
            self.image = pygame.transform.scale(self.image,(self.width,self.height))
        if number <= len(player.buffs)-1:
            self.level = player.buffs[number].level
            self.level_text = pygame_gui.elements.UILabel(relative_rect=pygame.Rect(self.x-5,self.y+27,40,30),
                text = f'lv.{self.level+1}', manager=manager,object_id=ObjectID('#level_text'))

    def show(self,screen):
        screen.blit(self.image,(self.x,self.y))
    
    def update(self):
        if self.level_text.text[3:] != 'MAX':
            if int(self.level_text.text[3:]) < self.player.buffs[self.number].level+1:
                self.level_text.set_text(f'lv.{int(self.player.buffs[self.number].level) + 1}')
            if int(self.level_text.text[3:]) == self.player.buffs[self.number].max_level+1:
                self.level_text.set_text(f'lv.MAX')

    def kill(self):
        self.level_text.kill()

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
        self.gold_counter = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect(-250,50,int(config['gold_counter']['width']),int(config['gold_counter']['height'])),
            anchors={'right':'right','top_target':self.xp_bar}, text = 'golds:0', manager=manager,
            object_id=ObjectID('#guide_text')
            )
        self.weapon_icons = [Weapon_icon(screen,manager,player,'weapon_icon',0), Weapon_icon(screen,manager,player,'weapon_icon',1), Weapon_icon(screen,manager,player,'weapon_icon',2), Weapon_icon(screen,manager,player,'weapon_icon',3)]
        self.buff_icons = [Buff_icon(screen,manager,player,'buff_icon',0), Buff_icon(screen,manager,player,'buff_icon',1), Buff_icon(screen,manager,player,'buff_icon',2), Buff_icon(screen,manager,player,'buff_icon',3)]
        self.weapons = 0
        self.buffs = 0
        self.weapon_icons[0].level_text.kill()
        #self.timer.set_text_scale(1)
        
        
    def update(self, time_elapsed,kill_counts,gold_counts):
        self.timer.set_text(f'{(int(time_elapsed // 60)):02d} : {(int(time_elapsed) % 60):02d}')
        self.kill_counter.set_text(f'kills:{kill_counts}')
        self.gold_counter.set_text(f'golds:{int(gold_counts)}')
        if self.weapons < len(self.player.weapons):
            self.weapon_icons[self.weapons] = Weapon_icon(self.screen,self.manager,self.player,self.player.weapons[self.weapons],self.weapons)
            self.weapons += 1
        if self.buffs < len(self.player.buffs):
            self.buff_icons[self.buffs] = Buff_icon(self.screen,self.manager,self.player,self.player.buffs[self.buffs],self.buffs)
            self.buffs += 1
        for i in range(len(self.player.weapons)):
            self.weapon_icons[i].update()
        for i in range(len(self.player.buffs)):
            self.buff_icons[i].update()

    def kill(self):
        self.timer.kill()
        self.hp_bar.kill()
        self.xp_bar.kill()
        self.kill_counter.kill()
        self.gold_counter.kill()
        for i in range(len(self.player.weapons)):
            self.weapon_icons[i].level_text.kill()
        for i in range(len(self.player.buffs)):
            self.buff_icons[i].level_text.kill()

    def draw(self,screen):
            for icon in self.weapon_icons:
                icon.show(screen)
            for icon in self.buff_icons:
                icon.show(screen)

