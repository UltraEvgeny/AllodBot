import asyncio
import serial
from devices.keymaping import key_arduino_code_mapping
import keyboard
from time import sleep
from devices.validate_device_action import validate_device_action


class ArduinoKB:
    def __init__(self):
        self.arduino = serial.Serial(port='COM11', baudrate=115200, timeout=.1)

    def reconnect(self):
        self.arduino.close()
        sleep(0.1)
        self.__init__()

    def _write(self, code):
        self.arduino.write(bytes(code, 'utf-8'))

    @staticmethod
    def _keys_to_codes(keys):
        codes = ','.join([str(key_arduino_code_mapping[key]) for key in keys])
        return codes

    @validate_device_action(is_pressed=True)
    async def press(self, keys: list[str], validation_level=1):
        codes = ArduinoKB._keys_to_codes(keys)
        self._write(f'$,P,{codes};')

    @validate_device_action(is_pressed=False)
    async def release(self, keys: list[str], validation_level=1):
        codes = ArduinoKB._keys_to_codes(keys)
        self._write(f'$,R,{codes};')

    def release_all(self):
        self._write('$,L;')

    async def click(self, keys, delay=0.1, validation_level_press=0):
        await self.press(keys, validation_level=validation_level_press)
        await asyncio.sleep(delay)
        await self.release(keys)
