from flask_login import UserMixin


# from db import get_db
class User(UserMixin):
    def __init__(self, id_, name, email, profile_pic):
        self.id = id_
        self.name = name
        self.email = email
        self.profile_pic = profile_pic

    @staticmethod
    def get(user_id):
        return DB.get(user_id)

    @staticmethod
    def create(id_, name, email, profile_pic):
        DB[id_] = User(id_, name, email, profile_pic)
        print(DB[id_])


DB = {"1234": User("1234", "Mi", "test@gmail.com", "")}
