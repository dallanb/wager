import pytest

from src import services


@pytest.fixture(scope="function")
def seed_participant():
    # create participant
    pytest.participant = services.ParticipantService().create(party_uuid=pytest.party.uuid,
                                                              member_uuid=pytest.member_uuid,
                                                              status='pending')
    return pytest.participant
