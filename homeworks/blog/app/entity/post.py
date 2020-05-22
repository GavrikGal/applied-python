from ..repository import blogrepository, commentrepository


class Post:
    def __init__(self, id, title, content, datetime):
        self.id = id
        self.title = title
        self.content = content
        self.datetime = datetime
        self._blogs = []
        self._comments = []

    @property
    def blogs(self):
        blog_repository = blogrepository.BlogRepository()
        self._blogs = blog_repository.find_by_post_id(self.id)
        return self._blogs

    @property
    def comments(self):
        comment_repository = commentrepository.CommentRepository()
        self._comments = comment_repository.find_by_parent_post(self)
        return self._comments
