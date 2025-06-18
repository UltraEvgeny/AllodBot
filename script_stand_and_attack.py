from keyboard_listeners.KeyboardDefaultListener import KeyboardDefaultListener
from models.StandAndAtackModel import StandAndAtackModel
from screen_scanner.ScreenScanner import ScreenScanner
import pytesseract
from devices.ArduinoKeyBoard import ArduinoKB
from devices.ArduinoMouse import ArduinoMouse
from utils.funcs import wait_until_not_pressed
import run_scanner
from multiprocessing import Process
from time import sleep
import screen_video_recorder
import print_all_key_pressed
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'


if __name__ == '__main__':
    Process(target=screen_video_recorder.main, ).start()
    Process(target=print_all_key_pressed.main, ).start()

    kb = ArduinoKB()
    mouse = ArduinoMouse()
    scanner = ScreenScanner()
    scanner.allocate_memory()
    p = Process(target=run_scanner.run_scanner_server, kwargs=dict(scanner=scanner))
    p.start()

    model = StandAndAtackModel(kb=kb, screen_scanner=scanner, mouse=mouse)
    model.start()
