import os
from abc import ABCMeta, abstractmethod
from random import random, randrange

import pygame
import pygame_gui
from numpy import array
from numpy.linalg import norm
from pygame.locals import *  # CONSTS
from pygame_gui.core import ObjectID
from .store_buff import read_level, save_level
from .upgrade import *
from .config import *
from configparser import ConfigParser, ExtendedInterpolation


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
        
        self.shaodw_imgs = [pygame.image.load(path).convert_alpha() for path in ui_config['main_page_shadow']['img_dirs'].split('\n')]
        self.shaodw_imgs_x = [int(x) for x in ui_config['main_page_shadow']['x'].split('\n')]
        self.shaodw_imgs_y = [int(y) for y in ui_config['main_page_shadow']['y'].split('\n')]
        self.shaodw_imgs_speed = [int(speed) for speed in ui_config['main_page_shadow']['speed'].split('\n')]

    def draw(self):
        self.screen.blit(self.img,(self.x,self.y))
        for i in range(len(self.shaodw_imgs)):
            if self.shaodw_imgs_x[i] > 1500:
                self.shaodw_imgs_x[i] = -150
            else:
                self.shaodw_imgs_x[i] += self.shaodw_imgs_speed[i]*0.5
            self.screen.blit(self.shaodw_imgs[i],(self.shaodw_imgs_x[i],self.shaodw_imgs_y[i]))
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

class Shop():
    def __init__(self,screen):
        self.screen = screen
        config:dict = ui_config['shop']
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
class Shop_option():
    def __init__(self,screen,manager,number):
        self.screen = screen
        self.number = number
        self.bought = False
        config:dict = ui_config['shop_option']
        self.name = [name for name in config['name'].split('\n')][number]
        self.x = [int(x) for x in config['x'].split('\n')]
        self.y = [int(y) for y in config['y'].split('\n')]
        self.width = int(config['width'])
        self.height = int(config['height'])
        self.selected = False
        self.img = [pygame.image.load(path).convert_alpha() for path in config['img_dirs'].split('\n')]
        for i in range(len(self.img)):
            self.img[i] = pygame.transform.scale(self.img[i],(self.width,self.height))

    def draw(self):
        if self.selected:
            self.screen.blit(self.img[9],(self.x[self.number],self.y[self.number]))
            self.screen.blit(self.img[self.number],(self.x[self.number],self.y[self.number]))
            self.screen.blit(self.img[11],(self.x[self.number],self.y[self.number]))
        else:
            self.screen.blit(self.img[8],(self.x[self.number],self.y[self.number]))        
            self.screen.blit(self.img[self.number],(self.x[self.number],self.y[self.number]))
            self.screen.blit(self.img[10],(self.x[self.number],self.y[self.number]))
        if self.bought:
            self.screen.blit(self.img[12],(self.x[self.number]+50,self.y[self.number]-50))
class Tutorial():
    def __init__(self,screen):
        self.screen = screen
        config:dict = ui_config['tutorial']
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
    
class Show_tutorial():
    def __init__(self,screen,manager):
        self.screen = screen
        config:dict = ui_config['show_tutorial']
        self.x = int(config['x'])
        self.y = int(config['y'])
        self.width = int(config['width'])
        self.height = int(config['height'])
        self.guide_texts = [text for text in ui_config['show_tutorial']['guide_texts'].split('\n')]
        self.img = [pygame.image.load(path).convert_alpha() for path in ui_config['show_tutorial']['img_dirs'].split('\n')]
        self.text = pygame_gui.elements.UILabel(relative_rect=pygame.Rect(340,450,600,270),
            text = f"{ui_config['santa']['hp_r']}", manager=manager,object_id=ObjectID('#guide_text'))
        for i in range(len(self.img)):
            self.img[i] = pygame.transform.scale(self.img[i],(self.width,self.height))

    def draw(self,stage):
            self.screen.blit(self.img[stage],(self.x,self.y))
            self.text.set_text(self.guide_texts[stage])
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
    def __init__(self,screen,manager,character_name):
        self.screen = screen
        self.name = character_name
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

def character_info(manager):
    hp = pygame_gui.elements.UILabel(relative_rect=pygame.Rect(250,390,200,50),
    text = f"hp: {ui_config['santa']['hp']}", manager=manager, object_id=ObjectID('#guide_text'))

    hp_r = pygame_gui.elements.UILabel(relative_rect=pygame.Rect(250,450,200,50),
        text = f"{ui_config['santa']['hp_r']}", manager=manager,object_id=ObjectID('#guide_text'))

    atk = pygame_gui.elements.UILabel(relative_rect=pygame.Rect(250,510,200,50),
        text = f"{ui_config['santa']['atk']}", manager=manager,object_id=ObjectID('#guide_text'))

    speed = pygame_gui.elements.UILabel(relative_rect=pygame.Rect(425,390,200,50),
        text = f"{ui_config['santa']['speed']}", manager=manager,object_id=ObjectID('#guide_text'))

    absorb_range = pygame_gui.elements.UILabel(relative_rect=pygame.Rect(425,450,200,50),
        text = f"{ui_config['santa']['absorb_range']}", manager=manager,object_id=ObjectID('#guide_text'))

    init_weapon = pygame_gui.elements.UILabel(relative_rect=pygame.Rect(725,390,200,50),
        text = f"{ui_config['santa']['init_weapon']}", manager=manager,object_id=ObjectID('#guide_text'))

    return {'hp':hp,'hp_r':hp_r,'absorb_range':absorb_range,'speed':speed,'atk':atk, 'init_weapon':init_weapon}

def chracter_info_update(infos,name):
    infos['hp'].set_text(f'{ui_config[name]["hp"]}')
    infos['hp_r'].set_text(f'{ui_config[name]["hp_r"]}')
    infos['absorb_range'].set_text(f'{ui_config[name]["absorb_range"]}')
    infos['speed'].set_text(f'{ui_config[name]["speed"]}')
    infos['atk'].set_text(f'{ui_config[name]["atk"]}')
    infos['init_weapon'].set_text(f'{ui_config[name]["init_weapon"]}')

def character_info_icons():
    hp_img = pygame.image.load(ui_config['hp']['img_dir']).convert_alpha()
    hp_img = pygame.transform.scale(hp_img,(30,30))

    hp_r_img = pygame.image.load(ui_config['hp_r']['img_dir']).convert_alpha()
    hp_r_img = pygame.transform.scale(hp_r_img,(30,30))

    speed_img = pygame.image.load(ui_config['speed']['img_dir']).convert_alpha()
    speed_img = pygame.transform.scale(speed_img,(30,30))

    absorb_range_img = pygame.image.load(ui_config['absorb_range']['img_dir']).convert_alpha()
    absorb_range_img = pygame.transform.scale(absorb_range_img,(30,30))

    atk_img = pygame.image.load(ui_config['atk']['img_dir']).convert_alpha()
    atk_img = pygame.transform.scale(atk_img,(30,30))

    return[hp_img,hp_r_img,atk_img,speed_img,absorb_range_img,atk_img]

def character_info_icons_show(screen,icons):
    screen.blit(icons[0],(270,400))
    screen.blit(icons[1],(270,460))
    screen.blit(icons[2],(270,520))
    screen.blit(icons[3],(440,400))
    screen.blit(icons[4],(440,460))

def init_weapon_icons():
    santa_init_weapon_img = pygame.image.load(ui_config['santa']['weapon_img_dir']).convert_alpha()
    santa_init_weapon_img = pygame.transform.scale(santa_init_weapon_img,(30,30))
    reindeer_init_weapon_img  = pygame.image.load(ui_config['reindeer']['weapon_img_dir']).convert_alpha()
    reindeer_init_weapon_img  = pygame.transform.scale(reindeer_init_weapon_img,(30,30))
    gnome_init_weapon_img = pygame.image.load(ui_config['gnome']['weapon_img_dir']).convert_alpha()
    gnome_init_weapon_img = pygame.transform.scale(gnome_init_weapon_img,(30,30))
    return {'santa':santa_init_weapon_img, 'reindeer':reindeer_init_weapon_img, 'gnome':gnome_init_weapon_img}

def init_weapon_icon_show(screen,init_weapon_icons,name):
    screen.blit(init_weapon_icons[name],(700,400))
    
def draw_text(surface,text,x,y):
    font = pygame.font.Font(ui_config['font']['dir'],32)
    text_surface = font.render(text,True,(255,255,255))#(字,反鋸齒,顏色)
    text_rect = text_surface.get_rect()
    text_rect.left = x
    text_rect.top = y
    surface.blit(text_surface,text_rect)

class Upgrade_option():
    def __init__(self,screen,manager,option_name,number):
        self.screen = screen
        self.manager = manager
        self.number = number
        config:dict = ui_config['upgrade_option']
        self.x = int(config['x'])
        self.y = [int(y) for y in config['y'].split('\n')]
        self.y = self.y[number]
        self.width = [int(width) for width in config['width'].split('\n')]
        self.height = [int(height) for height in config['height'].split('\n')]
        self.selected = False
        self.img = [pygame.image.load(path).convert_alpha() for path in config['img_dirs'].split('\n')]
        if option_name in weapon_list:
            if option_name == "LED":
                self.option_image = pygame.image.load(ui_config['led_icon']['img_dir']).convert_alpha()
                self.option_image = pygame.transform.scale(self.option_image,(100,100))
                self.option_name = option_name
            else:
                self.option_image = pygame.image.load(weapon_config[option_name]['img_dir']).convert_alpha()
                self.option_image = pygame.transform.scale(self.option_image,(100,100))
                self.option_name = option_name
        else:
            self.option_image = pygame.image.load(buff_config[option_name]['img_dir']).convert_alpha()
            self.option_image = pygame.transform.scale(self.option_image,(100,100))
            self.option_name = option_name

        for i in range(len(self.img)):
            self.img[i] = pygame.transform.scale(self.img[i],(self.width[i],self.height[i]))

        
    def draw(self):
        if self.selected:
            self.screen.blit(self.img[1],(self.x,self.y))
            self.screen.blit(self.img[3],(self.x+10,self.y+10))
            self.screen.blit(self.option_image,(self.x+10,self.y+10))
            draw_text(self.screen,self.option_name,self.x+150,self.y+38)
            self.screen.blit(self.img[5],(self.x+10,self.y+10))

        else:
            self.screen.blit(self.img[0],(self.x,self.y))
            self.screen.blit(self.img[2],(self.x+10,self.y+10))
            self.screen.blit(self.option_image,(self.x+10,self.y+10))
            draw_text(self.screen,self.option_name,self.x+150,self.y+38)
            self.screen.blit(self.img[4],(self.x+10,self.y+10))


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
    tutorial = Tutorial(screen)
    shop = Shop(screen)
    quit = Quit(screen)
    options = [start,tutorial,shop,quit]

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
                if event.key == K_w and selected>0:
                    selected-=1
                if event.key == K_s and selected<len(options)-1:
                    selected+=1

                # next stage
                if event.key == K_RETURN:
                    if options[selected] == start:
                        return "select_character",False
                    if options[selected] == tutorial:
                        return "tutorial",False
                    if options[selected] == shop:
                        return "shop",False
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

def tutorial(screen,manager,clock):
    screen.fill("#90EE90")
    running = True
    dt = 0
    stage = 0
    # create title and options
    main_page_background = Main_page_background(screen)
    show_tutorial = Show_tutorial(screen,manager)
    while running:
        main_page_background.draw()
        if stage >= 4:
            show_tutorial.text.kill()
            return 'main_page',False
        show_tutorial.draw(stage)
        # - events -
        dt = clock.tick(FPS)/1000
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                # next stage
                stage += 1
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
        # - update -
        manager.update(dt)
        # - draws -
        manager.draw_ui(screen)
        pygame.display.flip()

def shop(screen,manager,clock,money):
    screen.fill("#90EE90")
    running = True
    dt = 0
    selected = 0
    shop_option0 = Shop_option(screen,manager,0)
    shop_option1 = Shop_option(screen,manager,1)
    shop_option2 = Shop_option(screen,manager,2)
    shop_option3 = Shop_option(screen,manager,3)
    shop_option4 = Shop_option(screen,manager,4)
    shop_option5 = Shop_option(screen,manager,5)
    shop_option6 = Shop_option(screen,manager,6)
    shop_option7 = Shop_option(screen,manager,7)
    money_icon = pygame.image.load(ui_config['money']['img_dir']).convert_alpha()
    money_icon = pygame.transform.scale(money_icon,(40,40))
    money_text = pygame_gui.elements.UILabel(relative_rect=pygame.Rect(750,200,200,50),
        text = f"{money}", manager=manager, object_id=ObjectID('#guide_text'))
    quit = Quit(screen)
    options = [shop_option0,shop_option1,shop_option2,shop_option3,shop_option4,shop_option5,shop_option6,shop_option7,quit]
    buff_list = ['fortune','muscle','nike','warming','hell','wd_40','wise','strong']
    result = {}
    # create title and options
    main_page_background = Main_page_background(screen)
    options += [quit]

    while running:
        main_page_background.draw()
        screen.blit(money_icon,(760,200))
        for option in options:
            if options[selected] == option:
                option.selected = True
            else:
                option.selected = False
            option.draw()
        money_text.set_text(f'{money}')
        # - events -
        dt = clock.tick(FPS)/1000
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                # select 
                if event.key == K_w and selected-4>=0:
                    selected-=4
                if event.key == K_s and selected+4<len(options)-1:
                    selected+=4
                if event.key == K_a and selected>0:
                    selected-=1
                if event.key == K_d and selected<len(options)-1:
                    selected+=1
                # next stage
                if event.key == K_RETURN:
                    for option in options[:8]:
                        if options[selected] == option:
                            if option.bought == False and money>=10:
                                money-=10
                                option.bought = True
                            else:
                                money+=10
                                option.bought = False
                        option.draw()
                    if options[selected] == quit:
                        money_text.kill()
                        for i in range(8):
                            print(options[i].name,options[i].bought)
                            result[options[i].name] = 1 if options[i].bought else 0
                        print(result)
                        save_level(result)
                        return 'main_page',False
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

    infos = character_info(manager)
    info_icons = character_info_icons()
    info_init_weapon_icons = init_weapon_icons()
    # create title and options
    main_page_background = Main_page_background(screen)
    santa = Charcter_option(screen,manager,'santa')
    reindeer = Charcter_option(screen,manager,'reindeer')
    gnome = Charcter_option(screen,manager,'gnome')
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
                    for info in infos:
                        infos[info].kill()
                    return 'start', chosen, False
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
        init_weapon_icon_show(screen,info_init_weapon_icons,options[selected].name)
        character_info_icons_show(screen,info_icons)
        chracter_info_update(infos,options[selected].name)
        # - update -    
        manager.update(dt)
        # - draws -
        manager.draw_ui(screen)
        pygame.display.flip()

def game_over(screen,manager,clock,enemy_killed,golds):
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
            object_id=ObjectID('#guide_text')
            )
    gold_counter = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect(100,500,200,50),
             text = f'golds:{golds}', manager=manager,
            object_id=ObjectID('#guide_text')
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
                if event.key == K_w and selected>0:
                    selected-=1
                if event.key == K_s and selected<len(options)-1:
                    selected+=1

                # next stage
                if event.key == K_RETURN:
                    if options[selected] == again:
                        chosen = "main_page"
                        kill_counter.kill()
                        gold_counter.kill()
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
        if event.key == K_w and self.selected>0:
            self.selected-=1
        if event.key == K_s and self.selected<len(self.options)-1:
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
        result = upgrade(weapon_list,available_buffs,player.weapons,player.buffs)
        print(result)
        self.backend = backend
        self.maxlevel = False
        if result != 0:
            self.upgrade_option0 = Upgrade_option(screen, manager, result[0], 0)
            self.upgrade_option1 = Upgrade_option(screen, manager, result[1], 1)
            self.upgrade_option2 = Upgrade_option(screen, manager, result[2], 2)
            self.upgrade_option3 = Upgrade_option(screen, manager, result[3], 3)
            self.options = [self.upgrade_option0,self.upgrade_option1,self.upgrade_option2,self.upgrade_option3]
        else:
            self.maxlevel = True

    def choose(self,event):
        if not self.maxlevel:
            if event.key == K_w and self.selected>0:
                self.selected-=1
            if event.key == K_s and self.selected<len(self.options)-1:
                self.selected+=1
            if event.key == K_RETURN:
                for option in self.options:
                    del option
                self.backend.upgrade_menu = False
                if self.options[self.selected].option_name in weapon_list:
                    for weapon in self.player.weapons:
                        if  weapon.name == self.options[self.selected].option_name:
                            weapon.level += 1
                            return 0
                    self.player.weapons += [weapon_list[self.options[self.selected].option_name](self.player)]
                else:
                    for buff in self.player.buffs:
                        if  buff.name == self.options[self.selected].option_name:
                            buff.level += 1
                            return 0

                    self.player.buffs += [available_buffs[self.options[self.selected].option_name]()]
                self.player.calc_stats() #make buffs work

        else:
            self.backend.upgrade_menu = False
           

    def show(self):
        if not self.maxlevel:
            for option in self.options:
                if self.options[self.selected] == option:
                    option.selected = True
                else:
                    option.selected = False


    def draw(self):
        if not self.maxlevel:
            for option in self.options:
                option.draw()