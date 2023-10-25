# Copyright (c) 2023 Jakub Więckowski

from server import app
import json
import pytest

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

# def test_matrix_converter_crisp(client):
#     """
#         Test verifying the functionality of crisp matrix converter from file to array.
#         Tests both for correct and incorrect files
#     """

#     file_correct = open('./examples/files/crisp_data JSON.json', 'rb')
#     data_correct = {"file": (file_correct, "crisp_data JSON.json")}

#     response = client.post('/api/v1/matrix', headers={'locale': 'en'}, data={'matrix': data_correct, 'extension': "crisp"}, content_type='multipart/form-data', follow_redirects=True)
#     payload = json.loads(response.data.decode('utf-8'))

#     print(payload)
#     assert response.status_code == 200
#     assert type(payload) is dict
#     assert 'matrix' in payload.keys()
    
# def test_matrix_converter_fuzzy(client):
#     """
#         Test verifying the functionality of fuzzy matrix converter from file to array.
#         Tests both for correct and incorrect files
#     """

#     file_correct = open('./examples/files/crisp_data JSON.json', 'rb')
#     data_correct = {"files": (file_correct, "crisp_data JSON.json")}

#     response = client.post('/api/v1/matrix', headers={'locale': 'en'}, data={'matrix': data_correct, 'extension': 'crisp'}, content_type='multipart/form-data')
#     payload = json.loads(response.data.decode('utf-8'))

#     assert response.status_code == 200
#     assert type(payload) is dict
#     assert 'matrix' in payload.keys()

def test_matrix_converter_missing_field(client):
    """
        Test verifying the functionality of matrix converter from file to array when missing required field
    """

    response = client.post('/api/v1/matrix', headers={'locale': 'en'}, data={'extension': 'crisp'}, content_type='multipart/form-data')
    payload = json.loads(response.data.decode('utf-8'))

    assert response.status_code == 400
    assert type(payload) is dict
    assert 'errors' in payload.keys()
    assert 'matrix' in payload['errors'].keys()

def test_matrix_converter_no_locale(client):
    """
        Test verifying the functionality of matrix converter from file to array with no locale given in headers
    """

    file_correct = open('./examples/files/crisp_data JSON.json', 'rb')
    data_correct = {"files": (file_correct, "crisp_data JSON.json")}

    response = client.post('/api/v1/matrix', data={'extension': 'crisp', 'matrix': data_correct}, content_type='multipart/form-data')
    payload = json.loads(response.data.decode('utf-8'))

    assert response.status_code == 400
    assert type(payload) is dict
    assert 'errors' in payload.keys()
    assert 'locale' in payload['errors'].keys()
