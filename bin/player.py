import pygame
from pygame.locals import * # CONSTS
from .weapon import Weapon
from .config import fps
from numpy import array
class Player(pygame.sprite.Sprite):
    MAX_WEAPONS = 6
    MAX_UPGRADES = 6

    def __init__(self, pos=[0,0], visible=True,
    atk=1, amr=0, max_hp=10, hp_r=0, speed=50):
        super().__init__()
        self.visible = visible 
        self.image = pygame.Surface([50,50])
        self.image.fill("#ffff00")
        self.rect = self.image.get_rect()
        self.pos = array(pos, dtype='float64')

        self.weapons: List[Weapon] = []
        self.upgrades = []
       
        
        self.atk = atk
        self.amr = amr
        self.max_hp = max_hp
        self.hp = max_hp
        self.hp_r = hp_r
        self.speed = speed

    def move(self, drct):
        global fps
        if drct == 'up':
            self.pos[1] -= 1/fps*self.speed

        if drct == 'down':
            self.pos[1] += 1/fps*self.speed

        if drct == 'left':
            self.pos[0] -= 1/fps*self.speed

        if drct == 'right':
            self.pos[0] += 1/fps*self.speed

    def update(self):
        self.rect.center = self.pos #self.rect.center is tuple 