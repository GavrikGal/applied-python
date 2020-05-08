from collections.abc import MutableMapping
from functools import wraps
from typing import Iterator
import os


def _update_dict(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        self._temp_dic = {}
        try:
            for file_name in os.listdir(self._path):
                with open(self._path + os.path.sep + file_name) as f:
                    self._temp_dict[file_name] = f.readline()
        except OSError:
            print("can't open " + str(self._path))
        return func(self, *args, **kwargs)
    return wrapper


class DirDict(MutableMapping):
    def __init__(self, path):
        self._path = path
        self._temp_dict = {}
        if not os.path.isdir(self._path):
            os.mkdir(path)

    @_update_dict
    def __delitem__(self, k: '_KT') -> None:
        if k in self:
            try:
                os.remove(self._path + os.path.sep + k)
            except FileNotFoundError:
                print('item with key: ' + str(self._path + os.path.sep + k) + ' not found')
            except PermissionError as error:
                print("can't delete item with key: " + str(self._path + os.path.sep + k) + str(error.args[0]))

    @_update_dict
    def __getitem__(self, k: '_KT') -> '_VT_co':
        return self._temp_dict[k]

    def __len__(self) -> int:
        return len(os.listdir(self._path))

    @_update_dict
    def __iter__(self) -> Iterator['_T_co']:
        for i in self._temp_dict.items():
            yield i

    @_update_dict
    def items(self):
        for i in self:
            yield i

    @_update_dict
    def keys(self):
        for k in self._temp_dict.keys():
            yield k

    @_update_dict
    def values(self):
        for v in self._temp_dict.values():
            yield v

    def __setitem__(self, k: '_KT', v: '_VT') -> None:
        try:
            with open(self._path + os.path.sep + k, 'w') as f:
                f.write(v)
                f.close()
        except OSError:
            print("can't write data on disk")


test_d = DirDict('d:\Temp\dir_dict')
print('len() - ', len(test_d))
print('items:')
for key, value in test_d:
    print('\t' + str(key) + ' - ' + str(value))
test_d['test_write'] = 'string to test to write'
print('len() - ', len(test_d))
print('update items:')
for key, value in test_d:
    print('\t' + str(key) + ' - ' + str(value))
del test_d['test_write']
print('len() - ', len(test_d))
print('update items after deleting:')
for key, value in test_d.items():
    print('\t' + str(key) + ' - ' + str(value))

print('test keys:')
for key in test_d.keys():
    print(key, end=', ')

print('test value:')
for value in test_d.values():
    print(value, end=', ')
