from functools import wraps
from monitors.EventLogger import write_to_log
import asyncio


def validate_device_action(is_pressed):
    def decorator(action):
        @wraps(action)
        async def func(self, keys):
            tries = 0
            while True:
                tries += 1
                if tries > 2:
                    write_to_log({'method': 'release', 'keys': keys, 'tries': tries}, level='ERROR')
                if tries > 50:
                    self.release_all()
                action(self, keys)
                await asyncio.sleep(0.001)
                if self.ensure_keys_status(keys, is_pressed=is_pressed):
                    break
            write_to_log({'tries': tries, 'keys': keys})
            print(f'tries: {tries}, keys={keys}')
            return tries
        return func
    return decorator