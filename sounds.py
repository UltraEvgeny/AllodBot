import winsound
from threading import Thread
from functools import wraps
low = 220
high = 440
semitone = 2 ** (1/12)
arpeggio = [low, low*semitone**4, low*semitone**7, low*semitone**12]


def run_parallel(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not kwargs.get('parallel', False):
            return func(*args, **kwargs)
        t = Thread(target=func, args=args, kwargs=kwargs)
        t.start()
    return wrapper


@run_parallel
def ascending_sound(parallel=True):
    for tone in arpeggio:
        winsound.Beep(int(tone), 200)


@run_parallel
def descending_sound(parallel=True):
    for tone in arpeggio[::-1]:
        winsound.Beep(int(tone), 200)


@run_parallel
def high_sound(length=1, parallel=True):
    winsound.Beep(high, round(length*1000))


@run_parallel
def low_sound(length=1, parallel=True):
    winsound.Beep(low, round(length*1000))
