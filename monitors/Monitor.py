from __future__ import annotations

from typing import TYPE_CHECKING

from monitors.EventLogger import write_to_log
from print_all_key_pressed import get_all_keys_pressed

if TYPE_CHECKING:
    from keyboard_listeners.KeyboardDefaultListener import KeyboardDefaultListener
    from screen_scanner.ScreenScanner import ScreenScanner
    from devices.ArduinoKeyBoard import ArduinoKB
    from models.Model import Model
from asyncio import sleep
from datetime import datetime
import asyncio


class Monitor:
    def __init__(self, *, screen_scanner: ScreenScanner, parent_model: Model):
        self.screen_scanner = screen_scanner
        self.parent_model = parent_model
        self.cur_target_selection_time = 0
        self.nocombat_start_dt = datetime.now()
        self.cur_target_selection_dt = None
        self.cur_target_id = None
        self.last_release_add_dt = datetime.now()

    async def start_monitor(self):
        while not self.parent_model.status == 2:
            if self.parent_model.screen_scanner.state.is_combat_me:
                self.nocombat_start_dt = None
            elif self.nocombat_start_dt is None:
                self.nocombat_start_dt = datetime.now()
            keys_pressed = await get_all_keys_pressed()
            write_to_log({'keys_pressed': keys_pressed})
            print(keys_pressed)
            if (datetime.now() - self.last_release_add_dt).total_seconds() > 10:
                self.parent_model.kb.release_all()
                write_to_log({'release_all': keys_pressed})
                self.last_release_add_dt = datetime.now()

            await sleep(0.1)

    @property
    def out_of_combat_seconds(self):
        return 0 if self.nocombat_start_dt is None else (datetime.now() - self.nocombat_start_dt).total_seconds()
