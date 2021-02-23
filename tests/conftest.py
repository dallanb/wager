from uuid import uuid4

import pytest
from .fixtures import *


def pytest_configure(config):
    pytest.wager = None
    pytest.contest = None
    pytest.party = None
    pytest.participant = None
    pytest.stake = None
    pytest.payouts = None
    pytest.contest_uuid = uuid4()
    pytest.member_uuid = uuid4()
    pytest.participant_uuid = uuid4()
    pytest.user_uuid = uuid4()
    pytest.buy_in = 5.0
    pytest.payout = [0.75, 0.25]
