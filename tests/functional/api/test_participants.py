import json

from src import app


###########
# Fetch
###########
def test_fetch_participant(reset_db, get_user_uuid, get_member_uuid, get_contest_uuid, get_participant_uuid,
                           create_wager,
                           create_party, create_participant):
    """
    GIVEN a Flask application configured for testing
    WHEN the GET endpoint 'participant' is requested
    THEN check that the response is valid
    """
    user_uuid = get_user_uuid()
    member_uuid = get_member_uuid()
    contest_uuid = get_contest_uuid()
    wager = create_wager(contest_uuid=contest_uuid, buy_in=5.0)
    wager_uuid = wager.uuid
    party = create_party(wager_uuid=wager_uuid)
    party_uuid = party.uuid
    participant = create_participant(party_uuid=party_uuid, member_uuid=member_uuid)
    participant_uuid = participant.uuid

    # Headers
    headers = {'X-Consumer-Custom-ID': user_uuid}

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
def test_fetch_all_participant(reset_db, get_user_uuid, seed_participant):
    """
    GIVEN a Flask application configured for testing
    WHEN the GET endpoint 'participants' is requested
    THEN check that the response is valid
    """
    user_uuid = get_user_uuid()

    # Headers
    headers = {'X-Consumer-Custom-ID': user_uuid}

    # Request
    response = app.test_client().get('/participants',
                                     headers=headers)

    # Response
    assert response.status_code == 200
    response = json.loads(response.data)
    assert response['msg'] == "OK"
    participants = response['data']['participants']
    assert len(participants) == 1
    metadata = response['data']['_metadata']
    assert metadata['total_count'] == 1


def test_fetch_all_participant_expand_party(reset_db, get_user_uuid, seed_participant):
    """
    GIVEN a Flask application configured for testing
    WHEN the GET endpoint 'participants' with expand query param 'party' is requested
    THEN check that the response is valid
    """
    user_uuid = get_user_uuid()

    # Headers
    headers = {'X-Consumer-Custom-ID': user_uuid}

    # Request
    response = app.test_client().get('/participants?expand=party',
                                     headers=headers)

    # Response
    assert response.status_code == 200
    response = json.loads(response.data)
    assert response['msg'] == "OK"
    participants = response['data']['participants']
    assert 'party' in participants[0]
    assert participants[0]['party']['uuid'] is not None


def test_fetch_all_participant_include_stakes(reset_db, get_user_uuid, seed_stake):
    """
    GIVEN a Flask application configured for testing
    WHEN the GET endpoint 'participants' with include query param 'stakes' is requested
    THEN check that the response is valid
    """
    user_uuid = get_user_uuid()

    # Headers
    headers = {'X-Consumer-Custom-ID': user_uuid}

    # Request
    response = app.test_client().get('/participants?include=stakes',
                                     headers=headers)

    # Response
    assert response.status_code == 200
    response = json.loads(response.data)
    assert response['msg'] == "OK"
    participants = response['data']['participants']
    assert 'stakes' in participants[0]
    assert len(participants[0]['stakes']) == 1
    assert participants[0]['stakes'][0]['uuid'] is not None
