import pytest

from src import services


@pytest.fixture(scope="function")
def seed_stake():
    # create stake
    pytest.stake = services.StakeService().create(participant_uuid=pytest.participant.uuid,
                                                  amount=pytest.buy_in)
    return pytest.stake
