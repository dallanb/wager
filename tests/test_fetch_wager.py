from src import app


def test_fetch_wager():
    response = app.test_client().get('/')

    assert response.status_code == 200
    assert b'OK' in response.data
