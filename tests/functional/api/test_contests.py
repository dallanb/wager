import json

from src import app


###########
# Fetch
###########
def test_fetch_contest_complete(get_user_uuid, get_contest_uuid, get_participant_uuid, create_wager,
                                create_party, create_participant):
    member_uuid = get_user_uuid()
    contest_uuid = get_contest_uuid()
    _ = create_wager(contest_uuid=contest_uuid, buy_in=5.0)

    # Headers
    headers = {'X-Consumer-Custom-ID': member_uuid}

    # Request
    response = app.test_client().get(f'/contests/{contest_uuid}/complete',
                                     headers=headers)

    # Response
    assert response.status_code == 200
    response = json.loads(response.data)
    assert response['msg'] == "OKAY"
    assert response['data'] is not None
    assert response['data']['contest'] is not None
