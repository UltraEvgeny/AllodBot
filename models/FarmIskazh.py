from __future__ import annotations
from typing import TYPE_CHECKING
from utils.funcs import yaml_load

from actions.AttackMove import AttackMove, get_nearest_point_i, forward_backward_generator
from actions.FightAction import FightAction
from models.Model import Model
from keyboard_listeners.KeyboardDefaultListener import KeyboardDefaultListener
import numpy as np
from utils.trajectory_utils import load_trajectory
from utils.funcs import wait_until_not_pressed
from sounds import ascending_sound
import asyncio
from subactions.MoveToPoint import MoveToPoint
from asyncio import sleep
import time
from monitors.EventLogger import write_to_log

if TYPE_CHECKING:
    from screen_scanner.ScreenScanner import ScreenScanner
    from devices.ArduinoKeyBoard import ArduinoKB
    from devices.ArduinoMouse import ArduinoMouse


class FarmIskazh(Model):
    def __init__(self, *, screen_scanner: ScreenScanner, kb: ArduinoKB, mouse: ArduinoMouse, trajectory_name):
        super().__init__(screen_scanner=screen_scanner, kb=kb, mouse=mouse)
        self.kb_listener = KeyboardDefaultListener(self)
        self.fight_action = FightAction(parent_model=self)
        self.move = MoveToPoint(parent_model=self)
        self.trajectory = load_trajectory(trajectory_name)
        self.iskazhs = ['iskazh_ice']
        self.loc_names = [yaml_load(f'trajectories/{iskazh}.yaml')[0]['loc'] for iskazh in self.iskazhs]

    async def on_death(self):
        await self.accept_death()
        await sleep(10)
        await self.leave_iskazh()

    async def _start(self):
        loop = asyncio.get_running_loop()
        loop.create_task(self.monitor.start_monitor())
        dispatcher_task = loop.create_task(self.run_dispatcher())
        loop.create_task(self.fight_action.start_listening())
        await dispatcher_task

    async def run_dispatcher(self):
        write_to_log({'event': 'session_start'})
        while True:
            write_to_log({'event': 'starting_enter_specific_iskazh'})
            await self.enter_specific_iskazh()
            for cur_target in self.trajectory:
                self.move.set_target_coords(cur_target)
                write_to_log({'event': 'move', 'target': self.move.target_coords})
                await self.move.subact()
                if self.screen_scanner.state.is_combat_me or 'fight' in cur_target.keys():
                    if 'fight' in cur_target.keys():
                        self.fight_action.set_single_target(cur_target['fight']['single_target'])
                    write_to_log({'event': 'kill_all', 'target': self.move.target_coords})
                    await self.fight_action.kill_all(only_one_combat=True)
                    if not self.screen_scanner.state.is_alive:
                        write_to_log({'event': 'death', 'target': self.screen_scanner.state.coords})
                        await self.on_death()
                        break
                if cur_target.get('has_reward', False):
                    await self.kb.click(['left_alt', 'x'], delay=0.2)
                    print('picked!!')
            else:
                await self.leave_iskazh(completed=True)

    async def enter_iskazh(self, delay=2):
        await self.kb.click(['left_control', 'm'])
        await self.mouse.move_mouse([0.36822917, 0.7287037])
        self.mouse.click()
        await self.mouse.move_mouse([0.49427083, 0.40555556])
        self.mouse.click()
        await self.mouse.move_mouse([0.3796875, 0.63240741])
        self.mouse.click()
        await self.mouse.move_mouse([0.68802083, 0.69722222])
        self.mouse.click()
        await self.mouse.move_mouse([0.4703125, 0.49259259])
        self.mouse.click()
        await self.wait_until_load(leave_locations=['Личный аллод'])

    async def leave_iskazh(self, completed=False, delay=2):
        await self.mouse.move_mouse([0.85520833, 0.08981481])
        self.mouse.click()
        confirm_leave_coords = [0.49166667, 0.51296296] if completed else [0.46770833, 0.47592593]
        await self.mouse.move_mouse(confirm_leave_coords)
        self.mouse.click()
        await self.wait_until_load(target_locations=['Личный аллод'])

    async def accept_death(self):
        await self.mouse.move_mouse([0.4984375, 0.48240741])
        self.mouse.click()

    async def enter_specific_iskazh(self):
        while True:
            await self.enter_iskazh()
            write_to_log({'event': 'enter_iskazh', 'location': self.screen_scanner.state.location, })
            if self.screen_scanner.state.location in self.loc_names:
                break
            else:
                await self.leave_iskazh()
        return

    async def wait_until_load(self, target_locations: list[str] | None = None, leave_locations: list[str] | None = None):
        if target_locations is not None:
            while self.screen_scanner.state.location not in target_locations:
                await sleep(0.1)
        if leave_locations is not None:
            while self.screen_scanner.state.location in leave_locations:
                await sleep(0.1)
