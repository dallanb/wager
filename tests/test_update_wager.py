from src import app


def test_update_wager():
    response = app.test_client().put('/', data={'data': '{}'},
                                     headers={'X-Consumer-Custom-ID': '16ba5507-71b2-4fc9-8bbd-1909259c1ea1'})

    assert response.status_code == 200
    assert b'OK' in response.data
