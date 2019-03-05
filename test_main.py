import pytest

import main


@pytest.fixture
def client():
    main.app.config['TESTING'] = True
    client = main.app.test_client()

    yield client


def test_index(client):
    rv = client.get('/')
    assert b'Cats Service welcomes you.' in rv.data


def test_limit(client):
    """Тестирование лимита обращений"""

    for i in range(601):
        rv = client.get('/cats')

    assert b'429 Too Many Requests' in rv.data
