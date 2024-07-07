from __future__ import annotations
from typing import TYPE_CHECKING

from actions.AttackMove import AttackMove
from models.Model import Model
from keyboard_listeners.KeyboardDefaultListener import KeyboardDefaultListener
from utils.trajectory_utils import load_trajectory
from utils.funcs import wait_until_not_pressed
from sounds import ascending_sound
import asyncio

if TYPE_CHECKING:
    from screen_scanner.ScreenScanner import ScreenScanner
    from devices.ArduinoKeyBoard import ArduinoKB


class FarmAlongPathModel_old(Model):
    def __init__(self, *, screen_scanner: ScreenScanner, kb: ArduinoKB, trajectory_name):
        super().__init__(screen_scanner=screen_scanner, kb=kb)
        self.trajectory = load_trajectory(trajectory_name)
        self.kb_listener = KeyboardDefaultListener(self)
        self.attack_move = AttackMove(screen_scanner=screen_scanner, kb=kb, trajectory=self.trajectory, )

    def start(self):
        wait_until_not_pressed('[')
        self.status = 1
        ascending_sound(parallel=False)
        asyncio.run(self._start())

    async def _start(self):
        loop = asyncio.get_running_loop()
        loop.create_task(self.attack_move.start())
        await self.wait_until_finish()
