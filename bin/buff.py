#status list
#health, atk, defense, speed, gold_obtain, enemy_amount, 
from configparser import ConfigParser, ExtendedInterpolation

import pygame

buff_config = ConfigParser(interpolation=ExtendedInterpolation())
buff_config.read('./data/config/buff.ini')

class Buff():
    def __init__(self, buff_name):
        self.name = buff_name
        config = buff_config[self.name]
        self.max_level = int(config['max_level'])
        self.effect = float(config['effect'])
        self.image = pygame.image.load(config['img_dir'])
        self.level = 0

    def can_upgrade(self):
        return self.level < self.max_level


available_names = buff_config.sections()

available_buffs = [Buff(name) for name in available_names]
