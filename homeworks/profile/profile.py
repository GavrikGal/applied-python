import time
from functools import wraps


def profile(f):
    @wraps(f)
    def wrapper():
        print("'" + f.__name__ + "'" + ' started')
        time_start = time.time()
        f()
        time_stop = time.time()
        time_process = time_stop - time_start
        print("'{}' finished in {:.2f}s\n".format(f.__name__, time_process))
    return wrapper


@profile
def foo():
    time.sleep(0.01)
    print('\t foo body')


class Bar:
    def __init__(self):
        print('\t Bar body')


foo()

Bar()
