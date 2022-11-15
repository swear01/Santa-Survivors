import pygame
from pygame.locals import * # CONSTS
from weapon import Weapon

class Player(pygame.sprite.Sprite):
    MAX_WEAPONS = 6
    MAX_UPGRADES = 6

    def __init__(self, pos=[0,0], visible=True,
    atk=1, amr=0, max_hp=10, hp_r=0):
        super().__init__()
        self.visible = visible 
        self.image = pygame.Surface([50,50])
        self.image.fill("#ffff00")
        self.rect = self.image.get_rect()
        self.rect.center = pos

        self.weapons: List[Weapon] = []
        self.upgrades = []
       
        
        self.atk = atk
        self.amr = amr
        self.max_hp = max_hp
        self.hp = max_hp
        self.hp_r = hp_r

    def move(self, drct):
        if drct == 'up':
            self.rect.center = (self.rect.center[0],self.rect.center[1]-1)

        if drct == 'down':
            self.rect.center = (self.rect.center[0],self.rect.center[1]+1)

        if drct == 'left':
            self.rect.center = (self.rect.center[0]-1,self.rect.center[1])

        if drct == 'right':
            self.rect.center = (self.rect.center[0]+1,self.rect.center[1])

