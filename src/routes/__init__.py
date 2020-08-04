from .. import api
from .v1 import Ping
from .v1 import CreateWagers, FetchWagers, FetchAllWagers
from .v1 import CreateParties, FetchParties, FetchAllParties, UpdateParties
from .v1 import CreateParticipants, FetchParticipants, FetchAllParticipants
from .v1 import CreateStakes, FetchStakes, FetchAllStakes, UpdateStakes, DestroyStakes

# Ping
api.add_resource(Ping, '/ping', methods=['GET'])

# Wager
api.add_resource(CreateWagers, '/wagers', methods=['POST'], endpoint="create_wagers")
api.add_resource(FetchWagers, '/wagers/<uuid:uuid>', methods=['GET'], endpoint="fetch_wagers")
api.add_resource(FetchAllWagers, '/wagers', methods=['GET'], endpoint="fetch_all_wagers")

# Party
api.add_resource(CreateParties, '/wagers/<uuid:uuid>/parties', methods=['POST'], endpoint="create_parties")
api.add_resource(FetchParties, '/parties/<uuid:uuid>', methods=['GET'], endpoint="fetch_parties")
api.add_resource(FetchAllParties, '/parties', methods=['GET'], endpoint="fetch_all_parties")
api.add_resource(UpdateParties, '/parties/<uuid:uuid>', methods=['PUT'], endpoint="update_parties")

# Participants
api.add_resource(CreateParticipants, '/parties/<uuid:uuid>/participants', methods=['POST'],
                 endpoint="create_participants")
api.add_resource(FetchParticipants, '/participants/<uuid:uuid>', methods=['GET'], endpoint="fetch_participants")
api.add_resource(FetchAllParticipants, '/participants', methods=['GET'], endpoint="fetch_all_participants")

# Stakes
api.add_resource(CreateStakes, '/participants/<uuid:uuid>/stakes', methods=['POST'],
                 endpoint="create_stakes")
api.add_resource(FetchStakes, '/stakes/<uuid:uuid>', methods=['GET'],
                 endpoint="fetch_stakes")
api.add_resource(FetchAllStakes, '/stakes', methods=['GET'],
                 endpoint="fetch_all_stakes")
api.add_resource(UpdateStakes, '/stakes/<uuid:uuid>', methods=['PUT'],
                 endpoint="update_stakes")
api.add_resource(DestroyStakes, '/stakes/<uuid:uuid>', methods=['DELETE'],
                 endpoint="destroy_stakes")
