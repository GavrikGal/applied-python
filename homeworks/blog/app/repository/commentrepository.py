from typing import Tuple

from .DBcm import UseDataBase
from .. import config
# from ..entity.post import Post
from ..entity.comment import Comment
from ..entity.user import User
from . import usersrepository, postrepository


class CommentNotFoundError(Exception):
    pass


class CommentRepository:
    def __init__(self):
        self.db_config = config.dbconfig
        self.user_repository = usersrepository.UsersRepository()
        self.post_repository = postrepository.PostRepository()

    def add_comment(self, text: str, user: User, parent_post: 'Post', parent_comment: Comment) -> None:
        with UseDataBase(self.db_config) as cursor:
            if parent_post:
                parent_post_id = parent_post.id
            else:
                parent_post_id = None
            if parent_comment:
                parent_comment_id = parent_comment.id
            else:
                parent_comment_id = None
            _SQL = """INSERT INTO comments 
                    (text, user_id, parent_post_id, parent_comment_id) 
                    VALUES 
                    (%s, %s, %s, %s)"""
            _VAL = (text, user.id, parent_post_id, parent_comment_id,)
            return cursor.execute(_SQL, _VAL)

    def find_by_parent_post(self, parent_post: 'Post') -> Tuple[Comment]:
        with UseDataBase(self.db_config) as cursor:
            _SQL = """SELECT id, text, datetime, user_id, parent_post_id, parent_comment_id
                        FROM comments
                        WHERE parent_post_id=%s
                        ORDER BY datetime DESC"""
            _VAL = (parent_post.id,)
            cursor.execute(_SQL, _VAL)
            contents = cursor.fetchall()
            comments = []
            for content in contents:
                parent_post = None
                parent_comment = None
                if content[4]:
                    parent_post = self.post_repository.find_by_id(content[4])
                if content[5]:
                    parent_comment = self.find_by_id(content[5])
                comments.append(Comment(content[0],
                                        content[1],
                                        content[2],
                                        self.user_repository.find_by_id(content[3]),
                                        parent_post,
                                        parent_comment))
            # comments = [Comment(content[0],
            #                     content[1],
            #                     self.user_repository.find_by_id(content[2]),
            #                     )
            #             for content in contents]
            return comments

    def find_by_parent_comment(self, parent_comment: Comment) -> Tuple[Comment]:
        with UseDataBase(self.db_config) as cursor:
            _SQL = """SELECT id, text, datetime, user_id, parent_post_id, parent_comment_id
                        FROM comments
                        WHERE parent_comment_id=%s
                        ORDER BY datetime DESC"""
            _VAL = (parent_comment.id,)
            cursor.execute(_SQL, _VAL)
            contents = cursor.fetchall()
            comments = []
            for content in contents:
                parent_post = None
                parent_comment = None
                if content[4]:
                    parent_post = self.post_repository.find_by_id(content[4])
                if content[5]:
                    parent_comment = self.find_by_id(content[5])
                comments.append(Comment(content[0],
                                        content[1],
                                        content[2],
                                        self.user_repository.find_by_id(content[3]),
                                        parent_post,
                                        parent_comment))
            return comments

    def find_by_id(self, id) -> Comment:
        with UseDataBase(self.db_config) as cursor:
            _SQL = """SELECT id, text, datetime, user_id, parent_post_id, parent_comment_id
                        FROM comments
                        WHERE id=%s"""
            _VAL = (id, )
            cursor.execute(_SQL, _VAL)
            content = cursor.fetchone()
            if content:
                parent_post = None
                parent_comment = None
                if content[4]:
                    parent_post = self.post_repository.find_by_id(content[4])
                if content[5]:
                    parent_comment = self.find_by_id(content[5])
                comment = Comment(content[0],
                                  content[1],
                                  content[2],
                                  self.user_repository.find_by_id(content[3]),
                                  parent_post,
                                  parent_comment)
                return comment
            else:
                raise CommentNotFoundError('Комментарий с заданным Id не найден')

    def find_by_user(self, user) -> Comment:
        with UseDataBase(self.db_config) as cursor:
            _SQL = """SELECT id, text, datetime, user_id, parent_post_id, parent_comment_id
                        FROM comments
                        WHERE user_id=%s
                        ORDER BY datetime DESC"""
            _VAL = (user.id, )
            cursor.execute(_SQL, _VAL)
            contents = cursor.fetchall()
            comments = []
            for content in contents:
                parent_post = None
                parent_comment = None
                if content[4]:
                    parent_post = self.post_repository.find_by_id(content[4])
                if content[5]:
                    parent_comment = self.find_by_id(content[5])
                comments.append(Comment(content[0],
                                        content[1],
                                        content[2],
                                        user,
                                        parent_post,
                                        parent_comment))

            return comments
