from __future__ import annotations
from keyboard_listeners.KeyboardDefaultListener import KeyboardDefaultListener
from sounds import ascending_sound, descending_sound, high_sound
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from models.PathCreatorModel import PathCreatorModel


class KeyboardPathCreatorDefaultListener(KeyboardDefaultListener):
    model: PathCreatorModel

    def on_press(self, key):
        if hasattr(key, 'char'):
            key = key.char
            updating_successfully = self.model.screen_scanner.state.updating_successfully
            if key == ";" and updating_successfully:
                self.model.make_checkpoint({})
                high_sound()
            elif key == "'" and updating_successfully:
                self.model.make_checkpoint({'fight': {'single_target': False}})
                high_sound()
            elif key == "\\" and updating_successfully:
                self.model.make_checkpoint({'has_reward': True})
                high_sound()
            elif key == ']' and updating_successfully:
                self.listener.stop()
                self.model.stop()
                descending_sound()
