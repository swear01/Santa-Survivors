import pygame
from .weapon import *
from .buff import *
import random


def upgrade(all_weapons,all_buffs,selected_weapons,selected_buffs):
    non_selecteds = []
    selecteds = []
    selected_weapons_names = []
    selected_buffs_names = []
    for selected_weapon in selected_weapons:
        selected_weapons_names += [selected_weapon.name]
    for selected_buff in selected_buffs:
        selected_buffs_names += [selected_buff.name]
    if len(selected_weapons)<4:
        for weapon in all_weapons:
            if weapon not in selected_weapons_names:
                non_selecteds += [weapon]
        for selected_weapon in selected_weapons:
            if selected_weapon.level < selected_weapon.max_level:
                selecteds += [selected_weapon.name]
    else:
        for selected_weapon in selected_weapons:
            if selected_weapon.level < selected_weapon.max_level:
                selecteds += [selected_weapon.name]
    if len(selected_buffs)<4:
        for buff in all_buffs:
            if buff not in  selected_buffs_names:
                non_selecteds += [buff]
        for selected_buff in selected_buffs:
            selecteds += [selected_buff.name]
    else:
        for selected_buff in selected_buffs:
            if selected_buff.level < selected_buff.max_level:
                selecteds += [selected_buff]
    weights = []
    result = []
    for selected in selecteds:
        for i in range(3):
            weights += [selected]
    for non_selected in non_selecteds:
        weights += [non_selected]
    times = 0
    i = 0
    while len(result) < 4:
        n = random.randint(0,len(weights)-1)
        if weights[n] not in result:
            result += [weights[n]]
        times+=1
        if times>20:
            break
    while len(result) < 4:
        result += [weights[0]]
        if i+3<len(weights):
            i+=3
    return result