from datetime import date
from pony.orm import *

db = Database()
db.bind(provider='sqlite', filename='database.sqlite', create_db=True)

class Player(db.Entity):
    id = PrimaryKey(int, auto=True)
    active_abilities = Set('ActiveAbility')
    round_log_records = Set('RoundRecord')
    session = Required('Session')
    user = Required('User')
    turn_number = Required(int)  # Очередность ходов
    units = Set('Unit')


class UnitState(db.Entity):
    id = PrimaryKey(int, auto=True)
    unit = Required('Unit')
    armour = Required('Armour')
    weapon = Required('Weapon')
    unit_class = Required('UnitClass')
    strength = Required(int)
    toghness = Required(int)
    reaction = Required(int)
    spirit = Required(int)
    speed = Required(int)
    vitality = Required(int)
    hp = Required(float)
    mp = Required(int)
    mp_regen = Required(int)
    passive_abilities = Set('PassiveAbility')
    active_abilities = Set('ActiveAbility')
    round_logs = Set('RoundRecord')
    unit_direction = Optional(str)
    can_act = Required(bool)
    x_pos = Required(int)
    y_pos = Required(int)
    round = Required('Round')


class Weapon(db.Entity):
    id = PrimaryKey(int, auto=True)
    name = Required(str)
    unitstates = Set(UnitState)
    damage_mod = Required(float)
    hp = Required(float)
    accuarcy = Required(int)
    weight = Required(float)
    ignore_armor = Optional(float)
    ignore_toughness = Optional(float)
    reaction_bonus = Optional(int)
    range_bonus = Required(int)
    damage_type = Required(str)
    session = Required('Session')


class Armour(db.Entity):
    id = PrimaryKey(int, auto=True)
    name = Required(str)
    unitstates = Set(UnitState)
    block_damage_mod = Required(float)
    hp = Required(float)
    weight = Required(float)
    session = Required('Session')


class UnitClass(db.Entity):
    id = PrimaryKey(int, auto=True)
    unitstates = Set(UnitState)
    name = Required(str)
    phys_damage_bonus = Optional(float)
    mag_damage_bonus = Optional(float)
    block_damage_bonus = Optional(float)
    active_abilities = Set('ActiveAbility')


class PassiveAbility(db.Entity):
    id = PrimaryKey(str, auto=True)
    unitstates = Set(UnitState)
    weight_bonus = Optional(float)
    session = Required('Session')


class ActiveAbility(db.Entity):
    id = PrimaryKey(int, auto=True)
    unitstates = Set(UnitState)
    players = Set(Player)
    unit_classs = Set(UnitClass)
    ability_visible = Required(bool)
    range = Required(int)
    area_of_effect = Optional(int)
    hostile_status = Required(bool)  # Can pick friends or enemies as target
    round_logs = Set('RoundRecord')
    use_weapon = Required(bool)
    damage_mod = Required(float)
    buff_rounds = Optional(int)
    mp_price = Required(int)
    vitality_price = Required(int)
    damage_type = Optional(str)
    session = Required('Session')


class MapTile(db.Entity):
    id = PrimaryKey(int, auto=True)
    passable = Required(bool)
    speed_cost = Required(int)
    x_pos = Required(int)
    y_pos = Required(int)
    session = Required('Session')


class RoundRecord(db.Entity):
    id = PrimaryKey(int, auto=True)
    player = Required(Player)
    unitstates = Set(UnitState)
    active_ability = Required(ActiveAbility)
    movement = Required(str)
    session = Required('Session')
    turn_number = Required(int)
    x_pos_from = Required(int)
    y_pos_from = Required(int)
    x_pos_to = Required(int)
    y_pos_to = Required(int)
    round = Required('Round')
    unit = Required('Unit')


class Session(db.Entity):
    id = PrimaryKey(int, auto=True)
    Date = Required(date)
    players = Set(Player)
    weapons = Set(Weapon)
    armours = Set(Armour)
    passive_abilities = Set(PassiveAbility)
    active_abilities = Set(ActiveAbility)
    round_logs = Set(RoundRecord)
    ActiveTurnNum = Required(int)
    ActivePlayer = Required(int)
    map_tiles = Set(MapTile)
    rounds = Set('Round')
    map_height = Required(int)
    map_width = Required(int)
    state = Required(str)


class User(db.Entity):
    id = PrimaryKey(int, auto=True)
    players = Set(Player)
    nickname = Required(str)


class Unit(db.Entity):
    id = PrimaryKey(int, auto=True)
    player = Required(Player)
    name = Required(str)
    unit_states = Set(UnitState)
    round_logs = Set(RoundRecord)


class Round(db.Entity):
    id = PrimaryKey(int, auto=True)
    session = Required(Session)
    unit_states = Set(UnitState)
    number = Required(int)
    round_logs = Set(RoundRecord)


db.generate_mapping(create_tables=True)

