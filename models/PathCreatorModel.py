from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from screen_scanner.ScreenScanner import ScreenScanner

from models.Model import Model
from screen_scanner.ScreenScanner import ScreenScanner
from keyboard_listeners.KeyboardPathCreatorListener import KeyboardPathCreatorDefaultListener
from utils.funcs import yaml_dump


class PathCreatorModel(Model):
    need_location = True

    def __init__(self, *, screen_scanner: ScreenScanner = None, name=None):
        super().__init__(screen_scanner=screen_scanner, kb=None, mouse=None)
        self.name = name
        self.kb_listener = KeyboardPathCreatorDefaultListener(self)
        self.path = []

    def make_checkpoint(self, add_params: dict):
        if self.screen_scanner.updating_successfully:
            self.path.append({**{'coords': self.screen_scanner.state.coords.tolist(), 'loc': self.screen_scanner.state.location},
                              **add_params},)

    def stop(self):
        yaml_dump(self.path, f'trajectories/{self.name}.yaml')
