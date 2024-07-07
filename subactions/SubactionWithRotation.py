from subactions.SubAction import SubAction
from asyncio import sleep
from itertools import cycle
import asyncio
from abc import ABC


def sleep_c(sec):
    return lambda: sleep(sec)


class SubactionWithRotation(ABC, SubAction):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rotation = []
        self.rotation_gen = None

    async def reset(self):
        self.rotation_gen = cycle(self.rotation)

    async def subact(self):
        if self.rotation_gen is None:
            await self.reset()
        try:
            await next(self.rotation_gen)()
        except TypeError:
            a = 3