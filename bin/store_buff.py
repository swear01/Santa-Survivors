#status list
#health, atk, defense, speed, gold_obtain, enemy_amount, 
from configparser import ConfigParser, ExtendedInterpolation

import pygame

buff_config = ConfigParser(interpolation=ExtendedInterpolation())
buff_config.read('./data/config/store_buff.ini')

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
        
def read_level(save_path = './save/player1.ini') -> dict:
    user_data = ConfigParser(interpolation=ExtendedInterpolation())
    user_data.read(save_path)
    return user_data['Store_upgrade']

def save_level(store_levels:dict, save_path = './save/player1.ini'):
    user_data = ConfigParser(interpolation=ExtendedInterpolation())
    user_data.read(save_path)
    user_data['Store_upgrade'] = store_levels
    with open(save_path,'w+') as f:
        ConfigParser.write(f)
    
    return buff_config.items('Store_upgrade')

def read_store_buff(save_path = './save/player1.ini') -> list:
    user_data = ConfigParser(interpolation=ExtendedInterpolation())
    user_data.optionxform = str
    user_data.read(save_path)
    store_buff_data = user_data['Store_upgrade']
    buffs = []
    for buff_name in store_buff_data:
        buff = available_buffs[buff_name]()
        buff.level = int(store_buff_data[buff_name])
        buffs.append(buff)
    return buffs

available_buffs:dict[str,Buff] = {'Fortune':Fortune, 'Muscle':Muscle, 'Nike':Nike,
                                  'Warming':Warming, 'Hell':Hell, 'WD_40':WD_40, 'Wise':Wise, 'Strong':Strong}
buff_types = ['gold','atk','speed','hp_r','enemy_period','shoot_period','xp','hp']
