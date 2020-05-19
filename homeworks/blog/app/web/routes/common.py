from flask import session, redirect
from functools import wraps


def authenticated(func):
    @wraps(func)
    def wrapper():
        if 'user_name' in session:
            result = func()
        else:
            result = redirect('/')
        return result

    return wrapper
