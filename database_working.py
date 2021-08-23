import json


#
class UnitState:
    def __init__(self, unit_id, coordinates, player, armour, unit_class, strength, toughness, reaction, spirit, speed,
                 vitality, hp, mp, mp_regen):
        # self.session = # for new sessions, may implement later
        self.current_round = 1  # Current round number
        self.active_status = 'Active'  # Has moved in round or not
        self.coordinates = coordinates
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
        self.direction = 'DOWN'


def update_unit(unit_state: UnitState):
    with open(f'session1/{unit_state.unit_id}.json', 'w+') as file:
        unit_entry = {unit_state.current_round: [unit_state.coordinates, unit_state.active_status, unit_state.player,
                                                 unit_state.armour, unit_state.unit_class, unit_state.strength,
                                                 unit_state.toughness, unit_state.reaction, unit_state.spirit,
                                                 unit_state.speed, unit_state.vitality, unit_state.hp, unit_state.mp,
                                                 unit_state.mp_regen, unit_state.direction]}
        json.dump(unit_entry, file)
