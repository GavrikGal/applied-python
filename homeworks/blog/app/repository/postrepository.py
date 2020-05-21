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

    def update_post(self, post_id, title, content, blog_ids) -> bool:
        with UseDataBase(self.dbconfig) as cursor:
            _SQL = """UPDATE posts 
                    SET title=%s, content=%s 
                    WHERE id=%s"""
            cursor.execute(_SQL, (title, content, post_id,))
            # post_id = cursor.lastrowid

            _SQL = """DELETE FROM blogs_posts WHERE post_id=%s"""
            _VAL = (post_id,)
            cursor.execute(_SQL, _VAL)

            for blog_id in blog_ids:
                _SQL = """INSERT INTO blogs_posts
                        (blog_id, post_id)
                        VALUES 
                        (%s, %s)"""
                _VAL = (blog_id, post_id, )
                cursor.execute(_SQL, _VAL)

    def find_by_blog_id(self, blog_id):
        with UseDataBase(self.dbconfig) as cursor:
            _SQL = """SELECT p.id, p.title, p.content, p.datetime
                      FROM blogs AS b, posts AS p, blogs_posts AS bp
                      WHERE b.id = %s
                            AND bp.post_id = p.id
                            AND bp.blog_id = b.id
                            AND b.deleted = 0
                            AND p.deleted = 0
                      ORDER BY p.datetime DESC;"""
            _VAL = (blog_id,)
            cursor.execute(_SQL, _VAL)
            contents = cursor.fetchall()
            if contents is not None:
                return [Post(content[0],
                             content[1],
                             content[2],
                             content[3]) for content in contents]
            else:
                raise PostNotFoundError('Посты с заданными ID не найдены')

    def find_by_id(self, post_id):
        with UseDataBase(self.dbconfig) as cursor:
            _SQL = """SELECT id, title, content, datetime
                        FROM posts
                        WHERE id = %s
                        AND deleted=0"""
            _VAL = (post_id,)
            cursor.execute(_SQL, _VAL)
            content = cursor.fetchone()
            if content is not None:
                return Post(*content)
            else:
                raise PostNotFoundError('Пост с заданным Id не найден')

    def delete_post(self, id):
        with UseDataBase(self.dbconfig) as cursor:
            _SQL = """UPDATE posts SET deleted=1 WHERE id = %s"""
            cursor.execute(_SQL, (id,))
