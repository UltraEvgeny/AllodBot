from keyboard_listeners.KeyboardDefaultListener import KeyboardDefaultListener
from models.FarmIskazh import FarmIskazh
from screen_scanner.ScreenScanner import ScreenScanner
import pytesseract
from devices.ArduinoKeyBoard import ArduinoKB
from devices.ArduinoMouse import ArduinoMouse
from utils.funcs import wait_until_not_pressed
import run_scanner
from multiprocessing import Process
from time import sleep
import logging
import screen_video_recorder
import print_all_key_pressed
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

logging.basicConfig(filename='logs.txt',  # 'D:/AllodLogs/logs.txt'
                    filemode='a',
                    format='%(asctime)s.%(msecs)03d %(levelname)s %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    level=logging.INFO, )

if __name__ == '__main__':
    Process(target=screen_video_recorder.main, ).start()
    Process(target=print_all_key_pressed.main, ).start()

    kb = ArduinoKB()
    mouse = ArduinoMouse()
    scanner = ScreenScanner(need_location=True)
    scanner.allocate_memory()
    p = Process(target=run_scanner.run_scanner_server, kwargs=dict(scanner=scanner), )
    p.start()

    model = FarmIskazh(kb=kb, mouse=mouse, screen_scanner=scanner, trajectory_name='iskazh_ice', )
    # wait_until_not_pressed('[')
    # model.enter_iskazh()
    # sleep(3)
    # model.leave_iskazh()
    # exit()
    model.start()
