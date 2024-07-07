from multiprocessing import shared_memory, Lock
import pickle
from time import sleep
from utils.funcs import timer
from typing import Union
from my_shared_memory.SharedMemoryWithLock import SharedMemoryWithLock
import asyncio


class ShareableObject:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._shared_memory_with_lock: Union[SharedMemoryWithLock, None] = None
        self.is_smwl_pickleable = True

    def dump_to_shared_memory(self):
        try:
            self._shared_memory_with_lock.dump(self)
        except RuntimeError:  # lock cannot be pickled (only to create subprocess)
            self.is_smwl_pickleable = False
            self._shared_memory_with_lock.dump(self)

    async def periodic_update_from_shared_memory(self, period=0.1):
        while True:
            self.update_from_shared_memory()
            await asyncio.sleep(period)

    def update_from_shared_memory(self):
        obj = self._shared_memory_with_lock.load()
        if obj is not None:
            self.__dict__.update(obj.__dict__)

    def set_shared_memory(self, shared_memory_with_lock: SharedMemoryWithLock):
        self._shared_memory_with_lock = shared_memory_with_lock

    def allocate_memory(self, size=10 * 10**6):
        self._shared_memory_with_lock = SharedMemoryWithLock(size=size)
        self._shared_memory_with_lock.dump(None)
        return self._shared_memory_with_lock

    def __getstate__(self):
        r = self.__dict__.copy()
        if not self.is_smwl_pickleable:
            del r['_shared_memory_with_lock']
        return r
