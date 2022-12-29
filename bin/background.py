import pygame
from pygame.locals import *  # CONSTS
from .config import width,height
from .player import Player

class Background(pygame.sprite.Sprite):
    def __init__(self, screen):
        self.map_image1 = pygame.image.load(filename = "C:\Users\user\Pictures\picture1.png") # 初始畫面
        self.map_image2 = pygame.image.load(filename = "C:\Users\user\Pictures\picture1.png") # 初始畫面的上方畫面
        self.map_image3 = pygame.image.load(filename = "C:\Users\user\Pictures\picture1.png") # 初始畫面的右方畫面
        self.map_image4 = pygame.image.load(filename = "C:\Users\user\Pictures\picture1.png")  # 初始畫面的下方畫面
        self.map_image5 = pygame.image.load(filename = "C:\Users\user\Pictures\picture1.png")  # 初始畫面的左方畫面

        self.screen = screen

        self.x1 = 0 # 初始畫面的座標
        self.y1 = 0
        self.x2 = 0  # 上方畫面的座標
        self.y2 = -height
        self.x3 = width  # 右方畫面的座標
        self.y3 = 0
        self.x4 = 0  # 下方畫面的座標
        self.y4 = height
        self.x5 = -width  # 左方畫面的座標
        self.y5 = 0

    def draw(self):
        self.screen.blit(self.map_image1,(self.x1, self.y1))
        self.screen.blit(self.map_image2,(self.x2, self.y2))
        self.screen.blit(self.map_image3,(self.x3, self.y3))
        self.screen.blit(self.map_image4,(self.x4, self.y4))
        self.screen.blit(self.map_image5,(self.x5, self.y5))

    def move(self):
        bound = 20  # 邊界
        if player.pos[0] <= bound:
            self.x1 -= width/2 - bound
            self.x2 -= width / 2 - bound
            self.x3 -= width / 2 - bound
            self.x4 -= width / 2 - bound
            self.x5 -= width / 2 - bound
        if player.pos[0] >= width - bound:
            self.x1 += width / 2 - bound
            self.x2 += width / 2 - bound
            self.x3 += width / 2 - bound
            self.x4 += width / 2 - bound
            self.x5 += width / 2 - bound
        if player.pos[1] <= bound:
            self.y1 -= height / 2 - bound
            self.y2 -= height / 2 - bound
            self.y3 -= height / 2 - bound
            self.y4 -= height / 2 - bound
            self.y5 -= height / 2 - bound
        if player.pos[1] >= height - bound:
            self.y1 += height / 2 - bound
            self.y2 += height / 2 - bound
            self.y3 += height / 2 - bound
            self.y4 += height / 2 - bound
            self.y5 += height / 2 - bound

