from collections.abc import MutableMapping
from functools import wraps
from typing import Iterator
import os


class DirDict(MutableMapping):

    def _update(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            for file_name in os.listdir(self._path):
                with open(self._path + os.path.sep + file_name) as f:
                    self._dic[file_name] = f.readline()
            return func(self, *args, **kwargs)

        return wrapper

    def __delitem__(self, v: '_KT') -> None:
        pass

    @_update
    def __getitem__(self, k: '_KT') -> '_VT_co':
        return self._dic[k]

    def __len__(self) -> int:
        return len(os.listdir(self._path))

    @_update
    def __iter__(self) -> Iterator['_T_co']:
        for i in self._dic.items():
            yield i

    def __setitem__(self, k: '_KT', v: '_VT') -> None:
        pass

    def __init__(self, path):
        self._path = path
        self._dic = {}
        if not os.path.isdir(self._path):
            os.mkdir(path)


d = DirDict('d:\Temp\dir_dict')
print('len() - ', len(d))
print('items:')
for k, v in d:
    print('\t' + str(k) + ' - ' + str(v))
