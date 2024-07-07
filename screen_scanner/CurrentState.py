import numpy as np
from dataclasses import dataclass


@dataclass
class CurrentState:
    is_alive: bool = None
    coords: np.array = None
    facing_angle: float = None
    is_combat_me: bool = None
    is_combat_target: bool = None
    target_is_hero: bool = None
    hp: float = None
    location: str = None
    updating_successfully: bool = None
    not_successful_consecutive_updates: int = 10
    mouse_facing_angle: float = None
    # target_id: int = None
    is_mounted: bool = None
    target_has_alch: bool = None
    target_has_lih: bool = None
    target_has_neurotoxin: bool = None
    is_nearby_enemy_combat_unit_without_neurotoxin: bool = None
    has_mogilnii_holod: bool = None

    def set_state(self, state_data, location_text):
        if len(state_data) != 13:
            raise ValueError('len(state_data) != 13')
        self.is_alive = bool(int(state_data[0]))
        self.coords = np.array([int(x) for x in [state_data[1], state_data[2]]])
        self.facing_angle = int(state_data[3]) / 100
        self.is_combat_me = bool(int(state_data[4]))
        self.is_combat_target = bool(int(state_data[5]))
        self.target_is_hero = bool(int(state_data[6]))
        self.hp = float(state_data[7]) / 100
        self.mouse_facing_angle = int(state_data[8]) / 100
        # self.target_id = int(state_data[9]) if int(state_data[9]) != 0 else None
        self.is_mounted = bool(int(state_data[9]))

        self.target_has_alch = bool(int(state_data[10][0]))
        self.target_has_lih = bool(int(state_data[10][1]))
        self.target_has_neurotoxin = bool(int(state_data[10][2]))

        self.is_nearby_enemy_combat_unit_without_neurotoxin = bool(int(state_data[11]))
        self.has_mogilnii_holod = bool(int(state_data[12]))
        self.location = location_text

    @property
    def target_has_all_dots(self):
        return self.target_has_alch and self.target_has_lih and self.target_has_neurotoxin
