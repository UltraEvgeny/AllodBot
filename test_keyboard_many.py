import datetime

from devices.ArduinoKeyBoard import ArduinoKB
from devices.ArduinoMouse import ArduinoMouse
from time import sleep
import asyncio
import keyboard

from devices.KeyboardValidator import keys_to_ensure_status
from utils.funcs import timer
import pandas as pd
from pprint import pprint

from devices.keymaping import keyboard_mapping
from print_all_key_pressed import get_all_keys_pressed
from pynput.keyboard import Key, Listener


kb = ArduinoKB()
keys_to_test = list(keyboard_mapping.keys())

[k for k in keys_to_ensure_status if keyboard.is_pressed(keyboard_mapping[k])]

r = []
r_single_press_keys = []
kb.release_all()
for _ in range(2):
    for keys in [['left_control', 'm'], ['d'], ['arrow_up']]:# keys_to_test[:]:
        with timer(f'press {keys}'):
            asyncio.run(kb.press(keys, validation_level=1))
        print([k for k in keys_to_ensure_status if keyboard.is_pressed(keyboard_mapping[k])])
        with timer(f'release {keys}'):
            asyncio.run(kb.release(keys, validation_level=1))



