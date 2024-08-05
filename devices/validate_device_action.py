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
        async def func(self, keys, validate=True):
            func_start_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M%S.%f')
            func_properties = {'keys': keys, 'validate': validate, 'func_start_time': func_start_time}
            write_to_log({'function started': func.__name__, **func_properties})
            tries = 0
            status = False
            while True:
                tries += 1
                if tries >= 2:
                    write_to_log({'function': func.__name__, 'tries': tries, **func_properties}, level='ERROR')
                if tries > 5:
                    self.release_all()
                    await asyncio.sleep(0.3 * random.random())
                    break
                if tries > 20:
                    break
                    # if action.__name__ == 'release':
                    #     await self.press(keys)
                    # else:
                    #     await self.release.__wrapped__(self, keys)
                    # self.release_all()
                    # await asyncio.sleep(1*random.random())
                if validate:
                    validator = validator_class(keys, func.__name__)
                await action(self, keys)
                if not validate:
                    write_to_log({'function ended': func.__name__, 'tries': tries, **func_properties})
                    return tries
                await asyncio.sleep(0.2)

                if validator.validate():
                    status = True
                    break

            validator.stop()
            write_to_log({'function ended': func.__name__, 'tries': tries, 'status': status, **func_properties})
            print({'function ended': func.__name__, 'tries': tries, **func_properties})
            return tries
        return func
    return decorator
