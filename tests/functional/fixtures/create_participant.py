import pytest
from src import services


@pytest.fixture
def create_participant():
    def _method(party_uuid, user_uuid):
        return services.ParticipantService().create(party_uuid=party_uuid, user_uuid=user_uuid, status='pending')

    return _method
