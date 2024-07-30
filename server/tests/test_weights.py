# Copyright (c) 2023 - 2024 Jakub Więckowski

from server import app
import json
import pytest

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_results_calculation_weights_method_crisp(client):
    """
        Test verifying the functionality of multi-criteria calculations for basic model structure with weights method with crisp data
    """
    data = [
        {
            "id": 1,
            "node_type": "matrix",
            "extension": "crisp",
            "matrix": [
                [6, 2, 3],
                [3, 7, 2],
                [2, 3, 8],
            ],
            "criteria_types": [1, -1, 1],
            "method": "input",
            "connections_from": [],
            "connections_to": [2],
            "position_x": 10,
            "position_y": 10,
        },
        {
            "id": 2,
            "node_type": "weights",
            "extension": "crisp",
            "weights": [],
            "method": "IDOCRIW",
            "connections_from": [1],
            "connections_to": [],
            "position_x": 20,
            "position_y": 20,
        }
    ]


    response = client.post('/api/v1/calculations/calculate', headers={'locale': 'en'}, json={'data': data}, content_type='application/json')
    payload = json.loads(response.data.decode('utf-8'))

    assert response.status_code == 200
    assert 'response' in list(payload.keys())
    assert type(payload['response']) is list
    assert len(payload['response']) == 2
    assert type(payload['response'][0]) is dict
    assert payload['response'][0]['node_type'] == 'matrix'
    assert payload['response'][1]['node_type'] == 'weights'
    assert type(payload['response'][1]['data'][0]) is dict
    assert len(payload['response'][1]['data'][0]['weights']) == 3

def test_results_calculation_multiple_weights_method_crisp(client):
    """
        Test verifying the functionality of multi-criteria calculations for basic model structure with weights method with crisp data
    """
    data = [
        {
            "id": 1,
            "node_type": "matrix",
            "extension": "crisp",
            "matrix": [
                [6, 2, 3],
                [3, 7, 2],
                [2, 3, 8],
            ],
            "criteria_types": [1, -1, 1],
            "method": "input",
            "connections_from": [],
            "connections_to": [2, 3],
            "position_x": 10,
            "position_y": 10,
        },
        {
            "id": 2,
            "node_type": "weights",
            "extension": "crisp",
            "weights": [],
            "method": "IDOCRIW",
            "connections_from": [1],
            "connections_to": [],
            "position_x": 20,
            "position_y": 20,
        },
        {
            "id": 3,
            "node_type": "weights",
            "extension": "crisp",
            "weights": [],
            "method": "MEREC",
            "connections_from": [1],
            "connections_to": [],
            "position_x": 30,
            "position_y": 30,
        }
    ]


    response = client.post('/api/v1/calculations/calculate', headers={'locale': 'en'}, json={'data': data}, content_type='application/json')
    payload = json.loads(response.data.decode('utf-8'))

    assert response.status_code == 200
    assert 'response' in list(payload.keys())
    assert type(payload['response']) is list
    assert type(payload['response'][0]) is dict
    assert len(payload['response']) == 3
    assert payload['response'][0]['node_type'] == 'matrix'
    assert payload['response'][1]['node_type'] == 'weights'
    assert type(payload['response'][1]['data'][0]) is dict
    assert len(payload['response'][1]['data'][0]['weights']) == 3
    assert payload['response'][1]['method'] == 'IDOCRIW'
    assert len(payload['response'][2]['data'][0]['weights']) == 3
    assert payload['response'][2]['method'] == 'MEREC'
    

def test_results_calculation_weights_method_fuzzy(client):
    """
        Test verifying the functionality of multi-criteria calculations for basic model structure with weights method with fuzzy data
    """
    data = [
        {
            "id": 1,
            "node_type": "matrix",
            "extension": "fuzzy",
            "matrix": [
                [[1, 2, 3], [4, 5, 6], [7, 8, 9]],
                [[5, 7, 8], [7, 8, 9], [3, 4, 5]],
                [[2, 3, 4], [5, 7, 9], [6, 8, 9]],
            ],
            "criteria_types": [1, -1, 1],
            "method": "input",
            "connections_from": [],
            "connections_to": [2],
            "position_x": 10,
            "position_y": 10,
        },
        {
            "id": 2,
            "node_type": "weights",
            "extension": "fuzzy",
            "weights": [],
            "method": "EQUAL",
            "connections_from": [1],
            "connections_to": [],
            "position_x": 20,
            "position_y": 20,
        }
    ]

    response = client.post('/api/v1/calculations/calculate', headers={'locale': 'en'}, json={'data': data}, content_type='application/json')
    payload = json.loads(response.data.decode('utf-8'))

    assert response.status_code == 200
    assert 'response' in list(payload.keys())
    assert type(payload['response']) is list
    assert len(payload['response']) == 2
    assert type(payload['response'][0]) is dict
    assert payload['response'][0]['node_type'] == 'matrix'
    assert payload['response'][1]['node_type'] == 'weights'
    assert type(payload['response'][1]['data'][0]) is dict
    assert len(payload['response'][1]['data'][0]['weights']) == 3

def test_results_calculation_multiple_weights_method_fuzzy(client):
    """
        Test verifying the functionality of multi-criteria calculations for basic model structure with weights method with fuzzy data
    """
    data = [
        {
            "id": 1,
            "node_type": "matrix",
            "extension": "fuzzy",
            "matrix": [
                [[1, 2, 3], [4, 5, 6], [7, 8, 9]],
                [[5, 7, 8], [7, 8, 9], [3, 4, 5]],
                [[2, 3, 4], [5, 7, 9], [6, 8, 9]],
            ],
            "criteria_types": [1, -1, 1],
            "method": "input",
            "connections_from": [],
            "connections_to": [2, 3],
            "position_x": 10,
            "position_y": 10,
        },
        {
            "id": 2,
            "node_type": "weights",
            "extension": "fuzzy",
            "weights": [],
            "method": "EQUAL",
            "connections_from": [1],
            "connections_to": [],
            "position_x": 20,
            "position_y": 20,
        },
        {
            "id": 3,
            "node_type": "weights",
            "extension": "fuzzy",
            "weights": [],
            "method": "ENTROPY",
            "connections_from": [1],
            "connections_to": [],
            "position_x": 30,
            "position_y": 30,
        }
    ]


    response = client.post('/api/v1/calculations/calculate', headers={'locale': 'en'}, json={'data': data}, content_type='application/json')
    payload = json.loads(response.data.decode('utf-8'))

    assert response.status_code == 200
    assert 'response' in list(payload.keys())
    assert type(payload['response']) is list
    assert type(payload['response'][0]) is dict
    assert len(payload['response']) == 3
    assert payload['response'][0]['node_type'] == 'matrix'
    assert payload['response'][1]['node_type'] == 'weights'
    assert type(payload['response'][1]['data'][0]) is dict
    assert len(payload['response'][1]['data'][0]['weights']) == 3
    assert payload['response'][1]['method'] == 'EQUAL'
    assert len(payload['response'][2]['data'][0]['weights']) == 3
    assert payload['response'][2]['method'] == 'ENTROPY'

def test_results_calculation_no_weights_method(client):
    """
        Test verifying the functionality of multi-criteria calculations for model with no weights
    """
    data = [
        {
            "id": 1,
            "node_type": "matrix",
            "extension": "crisp",
            "matrix": [
                [6, 2, 3],
                [3, 7, 2],
                [2, 3, 8],
            ],
            "criteria_types": [1, -1, 1],
            "method": "input",
            "connections_from": [],
            "connections_to": [2, 3],
            "position_x": 10,
            "position_y": 10,
        }
    ]


    response = client.post('/api/v1/calculations/calculate', headers={'locale': 'en'}, json={'data': data}, content_type='application/json')
    payload = json.loads(response.data.decode('utf-8'))

    assert response.status_code == 400
    assert 'message' in list(payload.keys())
    
def test_results_calculation_wrong_weights_method(client):
    """
        Test verifying the functionality of multi-criteria calculations for model with wrong name of weights method
    """
    data = [
        {
            "id": 1,
            "node_type": "matrix",
            "extension": "crisp",
            "matrix": [
                [6, 2, 3],
                [3, 7, 2],
                [2, 3, 8],
            ],
            "criteria_types": [1, -1, 1],
            "method": "input",
            "connections_from": [],
            "connections_to": [2, 3],
            "position_x": 10,
            "position_y": 10,
        },
        {
            "id": 2,
            "node_type": "weights",
            "extension": "crisp",
            "weights": [],
            "method": "Wrong name",
            "connections_from": [1],
            "connections_to": [],
            "position_x": 20,
            "position_y": 20,
        }
    ]


    response = client.post('/api/v1/calculations/calculate', headers={'locale': 'en'}, json={'data': data}, content_type='application/json')
    payload = json.loads(response.data.decode('utf-8'))

    assert response.status_code == 400
    assert 'message' in list(payload.keys())

def test_results_calculation_weights_method_with_wrong_matrix(client):
    """
        Test verifying the functionality of multi-criteria calculations for model with weights method and wrong matrix
    """
    data = [
        {
            "id": 1,
            "node_type": "matrix",
            "extension": "crisp",
            "matrix": [
                [6, 2, 3],
                [3, 7, 2],
                [2, 3],
            ],
            "criteria_types": [1, -1, 1],
            "method": "input",
            "connections_from": [],
            "connections_to": [2, 3],
            "position_x": 10,
            "position_y": 10,
        },
        {
            "id": 2,
            "node_type": "weights",
            "extension": "crisp",
            "weights": [],
            "method": "EQUAL",
            "connections_from": [1],
            "connections_to": [],
            "position_x": 20,
            "position_y": 20,
        }
    ]


    response = client.post('/api/v1/calculations/calculate', headers={'locale': 'en'}, json={'data': data}, content_type='application/json')
    payload = json.loads(response.data.decode('utf-8'))

    assert response.status_code == 400
    assert 'message' in list(payload.keys())
    