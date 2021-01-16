import pytest
from src import services


@pytest.fixture
def create_participant():
    def _method(party_uuid, member_uuid):
        return services.ParticipantService().create(party_uuid=party_uuid, member_uuid=member_uuid, status='pending')

    return _method
