from app.storage import db
from hashlib import sha256
from time import time
import pymongo
from config import TOKEN_EXPIRE_LIMIT


def generate_token(email, password):
    user = db.users.find_one({'email': email, 'password': password})
    if user:
        t = int(time())
        token = sha256(
            (str(user['_id']) + '|' + str(t)).encode('utf8')).hexdigest()
        db.tokens.insert({'uid': user['_id'],
                          'token': token,
                          'timestamp': t})
        return token


def get_user_from_token(token):
    current_time = time()
    token_record = db.tokens.find_one({'token': token})
    if not token_record:
        return None
    user = db.users.find_one({'_id': token_record['uid']})

    latest_token_record = db.tokens.find_one(
        {'uid': token_record['uid']},
        sort=(('_id', pymongo.DESCENDING),))

    if latest_token_record['token'] != token_record['token']:
        print('#! Removing expired token.')
        db.tokens.remove(token_record)
        return None

    elif current_time - latest_token_record['timestamp'] > TOKEN_EXPIRE_LIMIT:
        db.tokens.remove(token_record)
        return None

    return user
