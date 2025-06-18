from threading import Thread
import serial
from devices.keymaping import key_arduino_code_mapping
from time import sleep
import asyncio
import numpy as np
import pyautogui
import win32api


class ArduinoMouse:
    def __init__(self):
        self.arduino = serial.Serial(port='COM10', baudrate=115200, timeout=.1)

    @staticmethod
    def ensure_keys_status(button: str, is_pressed):
        return (win32api.GetKeyState(int(button)) in (-128, -127)) == is_pressed

    def _write(self, code):
        self.arduino.write(bytes(code, 'utf-8'))

    @staticmethod
    def _keys_to_codes(keys):
        codes = ','.join([str(key_arduino_code_mapping[key]) for key in keys])
        return codes

    def _move(self, dx, dy):
        self._write(f'$,M,{dx},{dy};')

    async def click(self, button='1', delay=0.1):
        await self.press(button)
        await asyncio.sleep(delay)
        await self.release_all(button_to_check=button)

    async def press(self, button):
        while True:
            self._write(f'$,P,{button};')
            await asyncio.sleep(0.001)
            if self.ensure_keys_status(button, is_pressed=True):
                break

    async def release_all(self, button_to_check='1'):
        while True:
            self._write(f'$,R;')
            await asyncio.sleep(0.001)
            if self.ensure_keys_status(button_to_check, is_pressed=False):
                break

    async def move_mouse(self, target_coords_fraction):
        mouse_speed_factor = 2
        target_coords = (np.array(target_coords_fraction) * np.array(pyautogui.size())).astype(int)
        while True:
            delta = target_coords - np.array(pyautogui.position())
            if np.abs(delta).max() < 5:
                break
            delta_with_factor = [np.sign(x)*max(abs(x//mouse_speed_factor), 1) for x in delta]
            self._move(*delta_with_factor)
            await asyncio.sleep(0.1)
