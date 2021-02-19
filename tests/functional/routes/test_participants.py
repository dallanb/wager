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


def test_fetch_participant(reset_db, seed_wager, seed_party, seed_participant):
    """
    GIVEN a Flask application configured for testing
    WHEN the GET endpoint 'participant' is requested
    THEN check that the response is valid
    """
    participant_uuid = pytest.participant.uuid
    # Request
    response = app.test_client().get(f'/participants/{participant_uuid}')

    # Response
    assert response.status_code == 200
    response = json.loads(response.data)
    assert response['msg'] == "OK"
    assert response['data']['participants']['uuid'] == str(participant_uuid)


###########
# Fetch All
###########
def test_fetch_all_participant():
    """
    GIVEN a Flask application configured for testing
    WHEN the GET endpoint 'participants' is requested
    THEN check that the response is valid
    """

    # Request
    response = app.test_client().get('/participants')

    # Response
    assert response.status_code == 200
    response = json.loads(response.data)
    assert response['msg'] == "OK"
    participants = response['data']['participants']
    assert len(participants) == 1
    metadata = response['data']['_metadata']
    assert metadata['total_count'] == 1


def test_fetch_all_participant_w_pagination():
    """
    GIVEN a Flask application configured for testing
    WHEN the GET endpoint 'participants' is requested with pagination
    THEN check that the response is valid
    """

    # Request
    response = app.test_client().get(f'/participants?page=1&per_page=1')

    # Response
    assert response.status_code == 200
    response = json.loads(response.data)
    assert response['msg'] == "OK"
    participants = response['data']['participants']
    assert len(participants) == 1
    metadata = response['data']['_metadata']
    assert metadata['total_count'] == 1
    assert metadata['page_count'] == 1
    assert metadata['page'] == 1
    assert metadata['per_page'] == 1
    assert response['data']['participants'][0]['uuid'] is not None


def test_fetch_all_participant_empty(reset_db):
    """
    GIVEN a Flask application configured for testing
    WHEN the GET endpoint 'participants' is requested with no participants
    THEN check that the response is valid
    """

    # Request
    response = app.test_client().get('/participants')

    # Response
    assert response.status_code == 200
    response = json.loads(response.data)
    assert response['msg'] == "OK"
    participants = response['data']['participants']
    assert len(participants) == 0
    metadata = response['data']['_metadata']
    assert metadata['total_count'] == 0


def test_fetch_all_participant_expand_party(reset_db, seed_wager, seed_party, seed_participant):
    """
    GIVEN a Flask application configured for testing
    WHEN the GET endpoint 'participants' with expand query param 'party' is requested
    THEN check that the response is valid
    """

    # Request
    response = app.test_client().get('/participants?expand=party')

    # Response
    assert response.status_code == 200
    response = json.loads(response.data)
    assert response['msg'] == "OK"
    participants = response['data']['participants']
    assert 'party' in participants[0]
    assert participants[0]['party']['uuid'] is not None


def test_fetch_all_participant_include_stake(seed_stake):
    """
    GIVEN a Flask application configured for testing
    WHEN the GET endpoint 'participants' with include query param 'stake' is requested
    THEN check that the response is valid
    """
    # Request
    response = app.test_client().get('/participants?include=stake')

    # Response
    assert response.status_code == 200
    response = json.loads(response.data)
    assert response['msg'] == "OK"
    participants = response['data']['participants']
    assert 'stake' in participants[0]
    assert participants[0]['stake']['uuid'] is not None


#############
# FAIL
#############

###########
# Fetch
###########
def test_fetch_participant_bad_participant_uuid(reset_db, seed_wager, seed_party, seed_participant):
    """
    GIVEN a Flask application configured for testing
    WHEN the GET endpoint 'participant' is requested with incorrect 'uuid'
    THEN check that the response is valid
    """
    member_uuid = pytest.member_uuid

    # Request
    response = app.test_client().get(f'/participants/{member_uuid}')

    # Response
    assert response.status_code == 404


###########
# Fetch All
###########
def test_fetch_all_participant_w_bad_member_uuid():
    """
    GIVEN a Flask application configured for testing
    WHEN the GET endpoint 'participants' is requested with invalid query param 'member_uuid'
    THEN check that the response is valid
    """
    member_uuid = generate_uuid()

    # Request
    response = app.test_client().get(f'/participants?member_uuid={member_uuid}')

    # Response
    assert response.status_code == 200
    response = json.loads(response.data)
    assert response['msg'] == "OK"
    participants = response['data']['participants']
    assert len(participants) == 0
    metadata = response['data']['_metadata']
    assert metadata['total_count'] == 0


def test_fetch_all_participant_w_bad_expand():
    """
    GIVEN a Flask application configured for testing
    WHEN the GET endpoint 'participants' is requested with invalid query param 'expand'
    THEN check that the response is valid
    """
    # Request
    response = app.test_client().get(f'/participants?expand=contest')

    # Response
    assert response.status_code == 400


def test_fetch_all_participant_w_bad_include():
    """
    GIVEN a Flask application configured for testing
    WHEN the GET endpoint 'participants' is requested with invalid query param 'include'
    THEN check that the response is valid
    """
    # Request
    response = app.test_client().get(f'/participants?include=contest')

    # Response
    assert response.status_code == 400


def test_fetch_all_participant_w_bad_pagination():
    """
    GIVEN a Flask application configured for testing
    WHEN the GET endpoint 'participants' is requested with pagination
    THEN check that the response is valid
    """

    # Request
    response = app.test_client().get(f'/participants?page=2&per_page=1')

    # Response
    assert response.status_code == 200
    response = json.loads(response.data)
    assert response['msg'] == "OK"
    participants = response['data']['participants']
    assert len(participants) == 0
    metadata = response['data']['_metadata']
    assert metadata['total_count'] == 1
    assert metadata['page_count'] == 0
    assert metadata['page'] == 2
    assert metadata['per_page'] == 1
