import pygame
from pygame.locals import * # CONSTS
from math import cos, sin, pi, dist
from numpy import array
from numpy.linalg import norm
from .enemy import Enemy

BULLET_MAX_DIST = 400

class Weapon:
    def __init__(self, name, player, 
        atk=10, reload=1, b_speed=70, b_hp=1,b_amt=1):
        self.name = name
        self.player = player
        self.cooldown = reload
        self.reload = reload
        self.atk = atk
        self.b_speed = b_speed
        self.b_hp = b_hp
        self.b_amt = b_amt


    def shoot(self, pos, enemies):
        if self.name == 'test':
            bullets = pygame.sprite.Group()
            for i in range(self.b_amt):
                angle = 2*i*pi/self.b_amt
                vec = (self.b_speed*cos(angle),self.b_speed*sin(angle))
                bullets.add(Bullet(pos, vec, self.player, color='#0000ff', hp=self.b_hp, atk=self.atk, kind='normal'))
            return bullets

        if self.name == 'autoaim':
            if not enemies : return []
            nearest_enemy = Enemy.nearest_enemy(pos, enemies)
            vec = nearest_enemy.pos-self.player.pos
            vec *= self.b_speed/norm(vec)
            return Bullet(pos, vec, self.player, color='#ff00ff', hp=self.b_hp, atk=self.atk, kind='autoaim')
            

class Bullet(pygame.sprite.Sprite):
    def __init__(self,pos, vec, player, color,
        hp, atk, kind):
        super().__init__()
        self.image = pygame.Surface([8,8])
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.player = player
        self.pos = array(pos, dtype='float64')
        self.vec = array(vec, dtype='float64') 
        self.kind = kind
        
        self.hp = hp # hp is how many enemies can the bullet hit
        self.atk = atk

    def update(self, dt):
        if dist(self.pos, self.player.pos) > 300 :
            self.kill()
            return
        if self.hp == 0 : 
            self.kill()
            return
        self.pos += self.vec*dt
        self.rect.center = self.pos

