class User:
    def __init__(self, id, first_name, last_name, login, password_hash):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.login = login
        self.password_hash = password_hash
