from .. import api
from .v1 import Ping
from .v1 import CreateWager, DestroyWager, FetchWager, UpdateWager

# Ping
api.add_resource(Ping, '/ping', methods=['GET'])

# Wager
api.add_resource(CreateWager, '/', methods=['POST'])
api.add_resource(DestroyWager, '/<uuid>', methods=['DELETE'])
api.add_resource(FetchWager, '/', '/<uuid>', methods=['GET'])
api.add_resource(UpdateWager, '/<uuid>', methods=['PUT'])
