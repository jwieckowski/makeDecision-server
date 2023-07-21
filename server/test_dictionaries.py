# Copyright (c) 2023 Jakub Więckowski

from .server import app
import json
import pytest

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_all_methods_dictionary(client):
    """
        Test verifying the content of the obtained dictionaries for all methods with given locale in headers
    """

    response = client.get('/api/v1/dictionary/all-methods', headers={'locale': 'en'})
    payload = json.loads(response.data.decode('utf-8'))

    assert response.status_code == 200
    assert type(payload) is list
    assert type(payload[0]) is dict
    assert type(payload[0]['data']) is list
    
    assert payload[0]['key'] == 'Decision matrix'

def test_all_methods_dictionary_no_locale(client):
    """
        Test verifying the content of the obtained dictionaries for all methods with no locale given in headers
    """

    response = client.get('/api/v1/dictionary/all-methods')
    payload = json.loads(response.data.decode('utf-8'))

    assert response.status_code == 400
    assert 'locale' in payload['errors'].keys()

def test_all_methods_dictionary_unhandled_locale(client):
    """
        Test verifying the content of the obtained dictionaries for all methods with locale not handled in server given in headers.
        The default locale should be set to en
    """

    response = client.get('/api/v1/dictionary/all-methods', headers={'locale': 'ua'})
    payload = json.loads(response.data.decode('utf-8'))

    assert response.status_code == 200
    assert type(payload) is list
    assert type(payload[0]) is dict
    assert type(payload[0]['data']) is list
    
    assert payload[0]['key'] == 'Decision matrix'


