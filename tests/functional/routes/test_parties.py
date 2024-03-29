import json

import pytest

from src import app


#############
# SUCCESS
#############

###########
# Fetch
###########
def test_fetch_party(reset_db, seed_wager, seed_party):
    """
    GIVEN a Flask application configured for testing
    WHEN the GET endpoint 'party' is requested
    THEN check that the response is valid
    """
    party_uuid = pytest.party.uuid
    # Request
    response = app.test_client().get(f'/parties/{party_uuid}')

    # Response
    assert response.status_code == 200
    response = json.loads(response.data)
    assert response['msg'] == "OK"
    assert response['data']['parties']['uuid'] == str(party_uuid)


###########
# Fetch All
###########
def test_fetch_all_party():
    """
    GIVEN a Flask application configured for testing
    WHEN the GET endpoint 'parties' is requested
    THEN check that the response is valid
    """

    # Request
    response = app.test_client().get('/parties')

    # Response
    assert response.status_code == 200
    response = json.loads(response.data)
    assert response['msg'] == "OK"
    parties = response['data']['parties']
    assert len(parties) == 1
    metadata = response['data']['_metadata']
    assert metadata['total_count'] == 1


def test_fetch_all_party_w_pagination():
    """
    GIVEN a Flask application configured for testing
    WHEN the GET endpoint 'parties' is requested with pagination
    THEN check that the response is valid
    """

    # Request
    response = app.test_client().get(f'/parties?page=1&per_page=1')

    # Response
    assert response.status_code == 200
    response = json.loads(response.data)
    assert response['msg'] == "OK"
    parties = response['data']['parties']
    assert len(parties) == 1
    metadata = response['data']['_metadata']
    assert metadata['total_count'] == 1
    assert metadata['page_count'] == 1
    assert metadata['page'] == 1
    assert metadata['per_page'] == 1
    assert response['data']['parties'][0]['uuid'] is not None


def test_fetch_all_party_empty(reset_db):
    """
    GIVEN a Flask application configured for testing
    WHEN the GET endpoint 'parties' is requested with no parties
    THEN check that the response is valid
    """

    # Request
    response = app.test_client().get('/parties')

    # Response
    assert response.status_code == 200
    response = json.loads(response.data)
    assert response['msg'] == "OK"
    parties = response['data']['parties']
    assert len(parties) == 0
    metadata = response['data']['_metadata']
    assert metadata['total_count'] == 0


def test_fetch_all_party_expand_wager(reset_db, seed_wager, seed_party):
    """
    GIVEN a Flask application configured for testing
    WHEN the GET endpoint 'parties' with expand query param 'wager' is requested
    THEN check that the response is valid
    """

    # Request
    response = app.test_client().get('/parties?expand=wager')

    # Response
    assert response.status_code == 200
    response = json.loads(response.data)
    assert response['msg'] == "OK"
    parties = response['data']['parties']
    assert 'wager' in parties[0]
    assert parties[0]['wager']['uuid'] is not None


def test_fetch_all_party_include_participants(seed_participant):
    """
    GIVEN a Flask application configured for testing
    WHEN the GET endpoint 'parties' with include query param 'participants' is requested
    THEN check that the response is valid
    """

    # Request
    response = app.test_client().get('/parties?include=participants')

    # Response
    assert response.status_code == 200
    response = json.loads(response.data)
    assert response['msg'] == "OK"
    parties = response['data']['parties']
    assert 'participants' in parties[0]
    assert len(parties[0]['participants']) == 1
    assert parties[0]['participants'][0]['uuid'] is not None


#############
# FAIL
#############

###########
# Fetch
###########
def test_fetch_party_bad_party_uuid(reset_db, seed_wager, seed_party):
    """
    GIVEN a Flask application configured for testing
    WHEN the GET endpoint 'party' is requested with incorrect 'uuid'
    THEN check that the response is valid
    """
    member_uuid = pytest.member_uuid

    # Request
    response = app.test_client().get(f'/parties/{member_uuid}')

    # Response
    assert response.status_code == 404


###########
# Fetch All
###########
def test_fetch_all_party_w_bad_expand():
    """
    GIVEN a Flask application configured for testing
    WHEN the GET endpoint 'parties' is requested with invalid query param 'expand'
    THEN check that the response is valid
    """
    # Request
    response = app.test_client().get(f'/parties?expand=contest')

    # Response
    assert response.status_code == 400


def test_fetch_all_party_w_bad_include():
    """
    GIVEN a Flask application configured for testing
    WHEN the GET endpoint 'parties' is requested with invalid query param 'include'
    THEN check that the response is valid
    """
    # Request
    response = app.test_client().get(f'/parties?include=contest')

    # Response
    assert response.status_code == 400


def test_fetch_all_party_w_bad_pagination():
    """
    GIVEN a Flask application configured for testing
    WHEN the GET endpoint 'parties' is requested with pagination
    THEN check that the response is valid
    """

    # Request
    response = app.test_client().get(f'/parties?page=2&per_page=1')

    # Response
    assert response.status_code == 200
    response = json.loads(response.data)
    assert response['msg'] == "OK"
    parties = response['data']['parties']
    assert len(parties) == 0
    metadata = response['data']['_metadata']
    assert metadata['total_count'] == 1
    assert metadata['page_count'] == 0
    assert metadata['page'] == 2
    assert metadata['per_page'] == 1
