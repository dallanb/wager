import pytest
from src import services, models


@pytest.fixture
def create_participant():
    def _method(party_uuid, user_uuid):
        base = services.Base()
        participant = base.init(model=models.Participant, party_uuid=party_uuid, user_uuid=user_uuid, status='pending')
        participant = base.save(instance=participant)
        return participant

    return _method
