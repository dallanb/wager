import json

from src import app


###########
# Fetch
###########
def test_fetch_party(get_user_uuid, get_contest_uuid, create_wager, create_party):
    member_uuid = get_user_uuid()
    contest_uuid = get_contest_uuid()

    wager = create_wager(contest_uuid=contest_uuid, buy_in=5.0)
    wager_uuid = wager.uuid

    party = create_party(wager_uuid=wager_uuid)
    party_uuid = party.uuid

    # Headers
    headers = {'X-Consumer-Custom-ID': member_uuid}

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
def test_fetch_all_party(get_user_uuid):
    member_uuid = get_user_uuid()

    # Headers
    headers = {'X-Consumer-Custom-ID': member_uuid}

    # Request
    response = app.test_client().get('/parties',
                                     headers=headers)

    # Response
    assert response.status_code == 200
    response = json.loads(response.data)
    assert response['msg'] == "OK"


def test_fetch_all_party_expand_wager(get_user_uuid):
    member_uuid = get_user_uuid()

    # Headers
    headers = {'X-Consumer-Custom-ID': member_uuid}

    # Request
    response = app.test_client().get('/parties?expand=wager',
                                     headers=headers)

    # Response
    assert response.status_code == 200
    response = json.loads(response.data)
    assert response['msg'] == "OK"
    assert response['data'] is not None
    assert response['data']['parties'] is not None
    assert response['data']['parties'][0]['wager'] is not None


def test_fetch_all_party_include_participants(get_user_uuid):
    member_uuid = get_user_uuid()

    # Headers
    headers = {'X-Consumer-Custom-ID': member_uuid}

    # Request
    response = app.test_client().get('/parties?include=participants',
                                     headers=headers)

    # Response
    assert response.status_code == 200
    response = json.loads(response.data)
    assert response['msg'] == "OK"
    assert response['data'] is not None
    assert response['data']['parties'] is not None
    assert response['data']['parties'][0]['participants'] is not None
