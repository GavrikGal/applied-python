# from ..repository.blogrepository import BlogRepository
from ..repository import blogrepository, commentrepository


class User:
    def __init__(self, id, first_name, last_name, login, password_hash):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.login = login
        self.password_hash = password_hash
        self._blogs = []
        self._comments = []

    blogs = property()

    @blogs.getter
    def blogs(self):
        blog_repository = blogrepository.BlogRepository()
        self._blogs = blog_repository.all_user_blogs(self.id)
        return self._blogs

    @property
    def comments(self) -> 'Comment':
        comment_repository = commentrepository.CommentRepository()
        self._comments = comment_repository.find_by_user(self)
        return self._comments
