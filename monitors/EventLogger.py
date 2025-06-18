import logging
import json
from datetime import datetime
import numpy as np


class NumpyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return super().default(obj)


def write_to_log(event_data: dict, level='INFO', print_=True):
    if print_:
        print(event_data)
    # logging.info(json.dumps(event_data, ensure_ascii=False, cls=NumpyEncoder))
    logging.log(level=logging.getLevelName(level), msg=json.dumps(event_data, ensure_ascii=False, cls=NumpyEncoder))
