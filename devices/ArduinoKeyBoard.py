import asyncio
import serial
from devices.keymaping import key_arduino_code_mapping, key_python_keyboard_maping
import keyboard
from time import sleep


keys_to_ensure_status = ['arrow_left', 'arrow_right', 'arrow_up', ]


class ArduinoKB:
    def __init__(self):
        self.arduino = serial.Serial(port='COM9', baudrate=115200, timeout=.1)

    @staticmethod
    def ensure_keys_status(keys: list[str], is_pressed):
        return all([keyboard.is_pressed(key_python_keyboard_maping[key]) == is_pressed for key in keys if key in keys_to_ensure_status])

    def _write(self, code):
        self.arduino.write(bytes(code, 'utf-8'))

    @staticmethod
    def _keys_to_codes(keys):
        codes = ','.join([str(key_arduino_code_mapping[key]) for key in keys])
        return codes

    def press(self, keys: list[str]):
        codes = ArduinoKB._keys_to_codes(keys)
        while True:
            self._write(f'$,P,{codes};')
            if self.ensure_keys_status(keys, is_pressed=True):
                break
            sleep(0.001)

    def release(self, keys: list[str]):
        codes = ArduinoKB._keys_to_codes(keys)
        while True:
            self._write(f'$,R,{codes};')
            if self.ensure_keys_status(keys, is_pressed=False):
                break
            sleep(0.001)

    def release_all(self):
        self._write('$,L;')

    async def click(self, keys, delay=0.1):
        self.press(keys)
        await asyncio.sleep(delay)
        self.release(keys)