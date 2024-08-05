import datetime
import logging

from devices.ArduinoKeyBoard import ArduinoKB
from devices.ArduinoMouse import ArduinoMouse
from time import sleep
import asyncio
import keyboard
from utils.funcs import timer
import pandas as pd
from pprint import pprint

from devices.keymaping import keyboard_mapping, pynput_mapping
from print_all_key_pressed import get_all_keys_pressed
from pynput.keyboard import Key, Listener


def gb_single_press(x):
    rr = dict()
    rr['success'] = f"{x['success'].sum()} / {x.shape[0]}"
    rr['response_time_mean'] = x['response_time'].mean()
    return pd.Series(rr)


listener_keys_pressed = set()


def listener__check_key_pressed(key, is_pressed):
    global event_happened
    result = event_happened
    event_happened = False
    return result


def key_to_str(key):
    # global x
    # x = key
    # listener.stop()
    # return
    try:
        key_str = key.__dict__.get('_name_', key.__dict__.get('char', {})).lower()
        return key_str
    except AttributeError:
        print(f'Unknown key: {key.__dict__}')


def on_press(key):
    key_str = key_to_str(key)
    print(key_str)
    if key is not None:
        listener_keys_pressed.add(key_str)
    # print(listener_keys_pressed)


def on_release(key):
    key_str = key_to_str(key)
    if key is not None:
        listener_keys_pressed.discard(key_str)
    # print(listener_keys_pressed)

keyboard.add_hotkey('F1', on_press)

kb = ArduinoKB()
with timer('listener'):
    listener = Listener(on_press=on_press, on_release=on_release)
    listener.start()


while True:
    pass


logging.basicConfig(filename='logs.txt',  # 'D:/AllodLogs/logs.txt'
                    filemode='a',
                    format='%(asctime)s.%(msecs)03d %(levelname)s %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    level=logging.INFO, )


while True:
    asyncio.run(kb.click(keys=['arrow_left']))
    sleep(1)


measure_method_config = {
    'listener': {
        'get_key_status': lambda k: pynput_mapping[k] in listener_keys_pressed,
    },
    'pykeyboard': {
        'get_key_status': lambda k: kb.ensure_keys_status([k], is_pressed=True),
    },

}

keys_to_test = list(keyboard_mapping.keys())
press_function = lambda k: asyncio.run(kb.press.__wrapped__(kb, [k]))
release_function = lambda k: asyncio.run(kb.release.__wrapped__(kb, [k]))
# press_function = lambda k: asyncio.run(kb.press([k]))
# release_function = lambda k: asyncio.run(kb.release([k]))
check_delay = 0.1

r = []
sleep(1)
r_single_press_keys = []
for measure_method, config in measure_method_config.items():
    for _ in range(10):
        for key in keys_to_test[:4]:
            with timer('press'):
                start_time = datetime.datetime.now()
                press_function(key)
                while True:
                    success = config['get_key_status'](key)
                    cur_delay = (datetime.datetime.now() - start_time).total_seconds()
                    if success or cur_delay > check_delay:
                        break
                r_single_press_keys.append({'key': key, 'measure_method': measure_method, 'action': f'press_{check_delay}',
                                            'success': success,
                                            'response_time': cur_delay if success else None})
            if success:
                start_time = datetime.datetime.now()
                release_function(key)
                while True:
                    success = config['get_key_status'](key)
                    cur_delay = (datetime.datetime.now() - start_time).total_seconds()
                    if success or cur_delay > check_delay:
                        break
                r_single_press_keys.append({'key': key, 'measure_method': measure_method, 'action': f'release_{check_delay}',
                                            'success': success,
                                            'response_time': cur_delay if success else None})
            sleep(0.05)
            # kb.release_all()

df_r_single_press_keys = pd.DataFrame(r_single_press_keys)
r.extend(df_r_single_press_keys.groupby(['key', 'measure_method', 'action'])[df_r_single_press_keys.columns].apply(gb_single_press, include_groups=True).reset_index().to_dict(orient='records'))
listener.stop()
df_r = pd.DataFrame(r)
pprint(df_r)
kb.release_all()
exit()

for _ in range(100):
    pass
# Collect events until released
print_time('before listener')
listener = Listener(on_press=on_press, on_release=on_release)
print_time('after listener')
listener = Listener()
print_time('after listener')
listener.start()
print_time('after listener start')
for i in range(10):
    print(i)
    print_time('before click')
    kb.press.__wrapped__(kb, ['arrow_up'])
    print_time('after click')
    sleep(0.1)
    kb.release_all()
    sleep(0.1)
    exit()
