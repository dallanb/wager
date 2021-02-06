import json
from src import app


###########
# Fetch
###########
def test_fetch_wager(get_user_uuid, get_contest_uuid, create_wager):
    member_uuid = get_user_uuid()
    contest_uuid = get_contest_uuid()

    wager = create_wager(contest_uuid=contest_uuid, buy_in=5.0)
    wager_uuid = wager.uuid

    # Headers
    headers = {'X-Consumer-Custom-ID': member_uuid}

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
def test_fetch_all_wager(get_user_uuid):
    member_uuid = get_user_uuid()

    # Headers
    headers = {'X-Consumer-Custom-ID': member_uuid}

    # Request
    response = app.test_client().get('/wagers',
                                     headers=headers)

    # Response
    assert response.status_code == 200
    response = json.loads(response.data)
    assert response['msg'] == "OK"


def test_fetch_all_wager_include_parties(get_user_uuid):
    member_uuid = get_user_uuid()

    # Headers
    headers = {'X-Consumer-Custom-ID': member_uuid}

    # Request
    response = app.test_client().get('/wagers?include=parties',
                                     headers=headers)

    # Response
    assert response.status_code == 200
    response = json.loads(response.data)
    assert response['msg'] == "OK"
    assert response['data'] is not None
    assert response['data']['wagers'] is not None
    assert response['data']['wagers'][0]['parties'] is not None


def test_fetch_all_wager_include_participants(get_user_uuid):
    member_uuid = get_user_uuid()

    # Headers
    headers = {'X-Consumer-Custom-ID': member_uuid}

    # Request
    response = app.test_client().get('/wagers?include=parties.participants',
                                     headers=headers)

    # Response
    assert response.status_code == 200
    response = json.loads(response.data)
    assert response['msg'] == "OK"
    assert response['data'] is not None
    assert response['data']['wagers'] is not None
    assert response['data']['wagers'][0]['parties'] is not None
    assert response['data']['wagers'][0]['parties'][0]['participants'] is not None
