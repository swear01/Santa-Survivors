import sys
from abc import ABCMeta, abstractmethod
from bisect import bisect_right
from configparser import ConfigParser, ExtendedInterpolation
from random import random, randrange

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

class Drop(pygame.sprite.Sprite, metaclass=ABCMeta):
    def __init__(self, pos, player):
        super().__init__()
        self.image = pygame.Surface([6,6])
        self.image.fill("#ffff00")
        self.rect = self.image.get_rect()
        self.pos = array(pos)
        self.player = player
        
    @abstractmethod
    def update(self):
        pass

class Xporb(Drop):
    def __init__(self, pos, player, xp=1):
        super().__init__(pos, player)
        self.xp = xp
        
    def update(self, dt):
        if norm(self.pos-self.player.pos) < self.player.absorb_range :
            dist = norm(self.pos-self.player.pos)
            drct = (self.player.pos-self.pos)/dist
            self.pos += 3000/dist*drct*dt
        self.rect.center = self.pos
        
    def absorbed(self):
        self.kill()
        self.player.xp += self.xp
    

class Enemy(pygame.sprite.Sprite, metaclass=ABCMeta):

    def __init__(self, name, pos, player):
        super().__init__()
        self.player = player
        self.name = name
        self.config:dict = eneny_config[self.name]
        self.atk = float(self.config['atk'])
        self.max_hp = float(self.config['max_hp'])
        self.speed = float(self.config['speed'])
        #self.width = int(config['width'])
        #self.height = int(config['height'])
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
        drops.append(Xporb(self.pos, self.player))
        return drops


    def update(self, time_elapsed, dt):
        drct = self.player.pos-self.pos
        drct /= norm(drct)
        self.pos += self.speed*dt*drct
        self.rect.center = self.pos
        
        #animations
        self.image = self.images[int(time_elapsed) % len(self.images)]
        return [] #for compability

    def avoid(self, knockback=20):
        drct = self.pos - self.player.pos
        drct /= norm(drct)
        self.pos += drct*knockback

    
        
    
    
class Polarbear(Enemy):
    def __init__(self, pos, player):
        super().__init__('Polarbear', pos, player)

     
class Snowman_ball(Enemy):
    #images = [img.subsurface(img.get_bounding_rect()) for img in images] #if images have transparent skirts
    
    
    def __init__(self, pos, player):
        super().__init__('Snowman_ball', pos ,player)
        self.image = pygame.transform.scale(self.images[0], (int(self.config['width']), int(self.config['height'])))
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
    
    def __init__(self, pos, player):
        super().__init__('Snowman',pos,player)
        self.shoot_period = float(self.config['shoot_period'])
        self.shoot_timer = self.shoot_period   
        
    def update(self, time_elapsed, dt):
        super().update(time_elapsed, dt)
        self.shoot_timer -= dt
        if self.shoot_timer > 0 : return []
        self.shoot_timer += self.shoot_period
        return Snowman_ball(self.pos, self.player)
        
class Rick(Enemy):
    def __init__(self, pos, player):
        super().__init__('Rick', pos, player)
        self.player.movable_dir = ['left','right']

    def update(self, time_elapsed, dt):
        self.pos[1] = self.player.pos[1]
        return super().update(time_elapsed, dt)

    def death(self) -> Drop:
        self.player.movable_dir = ['left','right', 'up', 'down']
        return super().death()

class Spawner():
    def __init__(self):
        config = eneny_config['spawner']
        self.base_spawn_period = float(config['base_spawn_period'])
        self.timer = 0
        self.boss_lookup = [(int(i[0]),str_to_class(i[1])) for i in eneny_config.items('boss_lookup')]
        self.next_boss_index = 0
        self.spawn_lookup = [(int(i[0]),str_to_class(i[1])) for i in eneny_config.items('spawn_lookup')] #set types
        
    def spawn_period(self, player):
        return self.base_spawn_period
    
    def spawn_boss(self, player):
        spawn_pos = array((random()*width, random()*height))
        while norm(spawn_pos-player.pos) < 700 : #do while
            spawn_pos = array((random()*width, random()*height), dtype=float)  
        spawn_type = self.boss_lookup[self.next_boss_index][1] 
        self.next_boss_index += 1   
        return [spawn_type(spawn_pos, player)]
                 

    def spawn(self, time_elapsed, dt, player, amount):
        #need lots further modify    
        self.timer -= dt
        #spawn boss
        if self.boss_lookup[self.next_boss_index][0] <= time_elapsed :
            return self.spawn_boss(player)
        if self.timer > 0 : return []
        self.timer = self.spawn_period(player)
        
        spawn_type = self.spawn_lookup[bisect_right(self.spawn_lookup, (time_elapsed,))-1][1]
        enemies = []
        
        spawn_center_pos = array((random()*width, random()*height))
        while norm(spawn_center_pos-player.pos) < 700 : #do while
            spawn_center_pos = array((random()*width, random()*height), dtype=float)    
            
        for i in range(amount):
            spawn_pos = spawn_center_pos + array((random(), random()), dtype=float)*200
            enemies.append(spawn_type(spawn_pos, player))

        return enemies            
