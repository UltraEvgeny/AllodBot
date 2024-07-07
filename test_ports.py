from time import sleep
import pyautogui
import serial

iskazh_choose_point = (0.36749633967789164, 0.5455729166666666)


def click(point_frac):
    maxx, maxy = pyautogui.size()
    cur_pos = point_frac[0] * maxx, point_frac[1] * maxy
    pyautogui.click(*cur_pos)
    while True:
        sleep(1)
        pyautogui.click()


# sleep(5)
# click(iskazh_choose_point)
# pyautogui.click(x=700, y=700)

for s in range(30):
    try:
        serial.Serial(port=f'COM{s}', baudrate=115200, timeout=.1)
        print(s)
    except:
        pass
