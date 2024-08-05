import keyboard
from devices.keymaping import key_arduino_code_mapping, keyboard_mapping

keys_to_ensure_status = list(keyboard_mapping.keys())


class KeyboardValidator:
    def __init__(self, keys, action_name):
        self.keys = keys
        self.action_name = action_name

    def validate(self):
        is_pressed = self.action_name == 'press'
        bad_keys = [key for key in self.keys if key not in keys_to_ensure_status]
        if bad_keys:
            raise ValueError(f'Validating not in keys_to_ensure_status keys: {bad_keys}')
        return all([keyboard.is_pressed(keyboard_mapping[key]) == is_pressed for key in self.keys if
                    key in keys_to_ensure_status])

    def stop(self):
        pass
