from devices.ArduinoKeyBoard import ArduinoKB
from devices.ArduinoMouse import ArduinoMouse
from time import sleep
import asyncio

kb = ArduinoKB()
for _ in range(100):
    kb.press(['arrow_left'])
    sleep(0.01)
    kb.release_all()
    sleep(2)

