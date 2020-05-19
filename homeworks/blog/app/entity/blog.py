class Blog:
    def __init__(self, id: int, name: str, user: 'User', deleted: bool = False):
        self.id = id
        self.name = name
        self.user = user
        self.deleted = deleted
