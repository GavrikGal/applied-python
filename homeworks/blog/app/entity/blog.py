from ..repository import postrepository

class Blog:
    def __init__(self, id: int, name: str, user: 'User', deleted: bool = False):
        self.id = id
        self.name = name
        self.user = user
        self.deleted = deleted
        self._posts = []

    @property
    def posts(self):
        post_repository = postrepository.PostRepository()
        self._posts = post_repository.find_by_blog_id(self.id)
        return self._posts
