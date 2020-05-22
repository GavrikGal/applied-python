from typing import Union

from .DBcm import UseDataBase
from .. import config
from ..entity.user import User


class UserNotFoundError(Exception):
    pass


class UsersRepository:
    def __init__(self):
        self.dbconfig = config.dbconfig

    def all_users(self) -> 'list of User':
        with UseDataBase(self.dbconfig) as cursor:
            _SQL = """SELECT id, first_name, last_name, login, password FROM users"""
            cursor.execute(_SQL)
            contents = cursor.fetchall()
            users = [User(*item) for item in contents]
        if users is not None:
            return users
        else:
            raise UserNotFoundError('Пользователи не найдены')

    def add_user(self, first_name, last_name, login, password) -> bool:
        with UseDataBase(self.dbconfig) as cursor:
            _SQL = """INSERT INTO users 
                    (first_name, last_name, login, password) 
                    VALUES 
                    (%s, %s, %s, %s)"""
            return cursor.execute(_SQL, (first_name,
                                  last_name,
                                  login,
                                  password,))

    def find_by_login(self, login) -> Union[User, bool]:
        with UseDataBase(self.dbconfig) as cursor:
            _SQL = """SELECT id, first_name, last_name, login, password 
                    FROM users 
                    WHERE login = %s"""
            cursor.execute(_SQL, (login,))
            content = cursor.fetchone()
            if content is not None:
                return User(*content)
            else:
                raise UserNotFoundError('Пользователь с заданным логином не найден')

    def find_by_id(self, id) -> Union[User, bool]:
        with UseDataBase(self.dbconfig) as cursor:
            _SQL = """SELECT id, first_name, last_name, login, password 
                    FROM users 
                    WHERE id = %s"""
            cursor.execute(_SQL, (id,))
            content = cursor.fetchone()
            if content is not None:
                return User(*content)
            else:
                raise UserNotFoundError('Пользователь с заданным ID не найден')
