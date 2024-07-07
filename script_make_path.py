from keyboard_listeners.KeyboardPathCreatorListener import KeyboardPathCreatorDefaultListener
from models.PathCreatorModel import PathCreatorModel
from sounds import *
from time import sleep
from threading import Thread
from pynput.keyboard import Listener
from screen_scanner.ScreenScanner import ScreenScanner
from multiprocessing import Process
import run_scanner

# sleep(10)
if __name__ == '__main__':
    scanner = ScreenScanner(need_location=True)
    scanner.allocate_memory()
    p = Process(target=run_scanner.run_scanner_server, kwargs=dict(scanner=scanner))
    p.start()

    model = PathCreatorModel(name='iskazh_molten', screen_scanner=scanner,)
    model.start()
