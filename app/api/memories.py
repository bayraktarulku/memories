from flask import Blueprint, request, abort
from flask_restful import Api, Resource
from app.modules.memories import (create_memory, get_memory,
                                  get_memories_nearby, update_memory)
from schema import Schema, Use, Optional, And, SchemaError

api_bp = Blueprint('memory_api', __name__)
api = Api(api_bp)

MEMORY_SAVE_SCHEMA = Schema({
    'title': And(Use(str), lambda s:  0 < len(s) < 65),
    'text': Use(str),
})

MEMORY_UPDATE_SCHEMA = Schema({
    Optional('title'): And(Use(str), lambda s:  0 < len(s) < 65),
    Optional('text'): Use(str),
})

MEMORY_DELETE_SCHEMA = Schema({
    'active': bool
    })


class Memory(Resource):
    def get(self):
        memory_id = request.args.get('id', None)
        try:
            coords = (float(request.args.get('lat')),
                      float(request.args.get('long')))
        except:
            coords = ()

        token = request.headers.get('Authorization', None)

        if not token:
            abort(403)
        if not all((coords[0] != None,
                    coords[1] != None)):
            abort(400)
        if memory_id:
            m = get_memory(memory_id, coords, token)
            print(m)
            if m:
                return {'status': 'OK',
                        'memory': m}
            else:
                abort(404)
        else:
            mem_list = get_memories_nearby(coords, token)
            return {'status': 'OK',
                    'memories': list(mem_list)}

    def post(self):
        token = request.headers.get('Authorization', None)
        if not token:
            abort(403)
        try:
            data = MEMORY_SAVE_SCHEMA.validate(request.json)
        except SchemaError as e:
            return {'status': 'error'}

        expire_time = '1479162279'
        coords = (26.0, 36.0)
        data['expire_time'] = expire_time
        data['coords'] = coords
        data['token'] = token
        memory = create_memory(**data)

        return {'status': 'OK',
                'memory_id': memory}

    def put(self):
        memory_id = request.args.get('id', None)

        try:
            coords = (float(request.args.get('lat')),
                      float(request.args.get('long')))
        except:
            coords = ()

        token = request.headers.get('Authorization', None)
        if not token:
            abort(403)
        try:
            data = MEMORY_UPDATE_SCHEMA.validate(request.json)

        except SchemaError as e:
            return {'status': 'error'}
        result = update_memory(memory_id, coords, token, data)

        return {'status': 'OK'}

    def delete(self):
        memory_id = request.args.get('id', None)

        try:
            coords = (float(request.args.get('lat')),
                      float(request.args.get('long')))
        except:
            coords = ()

        token = request.headers.get('Authorization', None)
        if not token:
            abort(403)
        try:
            data = MEMORY_DELETE_SCHEMA.validate(request.json)

        except SchemaError as e:
            return {'status': 'error'}

        result = update_memory(memory_id, coords, token, data)
        return {'status': 'OK'}


api.add_resource(Memory, '/api/memory')
