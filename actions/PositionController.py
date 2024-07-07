from screen_scanner.ScreenScanner import ScreenScanner
from devices.ArduinoKeyBoard import ArduinoKB
import numpy as np
import asyncio
from concurrent.futures import ProcessPoolExecutor


def get_distance(x1, x2):
    r = np.linalg.norm(x1-x2)
    return r


def get_angle_to_rotate(current_point, target, facing_angle):
    target_vector = target - current_point
    target_angle = np.angle(target_vector[0] + 1j*target_vector[1])
    angle_to_rotate = (target_angle - facing_angle + np.pi) % (2*np.pi) - np.pi
    return angle_to_rotate


class PositionController:
    distance_threshold = 3
    rotation_speed = 2.498
    left_rotation_key = 'arrow_left'
    right_rotation_key = 'arrow_right'
    forward_key = 'arrow_up'

    def __init__(self, scanner: ScreenScanner, kb: ArduinoKB):
        self.active = False
        self.target_coords = None
        self.scanner = scanner
        self.kb = kb
        self.is_rotating = False

    def set_target_coords(self, target_coords, activate=True):
        self.target_coords = target_coords
        if activate:
            self.active = True

    @property
    def is_near_target(self):
        distance_to_target = get_distance(self.scanner.state.coords, self.target_coords)
        return distance_to_target < self.distance_threshold

    async def run(self):
        loop = asyncio.get_running_loop()
        loop.create_task(self.move_forward_if_needed())
        loop.create_task(self.rotate())
        await asyncio.sleep(0)

    async def move_forward_if_needed(self):
        while True:
            angle_to_target = get_angle_to_rotate(self.scanner.state.coords, self.target_coords, self.scanner.state.facing_angle)
            if 'arrow_up' in self.kb.pressed:
                if abs(angle_to_target) > 60 / 180 * np.pi or (abs(angle_to_target) > 30 / 180 * np.pi and self.is_near_target):
                    self.stop_moving()
            else:
                dist = get_distance(self.scanner.state.coords, self.target_coords)
                if abs(angle_to_target) < 60/180*np.pi and not self.is_near_target and not self.is_rotating:
                    if dist < 25:
                        await self.kb.click([self.forward_key], delay=dist/16.25*0.8)
                    else:
                        self.start_moving()
            await asyncio.sleep(0.01)

    async def rotate(self, only_if_needed=True):
        while True:
            angle_to_target = get_angle_to_rotate(self.scanner.state.coords, self.target_coords, self.scanner.state.facing_angle)
            if not only_if_needed or abs(angle_to_target) > 10 / 180 * np.pi:
                await self._rotate(angle_to_target)
            await asyncio.sleep(0)

    async def _rotate(self, angle_to_rotate):
        turning_time = abs(angle_to_rotate) / self.rotation_speed
        if all(map(lambda k: k not in self.kb.pressed, [self.left_rotation_key, self.right_rotation_key])):
            if angle_to_rotate > 0:
                rotation_key = self.left_rotation_key
            else:
                rotation_key = self.right_rotation_key
            self.is_rotating = True
            await self.kb.click([rotation_key], delay=turning_time)
            print(self.kb.pressed)
            await asyncio.sleep(0.5)
            self.is_rotating = False

    def start_moving(self):
        self.kb.press([self.forward_key])

    def stop_moving(self):
        self.kb.release([self.forward_key])
