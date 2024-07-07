from actions.Action import Action
from threading import Thread
import numpy as np
from asyncio import sleep


class SimpleMovingAction(Action):
    rotation_speed = 2.498
    left_rotation_key = 'arrow_left'
    right_rotation_key = 'arrow_right'
    forward_key = 'arrow_up'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.is_moving = False
        self.is_rotating = False

    def move_forward_if_needed(self, angle_to_target, distance_to_target):
        if 'arrow_up' in self.kb.pressed:
            if abs(angle_to_target) > 60 / 180 * np.pi or (abs(angle_to_target) > 30 / 180 * np.pi and distance_to_target < 20):
                self.stop_moving()
        else:
            if abs(angle_to_target) < 60/180*np.pi:
                self.start_moving()

    def start_moving(self):
        self.kb.press([self.forward_key])
        self.is_moving = True

    def stop_moving(self):
        self.kb.release([self.forward_key])
        self.is_moving = False

    async def rotate(self, angle_to_rotate, only_if_needed=True):
        if not only_if_needed or abs(angle_to_rotate) > 10 / 180 * np.pi:
            await self._rotate(angle_to_rotate, )

    async def _rotate(self, angle_to_rotate):
        if self.is_rotating:
            return
        turning_time = abs(angle_to_rotate) / self.rotation_speed
        if all(map(lambda k: k not in self.kb.pressed, [self.left_rotation_key, self.right_rotation_key])):
            if angle_to_rotate > 0:
                rotation_key = self.left_rotation_key
            else:
                rotation_key = self.right_rotation_key
            self.is_rotating = True
            self.kb.click([rotation_key], delay=turning_time)
            await sleep(1)
            self.is_rotating = False
