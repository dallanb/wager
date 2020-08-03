import pytest
from src import services


@pytest.fixture
def create_participant(party_uuid, user_uuid):
    wager_party_participant = services.init_wager_party_participant()
    wager_party_participant.party_uuid = party_uuid
    wager_party_participant.user_uuid = user_uuid

    # status
    status = services.find_wager_party_participant_status_by_enum('pending')
    wager_party_participant.status_uuid = status.uuid

    wager_party_participant.save_wager_party_participant()
    return wager_party_participant
