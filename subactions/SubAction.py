from __future__ import annotations
from typing import TYPE_CHECKING

from actions.Action import Action
from models.Model import Model

if TYPE_CHECKING:
    from screen_scanner.ScreenScanner import ScreenScanner
from devices.ArduinoKeyBoard import ArduinoKB
from abc import ABC, abstractmethod


class SubAction:
    def __init__(self, parent_model: Model):
        self.parent_model = parent_model

    @property
    @abstractmethod
    def success_condition(self):
        pass

    @abstractmethod
    async def subact(self):
        pass

    async def reset(self):
        pass

    async def subact_until_success(self, parent: Action):
        while not self.success_condition and parent.is_acting:
            await self.subact()
        await self.reset()
