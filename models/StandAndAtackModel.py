from __future__ import annotations
from typing import TYPE_CHECKING
import numpy as np
from actions.FightAction import FightAction
from subactions.MoveToPoint import MoveToPoint
from models.Model import Model
from keyboard_listeners.KeyboardDefaultListener import KeyboardDefaultListener
from utils.trajectory_utils import load_trajectory
from utils.funcs import wait_until_not_pressed
from sounds import ascending_sound
import datetime
import asyncio
from asyncio import sleep

if TYPE_CHECKING:
    from screen_scanner.ScreenScanner import ScreenScanner
    from devices.ArduinoKeyBoard import ArduinoKB
    from devices.ArduinoMouse import ArduinoMouse


class StandAndAtackModel(Model):
    def __init__(self, *, screen_scanner: ScreenScanner, kb: ArduinoKB, mouse: ArduinoMouse):
        super().__init__(screen_scanner=screen_scanner, kb=kb, mouse=mouse)
        self.kb_listener = KeyboardDefaultListener(self)
        self.fight_action = FightAction(parent_model=self, first_search_delay=15)
        self.move = MoveToPoint(parent_model=self, use_mount=False)
        self.last_move_dt = None
        self.target_coords = None

    async def _start(self):
        loop = asyncio.get_running_loop()
        loop.create_task(self.monitor.start_monitor())
        loop.create_task(self.run_position_monitor())
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

    async def run_position_monitor(self):
        self.target_coords = np.array(self.screen_scanner.state.coords)
        self.move.set_target_coords({'coords': self.target_coords})
        self.last_move_dt = datetime.datetime.now()
        while True:
            if self.status == 2:
                break
            if (datetime.datetime.now() - self.last_move_dt).total_seconds() >   200 and not self.screen_scanner.state.is_combat_me:
                self.fight_action.is_acting = False
                await self.move.subact()
                self.fight_action.is_acting = True
                self.last_move_dt = datetime.datetime.now()
            await sleep(0.1)


