import pygame
from .weapon import *
from .buff import *
import random

# def upgrade(all_weapons,all_buffs,selected_weapons,selected_buffs):
#     non_selecteds = []
#     selecteds = []
#     for weapon in all_weapons:
#         if weapon not in selected_weapons:
#             non_selecteds += [weapon]
#         else:
#             selecteds += [weapon]
#     for buff in all_buffs:
#         if buff not in selected_buffs:
#             non_selecteds += [buff]
#         else:
#             selecteds += [buff]
#     weights = []
#     result = []
#     for selected in selecteds:
#         for i in range(5):
#             weights += [selected]
#     for non_selected in non_selecteds:
#         weights += [non_selected]
#     while len(result) < 4:
#         n = random.randint(0,len(weights)-1)
#         if weights[n] not in result:
#             result += weights[n]
#     return result