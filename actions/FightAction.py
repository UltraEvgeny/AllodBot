from __future__ import annotations

from threading import Thread
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from models.Model import Model
    from screen_scanner.CurrentState import CurrentState
from devices.ArduinoKeyBoard import ArduinoKB


from subactions.StartNonHeroCombat import StartNonHeroCombat
from subactions.FindNonHeroCombatTarget import FindNonHeroCombatTarget
from subactions.DoCombatRotation import DoCombatRotation
from actions.Action import Action
from itertools import cycle
from asyncio import sleep


def sleep_c(sec):
    return lambda: sleep(sec)


class FightAction(Action):
    def __init__(self, first_search_delay, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.start_nonhero_combat = StartNonHeroCombat(*args, **kwargs)
        self.find_nonhero_combat_target = FindNonHeroCombatTarget(*args, **kwargs)
        self.do_combat_rotation = DoCombatRotation(*args, **kwargs)
        self.kill_all_search_time = 4
        self.first_search_delay = first_search_delay
        self.subaction_seq = [
            lambda: self.start_nonhero_combat.subact_until_success(self),
            lambda: self.find_nonhero_combat_target.subact_until_success(self),
            lambda: self.do_combat_rotation.subact_until_success(self),
        ]

    async def start_listening(self):
        while True:
            if self.is_acting:
                for subaction in cycle(self.subaction_seq):
                    await subaction()
                    if not self.is_acting:
                        break
            await sleep(0)

    async def kill_all(self, only_one_combat=False):
        self.is_acting = True
        await sleep(self.first_search_delay)
        while True:
            if only_one_combat:
                if not self.parent_model.screen_scanner.state.is_combat_me:
                    self.is_acting = False
                    break
                await sleep(0.1)
            else:
                if self.parent_model.monitor.out_of_combat_seconds > self.kill_all_search_time:
                    self.is_acting = False
                    await sleep(2)
                    if self.parent_model.monitor.out_of_combat_seconds > 5:
                        break
                    self.is_acting = True
                await sleep(0.1)

    def set_single_target(self, value):
        self.find_nonhero_combat_target.single_target = value
        self.do_combat_rotation.single_target = value
