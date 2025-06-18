import datetime
from functools import wraps
from subactions.SubAction import SubAction
from asyncio import sleep
from itertools import cycle
import asyncio


def sleep_c(sec):
    return lambda: sleep(sec)


def has_internal_cd(func):
    @wraps(func)
    def new_func(*args, **kwargs):
        args[0].last_skill_us_dttm[func.__name__] = datetime.datetime.now()
        return func(*args, **kwargs)

    new_func.has_internal_cd = True
    return new_func


class DoCombatRotation(SubAction):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.single_target = True
        self.queue = [self.agr_pet]
        self.dihanie_casts = 0
        self.last_skill_us_dttm = dict()

    def get_internal_last_cast(self, method_name):
        if not hasattr(getattr(self, method_name), 'has_internal_cd'):
            raise ValueError
        if method_name not in self.last_skill_us_dttm:
            return float('inf')
        return (datetime.datetime.now() - self.last_skill_us_dttm[method_name]).total_seconds()

    @property
    def success_condition(self):
        return not (self.parent_model.screen_scanner.state.is_combat_me
                    and self.parent_model.screen_scanner.state.is_combat_target
                    and not self.parent_model.screen_scanner.state.target_is_hero
                    and not self.parent_model.screen_scanner.state.target_is_invul
                    )

    async def subact(self):
        if not self.parent_model.screen_scanner.state.has_krovopuskanie and not self.parent_model.screen_scanner.state.is_krovopuskanie_in_cd and self.get_internal_last_cast('cast_krovopuskanie') > 2:
            self.queue.insert(0, self.cast_krovopuskanie)
        if len(self.queue) == 0:
            if self.get_internal_last_cast('cast_def') > 6 and self.parent_model.screen_scanner.state.hp < 0.5 and not self.parent_model.screen_scanner.state.is_def_in_cd:
                self.queue.extend([self.cast_def, sleep_c(0.9)])
            elif self.parent_model.screen_scanner.state.target_has_lih and not self.parent_model.screen_scanner.state.has_mrachnii_zhnec:
                self.queue.extend([self.cast_kasanie_smerti, sleep_c(0.9)])
            elif not self.parent_model.screen_scanner.state.target_has_lih and self.get_internal_last_cast('cast_lih') > 5:
                self.queue.extend([self.cast_lih, sleep_c(0.9)])
            elif not self.parent_model.screen_scanner.state.target_has_alch and not self.parent_model.screen_scanner.state.is_alch_in_cd and self.get_internal_last_cast('cast_alch') > 5:
                self.queue.extend([self.cast_alch, sleep_c(0.9)])
            elif not self.parent_model.screen_scanner.state.target_has_virus and self.get_internal_last_cast('cast_virus') > 5:
                self.queue.extend([self.cast_virus, sleep_c(0.9)])
            elif not self.parent_model.screen_scanner.state.target_has_neurotoxin and self.get_internal_last_cast('cast_neur') > 5:
                self.queue.extend([self.cast_neur, sleep_c(0.9)])
            else:
                self.queue.extend([self.cast_drain, sleep_c(0.9)])
            self.queue.extend([self.cast_dihanie, sleep_c(0.1)])
        await self.queue.pop(0)()

    async def reset(self):
        self.queue = [self.agr_pet]
        self.dihanie_casts = 0

    async def agr_pet(self):
        await self.parent_model.kb.click(['left_shift', '1'])

    @has_internal_cd
    async def cast_alch(self):
        await self.parent_model.kb.click(['3'])

    @has_internal_cd
    async def cast_kasanie_smerti(self):
        await self.parent_model.kb.click(['left_alt', '1'])

    @has_internal_cd
    async def cast_lih(self):
        await self.parent_model.kb.click(['left_alt', '3'])

    @has_internal_cd
    async def cast_neur(self):
        await self.parent_model.kb.click(['4'])

    @has_internal_cd
    async def cast_virus(self):
        await self.parent_model.kb.click(['f'])

    @has_internal_cd
    async def cast_krovopuskanie(self):
        await self.parent_model.kb.click(['left_alt', 'f'])

    async def cast_drain(self):
        await self.parent_model.kb.click(['1'])

    async def cast_dihanie(self):
        if self.parent_model.screen_scanner.state.has_mogilnii_holod:
            await self.parent_model.kb.click(['2'])
            self.dihanie_casts += 1

    @has_internal_cd
    async def cast_def(self):
        await self.parent_model.kb.click(['left_alt', 'q'])
