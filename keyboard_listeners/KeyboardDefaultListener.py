from pynput.keyboard import Listener
from abc import ABC
from models.Model import Model
from sounds import ascending_sound, descending_sound


class KeyboardDefaultListener:
    def __init__(self, model: Model):
        self.model = model
        self.listener = Listener(on_press=self.on_press)
        self.listener.start()

    def on_press(self, key):
        if hasattr(key, 'char'):
            key = key.char
            if key == ']':
                if self.model.status == 1:
                    descending_sound()
                    self.listener.stop()
                    self.model.stop()
