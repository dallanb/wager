import pytest
from src import services


@pytest.fixture
def create_participant():
    def _method(party_uuid, user_uuid):
        participant = services.init_participant(party_uuid=party_uuid, user_uuid=user_uuid, status='pending')
        participant = services.save_participant(participant)
        return participant

    return _method
