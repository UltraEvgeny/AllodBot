import re

template = '''\
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
{state_declarations}

    def set_state(self, state_data, location_text):
        if len(state_data) != 6:
            raise ValueError('len(state_data) != 6')
        self.location = location_text

        self.coords = np.array([int(x) for x in [state_data[0], state_data[1]]])
        self.hp = float(state_data[2]) / 100
        self.hero_facing_angle = int(state_data[3]) / 100
        self.camera_facing_angle = int(state_data[4]) / 100
        
        mask_data = [int(m) for m in state_data[5]]
{state_assignments}

    @property
    def target_has_all_dots(self):
        return self.target_has_alch and self.target_has_lih and self.target_has_neurotoxin
'''

lua_script_path = 'ACords/Script.lua'
state_class_path = 'screen_scanner/CurrentState.py'
with open(lua_script_path, 'r', encoding='windows-1251') as f:
    lua_script = f.read()

script_mask_part = re.findall(r'\t\t\t----- mask start\n(.*)\t\t\t----- mask end\n', lua_script, re.DOTALL)[0]
mask_fields = [re.findall(r'.*--# (.*)', x)[0] for x in script_mask_part.split('\n') if x]
state_declarations = ''
state_assignments = ''
for i, m in enumerate(mask_fields):
    state_declarations += f'\n    {m}: bool = None'
    state_assignments += f'\n        self.{m} = bool(mask_data[{i}])'

current_state_class_script = template.replace('{state_declarations}', state_declarations).replace('{state_assignments}', state_assignments)

with open(state_class_path, 'w', encoding='windows-1251') as f:
    f.write(current_state_class_script)
