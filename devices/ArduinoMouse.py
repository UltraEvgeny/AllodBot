from threading import Thread
import serial
from devices.keymaping import key_arduino_code_mapping
from asyncio import sleep
import numpy as np
import pyautogui


class ArduinoMouse:
    def __init__(self):
        self.arduino = serial.Serial(port='COM8', baudrate=115200, timeout=.1)

    def _write(self, code):
        self.arduino.write(bytes(code, 'utf-8'))

    @staticmethod
    def _keys_to_codes(keys):
        codes = ','.join([str(key_arduino_code_mapping[key]) for key in keys])
        return codes

    def _move(self, dx, dy):
        self._write(f'$,M,{dx},{dy};')

    def click(self, button='1'):
        self._write(f'$,C,{button};')

    def press(self, button):
        self._write(f'$,P,{button};')

    def release_all(self):
        self._write(f'$,R;')

    async def move_mouse(self, target_coords_fraction):
        mouse_speed_factor = 2
        target_coords = (np.array(target_coords_fraction) * np.array(pyautogui.size())).astype(int)
        while True:
            delta = target_coords - np.array(pyautogui.position())
            if np.abs(delta).max() < 5:
                break
            delta_with_factor = [np.sign(x)*max(abs(x//mouse_speed_factor), 1) for x in delta]
            self._move(*delta_with_factor)
            await sleep(0.1)

