import pygame
from pygame.locals import * # CONSTS
from .config import width,height
from random import randrange, random
from numpy import array 
from numpy.linalg import norm
from abc import ABCMeta, abstractmethod
import configparser
import sys
from bisect import bisect

eneny_config = configparser.ConfigParser()
eneny_config.read('./data/config/enemy.ini')

def str_to_class(classname):
    return getattr(sys.modules[__name__], classname)

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

    def __init__(self, player):
        super().__init__()
        self.player = player

    def death(self) -> Drop : #return drop
        self.kill()
        drops = []
        drops.append(Xporb(self.pos, self.player))
        return drops


    def update(self, dt):
        if self.hp <= 0:
            return self.death()
        
        drct = self.player.pos-self.pos
        drct /= norm(drct)
        self.pos += self.speed*dt*drct
        self.rect.center = self.pos
        return [] #for compability

    def avoid(self, knockback=20):
        drct = self.pos - self.player.pos
        drct /= norm(drct)
        self.pos += drct*knockback

    @staticmethod
    def nearest_enemy(player_pos, enemies):
        if not enemies : return None
        return min(enemies, key=lambda enemy: norm(enemy.pos-player_pos))
    
        
    
    
class Polarbear(Enemy):
    config:dict = eneny_config['Polarbear']
    atk = float(config['atk'])
    max_hp = float(config['max_hp'])
    speed = float(config['speed'])
    amr = float(config['amr'])
    width = int(config['width'])
    height = int(config['height'])
    
    
    def __init__(self, pos, player):
        super().__init__(player)
        self.image = pygame.Surface([self.width, self.height])
        self.image.fill("#ff0000")
        self.rect = self.image.get_rect()
        self.pos = array(pos)

        self.hp = self.max_hp

class Spawner():
    def __init__(self):
        self.spawn_period = 3
        self.timer = self.spawn_period
        self.spawn_lookup = [(int(i[0]),str_to_class(i[1])) for i in eneny_config.items('spawn_lookup')] #set types
        
    def update_period(self, period):
        self.spawn_period = period
    
    def spawn(self, time_elapsed, dt, player, amount):
        #need lots further modify    
        self.timer -= dt
        if self.timer > 0 : return []
        self.timer = self.spawn_period
        
        spawn_type = self.spawn_lookup[bisect(self.spawn_lookup, (time_elapsed,))][1]
        enemies = []
        
        spawn_center_pos = array((random()*width, random()*height))
        while norm(spawn_center_pos-player.pos) < 250 : #do while
            spawn_center_pos = array((random()*width, random()*height), dtype=float)    
            
        for i in range(amount):
            spawn_pos = spawn_center_pos + array((random()*50, random()*50), dtype=float)
            enemies.append(spawn_type(spawn_pos, player))

        return enemies            
