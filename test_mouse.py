from devices.ArduinoKeyBoard import ArduinoKB
from devices.ArduinoMouse import ArduinoMouse
from time import sleep
import pyautogui
from utils.funcs import wait_until_not_pressed
import numpy as np
from math import copysign
import asyncio


mouse = ArduinoMouse()
print(pyautogui.size())
sleep(2)
for _ in range(10):
    # asyncio.run(mouse.straighten_camera())
    # sleep(0.5)
    # sleep(0.5)
    # mouse.click('2')

    mouse.press('1')
    sleep(2)
    mouse.click('2')
    sleep(2)
    mouse.release_all()
    # sleep(0.5)
