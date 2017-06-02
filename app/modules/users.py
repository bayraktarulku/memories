from app.storage import db
from pymongo.errors import DuplicateKeyError
from app.modules.auth import get_user_from_token


def create_user(email, password, nickname):
    user = {'email': email,
            'password': password,
            'nickname': nickname,
            'active': True}
    try:
        db.users.insert(user)
    except DuplicateKeyError:
        return None
    return str(user['_id'])


def get_user(token):
    user = get_user_from_token(token)
    return user


def change_password(token, new_password):
    user = get_user_from_token(token)
    if user:
        user['password'] = new_password
        db.users.save(user)
        return True
    return False


def delete_user(email, password, token):
    user = get_user_from_token(token)
    if user:
        db.users.remove(user)
        return True
    return False
