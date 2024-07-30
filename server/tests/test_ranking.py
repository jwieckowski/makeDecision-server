# Copyright (c) 2023 - 2024 Jakub Więckowski

from server import app
import json
import pytest

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_results_calculation_crisp_mcda_method_ranking(client):
    """
        Test verifying the functionality of multi-criteria calculations for basic model structure with mcda method with crisp data and ranking block
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
            "connections_to": [4],
            "kwargs": [{"matrix_id": 1, "normalization_function": "max_normalization"}],
            "position_x": 30,
            "position_y": 30,
        },
        {
            "id": 4,
            "node_type": "ranking",
            "extension": "crisp",
            "method": "rank",
            "connections_from": [3],
            "connections_to": [],
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
    assert payload['response'][3]['node_type'] == 'ranking'

def test_results_calculation_fuzzy_mcda_method_ranking(client):
    """
        Test verifying the functionality of multi-criteria calculations for basic model structure with mcda method with fuzzy data and multiple mcda methods
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
            "connections_to": [4],
            "kwargs": [{"matrix_id": 1, "normalization_function": "max_normalization"}],
            "position_x": 30,
            "position_y": 30,
        },
        {
            "id": 4,
            "node_type": "ranking",
            "extension": "crisp",
            "method": "rank",
            "connections_from": [3],
            "connections_to": [],
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
    assert payload['response'][3]['node_type'] == 'ranking'

def test_results_calculation_crisp_multiple_weights_method_ranking(client):
    """
        Test verifying the functionality of multi-criteria calculations for basic model structure with multiple weights method, mcda method with crisp data and ranking block
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
            "connections_to": [5],
            "kwargs": [{"matrix_id": 1, "normalization_function": "max_normalization"}],
            "position_x": 40,
            "position_y": 40,
        },
        {
            "id": 5,
            "node_type": "ranking",
            "extension": "crisp",
            "method": "rank",
            "connections_from": [4],
            "connections_to": [],
            "position_x": 50,
            "position_y": 50,
        }
    ]


    response = client.post('/api/v1/calculations/calculate', headers={'locale': 'en'}, json={'data': data}, content_type='application/json')
    payload = json.loads(response.data.decode('utf-8'))

    assert response.status_code == 200
    assert 'response' in list(payload.keys())
    assert type(payload['response']) is list
    assert len(payload['response']) == 5
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

    assert payload['response'][3]['node_type'] == 'method'
    assert type(payload['response'][3]['data'][0]) is dict
    assert payload['response'][3]['method'] == 'ARAS'
    assert len(payload['response'][3]['data']) == 2

    assert type(payload['response'][4]['data'][0]) is dict
    assert payload['response'][4]['node_type'] == 'ranking'
