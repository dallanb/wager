import json

from src import app


###########
# Fetch
###########
def test_fetch_contest_complete(reset_db, get_user_uuid, get_contest_uuid, get_participant_uuid, create_wager,
                                create_party, create_participant):
    """
    GIVEN a Flask application configured for testing
    WHEN the GET endpoint 'contest_complete' is requested
    THEN check that the response is valid
    """
    user_uuid = get_user_uuid()
    contest_uuid = get_contest_uuid()
    _ = create_wager(contest_uuid=contest_uuid, buy_in=5.0)

    # Headers
    headers = {'X-Consumer-Custom-ID': user_uuid}

    # Request
    response = app.test_client().get(f'/contests/{contest_uuid}/complete',
                                     headers=headers)

    # Response
    assert response.status_code == 200
    response = json.loads(response.data)
    assert response['msg'] == "OK"
    assert response['data'] is not None
    assert response['data']['contest'] is not None
    contest = response['data']['contest']
    assert contest['uuid'] is not None
    assert contest['parties'] == 0
    assert contest['total_payout'] == 0.0
    assert contest['buy_in'] == 5.0
    assert contest['party_payouts'] == {}
    assert contest['payout_proportions'] == {}
