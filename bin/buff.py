#status list
#health, atk, defense, speed, gold_obtain, enemy_amount, 
from configparser import ConfigParser, ExtendedInterpolation

import pygame

buff_config = ConfigParser(interpolation=ExtendedInterpolation())
buff_config.read('./data/config/buff.ini')

class Buff:
    def __init__(self, buff_name):
        self.name = buff_name
        config:dict = buff_config[self.name]
        self.type = config['type']
        self.max_level = int(config['max_level'])
        self.effect = float(config['effect'])
        self.image = pygame.image.load(config['img_dir'])
        self.level = 0

    def can_upgrade(self):
        return self.level < self.max_level

class Fortune(Buff):
    def __init__(self):
        super().__init__('Fortune')

class Dice(Buff):
    def __init__(self):
        super().__init__('Dice')

class Muscle(Buff):
    def __init__(self):
        super().__init__('Muscle')

class Nike(Buff):
    def __init__(self):
        super().__init__('Nike')

class Warming(Buff):
    def __init__(self):
        super().__init__('Warming')

class Hell(Buff):
    def __init__(self):
        super().__init__('Hell')

class WD_40(Buff):
    def __init__(self):
        super().__init__('WD_40')

class Wise(Buff):
    def __init__(self):
        super().__init__('Wise')

class Strong(Buff):
    def __init__(self):
        super().__init__('Strong')

available_names = buff_config.sections()

available_buffs:dict[str,Buff] = {'Fortune':Fortune, 'Dice':Dice, 'Muscle':Muscle, 'Nike':Nike,
                                  'Warming':Warming, 'Hell':Hell, 'WD_40':WD_40, 'Wise':Wise, 'Strong':Strong}
type_buff :dict[str,Buff] = {'gold':Fortune, 'reroll':Dice, 'atk':Muscle, 'speed':Nike,
                                  'hp_r':Warming, 'enemy_period':Hell, 'shoot_period':WD_40, 'xp':Wise, 'hp':Strong}
