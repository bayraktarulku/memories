from flask import Blueprint, request, abort
from flask_restful import Api, Resource
from app.modules.auth import generate_token
from schema import Schema, Use, SchemaError

api_bp = Blueprint('auth_api', __name__)
api = Api(api_bp)

AUTH_SCHEMA = Schema({
    'email': Use(str),
    'password': Use(str)
})


class Auth(Resource):
    def post(self):
        try:
            data = AUTH_SCHEMA.validate(request.json)
        except SchemaError as e:
            abort(400)

        email = data['email']
        password = data['password']
        token = generate_token(email, password)
        if not token:
            return {'status': 'ERROR'}

        return {'status': 'OK',
                'token': token}


api.add_resource(Auth, '/api/auth')
