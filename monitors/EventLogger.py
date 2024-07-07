import json
from datetime import datetime
import numpy as np


class NumpyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return super().default(obj)


def write_to_log(event_data: dict):
    version = 'add_mount'
    dt_str = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    with open('logs.txt', 'a', encoding='utf-8') as f:
        f.write(json.dumps({**{'version': version, 'dt': dt_str},  **event_data}, ensure_ascii=False, cls=NumpyEncoder)+'\n')
