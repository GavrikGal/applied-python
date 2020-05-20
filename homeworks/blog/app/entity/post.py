from ..repository import blogrepository


class Post:
    def __init__(self, id, title, content):
        self.id = id
        self.title = title
        self.content = content
        self._blogs = []

    @property
    def blogs(self):
        blog_repository = blogrepository.BlogRepository()
        self._blogs = blog_repository.find_by_post_id(self.id)
        return self._blogs
