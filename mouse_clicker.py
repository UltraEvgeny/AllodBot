from devices.ArduinoKeyBoard import ArduinoKB
from devices.ArduinoMouse import ArduinoMouse
from time import sleep
import pyautogui
from utils.funcs import wait_until_not_pressed
import numpy as np
from math import copysign
import asyncio
import win32api


mouse = ArduinoMouse()
asyncio.run(mouse.move_mouse([0.4703125, 0.49259259]))
# exit()
print(win32api.GetKeyState(1))
print(win32api.GetKeyState(2))
print(pyautogui.size())
button = '2'
for _ in range(100000):
    asyncio.run(mouse.click(button))
    sleep(0.5)
