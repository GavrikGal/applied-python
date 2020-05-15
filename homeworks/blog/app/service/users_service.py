from typing import Union

from ..entity.user import User
from ..repository.DBcm import UseDataBase
from .. import config
from . import password_service


class Users_service:
    def __init__(self):
        self.dbconfig = config.dbconfig

    def all_users(self) -> 'list of User':
        try:
            with UseDataBase(self.dbconfig) as cursor:
                _SQL = """SELECT id, first_name, last_name, login, password FROM users"""
                cursor.execute(_SQL)
                contents = cursor.fetchall()
                users = [User(*item) for item in contents]
            return users

        except Exception as err:
            print(str(err))
        return False

    def add_user(self, first_name, last_name, login, password) -> bool:
        try:
            with UseDataBase(self.dbconfig) as cursor:
                _SQL = """INSERT INTO users 
                        (first_name, last_name, login, password) 
                        VALUES 
                        (%s, %s, %s, %s)"""
                cursor.execute(_SQL, (first_name,
                                      last_name,
                                      login,
                                      password_service.hash_password(password),))
                return True

        except Exception as err:
            print(str(err))
        return False

    def find_by_login(self, login) -> Union[User, bool]:
        try:
            with UseDataBase(self.dbconfig) as cursor:
                _SQL = """SELECT id, first_name, last_name, login, password 
                        FROM users 
                        WHERE login = %s"""
                cursor.execute(_SQL, (login, ))
                content = cursor.fetchone()
                if content is None:
                    return False
                else:
                    return User(*content)
        except Exception as err:
            print(str(err))
        return False
