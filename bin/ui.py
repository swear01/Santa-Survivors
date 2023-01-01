import os
from abc import ABCMeta, abstractmethod
from random import random, randrange

import pygame
import pygame_gui
from numpy import array
from numpy.linalg import norm
from pygame.locals import *  # CONSTS
from pygame_gui.core import ObjectID
from .upgrade import *
from .config import *
from configparser import ConfigParser, ExtendedInterpolation
import os

ui_config = ConfigParser(interpolation=ExtendedInterpolation())
ui_config.read('./data/config/ui.ini')

class Main_page_background():
    def __init__(self,screen):
        self.screen = screen
        config:dict = ui_config['main_page_background']
        path = config['img_dirs']
        self.x = int(config['x'])
        self.y = int(config['y'])
        self.width = int(config['width'])
        self.height = int(config['height'])
        self.img = pygame.image.load(path).convert_alpha()
        self.img = pygame.transform.scale(self.img,(self.width,self.height))

    def draw(self):
        self.screen.blit(self.img,(self.x,self.y))
class Title():
    def __init__(self,screen):
        self.screen = screen
        config:dict = ui_config['title']
        path = config['img_dirs']
        self.x = int(config['x'])
        self.y = int(config['y'])
        self.width = int(config['width'])
        self.height = int(config['height'])
        self.img = pygame.image.load(path).convert_alpha()
        self.img = pygame.transform.scale(self.img,(self.width,self.height))

    def draw(self):
        self.screen.blit(self.img,(self.x,self.y))

class Start():
    def __init__(self,screen):
        self.screen = screen
        config:dict = ui_config['start']
        self.x = int(config['x'])
        self.y = int(config['y'])
        self.width = int(config['width'])
        self.height = int(config['height'])
        self.img = [pygame.image.load(path).convert_alpha() for path in config['img_dirs'].split('\n')]
        self.selected = False

        for i in range(len(self.img)):
            self.img[i] = pygame.transform.scale(self.img[i],(self.width,self.height))

    def draw(self):
        if self.selected:
            self.screen.blit(self.img[1],(self.x,self.y))
        else:
            self.screen.blit(self.img[0],(self.x,self.y))

class Quit():
    def __init__(self,screen):
        self.screen = screen
        config:dict = ui_config['quit']
        self.x = int(config['x'])
        self.y = int(config['y'])
        self.width = int(config['width'])
        self.height = int(config['height'])
        self.img = [pygame.image.load(path).convert_alpha() for path in config['img_dirs'].split('\n')]
        self.selected = False

        for i in range(len(self.img)):
            self.img[i] = pygame.transform.scale(self.img[i],(self.width,self.height))

    def draw(self):
        if self.selected:
            self.screen.blit(self.img[1],(self.x,self.y))
        else:
            self.screen.blit(self.img[0],(self.x,self.y))

class Resume():
    def __init__(self,screen):
        self.screen = screen
        config:dict = ui_config['resume']
        self.x = int(config['x'])
        self.y = int(config['y'])
        self.width = int(config['width'])
        self.height = int(config['height'])
        self.img = [pygame.image.load(path).convert_alpha() for path in config['img_dirs'].split('\n')]
        self.selected = False

        for i in range(len(self.img)):
            self.img[i] = pygame.transform.scale(self.img[i],(self.width,self.height))

    def draw(self):
        if self.selected:
            self.screen.blit(self.img[1],(self.x,self.y))
        else:
            self.screen.blit(self.img[0],(self.x,self.y))


class Charcter_option():
    def __init__(self,screen,character_name):
        self.screen = screen
        config:dict = ui_config[character_name]
        self.x = int(config['x'])
        self.y = int(config['y'])
        self.width = int(config['width'])
        self.height = int(config['height'])
        self.selected = False
        self.img = [pygame.image.load(path).convert_alpha() for path in config['img_dirs'].split('\n')]
        for i in range(len(self.img)):
            self.img[i] = pygame.transform.scale(self.img[i],(self.width,self.height))
        
    def draw(self):
        if self.selected:
            self.screen.blit(self.img[2],(self.x,self.y))
            self.screen.blit(self.img[0],(self.x,self.y))
            self.screen.blit(self.img[4],(self.x,self.y))
        else:
            self.screen.blit(self.img[1],(self.x,self.y))        
            self.screen.blit(self.img[0],(self.x,self.y))
            self.screen.blit(self.img[3],(self.x,self.y))

class Upgrade_option():
    def __init__(self,screen,manager,option_name,number):
        self.screen = screen
        config:dict = ui_config['upgrade_option']
        self.x = int(config['x'])
        self.y = [int(y) for y in config['y'].split('\n')]
        self.y = self.y[number]
        self.width = [int(width) for width in config['width'].split('\n')]
        self.height = [int(height) for height in config['height'].split('\n')]
        self.selected = False
        self.img = [pygame.image.load(path).convert_alpha() for path in config['img_dirs'].split('\n')]
        self.option_image = pygame.image.load(weapon_config[option_name]['img_dir']).convert_alpha()
        self.option_image = pygame.transform.scale(self.option_image,(30,30))
        self.option_text = option_name
        self.option_name = option_name
        for i in range(len(self.img)):
            self.img[i] = pygame.transform.scale(self.img[i],(self.width[i],self.height[i]))
        # self.timer = pygame_gui.elements.UILabel(
        #     relative_rect=pygame.Rect(0,0,int(config['timer']['width']),int(config['timer']['height'])),
        #     anchors={'centerx':'centerx','top_target':self.xp_bar}, text = '00 : 00', manager=manager,
        #     object_id=ObjectID('#timer')
        #     )
        
    def draw(self):
        if self.selected:
            self.screen.blit(self.img[1],(self.x,self.y))
            self.screen.blit(self.img[3],(self.x,self.y))
            self.screen.blit(self.option_image,(self.x,self.y))
            self.screen.blit(self.img[5],(self.x,self.y))


        else:
            self.screen.blit(self.img[0],(self.x,self.y))
            self.screen.blit(self.img[2],(self.x,self.y))
            self.screen.blit(self.option_image,(self.x,self.y))
            self.screen.blit(self.img[4],(self.x,self.y))

        

class Again():
    def __init__(self,screen):
        self.screen = screen
        config:dict = ui_config['again']
        self.x = int(config['x'])
        self.y = int(config['y'])
        self.width = int(config['width'])
        self.height = int(config['height'])
        self.img = [pygame.image.load(path).convert_alpha() for path in config['img_dirs'].split('\n')]
        self.selected = False

        for i in range(len(self.img)):
            self.img[i] = pygame.transform.scale(self.img[i],(self.width,self.height))

    def draw(self):
        if self.selected:
            self.screen.blit(self.img[1],(self.x,self.y))
        else:
            self.screen.blit(self.img[0],(self.x,self.y))

class Game_over_text():
    def __init__(self,screen):
        self.screen = screen
        config:dict = ui_config['game_over_text']
        path = config['img_dirs']
        self.x = int(config['x'])
        self.y = int(config['y'])
        self.width = int(config['width'])
        self.height = int(config['height'])
        self.img = pygame.image.load(path).convert_alpha()
        self.img = pygame.transform.scale(self.img,(self.width,self.height))
        
    def draw(self):
        self.screen.blit(self.img,(self.x,self.y))

def main_page(screen,manager,clock):
    screen.fill("#90EE90")
    running = True
    dt = 0
    selected = 0

    # create title and options
    main_page_background = Main_page_background(screen)
    title = Title(screen)
    start = Start(screen)
    quit = Quit(screen)
    options = [start,quit]

    while running:
        main_page_background.draw()
        title.draw()
        for option in options:
            if options[selected] == option:
                option.selected = True
            else:
                option.selected = False
            option.draw()

        # - events -
        dt = clock.tick(FPS)/1000
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                # select 
                if event.key == K_UP or event.key == K_w and selected>0:
                    selected-=1
                if event.key == K_DOWN or event.key == K_s and selected<len(options)-1:
                    selected+=1

                # next stage
                if event.key == K_RETURN:
                    if options[selected] == start:
                        return "select_character",False
                    if options[selected] == quit:
                        pygame.quit()
                        exit()
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
        # - update -
        manager.update(dt)
        # - draws -
        manager.draw_ui(screen)
        pygame.display.flip()

def select_role(screen,manager,clock):
    running = True
    dt = 0
    selected = 0

    # create title and options
    main_page_background = Main_page_background(screen)
    santa = Charcter_option(screen,'santa')
    reindeer = Charcter_option(screen,'reindeer')
    gnome = Charcter_option(screen,'gnome')
    options = [santa,reindeer,gnome]

    while running:
        main_page_background.draw()
        for option in options:
            if options[selected] == option:
                option.selected = True
            else:
                option.selected = False
            option.draw()

        # - events -
        dt = clock.tick(FPS)/1000
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                # select 
                if event.key == K_LEFT or event.key == K_a and selected>0:
                    selected-=1
                if event.key == K_RIGHT or event.key == K_d and selected<len(options)-1:
                    selected+=1

                # next stage
                if event.key == K_RETURN:
                    if options[selected] == santa:
                        chosen = "Santa"
                    if options[selected] == reindeer:
                        chosen = 'Reindeer'
                    if options[selected] == gnome:
                        chosen = "Gnome"
                    return 'start', chosen, False
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
        # - update -    
        manager.update(dt)
        # - draws -
        manager.draw_ui(screen)
        pygame.display.flip()

def game_over(screen,manager,clock,enemy_killed):
    screen.fill("#000000")
    running = True
    dt = 0
    selected = 0

    # create title and options
    game_over_text = Game_over_text(screen)
    again = Again(screen)
    quit = Quit(screen)
    options = [again,quit]
    kill_counter = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect(100,400,200,50),
             text = f'kills:{enemy_killed}', manager=manager,
            object_id=ObjectID('#kill_counter')
            )
    while running:
        game_over_text.draw()
        for option in options:
            if options[selected] == option:
                option.selected = True
            else:
                option.selected = False
            option.draw()

        # - events -
        dt = clock.tick(FPS)/1000
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                # select 
                if event.key == K_UP and selected>0:
                    selected-=1
                if event.key == K_DOWN and selected<len(options)-1:
                    selected+=1

                # next stage
                if event.key == K_RETURN:
                    if options[selected] == again:
                        chosen = "main_page"
                        kill_counter.kill()
                    if options[selected] == quit:
                        pygame.quit()
                        exit()
                    return chosen,False
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
        # - update -
        manager.update(dt)
        # - draws -
        manager.draw_ui(screen)
        pygame.display.flip()

class Pause():
    def __init__(self,screen,backend):
        self.backend = backend
        self.selected = 0
        self.reusme = Resume(screen)
        self.quit = Quit(screen)
        self.options = [self.reusme,self.quit]

    def choose(self,event):
        if event.key == K_UP and self.selected>0:
            self.selected-=1
        if event.key == K_DOWN and self.selected<len(self.options)-1:
            self.selected+=1
        if event.key == K_RETURN:
            for option in self.options:
                del option
            if self.options[self.selected] == self.reusme:
                self.backend.paused = False
            elif self.options[self.selected] == self.quit:
                self.backend.paused = False
                return True
           
    def show(self):
        for option in self.options:
            if self.options[self.selected] == option:
                option.selected = True
            else:
                option.selected = False

    def draw(self):
        for option in self.options:
            option.draw()


class Upgrade():
    def __init__(self,screen, manager, player, backend):
        self.selected = 0
        self.player = player
        result = upgrade(weapon_list,[],player.weapons,[])
        self.upgrade_option0 = Upgrade_option(screen, manager, result[0], 0)
        self.upgrade_option1 = Upgrade_option(screen, manager, result[1],1)
        self.upgrade_option2 = Upgrade_option(screen, manager, result[2], 2)
        self.upgrade_option3 = Upgrade_option(screen, manager, result[3],3)
        self.backend = backend
        self.options = [self.upgrade_option0,self.upgrade_option1,self.upgrade_option2,self.upgrade_option3]

    def choose(self,event):
        if event.key == K_UP and self.selected>0:
            self.selected-=1
        if event.key == K_DOWN and self.selected<len(self.options)-1:
            self.selected+=1
        if event.key == K_RETURN:
            for option in self.options:
                del option
            self.backend.upgrade_menu = False
            self.player.weapons += [weapon_list[self.options[self.selected].option_name](self.player)]
           
    def show(self):
        for option in self.options:
            if self.options[self.selected] == option:
                option.selected = True
            else:
                option.selected = False


    def draw(self):
        for option in self.options:
            option.draw()