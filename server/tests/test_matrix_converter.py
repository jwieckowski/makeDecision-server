# Copyright (c) 2023 - 2024 Jakub Więckowski

from server import app
import json
import pytest

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_matrix_generate_crisp(client):
    """
        Test verifying the functionality of crisp matrix generation
    """

    response = client.post('/api/v1/matrix/generate', headers={'locale': 'en'}, json={'extension': 'crisp', 'alternatives': 3, 'criteria': 3})
    payload = json.loads(response.data.decode('utf-8'))

    assert response.status_code == 200
    assert 'response' in list(payload.keys())
    assert type(payload['response']) is dict
    assert 'matrix' in list(payload['response'].keys())
    assert 'criteria_types' in list(payload['response'].keys())
    assert 'extension' in list(payload['response'].keys())
    assert payload['response']['extension'] == 'crisp'
    
def test_matrix_generate_fuzzy(client):
    """
        Test verifying the functionality of fuzzy matrix generation
    """

    response = client.post('/api/v1/matrix/generate', headers={'locale': 'en'}, json={"extension": "fuzzy", "alternatives": 4, "criteria": 4, "lower_bound": 0.2, "upper_bound": 1, "precision": 3})
    payload = json.loads(response.data.decode('utf-8'))

    assert response.status_code == 200
    assert 'response' in list(payload.keys())
    assert type(payload['response']) is dict
    assert 'matrix' in list(payload['response'].keys())
    assert 'criteria_types' in list(payload['response'].keys())
    assert 'extension' in list(payload['response'].keys())
    assert payload['response']['extension'] == 'fuzzy'

def test_matrix_generate_invalid_extension(client):
    """
        Test verifying the functionality of matrix generation with invalid extension
    """

    response = client.post('/api/v1/matrix/generate', headers={'locale': 'en'}, json={"extension": "ifs", "alternatives": 4, "criteria": 4, "lower_bound": 0.2, "upper_bound": 1, "precision": 3})
    payload = json.loads(response.data.decode('utf-8'))

    assert response.status_code == 400
    assert 'message' in list(payload.keys())
    
def test_matrix_upload_crisp(client):
    """
        Test verifying the functionality of crisp matrix upload from file to array.
        Tests both for correct and incorrect files
    """

    file_correct = open('./examples/matrix_files/crisp_data JSON.json', 'rb')
    data = {
            'matrix': (file_correct, 'crisp_data JSON.json'),
            'extension': 'crisp'
        }

    response = client.post('/api/v1/matrix/upload', 
                        headers={'locale': 'en'}, 
                        data=data,
                        content_type='multipart/form-data',
                        follow_redirects=True)
    payload = json.loads(response.data.decode('utf-8'))

    assert response.status_code == 200
    assert 'response' in list(payload.keys())
    assert type(payload) is dict
    assert 'matrix' in list(payload['response'].keys())
    assert 'criteria_types' in list(payload['response'].keys())
    assert 'extension' in list(payload['response'].keys())
    
def test_matrix_upload_fuzzy(client):
    """
        Test verifying the functionality of fuzzy matrix upload from file to array.
        Tests both for correct and incorrect files
    """

    file_correct = open('./examples/matrix_files/fuzzy_data JSON.json', 'rb')
    data = {
            'matrix': (file_correct, 'fuzzy_data JSON.json'),
            'extension': 'fuzzy'
        }

    response = client.post('/api/v1/matrix/upload', 
                        headers={'locale': 'en'}, 
                        data=data,
                        content_type='multipart/form-data',
                        follow_redirects=True)
    payload = json.loads(response.data.decode('utf-8'))

    assert response.status_code == 200
    assert 'response' in list(payload.keys())
    assert type(payload) is dict
    assert 'matrix' in list(payload['response'].keys())
    assert 'criteria_types' in list(payload['response'].keys())
    assert 'extension' in list(payload['response'].keys())
    
def test_matrix_upload_invalid_extension(client):
    """
        Test verifying the functionality of invalid matrix upload from file to array.
        Tests both for correct and incorrect files
    """

    file_correct = open('./examples/matrix_files/fuzzy_data JSON.json', 'rb')
    data = {
            'matrix': (file_correct, 'fuzzy_data JSON.json'),
            'extension': 'invalid'
        }

    response = client.post('/api/v1/matrix/upload', 
                        headers={'locale': 'en'}, 
                        data=data,
                        content_type='multipart/form-data',
                        follow_redirects=True)
    payload = json.loads(response.data.decode('utf-8'))

    assert response.status_code == 400
    assert 'message' in list(payload.keys())
    