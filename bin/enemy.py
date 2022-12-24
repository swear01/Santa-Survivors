import pygame
from pygame.locals import * # CONSTS
from .config import width,height
from random import randrange, random
from numpy import array 
from numpy.linalg import norm
from abc import ABCMeta, abstractmethod


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
    

class Enemy(pygame.sprite.Sprite):

    def __init__(self, pos, player,
        max_hp=10, atk=1, speed=20, amr=0):
        super().__init__()
        self.image = pygame.Surface([15,15])
        self.image.fill("#ff0000")
        self.rect = self.image.get_rect()
        self.pos = array(pos)
        self.player = player

        self.max_hp = max_hp
        self.hp = max_hp
        self.atk = atk
        self.speed = speed
        self.amr = amr

    def death(self) -> Drop : #return drop
        self.kill()
        drops = []
        drops.append(Xporb(self.pos, self.player))
        return drops


    def update(self, dt):
        if self.hp == 0:
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

    @classmethod
    def spawn_enemy(cls, player, type='test', amt=1):
        spawn_pos = (random()*width, random()*height)
        while norm(spawn_pos-player.pos) < 200 :
            # respawn if too near player
            spawn_pos = (random()*width, random()*height)            
        
        enemies = []
        for i in range(amt):
            enemies.append(Enemy(spawn_pos, player=player))

        return enemies

    @staticmethod
    def nearest_enemy(player_pos, enemies):
        return min(enemies, key=lambda enemy: norm(enemy.pos-player_pos))
    
