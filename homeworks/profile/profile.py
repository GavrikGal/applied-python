import time
from functools import wraps


def profile(f):
    @wraps(f)
    def wrapper():
        print("'{}' started".format(f.__name__))
        t = time.perf_counter()
        f()
        print("'{}' finished in {:f}s\n".format(f.__name__, (time.perf_counter()-t)))
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
