from typing import Union

from .. import config
from ..repository import blogrepository
from ..service import usersservice


class Blogs_service:
    def __init__(self):
        self.blog_repository = blogrepository.BlogRepository()
        # self.user_service = usersservice.UsersService()
        self.dbconfig = config.dbconfig

    def add_blog(self, name, user_id):
        deleted = False
        try:
            self.blog_repository.add_blog(name,
                                          deleted,
                                          user_id)
        except Exception as err:
            print(str(err))

    def update_blog(self, id, name):
        try:
            self.blog_repository.update_blog(id, name)
        except Exception as err:
            print(str(err))

    def all_blogs(self) -> 'list of Blog':
        try:
            return self.blog_repository.all_blogs()
        except Exception as err:
            print(str(err))

    def all_user_blogs(self, user_id) -> 'list of Blog':
        try:
            return self.blog_repository.all_user_blogs(user_id)
        except Exception as err:
            print(str(err))

    def delete_blog_id(self, id):
        try:
            self.blog_repository.delete_blog_id(id)
        except Exception as err:
            print(str(err))

    def find_by_id(self, id) -> Union['Blog', bool]:
        try:
            blog = self.blog_repository.find_by_id(id)
            return blog
        except Exception as err:
            print(str(err))
        return False
