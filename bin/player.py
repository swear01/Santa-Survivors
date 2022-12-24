import pygame
from pygame.locals import * # CONSTS
from .weapon import Weapon
from numpy import array

class Player(pygame.sprite.Sprite):
    MAX_WEAPONS = 6
    MAX_UPGRADES = 6

    def __init__(self, pos=[0,0], visible=True,
    atk=1, amr=0, max_hp=10, hp_r=0, speed=50):
        super().__init__()
        self.visible = visible 
        self.image = pygame.Surface([35,35])
        self.image.fill("#ffff00")
        self.rect = self.image.get_rect()
        self.pos = array(pos, dtype='float64')

        self.weapons: list[Weapon] = []
        self.upgrades = []
       
        
        self.atk = atk
        self.amr = amr
        self.max_hp = max_hp
        self.hp = max_hp
        self.hp_r = hp_r
        self.speed = speed
        self.xp = 0
        self.level = 0

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

    def update(self, dt):
        if self.xp > self.xp_to_next_level(self.level):
            self.upgrade()
        self.rect.center = self.pos #self.rect.center is tuple 

        # do this for health_bar work properly
        self.health_capacity = self.max_hp
        self.current_health = self.hp

    def upgrade(self):
        self.xp -= self.xp_to_next_level(self.level)
        self.level += 1

    def get_health_percent(self):
        return self.hp/self.max_hp

    def get_xp_percent(self):
        return self.xp/self.xp_to_next_level(self.level)

    @staticmethod
    def xp_to_next_level(level):
        return int(10*(level+1)**1.5)