from configparser import ConfigParser, ExtendedInterpolation

import pygame
import pygame_gui
from pygame.locals import *  # CONSTS
from pygame_gui.core import ObjectID

config = ConfigParser(interpolation=ExtendedInterpolation())
config.read('./data/config/huds.ini')

class Huds:
    def __init__(self, manager, width, height, player):
        self.manager = manager
        self.player = player
        xp_bar_width = width-2*int(config['xp_bar']['margin'])
        
        self.xp_bar = pygame_gui.elements.UIStatusBar(
            relative_rect=pygame.Rect(
                int(config['xp_bar']['margin']),int(config['xp_bar']['margin']),xp_bar_width,int(config['xp_bar']['height'])), 
            manager=manager,
            sprite=player, follow_sprite=False, anchors={'top':'top', 'left':'left'},
            percent_method=player.get_xp_percent ,object_id=ObjectID('#xp_bar','@player_bar'))
        self.xp_bar.status_text = lambda : f'Level {player.level}'
            
        self.hp_bar = pygame_gui.elements.UIStatusBar(relative_rect=(0,0,int(config['hp_bar']['width']),int(config['hp_bar']['height'])), 
            manager=manager,
            sprite=player, follow_sprite=True, anchors={},
            percent_method=player.get_health_percent, object_id=ObjectID('#hp_bar','@player_bar'))

        self.timer = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect(0,0,int(config['timer']['width']),int(config['timer']['height'])),
            anchors={'centerx':'centerx','top_target':self.xp_bar}, text = '00 : 00', manager=manager,
            object_id=ObjectID('#timer')
            )

        self.kill_counter = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect(-250,0,int(config['kill_counter']['width']),int(config['kill_counter']['height'])),
            anchors={'right':'right','top_target':self.xp_bar}, text = 'kills:0', manager=manager,
            object_id=ObjectID('#kill_counter')
            )
        #self.timer.set_text_scale(1)
        
        
    def update(self, time_elapsed,kill_counts):
        self.timer.set_text(f'{(int(time_elapsed // 60)):02d} : {(int(time_elapsed) % 60):02d}')
        self.kill_counter.set_text(f'kills:{kill_counts}')
    
    def kill(self):
        self.timer.kill()
        self.hp_bar.kill()
        self.xp_bar.kill()
        self.kill_counter.kill()
        self.kill_counter = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect(100,400,int(config['kill_counter']['width']),int(config['kill_counter']['height'])),
             text = f'kills:{self.player.enemy_killed}', manager=self.manager,
            object_id=ObjectID('#kill_counter')
            )
        