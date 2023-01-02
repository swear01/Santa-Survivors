from configparser import ConfigParser, ExtendedInterpolation

import pygame
from numpy import array
from numpy.linalg import norm
from pygame.locals import *  # CONSTS
import json

from .weapon import *
from .buff import type_buff


player_config = ConfigParser(interpolation=ExtendedInterpolation())
player_config.read('./data/config/player.ini')

input_binds = ConfigParser(interpolation=ExtendedInterpolation())
input_binds.read('./data/config/input_binding.ini')
key_binds = {} #final use objects
key_map = vars()
for option, key_texts in input_binds.items('keyboard'):
    keys = [key_map[f'K_{key_text}'] for key_text in json.loads(key_texts)]
    key_binds[option] = keys

class Player(pygame.sprite.Sprite):
    max_weapons = int(player_config['common']['max_weapons'])
    max_buffs = int(player_config['common']['max_buffs'])
    scroll = int(player_config['common']['scroll'])
    xp_a = float(player_config['common']['xp_a'])
    xp_b = float(player_config['common']['xp_b'])

    def __init__(self, name, pos, backend, weapon_list, enemies):
        super().__init__()
        self.name = name
        self.backend = backend
        self.enemies = enemies
        self.config = player_config[self.name]
        self.visible = True
        self.images = [pygame.image.load(path).convert_alpha() for path in self.config['img_dirs'].split('\n')]
        self.images = [{'left':image, 'right':pygame.transform.flip(image, True, False)} for image in self.images]
        self.image = self.images[0]['left']
        self.width, self.height = self.image.get_size()
        self.rect = self.image.get_rect()
        self.pos = array(pos, dtype='float64')
        self.movable_dir = ['left', 'right', 'down', 'up']
        self.weapons = [weapon_list[self.config['init_weapon']](self)]
        self.buffs = []
        self.base = {'atk':float(self.config['atk']),
                'hp':float(self.config['hp']),
                'speed':float(self.config['speed']),
                'hp_r':float(self.config['hp_r'])}

        self.ratio = {} #where others get value
        self.calc_stats()
        self.hp = self.max_hp
        self.drct = 'left'        
        self.absorb_range = float(self.config['absorb_range'])
        self.xp = 0
        self.level = 0
        self.enemy_killed = 0
        self.gold_obtained = 0 

    def move(self, keys, dt):
        vec = array((0,0))
        drct_map = {'up':(0,-1),'down':(0,1),'left':(-1,0),'right':(1,0)}
        for direction in ['up','down','left','right']:
            if direction not in self.movable_dir : continue
            for key_bind in key_binds[direction]:
                if keys[key_bind] :
                    vec += drct_map[direction]
                    break

        if norm(vec) == 0 : return
        vec = vec/norm(vec)
        self.pos += vec*self.speed*dt

        if vec[0] > 0 : self.drct = 'right'
        if vec[0] < 0 : self.drct = 'left'



    def update(self, keys, time_elapsed, dt):
        if self.xp > self.xp_to_next_level(self.level):
            self.upgrade()
        if self.hp <= 0:
            self.backend.game_over = True

        self.move(keys, dt)
        self.image = self.images[int(time_elapsed+0.5) % len(self.images)][self.drct]

        #update stats
        self.hp += self.hp_r * dt
        self.hp = min(self.hp, self.max_hp)

        self.rect.center = self.pos #self.rect.center is tuple 
        self.mask = pygame.mask.from_surface(self.image)

    def upgrade(self):
        self.xp -= self.xp_to_next_level(self.level)
        self.level += 1
        self.backend.upgrade = True
        
    def get_health_percent(self):
        return self.hp/self.max_hp

    def get_xp_percent(self):
        return self.xp/self.xp_to_next_level(self.level)

    def shift_pos(self, background, screen_xy, *shift_objs_list):
        scroll_x, scroll_y = 0, 0
        if self.pos[0] < self.scroll :
            scroll_x = self.scroll - self.pos[0]
        if self.pos[0] > screen_xy[0] - self.scroll :
            scroll_x = screen_xy[0] - self.scroll - self.pos[0]
        if self.pos[1] < self.scroll :
            scroll_y = self.scroll - self.pos[1]  
        if self.pos[1] > screen_xy[1] - self.scroll :
            scroll_y = screen_xy[1] - self.scroll - self.pos[1] 

        if scroll_x == 0 and scroll_y == 0 : return

        background.pos += (scroll_x,scroll_y)

        self.pos += (scroll_x,scroll_y)

        for shift_objs in shift_objs_list:
            for shift_obj in shift_objs:
                shift_obj.pos += (scroll_x, scroll_y)

        return

    @classmethod
    def xp_to_next_level(cls, level):
        return int(cls.xp_a*(level+1)**cls.xp_b)

    def calc_stats(self):
        for key in type_buff.keys():
            self.ratio[key] = 1
        for key, value in self.base.items():
            self.ratio[key] *= value
        for buff in self.buffs:
            self.ratio[buff.type] *= (1+buff.effect)*buff.level

        self.max_hp = self.ratio['hp']
        self.hp_r = self.ratio['hp_r']
        self.speed = self.ratio['speed']
        return

    def nearest_enemy(self):
        if not self.enemies : return None
        return min(self.enemies, key=lambda enemy: norm(enemy.pos-self.pos))