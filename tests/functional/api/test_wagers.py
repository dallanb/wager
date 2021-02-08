import json

from src import app


###########
# Fetch
###########
def test_fetch_wager(reset_db, get_user_uuid, get_contest_uuid, create_wager):
    """
    GIVEN a Flask application configured for testing
    WHEN the GET endpoint 'wager' is requested
    THEN check that the response is valid
    """
    user_uuid = get_user_uuid()
    contest_uuid = get_contest_uuid()

    wager = create_wager(contest_uuid=contest_uuid, buy_in=5.0)
    wager_uuid = wager.uuid

    # Headers
    headers = {'X-Consumer-Custom-ID': user_uuid}

    # Request
    response = app.test_client().get(f'/wagers/{wager_uuid}',
                                     headers=headers)

    # Response
    assert response.status_code == 200
    response = json.loads(response.data)
    assert response['msg'] == "OK"
    assert response['data']['wagers']['uuid'] == str(wager_uuid)


###########
# Fetch All
###########
def test_fetch_all_wager(reset_db, get_user_uuid, seed_wager):
    """
    GIVEN a Flask application configured for testing
    WHEN the GET endpoint 'wagers' is requested
    THEN check that the response is valid
    """
    user_uuid = get_user_uuid()

    # Headers
    headers = {'X-Consumer-Custom-ID': user_uuid}

    # Request
    response = app.test_client().get('/wagers',
                                     headers=headers)

    # Response
    assert response.status_code == 200
    response = json.loads(response.data)
    assert response['msg'] == "OK"
    wagers = response['data']['wagers']
    assert len(wagers) == 1
    metadata = response['data']['_metadata']
    assert metadata['total_count'] == 1


def test_fetch_all_wager_include_parties(reset_db, get_user_uuid, seed_party):
    """
    GIVEN a Flask application configured for testing
    WHEN the GET endpoint 'wager' with include query param 'parties' is requested
    THEN check that the response is valid
    """
    user_uuid = get_user_uuid()

    # Headers
    headers = {'X-Consumer-Custom-ID': user_uuid}

    # Request
    response = app.test_client().get('/wagers?include=parties',
                                     headers=headers)

    # Response
    assert response.status_code == 200
    response = json.loads(response.data)
    assert response['msg'] == "OK"
    wagers = response['data']['wagers']
    assert 'parties' in wagers[0]
    assert len(wagers[0]['parties']) == 1
    assert wagers[0]['parties'][0]['uuid'] is not None
