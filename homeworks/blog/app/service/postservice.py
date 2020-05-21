from ..repository import postrepository


class PostService:
    def __init__(self):
        self.post_repository = postrepository.PostRepository()

    def add_post(self, title, content, blog_ids) -> None:
        try:
            self.post_repository.add_post(title,
                                          content,
                                          blog_ids)
        except Exception as err:
            print(str(err))

    def update_post(self, id, title, content, blog_ids):
        try:
            self.post_repository.update_post(id,
                                             title,
                                             content,
                                             blog_ids)
        except Exception as err:
            print(str(err))

    def find_by_blog_id(self, blog_id):
        try:
            return self.post_repository.find_by_blog_id(blog_id)
        except Exception as err:
            print(str(err))

    def find_by_id(self, post_id):
        try:
            return self.post_repository.find_by_id(post_id)
        except Exception as err:
            print(str(err))

    def delete_post(self, id):
        try:
            self.post_repository.delete_post(id)
        except Exception as err:
            print(str(err))
