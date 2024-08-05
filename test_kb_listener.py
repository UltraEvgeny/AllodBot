import datetime

from devices.ArduinoKeyBoard import ArduinoKB
from devices.ArduinoMouse import ArduinoMouse
from time import sleep
import asyncio
import keyboard
from utils.funcs import timer
import pandas as pd
from pprint import pprint

from devices.keymaping import keyboard_mapping
from print_all_key_pressed import get_all_keys_pressed
from pynput.keyboard import Key, Listener


listener_keys_pressed = set()


def key_to_str(key):
    try:
        key_str = key.__dict__.get('_name_', key.__dict__.get('char', {})).lower()
        return key_str
    except AttributeError:
        print(f'Unknown key: {key.__dict__}')
        # global x
        # x = key
        # listener.stop()


def on_press(key):
    key_str = key_to_str(key)
    if key is not None:
        listener_keys_pressed.add(key_str)


def on_release(key):
    key_str = key_to_str(key)
    if key is not None:
        listener_keys_pressed.discard(key_str)


kb = ArduinoKB()
listener = Listener(on_press=on_press, on_release=on_release)
listener.start()


keys_to_test = list(keyboard_mapping.keys())
press_function = lambda k: kb.press.__wrapped__(kb, [k])
release_function = lambda k: kb.release.__wrapped__(kb, [k])
check_delay = 0.01

r = []
r_single_press_keys = []
for _ in range(10):
    for key in keys_to_test[:]:
        press_function(key)
        sleep(check_delay)
        release_function(key)
        sleep(check_delay)


print('\n', listener_keys_pressed)
