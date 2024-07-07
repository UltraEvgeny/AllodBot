from keyboard_listeners.KeyboardDefaultListener import KeyboardDefaultListener
from models.FarmAlongPathModel import FarmAlongPathModel
from screen_scanner.ScreenScanner import ScreenScanner
import pytesseract
from devices.ArduinoKeyBoard import ArduinoKB
from devices.ArduinoMouse import ArduinoMouse
from utils.funcs import wait_until_not_pressed
import run_scanner
from multiprocessing import Process
from time import sleep
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'


if __name__ == '__main__':
    kb = ArduinoKB()
    mouse = ArduinoMouse()
    scanner = ScreenScanner()
    scanner.allocate_memory()
    p = Process(target=run_scanner.run_scanner_server, kwargs=dict(scanner=scanner))
    p.start()

    # trajectory_name = 'cs_cobolds'
    trajectory_name = 'cs_firelords'
    model = FarmAlongPathModel(kb=kb, mouse=mouse, screen_scanner=scanner, trajectory_name=trajectory_name)
    model.start()
