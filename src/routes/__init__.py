from .. import api
from .v1 import Ping
from .v1 import CreateWagers, FetchWagers, FetchAllWagers
from .v1 import CreateParties, FetchParties, FetchAllParties, UpdateParties

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
