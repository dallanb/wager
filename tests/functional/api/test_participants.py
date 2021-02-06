import json

import pytest

from src import app
from tests.functional.helpers import generate_name, generate_uuid


###########
# Create
###########
def test_create_participant(get_user_uuid, get_contest_uuid, get_participant_uuid, create_wager,
                            create_party):
    member_uuid = get_user_uuid()
    contest_uuid = get_contest_uuid()
    wager = create_wager(contest_uuid=contest_uuid, buy_in=5.0)
    wager_uuid = wager.uuid
    party = create_party(wager_uuid=wager_uuid)
    party_uuid = party.uuid

    participant_member_uuid = generate_uuid()

    # Headers
    headers = {'X-Consumer-Custom-ID': member_uuid}

    # Payload
    payload = {'member_uuid': participant_member_uuid}

    # Request
    response = app.test_client().post(f'parties/{party_uuid}/participants', json=payload,
                                      headers=headers)

    # Response
    assert response.status_code == 200
    response = json.loads(response.data)
    assert response['msg'] == "OK"
    assert response['data']['participants']['status'] == 'pending'
    assert response['data']['participants']['uuid'] is not None


###########
# Fetch
###########
def test_fetch_participant(get_user_uuid, get_contest_uuid, get_participant_uuid, create_wager,
                           create_party, create_participant):
    member_uuid = get_user_uuid()
    contest_uuid = get_contest_uuid()
    wager = create_wager(contest_uuid=contest_uuid, buy_in=5.0)
    wager_uuid = wager.uuid
    party = create_party(wager_uuid=wager_uuid)
    party_uuid = party.uuid
    participant = create_participant(party_uuid=party_uuid, member_uuid=member_uuid)
    participant_uuid = participant.uuid

    # Headers
    headers = {'X-Consumer-Custom-ID': member_uuid}

    # Request
    response = app.test_client().get(f'/participants/{participant_uuid}',
                                     headers=headers)

    # Response
    assert response.status_code == 200
    response = json.loads(response.data)
    assert response['msg'] == "OK"
    assert response['data']['participants']['uuid'] == str(participant_uuid)


###########
# Fetch All
###########
def test_fetch_all_participant(get_user_uuid):
    member_uuid = get_user_uuid()

    # Headers
    headers = {'X-Consumer-Custom-ID': member_uuid}

    # Request
    response = app.test_client().get('/participants',
                                     headers=headers)

    # Response
    assert response.status_code == 200
    response = json.loads(response.data)
    assert response['msg'] == "OK"


def test_fetch_all_participant_expand_party(get_user_uuid):
    member_uuid = get_user_uuid()

    # Headers
    headers = {'X-Consumer-Custom-ID': member_uuid}

    # Request
    response = app.test_client().get('/participants?expand=party',
                                     headers=headers)

    # Response
    assert response.status_code == 200
    response = json.loads(response.data)
    assert response['msg'] == "OK"
    assert response['data'] is not None
    assert response['data']['participants'] is not None
    assert response['data']['participants'][0]['party'] is not None


def test_fetch_all_participant_expand_wager(get_user_uuid):
    member_uuid = get_user_uuid()

    # Headers
    headers = {'X-Consumer-Custom-ID': member_uuid}

    # Request
    response = app.test_client().get('/participants?expand=party.wager',
                                     headers=headers)

    # Response
    assert response.status_code == 200
    response = json.loads(response.data)
    assert response['msg'] == "OK"
    assert response['data'] is not None
    assert response['data']['participants'] is not None
    assert response['data']['participants'][0]['party'] is not None
    assert response['data']['participants'][0]['party']['wager'] is not None


def test_fetch_all_participant_include_stakes(get_user_uuid):
    member_uuid = get_user_uuid()

    # Headers
    headers = {'X-Consumer-Custom-ID': member_uuid}

    # Request
    response = app.test_client().get('/participants?include=stakes',
                                     headers=headers)

    # Response
    assert response.status_code == 200
    response = json.loads(response.data)
    assert response['msg'] == "OK"
    assert response['data'] is not None
    assert response['data']['participants'] is not None
    assert response['data']['participants'][0]['stakes'] is not None
