from .DBcm import UseDataBase
from .. import config
from ..entity.post import Post


class PostNotFoundError(Exception):
    pass


class PostRepository:
    def __init__(self):
        self.dbconfig = config.dbconfig

    def add_post(self, title, content, blog_ids) -> bool:
        with UseDataBase(self.dbconfig) as cursor:
            _SQL = """INSERT INTO posts 
                    (title, content) 
                    VALUES 
                    (%s, %s)"""
            cursor.execute(_SQL, (title, content, ))
            post_id = cursor.lastrowid

            for blog_id in blog_ids:
                _SQL = """INSERT INTO blogs_posts
                        (blog_id, post_id)
                        VALUES 
                        (%s, %s)"""
                _VAL = (blog_id, post_id, )
                cursor.execute(_SQL, _VAL)

    def find_by_blog_id(self, blog_id):
        with UseDataBase(self.dbconfig) as cursor:
            _SQL = """SELECT p.id, p.title, p.content
                      FROM blogs AS b, posts AS p, blogs_posts AS bp
                      WHERE b.id = %s
                            AND bp.post_id = p.id
                            AND bp.blog_id = b.id
                            AND b.deleted = 0;"""
            _VAL = (blog_id,)
            cursor.execute(_SQL, _VAL)
            contents = cursor.fetchall()
            if contents is not None:
                return [Post(content[0],
                             content[1],
                             content[2]) for content in contents]
            else:
                raise PostNotFoundError('Пост с заданным ID не найден')
