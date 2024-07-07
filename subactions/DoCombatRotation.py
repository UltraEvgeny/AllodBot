from subactions.SubAction import SubAction
from asyncio import sleep
from itertools import cycle
import asyncio


def sleep_c(sec):
    return lambda: sleep(sec)


class DoCombatRotation(SubAction):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.single_target = True
        self.queue = [self.agr_pet]
        self.dihanie_casts = 0

    @property
    def success_condition(self):
        if self.single_target:
            return not (self.parent_model.screen_scanner.state.is_combat_me
                        and self.parent_model.screen_scanner.state.is_combat_target
                        and not self.parent_model.screen_scanner.state.target_is_hero)
        else:
            return not (self.parent_model.screen_scanner.state.is_combat_me
                        and self.parent_model.screen_scanner.state.is_combat_target
                        and not self.parent_model.screen_scanner.state.target_is_hero
                        and (not self.parent_model.screen_scanner.state.target_has_all_dots
                             or not self.parent_model.screen_scanner.state.is_nearby_enemy_combat_unit_without_neurotoxin
                             or self.dihanie_casts <= 2))

    async def subact(self):
        if len(self.queue) == 0:
            if not self.parent_model.screen_scanner.state.target_has_alch:
                self.queue.extend([self.cast_alch, sleep_c(0.5)])
            elif not self.parent_model.screen_scanner.state.target_has_lih:
                self.queue.extend([self.cast_lih, sleep_c(0.5)])
            elif not self.parent_model.screen_scanner.state.target_has_neurotoxin:
                self.queue.extend([self.cast_neur, sleep_c(0.5)])
            else:
                self.queue.extend([self.cast_drain, sleep_c(0.5)])
            self.queue.extend([self.cast_dihanie, sleep_c(0.5)])
        await self.queue.pop(0)()

    async def reset(self):
        self.queue = [self.agr_pet]
        self.dihanie_casts = 0

    async def agr_pet(self):
        await self.parent_model.kb.click(['left_shift', '1'])

    async def cast_alch(self):
        await self.parent_model.kb.click(['3'])

    async def cast_lih(self):
        await self.parent_model.kb.click(['left_alt', '3'])

    async def cast_neur(self):
        await self.parent_model.kb.click(['4'])

    async def cast_drain(self):
        await self.parent_model.kb.click(['1'])

    async def cast_dihanie(self):
        if self.parent_model.screen_scanner.state.has_mogilnii_holod:
            await self.parent_model.kb.click(['2'])
            self.dihanie_casts += 1

