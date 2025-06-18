import datetime
from functools import wraps
from monitors.EventLogger import write_to_log
import asyncio
import random
from devices.KeyboardValidator import KeyboardValidator
from devices.PyinputValidator import PyinputValidator


validator_class = KeyboardValidator




def validate_device_action(is_pressed):
    def decorator(action):
        @wraps(action)
        async def func(self, keys, validation_level=1):
            func_start_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
            func_properties = {'keys': keys, 'validation_level': validation_level, 'func_start_time': func_start_time}
            write_to_log({'function started': func.__name__, **func_properties}, print_=False)
            tries = 0
            status = False
            while True:
                #self.reconnect()
                tries += 1
                if tries >= 2:
                    write_to_log({'function': func.__name__, 'tries': tries, **func_properties}, level='ERROR', print_=False)
                    await asyncio.sleep(0.1 * random.random())
                if tries > 5:
                    if validation_level < 2:
                        self.release_all()
                        write_to_log({'function': func.__name__, 'reconnecting': True, 'tries': tries, **func_properties}, level='ERROR', print_=False)
                        break
                    await asyncio.sleep(0.3 * random.random())
                if tries > 20:
                    if tries % 5 == 0:
                        self.release_all()
                        write_to_log({'function': func.__name__, 'reconnecting': True, 'tries': tries, **func_properties}, level='ERROR', print_=False)
                    await asyncio.sleep(1)
                    # if action.__name__ == 'release':
                    #     await self.press(keys)
                    # else:
                    #     await self.release.__wrapped__(self, keys)
                    # self.release_all()
                    # await asyncio.sleep(1*random.random())
                if validation_level > 0:
                    validator = validator_class(keys, func.__name__)
                await action(self, keys)
                if validation_level == 0:
                    write_to_log({'function ended': func.__name__, 'tries': tries, **func_properties}, print_=False)
                    return tries
                # await asyncio.sleep(0.2)
                await asyncio.sleep(0.01)
                if validator.validate():
                    status = True
                    break

            validator.stop()
            write_to_log({'function ended': func.__name__, 'tries': tries, 'status': status, **func_properties})
            return tries
        return func
    return decorator
