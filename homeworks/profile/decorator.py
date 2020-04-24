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
