from .. import api
from .v1 import Ping
from .v1 import Create as CreateWager, Destroy as DestroyWager, Fetch as FetchWager, FetchAll as FetchAllWager, \
    Update as UpdateWager

# Ping
api.add_resource(Ping, '/ping', methods=['GET'])

# Wager
api.add_resource(CreateWager, '/', methods=['POST'])
api.add_resource(DestroyWager, '/<uuid:uuid>', methods=['DELETE'])
api.add_resource(FetchWager, '/<uuid:uuid>', methods=['GET'])
api.add_resource(FetchAllWager, '/', methods=['GET'])
api.add_resource(UpdateWager, '/<uuid:uuid>', methods=['PUT'])
