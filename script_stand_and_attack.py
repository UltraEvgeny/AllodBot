from keyboard_listeners.KeyboardDefaultListener import KeyboardDefaultListener
from models.FarmAlongPathModel_old import FarmAlongPathModel_old
from models.StandAndAtackModel import StandAndAtackModel
from screen_scanner.ScreenScanner import ScreenScanner
import pytesseract
from devices.ArduinoKeyBoard import ArduinoKB
from utils.funcs import wait_until_not_pressed
import run_scanner
from multiprocessing import Process
from time import sleep
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'


if __name__ == '__main__':
    kb = ArduinoKB()
    scanner = ScreenScanner()
    scanner.allocate_memory()
    p = Process(target=run_scanner.run_scanner_server, kwargs=dict(scanner=scanner))
    p.start()

    model = StandAndAtackModel(kb=kb, screen_scanner=scanner)
    model.start()
