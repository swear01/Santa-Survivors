import os
from abc import ABCMeta, abstractmethod
from random import random, randrange

import pygame
import pygame_gui
from numpy import array
from numpy.linalg import norm
from pygame.locals import *  # CONSTS
from pygame_gui.core import ObjectID

from .config import *


def main_page(screen,manager):
    clock = pygame.time.Clock()
    running = True
    dt = 0
    start_game =  pygame_gui.elements.UITextBox(html_text="start",relative_rect=pygame.Rect((0,150), (100, 50)),
                manager=manager,anchors={'centerx': 'centerx'},object_id=ObjectID(class_id='@selected'))
    settings =  pygame_gui.elements.UITextBox(html_text="settings",relative_rect=pygame.Rect((0,225), (100, 50)),
            manager=manager,anchors={'centerx': 'centerx'},object_id=ObjectID(class_id='@selected'))
    quit_game =  pygame_gui.elements.UITextBox(html_text="quit",relative_rect=pygame.Rect((0,300), (100, 50)),
            manager=manager,anchors={'centerx': 'centerx'},object_id=ObjectID(class_id='@selected'))
    options = [start_game,settings,quit_game]
    selected = 0
    ui_reload = 1
    ui_cooldown = 1

    clock.tick()
    while running:
        # - events -
        dt = clock.tick(FPS)/1000*3
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
                    if options[selected] == start_game:
                        chosen = "start"
                    if options[selected] == settings:
                        chosen = "settings"
                    if options[selected] == quit_game:
                        chosen = 'quit'
                        pygame.quit()
                        exit()
                    for option in options:
                        option.kill()
                    return chosen,False
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
        # - blink - 
        ui_reload -= dt
        if ui_reload <= 0:
            options[selected].visible = 0
            ui_reload += ui_cooldown
        else:
            options[selected].visible = 1
        for i in range(len(options)):
            if i == selected:
                pass
            else:
                options[i].visible = 1
        # - update -
        manager.update(dt)
        # - draws -
        screen.fill('#000000')
        manager.draw_ui(screen)
        pygame.display.flip()

def pause():
    pass
def upgrade():
    pass