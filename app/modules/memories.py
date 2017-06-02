from app.storage import db
from app.modules.auth import get_user_from_token
from time import time
from bson.objectid import ObjectId

LAT_TOLERANCE = 0.0001
LONG_TOLERANCE = 0.0001


def create_memory(title, text, expire_time, coords, token):
    user = get_user_from_token(token)
    if user:
        memory = {'uid': user['_id'],
                  'title': title,
                  'text': text,
                  'time': int(time()),
                  'expire_time': expire_time,
                  'active': True,
                  'coord_lat': coords[0],
                  'coord_long': coords[1]}
        db.memories.insert(memory)
        return str(memory['_id'])


def get_memories_nearby(coords, token):
    user = get_user_from_token(token)
    if user:
        memories = db.memories.find({
            'coord_lat': {'$gt': coords[0] - LAT_TOLERANCE,
                          '$lt': coords[0] + LAT_TOLERANCE},
            'coord_long': {'$gt': coords[1] - LONG_TOLERANCE,
                           '$lt': coords[1] + LONG_TOLERANCE}
            }, {'_id': 1, 'title': 1, 'time': 1})
        for m in memories:
            yield {'id': str(m['_id']),
                   'title': m['title'],
                   'time': m['time']}


def get_memory(memory_id, coords, token):
    user = get_user_from_token(token)
    if user:
        memory = db.memories.find_one({
            '_id': ObjectId(memory_id),
            'coord_lat': {'$gt': coords[0] - LAT_TOLERANCE,
                          '$lt': coords[0] + LAT_TOLERANCE},
            'coord_long': {'$gt': coords[1] - LONG_TOLERANCE,
                           '$lt': coords[1] + LONG_TOLERANCE}
            }, {'_id': 0, 'title': 1, 'text': 1, 'time': 1, 'uid': 1})
        if not memory:
            return None
        user = db.users.find_one({'_id': memory['uid']},
                                 {'_id': 0, 'nickname': 1})
        memory['user'] = user['nickname']
        del memory['uid']
        return memory


def get_user_memories(user_id):
    user_memory = db.memories.find({'uid': ObjectId(user_id)},
                                   {'_id': 1, 'title': 1})
    return ({'id': str(m['_id']), 'title': m['title']} for m in user_memory)


def update_memory(memory_id, coords, token, data):
    data = {k: data[k] for k in data if k in ['text', 'title', 'active']}
    user = get_user_from_token(token)
    memory = get_memory(memory_id, coords, token)
    if not user or not memory:
        return False
    if memory['user'] == user['nickname']:
        r = db.memories.update({'_id': ObjectId(memory_id)},
                               {'$set': data},
                               upsert=False)
        print(r)
        return True
    return False
