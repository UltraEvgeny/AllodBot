from actions.PositionController import PositionController
from actions.FightAction import FightAction
from devices.ArduinoKeyBoard import ArduinoKB
from screen_scanner.ScreenScanner import ScreenScanner
import numpy as np
from time import sleep
import asyncio

from utils.trajectory_utils import load_trajectory


def forward_backward_generator(arr, initial_i):
    cur_direction = 1
    cur_i = initial_i
    while True:
        print(cur_i, arr[cur_i])
        yield arr[cur_i]
        if cur_direction == 1 and cur_i == len(arr) - 1 or cur_direction == -1 and cur_i == 0:
            cur_direction *= -1
        cur_i += cur_direction


def get_nearest_point_i(single_point, points):
    r = ((points - single_point)**2).sum(axis=1).argmin()
    return r


class AttackMove:
    distance_threshold = 5

    def __init__(self, *, screen_scanner: ScreenScanner, kb: ArduinoKB, trajectory):
        self.trajectory = trajectory
        self.position_controller = PositionController(scanner=screen_scanner, kb=kb)
        self.fight_action = FightAction(screen_scanner=screen_scanner, kb=kb)
        self.scanner = screen_scanner

    async def start(self):
        cur_coords = None
        while cur_coords is None:
            cur_coords = self.scanner.state.coords
        nearest_i = get_nearest_point_i(cur_coords, np.array([x['coords'] for x in self.trajectory]))

        asyncio.get_running_loop().create_task(self.position_controller.run())
        for target_point in forward_backward_generator(self.trajectory, initial_i=nearest_i):
            target_point_coords = target_point['coords']
            self.position_controller.set_target_coords(target_point_coords)
            while True:
                if self.position_controller.is_near_target:
                    break
                await asyncio.sleep(0.1)
