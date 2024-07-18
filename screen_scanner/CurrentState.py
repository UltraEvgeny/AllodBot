import numpy as np
from dataclasses import dataclass


@dataclass
class CurrentState:
    location: str = None
    updating_successfully: bool = None
    not_successful_consecutive_updates: int = 10

    coords: np.array = None
    hp: float = None
    hero_facing_angle: float = None
    camera_facing_angle: float = None

    is_alive: bool = None
    is_combat_me: bool = None
    is_combat_target: bool = None
    target_is_invul: bool = None
    target_is_hero: bool = None
    is_mounted: bool = None
    has_mogilnii_holod: bool = None
    has_krovopuskanie: bool = None
    target_has_alch: bool = None
    target_has_lih: bool = None
    target_has_neurotoxin: bool = None
    target_has_virus: bool = None
    is_alch_in_cd: bool = None
    is_krovopuskanie_in_cd: bool = None

    def set_state(self, state_data, location_text):
        if len(state_data) != 6:
            raise ValueError('len(state_data) != 6')
        self.location = location_text

        self.coords = np.array([int(x) for x in [state_data[0], state_data[1]]])
        self.hp = float(state_data[2]) / 100
        self.hero_facing_angle = int(state_data[3]) / 100
        self.camera_facing_angle = int(state_data[4]) / 100
        
        mask_data = [int(m) for m in state_data[5]]

        self.is_alive = bool(mask_data[0])
        self.is_combat_me = bool(mask_data[1])
        self.is_combat_target = bool(mask_data[2])
        self.target_is_invul = bool(mask_data[3])
        self.target_is_hero = bool(mask_data[4])
        self.is_mounted = bool(mask_data[5])
        self.has_mogilnii_holod = bool(mask_data[6])
        self.has_krovopuskanie = bool(mask_data[7])
        self.target_has_alch = bool(mask_data[8])
        self.target_has_lih = bool(mask_data[9])
        self.target_has_neurotoxin = bool(mask_data[10])
        self.target_has_virus = bool(mask_data[11])
        self.is_alch_in_cd = bool(mask_data[12])
        self.is_krovopuskanie_in_cd = bool(mask_data[13])

    @property
    def target_has_all_dots(self):
        return self.target_has_alch and self.target_has_lih and self.target_has_neurotoxin
