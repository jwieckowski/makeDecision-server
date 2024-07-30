# Copyright (c) 2023 - 2024 Jakub Więckowski

from server import app
import json
import pytest

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_results_calculation_mcda_method_crisp(client):
    """
        Test verifying the functionality of multi-criteria calculations for basic model structure with mcda method with crisp data
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
            "method": "EQUAL",
            "connections_from": [1],
            "connections_to": [3],
            "position_x": 20,
            "position_y": 20,
        },
        {
            "id": 3,
            "node_type": "method",
            "extension": "crisp",
            "method": "ARAS",
            "connections_from": [2],
            "connections_to": [],
            "kwargs": [{"matrix_id": 1, "normalization_function": "max_normalization"}],
            "position_x": 30,
            "position_y": 30,
        }
    ]


    response = client.post('/api/v1/calculations/calculate', headers={'locale': 'en'}, json={'data': data}, content_type='application/json')
    payload = json.loads(response.data.decode('utf-8'))

    assert response.status_code == 200
    assert 'response' in list(payload.keys())
    assert type(payload['response']) is list
    assert len(payload['response']) == 3
    assert type(payload['response'][0]) is dict
    assert payload['response'][0]['node_type'] == 'matrix'
    assert payload['response'][1]['node_type'] == 'weights'
    assert type(payload['response'][1]['data'][0]) is dict
    assert len(payload['response'][1]['data'][0]['weights']) == 3
    assert payload['response'][1]['method'] == 'EQUAL'
    assert type(payload['response'][2]['data'][0]) is dict
    assert payload['response'][2]['node_type'] == 'method'
    assert payload['response'][2]['method'] == 'ARAS'

def test_results_calculation_mcda_method_fuzzy(client):
    """
        Test verifying the functionality of multi-criteria calculations for basic model structure with mcda method with fuzzy data
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
            "connections_to": [3],
            "position_x": 20,
            "position_y": 20,
        },
        {
            "id": 3,
            "node_type": "method",
            "extension": "fuzzy",
            "method": "ARAS",
            "connections_from": [2],
            "connections_to": [],
            "kwargs": [{"matrix_id": 1, "normalization_function": "max_normalization"}],
            "position_x": 30,
            "position_y": 30,
        }
    ]


    response = client.post('/api/v1/calculations/calculate', headers={'locale': 'en'}, json={'data': data}, content_type='application/json')
    payload = json.loads(response.data.decode('utf-8'))

    assert response.status_code == 200
    assert 'response' in list(payload.keys())
    assert type(payload['response']) is list
    assert len(payload['response']) == 3
    assert type(payload['response'][0]) is dict
    assert payload['response'][0]['node_type'] == 'matrix'
    assert payload['response'][1]['node_type'] == 'weights'
    assert type(payload['response'][1]['data'][0]) is dict
    assert len(payload['response'][1]['data'][0]['weights']) == 3
    assert payload['response'][1]['method'] == 'EQUAL'
    assert type(payload['response'][2]['data'][0]) is dict
    assert payload['response'][2]['node_type'] == 'method'
    assert payload['response'][2]['method'] == 'ARAS'

def test_results_calculation_mcda_method_wrong_matrix_id(client):
    """
        Test verifying the functionality of multi-criteria calculations for basic model structure with mcda method with fuzzy data and wrong matrix id
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
            "connections_to": [3],
            "position_x": 20,
            "position_y": 20,
        },
        {
            "id": 3,
            "node_type": "method",
            "extension": "fuzzy",
            "method": "ARAS",
            "connections_from": [2],
            "connections_to": [],
            "kwargs": [{"matrix_id": 2, "normalization_function": "max_normalization"}],
            "position_x": 30,
            "position_y": 30,
        }
    ]


    response = client.post('/api/v1/calculations/calculate', headers={'locale': 'en'}, json={'data': data}, content_type='application/json')
    payload = json.loads(response.data.decode('utf-8'))

    assert response.status_code == 200
    assert 'response' in list(payload.keys())
    assert type(payload['response']) is list
    assert len(payload['response']) == 3
    assert type(payload['response'][0]) is dict
    assert payload['response'][0]['node_type'] == 'matrix'
    assert payload['response'][1]['node_type'] == 'weights'
    assert type(payload['response'][1]['data'][0]) is dict
    assert len(payload['response'][1]['data'][0]['weights']) == 3
    assert payload['response'][1]['method'] == 'EQUAL'
    assert type(payload['response'][2]['data'][0]) is dict
    assert payload['response'][2]['node_type'] == 'method'
    assert payload['response'][2]['method'] == 'ARAS'
    assert len(payload['response'][2]['data'][0]['kwargs']) == 0

def test_results_calculation_mcda_method_multiple_matrices(client):
    """
        Test verifying the functionality of multi-criteria calculations for basic model structure with mcda method with crisp data and multiple matrices
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
            "connections_to": [3],
            "position_x": 10,
            "position_y": 10,
        },
        {
            "id": 2,
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
            "connections_to": [3],
            "position_x": 10,
            "position_y": 10,
        },
        {
            "id": 3,
            "node_type": "weights",
            "extension": "crisp",
            "weights": [],
            "method": "EQUAL",
            "connections_from": [1, 2],
            "connections_to": [4],
            "position_x": 20,
            "position_y": 20,
        },
        {
            "id": 4,
            "node_type": "method",
            "extension": "crisp",
            "method": "ARAS",
            "connections_from": [3],
            "connections_to": [],
            "kwargs": [{"matrix_id": 1, "normalization_function": "max_normalization"}, {"matrix_id": 2, "normalization_function": "max_normalization"}],
            "position_x": 30,
            "position_y": 30,
        }
    ]


    response = client.post('/api/v1/calculations/calculate', headers={'locale': 'en'}, json={'data': data}, content_type='application/json')
    payload = json.loads(response.data.decode('utf-8'))

    assert response.status_code == 200
    assert 'response' in list(payload.keys())
    assert type(payload['response']) is list
    assert len(payload['response']) == 4
    assert type(payload['response'][0]) is dict
    assert payload['response'][0]['node_type'] == 'matrix'
    assert payload['response'][1]['node_type'] == 'matrix'
    assert payload['response'][2]['node_type'] == 'weights'
    assert type(payload['response'][2]['data'][0]) is dict
    assert len(payload['response'][2]['data'][0]['weights']) == 3
    assert payload['response'][2]['method'] == 'EQUAL'
    assert type(payload['response'][3]['data'][0]) is dict
    assert payload['response'][3]['node_type'] == 'method'
    assert payload['response'][3]['method'] == 'ARAS'
    assert len(payload['response'][3]['data']) == 2

def test_results_calculation_mcda_method_multiple_weights_methods(client):
    """
        Test verifying the functionality of multi-criteria calculations for basic model structure with mcda method with crisp data and multiple weights methods
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
            "method": "EQUAL",
            "connections_from": [1],
            "connections_to": [4],
            "position_x": 20,
            "position_y": 20,
        },
        {
            "id": 3,
            "node_type": "weights",
            "extension": "crisp",
            "weights": [],
            "method": "ENTROPY",
            "connections_from": [1],
            "connections_to": [4],
            "position_x": 30,
            "position_y": 30,
        },
        {
            "id": 4,
            "node_type": "method",
            "extension": "crisp",
            "method": "ARAS",
            "connections_from": [2, 3],
            "connections_to": [],
            "kwargs": [{"matrix_id": 1, "normalization_function": "max_normalization"}],
            "position_x": 40,
            "position_y": 40,
        }
    ]


    response = client.post('/api/v1/calculations/calculate', headers={'locale': 'en'}, json={'data': data}, content_type='application/json')
    payload = json.loads(response.data.decode('utf-8'))

    assert response.status_code == 200
    assert 'response' in list(payload.keys())
    assert type(payload['response']) is list
    assert len(payload['response']) == 4
    assert type(payload['response'][0]) is dict
    assert payload['response'][0]['node_type'] == 'matrix'
    assert payload['response'][1]['node_type'] == 'weights'
    assert type(payload['response'][1]['data'][0]) is dict
    assert len(payload['response'][1]['data'][0]['weights']) == 3
    assert payload['response'][1]['method'] == 'EQUAL'
    assert payload['response'][2]['node_type'] == 'weights'
    assert type(payload['response'][2]['data'][0]) is dict
    assert len(payload['response'][2]['data'][0]['weights']) == 3
    assert payload['response'][2]['method'] == 'ENTROPY'
    assert type(payload['response'][3]['data'][0]) is dict
    assert payload['response'][3]['node_type'] == 'method'
    assert payload['response'][3]['method'] == 'ARAS'
    assert len(payload['response'][3]['data']) == 2

def test_results_calculation_mcda_method_multiple_mcda_methods(client):
    """
        Test verifying the functionality of multi-criteria calculations for basic model structure with mcda method with crisp data and multiple mcda methods
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
            "method": "EQUAL",
            "connections_from": [1],
            "connections_to": [3, 4],
            "position_x": 20,
            "position_y": 20,
        },
        {
            "id": 3,
            "node_type": "method",
            "extension": "crisp",
            "method": "ARAS",
            "connections_from": [2],
            "connections_to": [],
            "kwargs": [{"matrix_id": 1, "normalization_function": "max_normalization"}],
            "position_x": 30,
            "position_y": 30,
        },
        {
            "id": 4,
            "node_type": "method",
            "extension": "crisp",
            "method": "TOPSIS",
            "connections_from": [2],
            "connections_to": [],
            "kwargs": [{"matrix_id": 1, "normalization_function": "max_normalization"}],
            "position_x": 40,
            "position_y": 40,
        }
    ]


    response = client.post('/api/v1/calculations/calculate', headers={'locale': 'en'}, json={'data': data}, content_type='application/json')
    payload = json.loads(response.data.decode('utf-8'))

    assert response.status_code == 200
    assert 'response' in list(payload.keys())
    assert type(payload['response']) is list
    assert len(payload['response']) == 4
    assert type(payload['response'][0]) is dict
    assert payload['response'][0]['node_type'] == 'matrix'
    assert payload['response'][1]['node_type'] == 'weights'
    assert type(payload['response'][1]['data'][0]) is dict
    assert len(payload['response'][1]['data'][0]['weights']) == 3
    assert payload['response'][1]['method'] == 'EQUAL'
    assert payload['response'][2]['node_type'] == 'method'
    assert type(payload['response'][2]['data'][0]) is dict
    assert payload['response'][2]['method'] == 'ARAS'
    assert len(payload['response'][2]['data']) == 1
    assert type(payload['response'][3]['data'][0]) is dict
    assert payload['response'][3]['node_type'] == 'method'
    assert payload['response'][3]['method'] == 'TOPSIS'
    assert len(payload['response'][3]['data']) == 1

