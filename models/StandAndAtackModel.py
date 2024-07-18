from __future__ import annotations
from typing import TYPE_CHECKING

from actions.FightAction import FightAction
from models.Model import Model
from keyboard_listeners.KeyboardDefaultListener import KeyboardDefaultListener
from utils.trajectory_utils import load_trajectory
from utils.funcs import wait_until_not_pressed
from sounds import ascending_sound
import asyncio
from asyncio import sleep

if TYPE_CHECKING:
    from screen_scanner.ScreenScanner import ScreenScanner
    from devices.ArduinoKeyBoard import ArduinoKB


class StandAndAtackModel(Model):
    def __init__(self, *, screen_scanner: ScreenScanner, kb: ArduinoKB):
        super().__init__(screen_scanner=screen_scanner, kb=kb)
        self.kb_listener = KeyboardDefaultListener(self)
        self.fight_action = FightAction(screen_scanner=screen_scanner, kb=kb)

    async def _start(self):
        loop = asyncio.get_running_loop()
        loop.create_task(self.monitor.start_monitor())
        dispatcher_task = loop.create_task(self.run_dispatcher())
        loop.create_task(self.fight_action.start_listening())
        await dispatcher_task

    async def run_dispatcher(self):
        self.fight_action.is_acting = True
        while True:
            if self.status == 2:
                self.fight_action.is_acting = False
                break
            await sleep(0.1)
        print('end disp')

