from .. import api
from .v1 import Ping, Wager

api.add_resource(Ping, '/ping', methods=['GET'])
api.add_resource(Wager, '/', '/<uuid>', methods=['GET', 'POST', 'PUT', 'DELETE'])