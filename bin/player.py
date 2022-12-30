import pygame
from numpy import array
from pygame.locals import *  # CONSTS

from .weapon import Weapon


class Player(pygame.sprite.Sprite):
    MAX_WEAPONS = 6
    MAX_UPGRADES = 6

    def __init__(self, pos=[0,0], visible=True,
    atk=1, amr=0, max_hp=10, hp_r=0, speed=50, absorb_range = 50,backend=None):
        super().__init__()
        self.visible = visible 
        self.image_ori = pygame.Surface([35,35])
        self.image_ori.fill("#ffff00")
        self.image = self.image_ori.copy()
        self.rect = self.image.get_rect()
        self.pos = array(pos, dtype='float64')
        self.backend = backend
        self.weapons: list[Weapon] = []
        self.upgrades = []
       
        self.drct = 'left'        
        self.atk = atk
        self.amr = amr
        self.max_hp = max_hp
        self.hp = max_hp
        self.hp_r = hp_r
        self.speed = speed+150
        self.xp = 0
        self.level = 0
        self.absorb_range = absorb_range
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

    def update(self, dt):
        if self.xp > self.xp_to_next_level(self.level):
            self.upgrade()
        if self.hp <= 0:
            self.backend.game_over = True
        self.rect.center = self.pos #self.rect.center is tuple 

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
        return int(10*(level+1)**1.5)