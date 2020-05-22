from ..entity.comment import Comment
from ..entity.post import Post
from ..entity.user import User
from ..repository.commentrepository import CommentRepository


class CommentService:
    def __init__(self):
        self.comment_repository = CommentRepository()

    def add_comment(self, text: str, user: User, parent_post: Post, parent_comment: Comment) -> None:
        try:
            self.comment_repository.add_comment(text, user, parent_post, parent_comment)
        except Exception as err:
            print(str(err))

    def find_by_id(self, id):
        try:
            return self.comment_repository.find_by_id(id)
        except Exception as err:
            print(str(err))
