from __future__ import annotations

from typing import TYPE_CHECKING

from monitors.Monitor import Monitor

if TYPE_CHECKING:
    from keyboard_listeners.KeyboardDefaultListener import KeyboardDefaultListener
    from screen_scanner.ScreenScanner import ScreenScanner
    from devices.ArduinoKeyBoard import ArduinoKB
    from devices.ArduinoMouse import ArduinoMouse
from abc import ABC
import asyncio
import time
from utils.funcs import wait_until_not_pressed
from sounds import ascending_sound, low_sound


class Model(ABC):
    kb_listener: KeyboardDefaultListener
    need_location: bool

    def __init__(self, *, screen_scanner: ScreenScanner, kb: ArduinoKB | None, mouse: ArduinoMouse | None):
        self.screen_scanner = screen_scanner
        self.kb = kb
        self.mouse = mouse
        self.monitor = Monitor(screen_scanner=screen_scanner, parent_model=self)
        self.status = 0  # 0(not started)->1(started)->2(stopped)

    def stop(self):
        self.status = 2
        time.sleep(1)
        self.kb.release_all()

    def start(self):
        while self.screen_scanner.state.not_successful_consecutive_updates > 0:
            time.sleep(1)
        low_sound()
        wait_until_not_pressed('[')
        self.status = 1
        ascending_sound(parallel=False)
        asyncio.run(self._start())

    async def _start(self):
        pass

    async def straighten_camera(self):
        # await self.kb.click(['end'])
        # for _ in range(4):
        #     await self.kb.click(['page_down'])
        self.mouse.click('2')
