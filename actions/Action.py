from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from screen_scanner.ScreenScanner import ScreenScanner
from devices.ArduinoKeyBoard import ArduinoKB
from abc import ABC, abstractmethod
from asyncio import sleep
from models import Model


class Action(ABC):
    def __init__(self, parent_model: Model):
        self.parent_model = parent_model
        self.is_acting = False
