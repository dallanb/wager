from .. import api
from .v1 import PingAPI
from .v1 import WagersAPI, WagersListAPI
from .v1 import PartiesAPI, PartiesListAPI
from .v1 import ParticipantsAPI, ParticipantsListAPI
from .v1 import StakesAPI, StakesListAPI

# Ping
api.add_resource(PingAPI, '/ping', methods=['GET'])

# Wagers
api.add_resource(WagersAPI, '/wagers/<uuid:uuid>', endpoint="wager")
api.add_resource(WagersListAPI, '/wagers', endpoint="wagers")

# Parties
api.add_resource(PartiesAPI, '/parties/<uuid:uuid>', endpoint="party")
api.add_resource(PartiesListAPI, '/wagers/<uuid:uuid>/parties', '/parties', endpoint="parties")

# Participants
api.add_resource(ParticipantsAPI, '/participants/<uuid:uuid>', endpoint="participant")
api.add_resource(ParticipantsListAPI, '/parties/<uuid:uuid>/participants', '/participants', endpoint="participants")

# Stakes
api.add_resource(StakesAPI, '/stakes/<uuid:uuid>', endpoint="stake")
api.add_resource(StakesListAPI, '/participants/<uuid:uuid>/stakes', '/stakes', endpoint="stakes")
