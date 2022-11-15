import pygame
from pygame.locals import * # CONSTS
from math import cos, sin, pi

BULLET_MAX_DIST = 400

class Weapon:
    def __init__(self, name, reload=1, dmg=1, b_speed=2):
        self.name = name
        self.cooldown = reload
        self.reload = reload
        self.dmg = dmg
        self.b_speed = b_speed


    def shoot(self, pos):
        if self.name == 'test':
            bullets = []
            for i in range(8):
                vec = (self.b_speed*cos(i/4*pi),self.b_speed*sin(i/4*pi))
                bullets.append(Bullet(pos, vec))
            return bullets



class Bullet(pygame.sprite.Sprite):
    def __init__(self,pos,vec):
        super().__init__()
        self.image = pygame.Surface([5,5])
        self.image.fill("#0000ff")
        self.rect = self.image.get_rect()
        self.rect.center = pos
        self.vec = vec

    def update(self):
        self.rect.center = self.rect.center+self.vec

