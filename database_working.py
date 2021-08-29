# Описание классов, функция записи текущего состояния юнита в БД, функции попадания, атаки

import json
import os
import random

all_units_list = []
all_current_coordinates = {}

class UnitWeapon:
    def __init__(self, weapon_name, damage_mod, w_hp, w_accuracy, w_weight, ignore_arm, w_range, damage_type):
        self.weapon_name = weapon_name
        self.damage_mod = damage_mod
        self.w_hp = w_hp
        self.w_accuracy = w_accuracy
        self.w_weight = w_weight
        self.ignore_arm = ignore_arm
        self.w_range = w_range
        self.damage_type = damage_type

    def dict_return(self):
        return {self.weapon_name: [self.weapon_name, self.damage_mod, self.w_hp, self.w_accuracy, self.w_weight,
                                   self.ignore_arm, self.w_range, self.damage_type]}


class UnitArmour:
    def __init__(self, armour_name, arm_mod, arm_hp, arm_weight, element_type):
        self.armour_name = armour_name
        self.arm_mod = arm_mod
        self.arm_hp = arm_hp
        self.arm_weight = arm_weight
        self.element_type = element_type

    def dict_return(self):
        return {self.armour_name: [self.armour_name, self.arm_mod, self.arm_hp, self.arm_weight, self.element_type]}


#
class UnitState:
    def __init__(self, unit_id, coordinates, player, armour, weapon, unit_class, strength,
                 toughness, reaction, spirit, speed, vitality, hp, mp, mp_regen):
        # self.session = # for new sessions, may implement later
        self.current_round = 1  # Round counter for rollbacks
        self.active_status = 'Active'  # Has moved in round or not
        self.coordinates = coordinates
        self.player = player
        self.unit_id = unit_id
        self.armour = UnitArmour(*armour)
        self.weapon = UnitWeapon(*weapon)
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
        self.direction = 'DOWN'


#
def create_unit_classes():
    global all_units_list
    with open('session1/session_init/unit_db.json', 'r') as file:
        unit_db = dict(json.load(file))
        for unit_db_ids in unit_db.keys():
            all_units_list.append(exec(f'{unit_db_ids} = 1'))
        for counter in range(len(all_units_list)):
            all_units_list[counter] = UnitState(*list(unit_db.values())[counter])
    print(all_units_list)

'''
        for each_unit in unit_db.values():
            #print(each_unit)
            #all_units_list = UnitState(*each_unit)
            all_units_list.append(exec(f'{each_unit[0]} = {UnitState(*each_unit)}'))
    print(all_units_list)

        if unit_db['Tima1']:
            Tima1 = UnitState(*unit_db['Tima1'])
            all_units_list.append(Tima1)
        if unit_db['Tima2']:
            Tima2 = UnitState(*unit_db['Tima2'])
            all_units_list += Tima2
        if unit_db['Tima3']:
            Tima3 = UnitState(*unit_db['Tima3'])
            all_units_list += Tima3
        if unit_db['Dima1']:
            Dima1 = UnitState(*unit_db['Dima1'])
            all_units_list += Dima1
        if unit_db['Dima2']:
            Dima2 = UnitState(*unit_db['Dima2'])
            all_units_list += Dima2
        if unit_db['Dima3']:
            Dima3 = UnitState(*unit_db['Dima3'])
            all_units_list += Dima3
        if unit_db['Dalamar1']:
            Dalamar1 = UnitState(*unit_db['Dalamar1'])
            all_units_list += Dalamar1
        if unit_db['Dalamar2']:
            Dalamar2 = UnitState(*unit_db['Dalamar2'])
            all_units_list += Dalamar2
        if unit_db['Dalamar3']:
            Dalamar3 = UnitState(*unit_db['Dalamar3'])
            all_units_list += Dalamar3
        if unit_db['Shini1']:
            Shini1 = UnitState(*unit_db['Shini1'])
            all_units_list += Shini1
        if unit_db['Shini2']:
            Shini2 = UnitState(*unit_db['Shini2'])
            all_units_list += Shini2
        if unit_db['Shini3']:
            Shini3 = UnitState(*unit_db['Shini3'])
            all_units_list += Shini3
            #all_units_list = [Tima1, Tima2, Tima3, Dima1, Dima2, Dima3, Dalamar1, Dalamar2, Dalamar3,
            # Shini1, Shini2, Shini3]
            #all_units_list = [Tima1, Dima1]
            #for n in all_units_list:
            #    update_unit(n)
        #except:
        #    print('Не все юниты созданы')
        print(all_units_list)



    for any_file in os.listdir('session1/units/'):
        with open(f'session1/units/{any_file}', 'r') as file:
            current_unit_list = json.load(file)
            print(current_unit_list)
            for cur_un_list_elem in current_unit_list:
                all_units_list.append(exec(f'{cur_un_list_elem.keys()} = {UnitState(cur_un_list_elem.values())}'))
'''

# сохраняет в отдельную БД лог состояний юнита, чтобы можно было откатить на определённый раунд
def update_unit(unit_state: UnitState):
    with open(f'session1/units/{unit_state.unit_id}.json', 'w+') as file:
        unit_entry = {unit_state.current_round: [unit_state.coordinates, unit_state.active_status, unit_state.player,
                                                 unit_state.armour.dict_return(), unit_state.weapon.dict_return(), unit_state.unit_class, unit_state.strength,
                                                 unit_state.toughness, unit_state.reaction, unit_state.spirit,
                                                 unit_state.speed, unit_state.vitality, unit_state.hp, unit_state.mp,
                                                 unit_state.mp_regen, unit_state.direction]}
        json.dump(unit_entry, file)


# формула атаки
def attack_calc(attacker: UnitState, defender: UnitState):
    if attacker.weapon.damage_mod <= defender.armour.arm_mod:
        armour_hp_lost = defender.armour.arm_hp - attacker.weapon.damage_mod
        weapon_hp_lost = attacker.weapon.damage_mod
        return armour_hp_lost, weapon_hp_lost, 0, 'HIT!'
    else:
        armour_hp_lost = defender.armour.arm_hp - attacker.weapon.damage_mod
        unit_hp_lost = ((attacker.weapon.damage_mod - defender.armour.arm_mod)*(attacker.strength/defender.toughness))
        weapon_hp_lost = defender.armour.arm_hp
        return armour_hp_lost, weapon_hp_lost, unit_hp_lost, 'HIT!'


# формула попадания
def hit_calc(attacker: UnitState, defender: UnitState):
    if (attacker.weapon.w_accuracy + random.randint(1, 6)) >= (defender.reaction + random.randint(1, 6)):
        attack_calc(attacker, defender)
    else:
        return 0, 0, 0, 'MISS!'

def all_coordinates():
    for each_unit in all_units_list:
        all_current_coordinates[f'{each_unit.coordinates}'] = [each_unit.unit_id ,each_unit]
    return all_current_coordinates

'''
with open('session1/session_init/unit_db.json', 'r') as file:
    p = json.load(file)
    for n in p.values():
        s = UnitState(*n)
        print(s.weapon.weapon_name)
'''
create_unit_classes()
#print(all_units_list)
print(all_coordinates())

