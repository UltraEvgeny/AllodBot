from contextlib import contextmanager
import pandas as pd
import cv2
import tkinter as tk
import numpy as np
import yaml
import pickle
from pynput.keyboard import Listener
from time import sleep


@contextmanager
def timer(text):
    start_time = pd.Timestamp.now()
    try:
        yield
    finally:
        print(f'Seconds spent on {text}: {(pd.Timestamp.now() - start_time).total_seconds()} seconds')


def is_close(x, y, tol=0.0001):
    return abs(x - y) < tol


def is_increasing(x):
    return all(x < y for x, y in zip(x, x[1:]))


def show_img(*imgs, original_size=False):
    for i, img in enumerate(imgs):
        if not original_size:
            window_factor = 0.85
            root = tk.Tk()
            screen_width = root.winfo_screenwidth()
            screen_height = root.winfo_screenheight()
            scale_factor = min(screen_height / img.shape[0], screen_width / img.shape[1]) * window_factor
            to_shape = (img.shape[0] * scale_factor, img.shape[1] * scale_factor)
            to_shape = tuple(int(x) for x in to_shape)[::-1]
            img = cv2.resize(img, to_shape)

        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        cv2.imshow(f'{i}', img)
    cv2.waitKey(0)


def save_image(img, filename=None, folder='debug_screenshots/location_text'):
    if filename is None:
        filename = pd.Timestamp.now().strftime('%Y-%m-%d %H-%M-%S-%f')
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    print(f'saving to {folder}/{filename}.jpg')
    cv2.imwrite(f'{folder}/{filename}.jpg', img)


def rotate_image(image, angle):
    image_center = tuple(np.array(image.shape[1::-1]) / 2)
    rot_mat = cv2.getRotationMatrix2D(image_center, angle, 1.0)
    result = cv2.warpAffine(image, rot_mat, image.shape[1::-1], flags=cv2.INTER_LINEAR)
    return result


def yaml_load(filepath):
    with open(filepath, "r") as stream:
        return yaml.safe_load(stream)


def yaml_dump(data, filepath):
    with open(filepath, "w") as stream:
        yaml.dump(data, stream, allow_unicode=True)


def to_pickle(obj, filename):
    with open(filename, 'wb') as f:
        pickle.dump(obj, f)


def from_pickle(filename):
    with open(filename, 'rb') as f:
        obj = pickle.load(f)
    return obj


def wait_until_not_pressed(key_to_wait):
    def on_press(key):
        if hasattr(key, 'char'):
            key = key.char
            # [print(f'Keypressed: {key}, key_to_wait: {key_to_wait}, equal? {key == key_to_wait}')
            if key == key_to_wait:
                listener.stop()

    listener = Listener(on_press=on_press)
    listener.start()
    while listener.is_alive():
        sleep(0.1)


# writer = pd.ExcelWriter(folder / "Офлайн эксперимент.xlsx", engine='xlsxwriter')
# dataframe_to_sheet(writer, df, 'exp_result')
# writer.close()
def dataframe_to_sheet(writer, df, sheet_name):
    df.to_excel(writer, index=False, sheet_name=sheet_name, float_format="%.3f")
    ws = writer.book.sheetnames[sheet_name]
    ws.freeze_panes(1, 0)
    header_format = writer.book.add_format({'text_wrap': True})
    header_format.set_align('center')
    header_format.set_align('vcenter')
    ws.set_column(0, df.shape[1] - 1, 20)

    ws.add_table(0, 0, df.shape[0], df.shape[1] - 1,
                 {'header_row': True,
                  'columns': [{'header': col} for col in df.columns]
                  })

    for i, col_name in enumerate(df.columns.values):
        ws.write(0, i, col_name, header_format)
