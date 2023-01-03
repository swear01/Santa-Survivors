import sys
from abc import ABCMeta, abstractmethod
from bisect import bisect_right
from configparser import ConfigParser, ExtendedInterpolation
from random import random, uniform
from math import pi, cos, sin

import json
import pygame
from numpy import array
from numpy.linalg import norm
from pygame.locals import *  # CONSTS

from .config import height, width

eneny_config = ConfigParser(interpolation=ExtendedInterpolation())
eneny_config.read('./data/config/enemy.ini')

def str_to_class(classname):
    return getattr(sys.modules[__name__], classname)

def out_of_screen(pos):
    return pos[0] > width+100 or pos[0] < -100 or pos[1] > height+100 or pos[1] < -100 

def scale(image, ratio):
    return pygame.transform.scale(image, array(image.get_size())*ratio)

class Drop(pygame.sprite.Sprite, metaclass=ABCMeta):
    def __init__(self, name, pos, player):
        super().__init__()
        self.name = name
        config = eneny_config[self.name]
        self.image = pygame.image.load(config['img_dir']).convert_alpha()
        self.rect = self.image.get_rect()
        self.pos = pos
        self.player = player
        
    def update(self, dt):
        if norm(self.pos-self.player.pos) <= self.player.absorb_range :
            dist = norm(self.pos-self.player.pos)
            drct = (self.player.pos-self.pos)/dist
            self.pos += 100*self.player.absorb_range/dist*drct*dt
        self.rect.center = self.pos

class Xporb(Drop):
    def __init__(self, pos, player, xp):
        super().__init__('Xporb', pos, player)
        self.xp = xp
        
    def absorbed(self):
        self.kill()
        self.player.xp += self.xp*self.player.ratio['xp']
    
class Gold(Drop):
    def __init__(self, pos, player, gold):
        super().__init__('Gold', pos, player)
        self.gold = gold
        
    def absorbed(self):
        self.kill()
        self.player.gold += self.gold*self.player.ratio['gold']

class Enemy(pygame.sprite.Sprite, metaclass=ABCMeta):

    def __init__(self, name, pos, player):
        super().__init__()
        self.player = player
        self.name = name
        self.config:dict = eneny_config[self.name]
        self.atk = float(self.config['atk'])
        self.max_hp = float(self.config['max_hp'])
        self.speed = float(self.config['speed'])
        self.xp = float(self.config['xp'])
        self.images = [pygame.image.load(path).convert_alpha() for path in self.config['img_dirs'].split('\n')]
        self.image = self.images[0]
        self.rect = self.image.get_rect()
        self.pos = array(pos)
        self.rect.center = self.pos
        self.hp = self.max_hp
        #images = [img.subsurface(img.get_bounding_rect()) for img in images] #if images have transparent skirts

    def if_death(self) -> Drop:
        if self.hp > 0 : return []
        return self.death()

    def death(self) -> Drop : #return drop
        self.kill()
        self.player.enemy_killed += 1
        drops = []
        drops.append(Xporb(self.pos.copy(), self.player, self.xp))
        if random() < 0.1 :
            pos = self.pos + array((random(),random()))*30
            drops.append(Gold(pos, self.player, 1))
        return drops


    def update(self, time_elapsed, dt):
        drct = self.player.pos-self.pos
        drct /= norm(drct)
        self.pos += self.speed*dt*drct
        self.rect.center = self.pos
        
        #animations
        self.image = self.images[int(time_elapsed) % len(self.images)]
        return [] #for compability

    def avoid(self, knockback=200):
        drct = self.pos - self.player.pos
        drct =  drct / norm(drct)
        self.pos += drct*knockback

    
        
    
    
class Polarbear(Enemy):
    def __init__(self, pos, player):
        super().__init__('Polarbear', pos, player)
        
class Brownbear(Enemy):
    def __init__(self, pos, player):
        super().__init__('Brownbear', pos, player)

class Kid1(Enemy):
    def __init__(self, pos, player):
        super().__init__('Kid1', pos, player)
        
class Kid2(Enemy):
    def __init__(self, pos, player):
        super().__init__('Kid2', pos, player)
        
class Kid3(Enemy):
    def __init__(self, pos, player):
        super().__init__('Kid3', pos, player)
        
class Kid4(Enemy):
    def __init__(self, pos, player):
        super().__init__('Kid4', pos, player) 
class Seal(Enemy):
    def __init__(self, pos, player):
        super().__init__('Seal', pos, player)
        config = eneny_config[self.name]
        self.dash_period = float(config['dash_period'])
        self.dash_speed = float(config['dash_speed'] )
        self.timer = self.dash_period

    def update(self, time_elapsed, dt):
        self.timer -= dt
        if self.timer <= 0.2:
            if self.timer <= 0:
                self.timer += self.dash_period
            else:
                drct = self.player.pos-self.pos
                drct /= norm(drct)
                self.pos += self.speed*drct*self.dash_speed*dt
        return super().update(time_elapsed, dt)

class Candy(Enemy):
    #images = [img.subsurface(img.get_bounding_rect()) for img in images] #if images have transparent skirts
    
    def __init__(self, pos, player):
        super().__init__('Candy', pos, player)
        self.image = self.images[0]
        self.drct = self.player.pos-self.pos 
        self.drct /= norm(self.drct)   
        
    def update(self, time_elapsed, dt):
        self.image = self.images[int(time_elapsed*4) % len(self.images)]
        self.pos += self.speed*dt*self.drct
        self.rect.center = self.pos
        return []

    def if_death(self) -> Drop:
        if self.hp <= 0 : return self.death()
        if out_of_screen(self.pos) : return self.death()
        return []

    def death(self) -> Drop : #return drop
        self.kill()
        return []  

    def avoid(self):
        self.death()

class Tree(Enemy):
    def __init__(self, pos, player):
        super().__init__('Tree', pos, player)
        self.shoot_period = float(self.config['shoot_period'])
        self.shoot_timer = self.shoot_period/2
                
    def update(self, time_elapsed, dt):
        self.image = self.images[int(time_elapsed) % len(self.images)]
        self.shoot_timer -= dt
        if self.shoot_timer > 0 : return []
        self.shoot_timer += self.shoot_period
        return Candy(self.pos, self.player)
    
class Snowman_ball(Enemy):
    #images = [img.subsurface(img.get_bounding_rect()) for img in images] #if images have transparent skirts
    def __init__(self, pos, player):
        super().__init__('Snowman_ball', pos ,player)
        self.drct = self.player.pos-self.pos 
        self.drct /= norm(self.drct)   
        
    def update(self, time_elapsed, dt):
        self.pos += self.speed*dt*self.drct
        self.rect.center = self.pos
        return []

    def if_death(self) -> Drop:
        if self.hp <= 0 : return self.death()
        if out_of_screen(self.pos) : return self.death()
        return []

    def death(self) -> Drop : #return drop
        self.kill()
        return []  

    def avoid(self):
        self.death()
        
class Snowman(Enemy):
    #images = [img.subsurface(img.get_bounding_rect()) for img in images] #if images have transparent skirts
    
    def __init__(self, name, pos, player):
        super().__init__(name, pos, player)
        self.shoot_period = float(self.config['shoot_period'])
        self.shoot_timer = self.shoot_period   
        
    def update(self, time_elapsed, dt):
        super().update(time_elapsed, dt)
        self.shoot_timer -= dt
        if self.shoot_timer > 0 : return []
        self.shoot_timer += self.shoot_period
        return Snowman_ball(self.pos, self.player)

class Snowman1(Snowman):
    def __init__(self, pos, player):
        super().__init__('Snowman1', pos, player)
        
class Snowman2(Snowman):
    def __init__(self, pos, player):
        super().__init__('Snowman2', pos, player)     
class Rick(Enemy):
    def __init__(self, name, pos, player):
        super().__init__(name, pos, player)
        self.player.movable_dir = ['left','right']

    def update(self, time_elapsed, dt):
        self.pos[1] = self.player.pos[1]
        return super().update(time_elapsed, dt)

    def death(self) -> Drop:
        self.player.movable_dir = ['left','right', 'up', 'down']
        return super().death()

class Rick1(Rick):
    def __init__(self, pos, player):
        super().__init__('Rick1', pos, player)
        
class Rick2(Rick):
    def __init__(self, pos, player):
        super().__init__('Rick2', pos, player)

class Rick3(Rick):
    def __init__(self, pos, player):
        super().__init__('Rick3', pos, player)

class Rick4(Rick):
    def __init__(self, pos, player):
        super().__init__('Rick4', pos, player)

class Spawner():
    def __init__(self, player):
        config = eneny_config['spawner']
        self.base_spawn_period = float(config['base_spawn_period'])
        self.spawn_range = json.loads(config['spawn_range'])
        self.timer = 0
        self.boss_lookup = [(int(i[0]),str_to_class(i[1])) for i in eneny_config.items('boss_lookup')]
        self.next_boss_index = 0
        self.spawn_lookup = [(i[0],i[2],str_to_class(i[1])) for i in json.loads(config['spawn_lookup'])] #set types
        self.player = player
        
    def spawn_period(self):
        return self.base_spawn_period*self.player.ratio['enemy_period']*uniform(0.5,1.5)
    
    def spawn_boss(self):
        spawn_pos = array((random()*width, random()*height))
        while norm(spawn_pos-self.player.pos) < 700 : #do while
            spawn_pos = array((random()*width, random()*height), dtype=float)  
        spawn_type = self.boss_lookup[self.next_boss_index][1] 
        self.next_boss_index += 1   
        return [spawn_type(spawn_pos, self.player)]
                 

    def spawn(self, time_elapsed, dt):
        #need lots further modify    
        self.timer -= dt
        #spawn boss
        if self.boss_lookup[self.next_boss_index][0] <= time_elapsed :
            return self.spawn_boss()
        if self.timer > 0 : return []
        self.timer = self.spawn_period()
        this_spawn = self.spawn_lookup[bisect_right(self.spawn_lookup, (time_elapsed,))-1]
        amount, spawn_type = this_spawn[1], this_spawn[2]
        enemies = []
        
        spawn_dist, spawn_angle = uniform(*self.spawn_range), uniform(0, 2*pi)
        spawn_center_pos = self.player.pos + array((spawn_dist*cos(spawn_angle),spawn_dist*sin(spawn_angle)))
            
        for i in range(amount):
            spawn_pos = spawn_center_pos + array((random(), random()), dtype=float)*200
            enemies.append(spawn_type(spawn_pos, self.player))

        return enemies            
