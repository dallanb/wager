import json

from src import app


###########
# Fetch
###########
def test_fetch_party(reset_db, get_user_uuid, get_contest_uuid, create_wager, create_party):
    """
    GIVEN a Flask application configured for testing
    WHEN the GET endpoint 'party' is requested
    THEN check that the response is valid
    """
    user_uuid = get_user_uuid()
    contest_uuid = get_contest_uuid()

    wager = create_wager(contest_uuid=contest_uuid, buy_in=5.0)
    wager_uuid = wager.uuid

    party = create_party(wager_uuid=wager_uuid)
    party_uuid = party.uuid

    # Headers
    headers = {'X-Consumer-Custom-ID': user_uuid}

    # Request
    response = app.test_client().get(f'/parties/{party_uuid}',
                                     headers=headers)

    # Response
    assert response.status_code == 200
    response = json.loads(response.data)
    assert response['msg'] == "OK"
    assert response['data']['parties']['uuid'] == str(party_uuid)


###########
# Fetch All
###########
def test_fetch_all_party(reset_db, get_user_uuid, seed_party):
    """
    GIVEN a Flask application configured for testing
    WHEN the GET endpoint 'parties' is requested
    THEN check that the response is valid
    """
    user_uuid = get_user_uuid()

    # Headers
    headers = {'X-Consumer-Custom-ID': user_uuid}

    # Request
    response = app.test_client().get('/parties',
                                     headers=headers)

    # Response
    assert response.status_code == 200
    response = json.loads(response.data)
    assert response['msg'] == "OK"
    parties = response['data']['parties']
    assert len(parties) == 1
    metadata = response['data']['_metadata']
    assert metadata['total_count'] == 1


def test_fetch_all_party_expand_wager(reset_db, get_user_uuid, seed_party):
    """
    GIVEN a Flask application configured for testing
    WHEN the GET endpoint 'parties' with expand query param 'wager' is requested
    THEN check that the response is valid
    """
    user_uuid = get_user_uuid()

    # Headers
    headers = {'X-Consumer-Custom-ID': user_uuid}

    # Request
    response = app.test_client().get('/parties?expand=wager',
                                     headers=headers)

    # Response
    assert response.status_code == 200
    response = json.loads(response.data)
    assert response['msg'] == "OK"
    parties = response['data']['parties']
    assert 'wager' in parties[0]
    assert parties[0]['wager']['uuid'] is not None


def test_fetch_all_party_include_participants(reset_db, get_user_uuid, seed_participant):
    """
    GIVEN a Flask application configured for testing
    WHEN the GET endpoint 'parties' with include query param 'participants' is requested
    THEN check that the response is valid
    """
    user_uuid = get_user_uuid()

    # Headers
    headers = {'X-Consumer-Custom-ID': user_uuid}

    # Request
    response = app.test_client().get('/parties?include=participants',
                                     headers=headers)

    # Response
    assert response.status_code == 200
    response = json.loads(response.data)
    assert response['msg'] == "OK"
    parties = response['data']['parties']
    assert 'participants' in parties[0]
    assert len(parties[0]['participants']) == 1
    assert parties[0]['participants'][0]['uuid'] is not None
