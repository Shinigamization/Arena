# Создание изначальных БД юнитов, оружия, брони для страницы инструментов мастера
import json
from database_working import UnitWeapon, UnitArmour


# Создаёт dict персонажа в базе данных с ключом по ID
def create_char(unit_id, coordinates, player, armour, weapon, unit_class, strength, toughness, reaction, spirit, speed, vitality,
                hp, mp, mp_regen):
    with open('session1/session_init/armour_db.json', 'r') as file:
        temp_arm = json.load(file)[f'{armour}']
    with open('session1/session_init/weapons_db.json', 'r') as file:
        temp_weapon = json.load(file)[f'{weapon}']
    temp = {unit_id: [unit_id, coordinates, player, temp_arm, temp_weapon, unit_class, strength, toughness, reaction, spirit, speed, vitality,
                      hp, mp, mp_regen]}
    with open('session1/session_init/unit_db.json', 'r') as file:
        unit_db = json.load(file)
    unit_db.update(temp)
    with open('session1/session_init/unit_db.json', 'w') as file:
        json.dump(unit_db, file)


# очистка выбранной БД
def db_flush(session, db):
    with open(f'session{session}/{db}_db.json', 'w') as file:
        json.dump({}, file)


# Создание dict оружия в БД с ключом по ID
#            <!-- weapon_name, damage_mod, w_hp, w_accuracy, weight, ignore_arm, w_range, damage_type   -->
def create_weapon(weapon_name, damage_mod, w_hp, w_accuracy, w_weight, ignore_arm, w_range, damage_type):
    temp = {weapon_name: [weapon_name, damage_mod, w_hp, w_accuracy, w_weight, ignore_arm, w_range, damage_type]}
    with open('session1/session_init/weapons_db.json', 'r') as file:
        w_db = json.load(file)
    w_db.update(temp)
    with open('session1/session_init/weapons_db.json', 'w') as file:
        json.dump(w_db, file)


# Создание dict брони в БД с ключом по ID
#            <!-- arm_name, arm_mod, arm_hp, weight, element_type   -->
def create_armour(armour_name, arm_mod, arm_hp, arm_weight, element_type):
    temp = {armour_name: [armour_name, arm_mod, arm_hp, arm_weight, element_type]}
    with open('session1/session_init/armour_db.json', 'r') as file:
        arm_db = json.load(file)
    arm_db.update(temp)
    with open('session1/session_init/armour_db.json', 'w') as file:
        json.dump(arm_db, file)


# Создание dict карты с ключами коорданами и 'Empty' содержанием с сторонами Х на Х клеток
def map_init(x):
    with open('session1/map_tiles.json', 'w') as file:
        tiled_map = {}
        for a in range(x):
            for b in range(x):
                c = str(a+1) + '_' + str(b+1)
                tiled_map[c] = 'Empty'
        json.dump(tiled_map, file)


# map_init(13)
# db_flush(1, 'armour')
create_char('Dima1', '3_1' ,'Dima','Test2','Test1','fight', 'str','thp','react','spir','speed','vit','hp','mp','mp_reg')

'''
unit_id, coordinates, player, armour, weapon, unit_class, strength,
                 toughness, reaction, spirit, speed, vitality, hp, mp, mp_regen

unit_id, coordinates, player, armour, weapon, unit_class, strength, toughness, reaction, spirit, speed, vitality,
                hp, mp, mp_regen

'''