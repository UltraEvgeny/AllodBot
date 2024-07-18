from devices.ArduinoKeyBoard import ArduinoKB
from screen_scanner.ScreenScanner import ScreenScanner
from time import sleep
import pandas as pd
from math import pi
from utils.funcs import is_close, is_increasing


def get_rotation_speed():
    kb = ArduinoKB()
    measure_time = pd.Timedelta(seconds=20)

    scanner = ScreenScanner(need_location=False)
    scanner.start()
    while not scanner.updating_successfully:
        sleep(0.1)

    sleep(1)
    kb.press(['arrow_left'])
    angles = []
    full_rounds = 0
    while not angles or pd.Timestamp.now() - angles[0]['time'] < measure_time:
        cur_angle = scanner.state.hero_facing_angle + 2 * pi * full_rounds
        if angles:
            if is_close(cur_angle, angles[-1]['angle']):
                sleep(0.1)
                continue
            if cur_angle < angles[-1]['angle']:
                cur_angle += 2*pi
                full_rounds += 1
                print(full_rounds)
        sleep(0.1)
        angles.append(dict(time=pd.Timestamp.now(), angle=cur_angle))
    kb.release(['arrow_left'])
    scanner.stop_updating()
    if not is_increasing([x['angle'] for x in angles]):
        print([x['angle'] for x in angles])
        raise ValueError
    total_angle = angles[-1]['angle'] - angles[0]['angle']
    total_time = (angles[-1]['time'] - angles[0]['time']).seconds
    rotation_speed = total_angle / total_time
    return rotation_speed


def main():
    rotation_speed = get_rotation_speed()
    print(rotation_speed)


if __name__ == '__main__':
    main()
    # 2.498
