from __future__ import annotations

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from monitors.Monitor import Monitor
from sounds import low_sound
from subactions.SubAction import SubAction
from asyncio import sleep
import numpy as np
import asyncio
import keyboard
from devices.ArduinoKeyBoard import key_python_keyboard_maping


def get_distance(x1, x2):
    r = np.linalg.norm(x1-x2)
    return r


def get_angle_to_rotate(current_point, target, facing_angle):
    target_vector = target - current_point
    target_angle = np.angle(target_vector[0] + 1j*target_vector[1])
    angle_to_rotate = (target_angle - facing_angle + np.pi) % (2*np.pi) - np.pi
    return angle_to_rotate


class MoveToPoint(SubAction):
    distance_threshold = 3
    rotation_speed = 2.498
    left_rotation_key = 'arrow_left'
    right_rotation_key = 'arrow_right'
    forward_key = 'arrow_up'

    def __init__(self, *arg, **kwargs):
        super().__init__(*arg, **kwargs)
        self.target_coords = None
        self.is_acting = False
        self.is_rotating = False

    def set_target_coords(self, target_coords):
        self.target_coords = target_coords
        return self

    @property
    def success_condition(self):
        return self.parent_model.screen_scanner.state.is_combat_me

    @property
    def is_near_target(self):
        distance_to_target = get_distance(self.parent_model.screen_scanner.state.coords, self.target_coords['coords'])
        return distance_to_target < self.distance_threshold

    async def subact(self):
        self.parent_model.kb.release_all()
        self.is_acting = True
        if not self.target_coords.get('has_reward', False):
            await self.mount()
        await asyncio.gather(self.move_forward_if_needed(), self.rotate(), self.parent_model.straighten_camera())
        self.parent_model.kb.release_all()
        low_sound(length=0.5)

    async def move_forward_if_needed(self):
        while True:
            angle_to_target = get_angle_to_rotate(self.parent_model.screen_scanner.state.coords, self.target_coords['coords'], self.parent_model.screen_scanner.state.facing_angle)
            if keyboard.is_pressed(key_python_keyboard_maping[self.forward_key]):
                if abs(angle_to_target) > 60 / 180 * np.pi or abs(angle_to_target) > 30 / 180 * np.pi and self.is_near_target:
                    self.stop_moving()
            else:
                dist = get_distance(self.parent_model.screen_scanner.state.coords, self.target_coords['coords'])
                if abs(angle_to_target) < 60/180*np.pi and not self.is_near_target and not self.is_rotating:
                    if dist < 25:
                        await self.parent_model.kb.click([self.forward_key], delay=dist/16.25*0.8)
                    else:
                        self.start_moving()
            if self.is_near_target or not self.parent_model.screen_scanner.state.is_alive:
                self.stop_moving()
                self.is_acting = False
                break

            await sleep(0.01)

    async def rotate(self, only_if_needed=True):
        while True:
            angle_to_target = get_angle_to_rotate(self.parent_model.screen_scanner.state.coords, self.target_coords['coords'], self.parent_model.screen_scanner.state.facing_angle)
            if not only_if_needed or abs(angle_to_target) > 10 / 180 * np.pi:
                await self._rotate(angle_to_target)
            await sleep(0.5)
            if not self.is_acting:
                break

    async def _rotate(self, angle_to_rotate):
        turning_time = abs(angle_to_rotate) / self.rotation_speed
        if all(map(lambda k: not keyboard.is_pressed(key_python_keyboard_maping[k]), [self.left_rotation_key, self.right_rotation_key])):
            if angle_to_rotate > 0:
                rotation_key = self.left_rotation_key
            else:
                rotation_key = self.right_rotation_key
            self.is_rotating = True
            await self.parent_model.kb.click([rotation_key], delay=turning_time)
            await sleep(0.5)
            self.is_rotating = False

    def start_moving(self):
        self.parent_model.kb.press([self.forward_key])

    def stop_moving(self):
        self.parent_model.kb.release([self.forward_key])

    async def mount(self):
        if not self.parent_model.screen_scanner.state.is_mounted:
            await self.parent_model.kb.click(['left_alt', 'z'])
            await sleep(0.75)
