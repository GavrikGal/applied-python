from functools import wraps
import copy


def whenthen(func):
    def when(condition_func):
        func_in_main = globals()[condition_func.__name__]
        if not hasattr(func_in_main, 'condition') or func_in_main.condition is None:
            setattr(func_in_main, 'condition', condition_func)
        else:
            raise AttributeError('when exist')
        # setattr(func_in_main, 'condition', condition_func)

        return func_in_main

    def then(then_func):
        func_in_main = globals()[then_func.__name__]
        if not hasattr(func_in_main, 'condition') or func_in_main.condition is None:
            raise AttributeError

        condition = copy.copy(func_in_main.condition)

        def new_condition(a):
            if condition(a):
                result = then_func(a)
                return result

        func_in_main.all_conditions.append(new_condition)
        func_in_main.condition = None
        return func_in_main

    setattr(func, 'all_conditions', [])
    setattr(func, 'when', when)
    setattr(func, 'then', then)

    @wraps(func)
    def wrapper(*args, **kwargs):
        func_in_main = globals()[func.__name__]

        if hasattr(func_in_main, 'all_conditions'):
            for condition in func_in_main.all_conditions:
                result = condition(*args, **kwargs)
                if result is not None:
                    return result

        return func(*args, **kwargs)
    return wrapper


@whenthen
def fract(x):
    return x * fract(x - 1)


@fract.when
def fract(x):
    return x == 0


@fract.then
def fract(x):
    return 1


@fract.when
def fract(x):
    return x > 5


@fract.then
def fract(x):
    return x * (x - 1) * (x - 2) * (x - 3) * (x - 4) * fract(x - 5)


print('__main__')

x = 10
print('fract({}) = {}'.format(x, fract(x)))

