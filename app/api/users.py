from flask import Blueprint, request, abort
from flask_restful import Api, Resource
from app.modules.users import (create_user, get_user,
                               change_password, delete_user)
from app.modules.memories import get_user_memories
from schema import Schema, Use, SchemaError

api_bp = Blueprint('user_api', __name__)
api = Api(api_bp)

USER_SCHEMA = Schema({
    'email': Use(str),
    'password': Use(str),
    'nickname': Use(str),
})

USER_CHANGE_PASSWORD_SCHEMA = Schema({
    'new_password': Use(str),
})

DELETE_USER_SCHEMA = Schema({
    'email': Use(str),
    'password': Use(str),
})


class User(Resource):

    def get(self):
        token = request.headers.get('Authorization', None)
        if not token:
            abort(403)
        user = get_user(token)
        if not user:
            abort(401)
        user_memories = get_user_memories(str(user['_id']))
        return {'status': 'OK',
                'memory_ids': list(user_memories)}

    def post(self):
        try:
            data = USER_SCHEMA.validate(request.json)
        except SchemaError as e:
            return {'status': 'error'}
        user = create_user(**data)

        return {'status': 'OK'}

    def put(self):
        token = request.headers.get('Authorization', None)
        if not token:
            abort(403)
        try:
            data = USER_CHANGE_PASSWORD_SCHEMA.validate(request.json)
        except SchemaError as e:
            return {'status': 'error'}
        update_password = change_password(token, data['new_password'])

        return {'status': 'OK'}

    def delete(self):
        token = request.headers.get('Authorization', None)
        if not token:
            abort(403)
        try:
            data = DELETE_USER_SCHEMA.validate(request.json)
        except SchemaError as e:
            return {'status': 'OK'}
        data['token'] = token
        result = delete_user(**data)

        return {'status':'OK'}


api.add_resource(User, '/api/user')
