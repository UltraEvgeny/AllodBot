from multiprocessing import shared_memory, Lock
import pickle


class SharedMemoryWithLock:
    def __init__(self, size=10 * 10**6):
        self.shared_memory = shared_memory.SharedMemory(create=True, size=size)
        self.lock = Lock()

    def load(self):
        size_list = []
        with self.lock:
            for i in range(self.shared_memory.size):
                symbol = chr(self.shared_memory.buf[i])
                if symbol == ' ':
                    break
                size_list.append(symbol)
            obj_bytes_length = int(''.join(size_list))
            obj_first_byte_index = len(size_list) + 1
            obj_bytes = self.shared_memory.buf[obj_first_byte_index:obj_first_byte_index+obj_bytes_length].tobytes()
        obj = pickle.loads(obj_bytes)
        return obj

    def dump(self, obj):
        obj_bytes = pickle.dumps(obj)
        obj_bytes_length = len(obj_bytes)
        obj_size_bytes: bytes = (str(obj_bytes_length) + ' ').encode()
        obj_first_byte_index = len(obj_size_bytes)
        with self.lock:
            self.shared_memory.buf[:obj_first_byte_index] = obj_size_bytes
            self.shared_memory.buf[obj_first_byte_index:obj_first_byte_index+obj_bytes_length] = obj_bytes
