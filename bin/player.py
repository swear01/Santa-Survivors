from configparser import ConfigParser, ExtendedInterpolation

import pygame
from numpy import array
from pygame.locals import *  # CONSTS

from .weapon import Weapon

player_config = ConfigParser(interpolation=ExtendedInterpolation())
player_config.read('./data/config/player.ini')

class Player(pygame.sprite.Sprite):
    max_weapons = player_config['common']['max_weapons']
    max_buffs = player_config['common']['max_buffs']

    def __init__(self, name, pos, backend):
        super().__init__()
        self.name = name
        self.backend = backend
        self.config = player_config[self.name]
        self.visible = True
        self.images = [pygame.image.load(path).convert_alpha() for path in self.config['img_dirs'].split('\n')]
        self.images = [{'left':image, 'right':pygame.transform.flip(image, True, False)} for image in self.images]
        self.image = self.images[0]['left']
        self.width, self.height = self.image.get_size()
        self.rect = self.image.get_rect()
        self.pos = array(pos, dtype='float64')
        self.weapons: list[Weapon] = []
        self.buffs = []
       

        self.drct = 'left'        
        self.atk_ratio = float(self.config['atk_ratio'])
        self.max_hp = float(self.config['init_health'])
        self.hp = self.max_hp
        self.hp_r = float(self.config['hp_r'])
        self.speed = float(self.config['speed'])
        self.absorb_range = float(self.config['absorb_range'])
        self.xp = 0
        self.level = 0
        self.enemy_killed = 0
        self.gold_obtained = 0 

        # do this for health_bar work properly
        self.health_capacity = self.max_hp
        self.current_health = self.hp


    def move(self, drct, dt):
        if drct == 'up':
            self.pos[1] -= self.speed*dt

        if drct == 'down':
            self.pos[1] += self.speed*dt

        if drct == 'left':
            self.pos[0] -= self.speed*dt

        if drct == 'right':
            self.pos[0] += self.speed*dt
    
    def turn(self, drct):
        if drct == 'left':
            self.image = self.image_ori
        if drct == 'right':
            self.image = pygame.transform.flip (self.image_ori,False,True)

    def turn(self, drct):
        self.drct = drct

    def update(self, time_elapsed, dt):
        if self.xp > self.xp_to_next_level(self.level):
            self.upgrade()
        if self.hp <= 0:
            self.backend.game_over = True
        self.rect.center = self.pos #self.rect.center is tuple 
        self.image = self.images[int(time_elapsed+0.5) % len(self.images)][self.drct]



        # do this for health_bar work properly
        self.health_capacity = self.max_hp
        self.current_health = self.hp

    def upgrade(self):
        self.xp -= self.xp_to_next_level(self.level)
        self.level += 1
        self.backend.upgrade = True
        
    def get_health_percent(self):
        return self.hp/self.max_hp

    def get_xp_percent(self):
        return self.xp/self.xp_to_next_level(self.level)

    @staticmethod
    def xp_to_next_level(level):
        return int(10*(level+1)**1.3)