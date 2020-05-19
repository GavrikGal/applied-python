from typing import Union

from ..entity.user import User
from . import password_service
from ..repository import usersrepository


class UsersService:
    def __init__(self):
        self.users_repository = usersrepository.UsersRepository()

    def all_users(self) -> 'list of User':
        try:
            users = self.users_repository.all_users()
            return users
        except Exception as err:
            print(str(err))
        return False

    def add_user(self, first_name, last_name, login, password) -> None:
        try:
            self.users_repository.add_user(first_name,
                                          last_name,
                                          login,
                                          password_service.hash_password(password))
        except Exception as err:
            print(str(err))

    def find_by_login(self, login) -> Union[User, bool]:
        try:
            user = self.users_repository.find_by_login(login)
            return user
        except Exception as err:
            print(str(err))
        return False

    def find_by_id(self, id) -> Union[User, bool]:
        try:
            user = self.users_repository.find_by_id(id)
            return user
        except Exception as err:
            print(str(err))
        return False

