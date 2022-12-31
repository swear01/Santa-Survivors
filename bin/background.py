import pygame
from pygame.locals import *  # CONSTS
from math import floor
from numpy import array


class Background():
    def __init__(self):
        self.image = pygame.image.load('./data/backgrounds/tileable_background1.jpg').convert()
        self.pos = array((0,0), dtype=float) #relative displacement
        self.width, self.height = self.image.get_size()

    def draw(self, screen):
        start_x = floor(self.pos[0]) % self.width - self.width
        start_y = floor(self.pos[1]) % self.height - self.height
        
        for x in range(start_x, 2*self.width, self.width):
            for y in range(start_y, 2*self.height, self.height):
                screen.blit(self.image, (x,y))

        

