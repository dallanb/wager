import json

import pytest

from src import app
###########
# Fetch
###########
from tests.helpers import generate_uuid


#############
# SUCCESS
#############


def test_fetch_contest_complete(reset_db, seed_wager, seed_party, seed_participant):
    """
    GIVEN a Flask application configured for testing
    WHEN the GET endpoint 'contest_complete' is requested
    THEN check that the response is valid
    """
    contest_uuid = pytest.contest_uuid
    # Request
    response = app.test_client().get(f'/contests/{contest_uuid}/complete')

    # Response
    assert response.status_code == 200
    response = json.loads(response.data)
    assert response['msg'] == "OK"
    assert response['data'] is not None
    assert response['data']['contest'] is not None
    contest = response['data']['contest']
    assert contest['uuid'] is not None
    assert contest['parties'] == 1
    assert contest['total_payout'] == pytest.buy_in
    assert contest['buy_in'] == pytest.buy_in
    assert contest['party_payouts'] == {}
    assert contest['payout_proportions'] == {}


#############
# FAIL
#############

###########
# Fetch
###########
def test_fetch_contest_complete_fail(reset_db, seed_wager, seed_party, seed_participant):
    """
    GIVEN a Flask application configured for testing
    WHEN the GET endpoint 'contest_complete' is requested with incorrect 'contest_uuid'
    THEN check that the response is valid
    """
    contest_uuid = generate_uuid()

    # Request
    response = app.test_client().get(f'/contests/{contest_uuid}/complete')

    # Response
    assert response.status_code == 404
