def shout(word='да'):
    return word.capitalize() + '!'


print(shout())

scream = shout

print(scream())
del shout
try:
    print(shout())
except NameError as e:
    print(e)

print(scream())


def talk():
    def whisper(word='да'):
        return word.lower()+'...'

    print(whisper())


talk()
try:
    print(whisper())
except NameError as e:
    print(e)


def getTalk(type='shout'):
    def shout(word='да'):
        return word.capitalize() + '!'

    def whisper(word='да'):
        return word.lower()+'...'

    if type == 'shout':
        return shout
    else:
        return whisper


talk = getTalk()

print(talk)

print(talk())

print(getTalk('whisper'))
print(getTalk('whisper')())


def doSomethingBefore(func):
    print('Я делаю что-то перед функцией, которую ты передал мне')
    print(func())


doSomethingBefore(scream)


print('-'*40)


def my_decorator(func):
    print('Я обычная функция')
    def wrapper():
        print('Я - функция, возвращаемая декоратором')
        func()
    return wrapper


def lazy_function():
    print('zzzzz')


decorated_function = my_decorator(lazy_function)


@my_decorator
def lazy_function():
    print('zzzzzzzzzzzzzz')


print('-'*40)


def decorator_maker():
    print('Я создаю декораторы и буду вызвантолько раз, когда ты попросишь создать декоратор.')

    def my_decorator(func):
        print('Я декоратор, буду вызван только раз в момент декорирования функции.')

        def wrapped():
            print('я - обертка вокруг декорируемой функции. И буду вызываться каждый раз когда вызывается функция.')
            return func()

        print('я возвращаю обернутую функцию')
        return wrapped

    print('я возвращаю декоратор')
    return my_decorator


new_decorator = decorator_maker()

print('-'*40)


def decorated_function():
    print('Я декорируемая функция')


decorated_function = new_decorator(decorated_function)

print('-'*40)

decorated_function()
decorated_function()

print('-'*40)


def decorated_function():
    print('Я декорируемая функция')


decorated_function = decorator_maker()(decorated_function)
print('-'*40)
decorated_function()
print('-'*40)
print('-'*40)


@decorator_maker()
def decorated_function():
    print('Я декорируемая функция')


print('-'*40)
decorated_function()


