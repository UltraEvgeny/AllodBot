from PIL import ImageGrab
import numpy as np
from my_shared_memory.ShareableObject import ShareableObject
from screen_scanner.CurrentState import CurrentState
import pytesseract
import tesserocr
# https://github.com/simonflueckiger/tesserocr-windows_build/releases
# pip install "C:\Users\Ksenia\Downloads\tesserocr-2.7.0-cp310-cp310-win_amd64.whl"
from sounds import low_sound, high_sound
from my_shared_memory.ShareableObject import ShareableObject
from time import sleep
import datetime
import asyncio
import pandas as pd
from itertools import chain
from win32gui import GetWindowText, GetForegroundWindow

from utils.funcs import save_image

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
api_state = tesserocr.PyTessBaseAPI(path=r'C:\Program Files\Tesseract-OCR\tessdata')
api_state.SetVariable('tessedit_char_whitelist', 'O0123456789X ')
api_loc = tesserocr.PyTessBaseAPI(path=r'C:\Program Files\Tesseract-OCR\tessdata', lang='rus')
use_tesserocr = True

addon_default_size = np.array([1080, 1920])  # (y, x)
addon_state1_rect = np.array([[0, 600], [50, 1300]])  # (y, x)
addon_state2_rect = np.array([[50, 600], [100, 1300]])
addon_location_rect = np.array([[100, 600], [150, 1300]])


def crop_numpy(screen, rect_coords):
    y_ratio = screen.shape[0] / addon_default_size[0]
    x_ratio = screen.shape[1] / addon_default_size[1]
    rect_coords = np.array([[rect_coords[0, 0] * y_ratio,
                             rect_coords[0, 1] * x_ratio],
                            [rect_coords[1, 0] * y_ratio,
                             rect_coords[1, 1] * x_ratio],
                            ]).round().astype(int)
    r = screen[tuple(slice(*x) for x in rect_coords.transpose())]
    return r


def crop_pil(screen, rect_coords):
    x_ratio = screen.size[1] / addon_default_size[0]
    y_ratio = screen.size[0] / addon_default_size[1]
    rect_coords = np.array([rect_coords[0, 1]*x_ratio,
                            rect_coords[0, 0]*y_ratio,
                            rect_coords[1, 1]*x_ratio,
                            rect_coords[1, 0]*y_ratio,
                            ]).round().astype(int)
    r = screen.crop(rect_coords)
    return r


class ScreenScanner(ShareableObject):
    def __init__(self, need_location: bool = False):
        super().__init__()
        self._state = CurrentState()
        self.need_location = need_location
        self.not_successful_consecutive_updates = float('inf')
        self.last_update_time = datetime.datetime.min
        self.update_period = 0.1

    @property
    def state(self):
        cur_time = datetime.datetime.now()
        if (cur_time - self.last_update_time).total_seconds() > self.update_period:
            self.update_from_shared_memory()
            self.last_update_time = cur_time
        return self._state

    def update(self, screen):
        screen_numpy = np.array(screen)
        if len(set([tuple(x) for x in list(chain.from_iterable(screen_numpy[:100, :100].round()))])) == 1:
            return False
        state_data = []
        np_crops = []
        for rect in [addon_state1_rect, addon_state2_rect]:
            if use_tesserocr:
                state_picture = crop_pil(screen, rect)
                api_state.SetImage(state_picture)
                state_text = api_state.GetUTF8Text().replace('O', '0')
                np_crops.append(np.array(state_picture))
            else:
                state_picture = crop_numpy(screen_numpy, rect)
                state_text = pytesseract.image_to_string(state_picture, lang='eng', config='--psm 10 --oem 3 -c tessedit_char_whitelist="O0123456789X "').replace('O', '0')
                np_crops.append(state_picture)
            # print(state_text)
            state_text = state_text.strip()
            state_data.extend([x.strip() for x in state_text.split('X')[1:]])
        # print(state_data)
        if self.need_location:
            if use_tesserocr:
                location_picture = crop_pil(screen, addon_location_rect)
                api_loc.SetImage(location_picture)
                location_text = api_loc.GetUTF8Text().strip()
            else:
                location_picture = crop_numpy(screen_numpy, addon_location_rect)
                location_text = pytesseract.image_to_string(location_picture, lang='rus', config='--psm 10 --oem 3').strip()
            # print(location_text)
        else:
            location_text = None
        try:
            self._state.set_state(state_data, location_text)
            success = True
            # high_sound(0.1)
        except (ValueError, IndexError) as e:
            success = False
            low_sound(0.1)
            # save_image(state_picture, f'{state_text}.png')
            # file_name = f"{pd.Timestamp.now().strftime('%Y-%m-%d %H-%M-%S-%f')}__{state_data}"
            # save_image(screen_numpy, f"{file_name}_orig")
            # for i, np_crop in enumerate(np_crops):
            #     save_image(np_crop, f"{file_name}_{i}.png")
        self._state.updating_successfully = self.updating_successfully
        self._state.not_successful_consecutive_updates = self.not_successful_consecutive_updates
        self.dump_to_shared_memory()
        return success

    def start(self):
        while True:
            if GetWindowText(GetForegroundWindow()) == 'Аллоды Онлайн':
                screen = ImageGrab.grab()
                self.updating_successfully = self.update(screen)
            else:
                self.updating_successfully = False

    @property
    def updating_successfully(self):
        return self.not_successful_consecutive_updates < 10

    @updating_successfully.setter
    def updating_successfully(self, value):
        if value:
            self.not_successful_consecutive_updates = 0
        else:
            self.not_successful_consecutive_updates += 1

    async def wait_for_successful_update(self, init_delay=0):
        await asyncio.sleep(init_delay)
        print(self.state.not_successful_consecutive_updates)
        while self.state.not_successful_consecutive_updates > 0:
            await asyncio.sleep(0.5)
            print(self.state.not_successful_consecutive_updates)

    def __repr__(self):
        return str(self.__dict__)
