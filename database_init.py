import json


#Создаёт dict персонажа в базе данных с ключом по ID
def create_char(player, unit_id, armour, weapon, unit_class, strength, toughness, reaction, spirit, speed, vitality, hp, mp, mp_regen):
    temp = {unit_id: [player, armour, weapon, unit_class, strength, toughness, reaction, spirit, speed, vitality, hp, mp, mp_regen]}
    with open('session1/unit_db.json', 'r') as file:
        unit_db = json.load(file)
    unit_db.update(temp)
    with open('session1/unit_db.json', 'w') as file:
        json.dump(unit_db, file)


#очистка выбранной БД
def db_flush(session, db):
    with open(f'session{session}/{db}_db.json', 'w') as file:
        json.dump({}, file)


#Создание dict оружия в БД с ключом по ID
#            <!-- weapon_name, damage_mod, w_hp, w_accuracy, weight, ignore_arm, w_range, damage_type   -->
def create_weapon(weapon_name, damage_mod, w_hp, w_accuracy, w_weight, ignore_arm, w_range, damage_type):
    temp = {weapon_name: [damage_mod, w_hp, w_accuracy, w_weight, ignore_arm, w_range, damage_type]}
    with open ('session1/weapons_db.json', 'r') as file:
        w_db = json.load(file)
    w_db.update(temp)
    with open('session1/weapons_db.json', 'w') as file:
        json.dump(w_db, file)


#Создание dict брони в БД с ключом по ID
#            <!-- arm_name, arm_mod, arm_hp, weight, element_type   -->
def create_armour(armour_name, arm_mod, arm_hp, arm_weight, element_type):
    temp = {armour_name: [arm_mod, arm_hp, arm_weight, element_type]}
    with open ('session1/armour_db.json', 'r') as file:
        arm_db = json.load(file)
    arm_db.update(temp)
    with open('session1/armour_db.json', 'w') as file:
        json.dump(arm_db, file)




#db_flush(1, 'armour')
#create_char(1, 1,1,1,1,1,1,1,1,1,1,1,1,1)










'''

import sqlite3
from database_init import *

@db_session
def add_new_player():
    pl1 = User(players=input('players: '), nickname=input('nick: '))
    commit()

add_new_player()

'''

'''
class Arena_unit():
    def __init__(self, player, unit_id, armour, unit_class, strength, toughness, reaction, spirit, speed, vitality, hp, mp, mp_regen):
        self.player = player
        self.unit_id = unit_id
        self.armour = armour
        self.unit_class = unit_class
        self.strength = strength
        self.toughness = toughness
        self.reaction = reaction
        self.spirit = spirit
        self.speed = speed
        self.vitality = vitality
        self.hp = hp
        self.mp = mp
        self.mp_regen = mp_regen
'''