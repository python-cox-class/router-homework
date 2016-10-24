from flask import Flask, request
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)


database = {
    'routers': {
        '_last_id': 2,
        1: {'url': 'http://somewhere', 'interfaces': []},
        2: {'url': 'http://somewhere-else', 'interfaces': []},
    },
    'links': {
        '_last_id': 2,
        1: {'netmask': '192.168.0.0/16', 'interfaces': []},
        2: {'netmask': '192.169.0.0/16', 'interfaces': []},
    },
    'interfaces': {
        '_last_id': 2,
        1: {'router': None, 'link': None},
        2: {'router': None, 'link': None},
    },
}


class RestCollection(Resource):

    def get(self):
        return dict(
            (k, v) for k, v in database[self.cname].items()
            if not (isinstance(k, basestring) and k.startswith('_')))

    def post(self):
        coll = database[self.cname]
        coll['_last_id'] += 1
        id = coll['_last_id']
        coll[id] = request.json
        return request.json


class RestResource(Resource):

    def get(self, id):
        return database[self.cname][id]

    def put(self, id):
        database[self.cname][id] = request.json
        return request.json

    def delete(self, id):
        database[self.cname].pop(id)
        return {}


class RouterCollection(RestCollection):
    cname = 'routers'


class Router(RestResource):
    cname = 'routers'


class LinkCollection(RestCollection):
    cname = 'links'


class Link(RestResource):
    cname = 'links'


class InterfaceCollection(RestCollection):
    cname = 'interfaces'


class Interface(RestResource):
    cname = 'interfaces'


api.add_resource(RouterCollection, '/api/router')
api.add_resource(Router, '/api/router/<int:id>')

api.add_resource(LinkCollection, '/api/link')
api.add_resource(Link, '/api/link/<int:id>')

api.add_resource(InterfaceCollection, '/api/interface')
api.add_resource(Interface, '/api/interface/<int:id>')


if __name__ == '__main__':
    app.run(debug=True)
