# https://www.youtube.com/watch?v=zdkZurbpqvA

import pyautogui
import cv2
import numpy as np
from datetime import datetime


def main():
    resolution = tuple((np.array([1920, 1080])*0.5).astype(int))
    codec = cv2.VideoWriter_fourcc(*"XVID")

    start_dt = datetime.now()
    print(start_dt)
    filename = f"D:/AllodLogs/video/{start_dt:%Y-%m-%d %H_%M_%S}.avi"
    print(filename)
    fps = 30.0

    out = cv2.VideoWriter(filename, codec, fps, resolution)

    while True:
        img = pyautogui.screenshot()
        frame = np.array(img)
        frame = cv2.resize(frame, resolution)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        out.write(frame)

        #if (datetime.now() - start_dt).total_seconds() > 8000:
        #    break

    out.release()

    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
