from flask import session, redirect
from functools import wraps


def authenticated(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if 'user_name' in session:
            result = func(*args, **kwargs)
        else:
            result = redirect('/')
        return result

    return wrapper
