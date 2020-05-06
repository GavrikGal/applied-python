import time
import types
from functools import wraps


def decorate_func(name_prefix=''):
    def decorator(f: types.FunctionType) -> types.FunctionType:
        @wraps(f)
        def wrapper(*args, **kwargs):
            print("'{}' started".format(name_prefix+f.__name__))
            t = time.perf_counter()
            f(*args, **kwargs)
            print("'{}' finished in {:.2f}s\n".format(name_prefix+f.__name__, (time.perf_counter() - t)))
        return wrapper
    return decorator


def decorate_cls(cls):
    for o in dir(cls):
        attr = getattr(cls, o)
        if isinstance(attr, types.FunctionType):
            decorated_a = decorate_func(cls.__name__+'.')(attr)
            setattr(cls, o, decorated_a)
    return cls


def profile(target):
    if isinstance(target, types.FunctionType):
        target = decorate_func()(target)
    else:
        target = decorate_cls(target)
    return target


@profile
def foo():
    time.sleep(0.01)
    print('\t foo body')


@profile
class Bar:
    def __init__(self):
        time.sleep(0.02)
        print('\t Bar body')

    def foo(self):
        time.sleep(0.03)
        print('\t Bar.foo body')


foo()

a = Bar()
a.foo()
