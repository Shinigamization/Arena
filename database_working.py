# Описание классов, функция записи текущего состояния юнита в БД, функции попадания, атаки

import json
import random
import functools
from typing import List, Any

all_units_list = []
all_current_coordinates = {}
unique_players = []
turn_phase = ['move_phase', 'attack_phase']
#pl_active_turn = ['Dima', 'Tima', 'Dima', 'Tima', 'Dima', 'Tima']
pl_active_turn = []
current_active_unit = []
possible_attack_points = []
log_comment = 'Nothing'

class UnitWeapon:
    def __init__(self, weapon_name, damage_mod, w_hp, w_accuracy, w_weight, ignore_arm, w_range, damage_type):
        self.weapon_name = weapon_name
        self.damage_mod = float(damage_mod.replace(',', '.'))
        self.w_hp = float(w_hp.replace(',', '.'))
        self.w_accuracy = int(w_accuracy)
        self.w_weight = float(w_weight.replace(',', '.'))
        self.ignore_arm = int(ignore_arm)
        self.w_range = int(w_range)
        self.damage_type = damage_type

    def dict_return(self):
        return {self.weapon_name: [self.weapon_name, self.damage_mod, self.w_hp, self.w_accuracy, self.w_weight,
                                   self.ignore_arm, self.w_range, self.damage_type]}

    def weapon_hp_loss(self, hp_loss):
        self.w_hp = self.w_hp - hp_loss


class UnitArmour:
    def __init__(self, armour_name, arm_mod, arm_hp, arm_weight, element_type):
        self.armour_name = armour_name
        self.arm_mod = float(arm_mod.replace(',', '.'))
        self.arm_hp = float(arm_hp.replace(',', '.'))
        self.arm_weight = float(arm_weight.replace(',', '.'))
        self.element_type = element_type

    def dict_return(self):
        return {self.armour_name: [self.armour_name, self.arm_mod, self.arm_hp, self.arm_weight, self.element_type]}

    def arm_hp_loss(self, hp_loss):
        self.arm_hp = self.arm_hp - hp_loss

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
        self.strength = int(strength)
        self.toughness = int(toughness)
        self.reaction = int(reaction)
        self.spirit = int(spirit)
        self.speed = int(speed)
        self.vitality = int(vitality)
        self.hp = float(hp.replace(',', '.'))
        self.mp = int(mp)
        self.mp_regen = int(mp_regen)
        self.direction = 'DOWN'

    def unit_coordinate_update(self, coordinate):
        self.coordinates = coordinate

    def unit_hp_loss(self, hp_loss):
        self.hp = self.hp - hp_loss


# Из .json базы куда записываются данные от мастера по юнитам, создаётся список объектов класса UnitState
def create_unit_classes():
    global all_units_list
    with open('session1/session_init/unit_db.json', 'r') as file:
        unit_db = dict(json.load(file))
        # создаёт отдельную переменную под каждый объект
        for unit_db_ids in unit_db.keys():
            all_units_list.append(exec(f'{unit_db_ids} = 1'))
        # трансформирует каждый объект в объект класса UnitState
        for counter in range(len(all_units_list)):
            all_units_list[counter] = UnitState(*list(unit_db.values())[counter])
        for each_unit in all_units_list:
            unique_players.append(each_unit.player) if each_unit.player not in unique_players else unique_players
    # print(all_units_list)


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
                                                 unit_state.armour.dict_return(), unit_state.weapon.dict_return(),
                                                 unit_state.unit_class, unit_state.strength,
                                                 unit_state.toughness, unit_state.reaction, unit_state.spirit,
                                                 unit_state.speed, unit_state.vitality, unit_state.hp, unit_state.mp,
                                                 unit_state.mp_regen, unit_state.direction]}
        json.dump(unit_entry, file)


# формула атаки
def attack_calc(attacker: UnitState, defender: UnitState):
    if attacker.weapon.damage_mod <= defender.armour.arm_mod:
        armour_hp_lost = defender.armour.arm_hp - attacker.weapon.damage_mod
        weapon_hp_lost = attacker.weapon.damage_mod
        attacker.weapon.weapon_hp_loss(weapon_hp_lost)
        defender.armour.arm_hp_loss(armour_hp_lost)
        return armour_hp_lost, weapon_hp_lost, 0, 'HIT!'
    else:
        armour_hp_lost = defender.armour.arm_hp - attacker.weapon.damage_mod
        unit_hp_lost = (
                    (attacker.weapon.damage_mod - defender.armour.arm_mod) * (attacker.strength / defender.toughness))
        weapon_hp_lost = defender.armour.arm_hp
        attacker.weapon.weapon_hp_loss(weapon_hp_lost)
        defender.armour.arm_hp_loss(armour_hp_lost)
        defender.unit_hp_loss(unit_hp_lost)
        return armour_hp_lost, weapon_hp_lost, unit_hp_lost, 'HIT!'


# формула попадания
def hit_calc(attacker: UnitState, defender: UnitState):
    if (attacker.weapon.w_accuracy + random.randint(1, 6)) >= (defender.reaction + random.randint(1, 6)):
        attack_calc(attacker, defender)
    else:
        return 0, 0, 0, 'MISS!'


def update_all_coordinates(moved_unit, coordinates_now):
    for n in all_units_list:  # Вспомнить как писать цикл for и if в одну строку
        if n.unit_id == (moved_unit):
            n.unit_coordinate_update(coordinates_now)
    all_current_coordinates = {}
    for each_unit in all_units_list:
        all_current_coordinates[f'{each_unit.coordinates}'] = [each_unit.unit_id, each_unit]
    return all_current_coordinates


# Создание последовательности ходов
def create_move_sequence():
    global pl_active_turn
    for n in range(3):
        for each in unique_players:
            pl_active_turn.append(each)


# Функция смены фазы хода
def turn_phase_forward():
    global turn_phase
    turn_phase.reverse()


# Функция смены хода
def turn_forward():
    global pl_active_turn
    if turn_phase[0] != 'move_phase':
        pl_active_turn.pop(0)
    turn_phase_forward()
    if pl_active_turn == []:
        create_move_sequence()
        round_forward()


# Функция смены раунда
def round_forward():
    pass


# Вернуть нужный Юнит объект от unit_id строки
def return_unit_object_by_name(func):
    @functools.wraps(func)
    def unit_by_name(unit):
        for n in all_units_list:
            if n.unit_id == unit:
                return func(n)
    return unit_by_name


# определение возможных целей для атаки
@return_unit_object_by_name
def possible_attack_targets(unit: UnitState):
    starting_point = unit.coordinates.split('_')
    possible_attack_cells = []
    if unit.weapon.w_range == 1:
        for n in range(-unit.weapon.w_range, unit.weapon.w_range+1):
            new_x = (str(int(starting_point[0]) + n) + '_' + str(int(starting_point[1])))
            new_y = (str(int(starting_point[0])) + '_' + str(int(starting_point[1]) + n))
            possible_attack_cells.append(new_x)
            possible_attack_cells.append(new_y)
        possible_attack_cells.remove(unit.coordinates)
        possible_attack_cells.remove(unit.coordinates)
        return possible_attack_cells


@return_unit_object_by_name
def determine_unit(unit):
    return unit

'''
with open('session1/session_init/unit_db.json', 'r') as file:
    p = json.load(file)
    for n in p.values():
        s = UnitState(*n)
        print(s.weapon.weapon_name)
'''
# create_unit_classes()
# print(all_units_list)
# update_unit()
# print(update_all_coordinates())
# print(unique_players)
