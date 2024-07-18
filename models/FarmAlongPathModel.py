from __future__ import annotations
from typing import TYPE_CHECKING

from actions.FightAction import FightAction
from models.Model import Model
from keyboard_listeners.KeyboardDefaultListener import KeyboardDefaultListener
import numpy as np
from utils.trajectory_utils import load_trajectory, forward_backward_generator, get_nearest_point_i
from utils.funcs import wait_until_not_pressed
from sounds import ascending_sound
import asyncio
from subactions.MoveToPoint import MoveToPoint
from asyncio import sleep

if TYPE_CHECKING:
    from screen_scanner.ScreenScanner import ScreenScanner
    from devices.ArduinoKeyBoard import ArduinoKB
    from devices.ArduinoMouse import ArduinoMouse


class FarmAlongPathModel(Model):
    def __init__(self, *, screen_scanner: ScreenScanner, kb: ArduinoKB, mouse: ArduinoMouse, trajectory_name):
        super().__init__(screen_scanner=screen_scanner, kb=kb, mouse=mouse)
        self.kb_listener = KeyboardDefaultListener(self)
        self.fight_action = FightAction(screen_scanner=screen_scanner, kb=kb)
        self.move = MoveToPoint(screen_scanner=screen_scanner, kb=kb, monitor=self.monitor)
        self.trajectory = load_trajectory(trajectory_name)

    async def _start(self):
        loop = asyncio.get_running_loop()
        loop.create_task(self.monitor.start_monitor())
        dispatcher_task = loop.create_task(self.run_dispatcher())
        loop.create_task(self.fight_action.start_listening())
        await dispatcher_task

    async def run_dispatcher(self):
        nearest_i = get_nearest_point_i(self.screen_scanner.state.coords, np.array([x['coords'] for x in self.trajectory]))
        print(nearest_i)
        path_gen = forward_backward_generator(self.trajectory, initial_i=nearest_i)
        await sleep(4)
        while True:
            await self.fight_action.kill_all()
            self.move.set_target_coords(next(path_gen))
            await self.move.subact()
