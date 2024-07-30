# Copyright (c) 2023 - 2024 Jakub Więckowski

from server import app
import json
import pytest

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_all_methods_descriptions(client):
    """
        Test verifying the content of the obtained descriptions with locale given in headers
    """

    response = client.get('/api/v1/descriptions/methods', headers={'locale': 'en'})
    payload = json.loads(response.data.decode('utf-8'))

    assert response.status_code == 200
    assert 'response' in list(payload.keys())
    assert type(payload['response']) is list
    assert type(payload['response'][0]) is dict
    assert type(payload['response'][0]['data']) is list
    
    assert payload['response'][0]['key'] == 'Weights'

def test_all_methods_descriptions_no_locale(client):
    """
        Test verifying the content of the obtained descriptions with no locale given in headers
    """

    response = client.get('/api/v1/descriptions/methods')
    payload = json.loads(response.data.decode('utf-8'))

    assert response.status_code == 400
    assert 'locale' in payload['errors'].keys()

def test_all_methods_descriptions_unhandled_locale(client):
    """
        Test verifying the content of the obtained descriptions with locale not handled in server given in headers.
        The default locale should be set to en
    """

    response = client.get('/api/v1/descriptions/methods', headers={'locale': 'ua'})
    payload = json.loads(response.data.decode('utf-8'))

    assert response.status_code == 200
    assert 'response' in list(payload.keys())
    assert type(payload['response']) is list
    assert type(payload['response'][0]) is dict
    assert type(payload['response'][0]['data']) is list
    
    assert payload['response'][0]['key'] == 'Weights'

