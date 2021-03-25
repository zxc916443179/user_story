from .models import User
from hashlib import md5

class UserController:
    def __init__(self):
        pass

    @staticmethod
    def create(username, password):
        userModel = User()
        userModel.username = username
        userModel.password = md5(password.encode('utf-8')).hexdigest()
        userModel.save()
        return userModel
    
    @staticmethod
    def get_by_username(username):
        return User.objects.filter(username=username)
