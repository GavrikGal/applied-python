import time

def profile(f):
    def wrap():
        print("'" + f.__name__ + "'" + ' started')
        time_start = time.time()
        f()
        time_stop = time.time()
        time_process = time_stop - time_start
        print("'{}' finished in {:.2f}s".format(f.__name__, time_process))
    return wrap


@profile
def foo():
    time.sleep(0.01)
    print('\t foo body')


class Bar:
    def __init__(self):
        pass


foo()
Bar()
