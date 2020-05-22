from ..repository import commentrepository


class Comment:
    def __init__(self, id, text, datetime, user, parent_post, parent_comment):
        self.id = id
        self.text = text
        self.datetime = datetime
        self.user = user
        self.parent_post = parent_post
        self.parent_comment = parent_comment
        self._child_comments = []

    @property
    def child_comments(self):
        comment_repository = commentrepository.CommentRepository()
        self._child_comments = comment_repository.find_by_parent_comment(self)
        return self._child_comments
