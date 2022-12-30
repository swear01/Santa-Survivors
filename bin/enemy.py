import pygame
from pygame.locals import * # CONSTS
from .config import width,height
from random import randrange, random
from numpy import array 
from numpy.linalg import norm
from abc import ABCMeta, abstractmethod
from configparser import ConfigParser, ExtendedInterpolation
import sys
from bisect import bisect

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

    def __init__(self, player):
        super().__init__()
        self.player = player

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

    @staticmethod
    def nearest_enemy(player_pos, enemies):
        if not enemies : return None
        return min(enemies, key=lambda enemy: norm(enemy.pos-player_pos))
    
        
    
    
class Polarbear(Enemy):
    config:dict = eneny_config['Polarbear']
    atk = float(config['atk'])
    max_hp = float(config['max_hp'])
    speed = float(config['speed'])
    width = int(config['width'])
    height = int(config['height'])
    images = [pygame.image.load(path).convert_alpha() for path in config['img_dirs'].split('\n')]
    #images = [img.subsurface(img.get_bounding_rect()) for img in images] #if images have transparent skirts
    
    
    def __init__(self, pos, player):
        super().__init__(player)
        self.image = self.images[0]
        self.rect = self.image.get_rect()
        self.pos = array(pos)

        self.hp = self.max_hp
     
class Snowman_ball(Enemy):
    config:dict = eneny_config['Snowman_ball']
    atk = float(config['atk'])
    max_hp = float(config['max_hp'])
    speed = float(config['speed'])
    width = int(config['width'])
    height = int(config['height'])
    images = [pygame.image.load(path).convert_alpha() for path in config['img_dirs'].split('\n')][0]
    images = pygame.transform.scale(images, (int(config['width']), int(config['height'])))
    #images = [img.subsurface(img.get_bounding_rect()) for img in images] #if images have transparent skirts
    
    
    def __init__(self, pos, player):
        super().__init__(player)
        self.image = self.images
        self.rect = self.image.get_rect()
        self.pos = array(pos)
        self.hp = self.max_hp
        self.drct = self.player.pos-self.pos 
        self.drct /= norm(self.drct)   
        
    def update(self, time_elapsed, dt):
        self.pos += self.speed*dt*self.drct
        self.rect.center = self.pos
        return []

    def if_death(self) -> Drop:
        if self.hp > 0 : return []
        if not out_of_screen(self.pos) : return []
        return self.death()

    def death(self) -> Drop : #return drop
        self.kill()
        return []  

    def avoid(self):
        self.death()
        
class Snowman(Enemy):
    config:dict = eneny_config['Snowman']
    atk = float(config['atk'])
    max_hp = float(config['max_hp'])
    speed = float(config['speed'])
    width = int(config['width'])
    height = int(config['height'])
    shoot_period = float(config['shoot_period'])
    images = [pygame.image.load(path).convert_alpha() for path in config['img_dirs'].split('\n')]
    #images = [img.subsurface(img.get_bounding_rect()) for img in images] #if images have transparent skirts
    
    
    def __init__(self, pos, player):
        super().__init__(player)
        self.image = self.images[0]
        self.rect = self.image.get_rect()
        self.pos = array(pos)
        self.shoot_timer = self.shoot_period
        self.hp = self.max_hp    
        
    def update(self, time_elapsed, dt):
        super().update(time_elapsed, dt)
        self.shoot_timer -= dt
        if self.shoot_timer > 0 : return []
        self.shoot_timer += self.shoot_period
        return Snowman_ball(self.pos, self.player)
        

class Spawner():
    def __init__(self):
        self.spawn_period = 3
        self.timer = 0
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
        while norm(spawn_center_pos-player.pos) < 700 : #do while
            spawn_center_pos = array((random()*width, random()*height), dtype=float)    
            
        for i in range(amount):
            spawn_pos = spawn_center_pos + array((random(), random()), dtype=float)*200
            enemies.append(spawn_type(spawn_pos, player))

        return enemies            
