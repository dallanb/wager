import json

import pytest

from src import app


#############
# SUCCESS
#############

###########
# Fetch
###########
def test_fetch_wager(reset_db, seed_wager):
    """
    GIVEN a Flask application configured for testing
    WHEN the GET endpoint 'wager' is requested
    THEN check that the response is valid
    """
    wager_uuid = pytest.wager.uuid
    # Request
    response = app.test_client().get(f'/wagers/{wager_uuid}')

    # Response
    assert response.status_code == 200
    response = json.loads(response.data)
    assert response['msg'] == "OK"
    assert response['data']['wagers']['uuid'] == str(wager_uuid)


###########
# Fetch All
###########
def test_fetch_all_wager():
    """
    GIVEN a Flask application configured for testing
    WHEN the GET endpoint 'wagers' is requested
    THEN check that the response is valid
    """

    # Request
    response = app.test_client().get('/wagers')

    # Response
    assert response.status_code == 200
    response = json.loads(response.data)
    assert response['msg'] == "OK"
    wagers = response['data']['wagers']
    assert len(wagers) == 1
    metadata = response['data']['_metadata']
    assert metadata['total_count'] == 1


def test_fetch_all_wager_w_pagination():
    """
    GIVEN a Flask application configured for testing
    WHEN the GET endpoint 'wagers' is requested with pagination
    THEN check that the response is valid
    """

    # Request
    response = app.test_client().get(f'/wagers?page=1&per_page=1')

    # Response
    assert response.status_code == 200
    response = json.loads(response.data)
    assert response['msg'] == "OK"
    wagers = response['data']['wagers']
    assert len(wagers) == 1
    metadata = response['data']['_metadata']
    assert metadata['total_count'] == 1
    assert metadata['page_count'] == 1
    assert metadata['page'] == 1
    assert metadata['per_page'] == 1
    assert response['data']['wagers'][0]['uuid'] is not None


def test_fetch_all_wager_empty(reset_db):
    """
    GIVEN a Flask application configured for testing
    WHEN the GET endpoint 'wagers' is requested with no wagers
    THEN check that the response is valid
    """

    # Request
    response = app.test_client().get('/wagers')

    # Response
    assert response.status_code == 200
    response = json.loads(response.data)
    assert response['msg'] == "OK"
    wagers = response['data']['wagers']
    assert len(wagers) == 0
    metadata = response['data']['_metadata']
    assert metadata['total_count'] == 0


def test_fetch_all_wager_include_parties(seed_wager, seed_party):
    """
    GIVEN a Flask application configured for testing
    WHEN the GET endpoint 'wager' with include query param 'parties' is requested
    THEN check that the response is valid
    """

    # Request
    response = app.test_client().get('/wagers?include=parties')

    # Response
    assert response.status_code == 200
    response = json.loads(response.data)
    assert response['msg'] == "OK"
    wagers = response['data']['wagers']
    assert 'parties' in wagers[0]
    assert len(wagers[0]['parties']) == 1
    assert wagers[0]['parties'][0]['uuid'] is not None


#############
# FAIL
#############

###########
# Fetch
###########
def test_fetch_wager_bad_wager_uuid(reset_db, seed_wager):
    """
    GIVEN a Flask application configured for testing
    WHEN the GET endpoint 'wager' is requested with incorrect 'uuid'
    THEN check that the response is valid
    """
    member_uuid = pytest.member_uuid

    # Request
    response = app.test_client().get(f'/wagers/{member_uuid}')

    # Response
    assert response.status_code == 404


###########
# Fetch All
###########
def test_fetch_all_wager_w_bad_expand():
    """
    GIVEN a Flask application configured for testing
    WHEN the GET endpoint 'wagers' is requested with invalid query param 'expand'
    THEN check that the response is valid
    """
    # Request
    response = app.test_client().get(f'/wagers?expand=stake')

    # Response
    assert response.status_code == 400


def test_fetch_all_wager_w_bad_include():
    """
    GIVEN a Flask application configured for testing
    WHEN the GET endpoint 'wagers' is requested with invalid query param 'include'
    THEN check that the response is valid
    """
    # Request
    response = app.test_client().get(f'/parties?include=stake')

    # Response
    assert response.status_code == 400


def test_fetch_all_wager_w_bad_pagination():
    """
    GIVEN a Flask application configured for testing
    WHEN the GET endpoint 'wagers' is requested with pagination
    THEN check that the response is valid
    """

    # Request
    response = app.test_client().get(f'/wagers?page=2&per_page=1')

    # Response
    assert response.status_code == 200
    response = json.loads(response.data)
    assert response['msg'] == "OK"
    wagers = response['data']['wagers']
    assert len(wagers) == 0
    metadata = response['data']['_metadata']
    assert metadata['total_count'] == 1
    assert metadata['page_count'] == 0
    assert metadata['page'] == 2
    assert metadata['per_page'] == 1
