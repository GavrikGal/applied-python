from .DBcm import UseDataBase
from .. import config
from ..entity.blog import Blog
from .usersrepository import UsersRepository


class BlogNotFoundError(Exception):
    pass


class BlogRepository:
    def __init__(self):
        self.dbconfig = config.dbconfig
        self.user_repository = UsersRepository()

    def add_blog(self, name, deleted, user_id):
        with UseDataBase(self.dbconfig) as cursor:
            _SQL = """INSERT INTO blogs 
                    (name, deleted, user_id) 
                    VALUES 
                    (%s, %s, %s)"""
            cursor.execute(_SQL, (name,
                                  deleted,
                                  user_id,))

    def update_blog(self, id, name):
        with UseDataBase(self.dbconfig) as cursor:
            _SQL = """UPDATE blogs SET name=%s WHERE id=%s"""
            cursor.execute(_SQL, (name, id,))


    def all_blogs(self):
        with UseDataBase(self.dbconfig) as cursor:
            _SQL = """SELECT id, name, user_id, deleted FROM blogs WHERE deleted = 0"""
            cursor.execute(_SQL)
            contents = cursor.fetchall()
            blogs = [Blog(content[0],
                          content[1],
                          self.user_repository.find_by_id(content[2]),
                          content[3]) for content in contents]
        return blogs

    def all_user_blogs(self, user_id):
        with UseDataBase(self.dbconfig) as cursor:
            _SQL = """SELECT id, name, user_id, deleted FROM blogs WHERE deleted = 0 AND user_id = %s"""
            cursor.execute(_SQL, (user_id,))
            contents = cursor.fetchall()
            user = self.user_repository.find_by_id(user_id)
            blogs = [Blog(content[0],
                          content[1],
                          user,
                          content[3]) for content in contents]
        return blogs

    def delete_blog_id(self, id):
        with UseDataBase(self.dbconfig) as cursor:
            _SQL = """UPDATE blogs SET deleted=1 WHERE id = %s"""
            cursor.execute(_SQL, (id,))

    def find_by_id(self, id):
        with UseDataBase(self.dbconfig) as cursor:
            _SQL = """SELECT id, name, user_id, deleted 
                        FROM blogs 
                        WHERE deleted = 0 AND id = %s"""
            cursor.execute(_SQL, (id,))
            content = cursor.fetchone()
            if content is not None:
                return Blog(content[0],
                            content[1],
                            self.user_repository.find_by_id(content[2]),
                            content[3])
            else:
                raise BlogNotFoundError('Блог с заданным ID не найден')

    def find_by_post_id(self, post_id):
        with UseDataBase(self.dbconfig) as cursor:
            _SQL = """SELECT b.id, b.name, b.user_id, b.deleted
                      FROM blogs AS b, posts AS p, blogs_posts AS bp
                      WHERE p.id = %s
                            AND bp.post_id = p.id
                            AND bp.blog_id = b.id
                            AND b.deleted = 0;"""
            _VAL = (post_id,)
            cursor.execute(_SQL, _VAL)
            contents = cursor.fetchall()
            if contents is not None:
                return [Blog(content[0],
                             content[1],
                             self.user_repository.find_by_id(content[2]),
                             content[3]) for content in contents]
            else:
                raise BlogNotFoundError('Блог с заданным ID не найден')

