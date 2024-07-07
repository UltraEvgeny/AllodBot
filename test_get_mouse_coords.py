from devices.ArduinoKeyBoard import ArduinoKB
from devices.ArduinoMouse import ArduinoMouse
from time import sleep
import pyautogui
from utils.funcs import wait_until_not_pressed
import numpy as np

print(pyautogui.size())
mouse = ArduinoMouse()
while True:
    wait_until_not_pressed('[')
    print(np.array(pyautogui.position())/np.array(pyautogui.size()))




