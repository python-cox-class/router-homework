from flask import Flask, request, url_for
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


class Root(Resource):

    def get(self):
        return {
            'routers': url_for('routercollection'),
            'links': url_for('linkcollection'),
            'interfaces': url_for('interfacecollection')
        }


class RestCollection(Resource):

    @property
    def cname(self):
        return self.resource.cname

    def get(self):
        return dict(
            (url_for(self.resource.endpoint, id=k), v)
            for k, v in database[self.cname].items()
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


class Router(RestResource):
    cname = 'routers'


class Link(RestResource):
    cname = 'links'


class Interface(RestResource):
    cname = 'interfaces'


class RouterCollection(RestCollection):
    resource = Router


class LinkCollection(RestCollection):
    resource = Link


class InterfaceCollection(RestCollection):
    resource = Interface

api.add_resource(Root, '/api')

api.add_resource(RouterCollection, '/api/router')
api.add_resource(Router, '/api/router/<int:id>')

api.add_resource(LinkCollection, '/api/link')
api.add_resource(Link, '/api/link/<int:id>')

api.add_resource(InterfaceCollection, '/api/interface')
api.add_resource(Interface, '/api/interface/<int:id>')


if __name__ == '__main__':
    app.run(debug=True)
