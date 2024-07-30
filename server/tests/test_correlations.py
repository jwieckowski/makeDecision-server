# Copyright (c) 2023 - 2024 Jakub Więckowski

from server import app
import json
import pytest

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_results_calculation_crisp_mcda_method_preferences_correlation(client):
    """
        Test verifying the functionality of multi-criteria calculations for basic model structure with mcda methods with crisp data and correlation of preferences
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
            "connections_to": [5],
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
            "connections_to": [5],
            "kwargs": [{"matrix_id": 1, "normalization_function": "max_normalization"}],
            "position_x": 40,
            "position_y": 40,
        },
        {
            "id": 5,
            "node_type": "correlation",
            "extension": "crisp",
            "method": "SPEARMAN",
            "connections_from": [3, 4],
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
    assert payload['response'][2]['node_type'] == 'method'
    assert type(payload['response'][2]['data'][0]) is dict
    assert payload['response'][2]['method'] == 'ARAS'
    assert len(payload['response'][2]['data']) == 1
    assert payload['response'][3]['node_type'] == 'method'
    assert type(payload['response'][3]['data'][0]) is dict
    assert payload['response'][3]['method'] == 'TOPSIS'
    assert len(payload['response'][3]['data']) == 1
    assert type(payload['response'][4]['data'][0]) is dict
    assert payload['response'][4]['node_type'] == 'correlation'


def test_results_calculation_crisp_weights_method_correlation(client):
    """
        Test verifying the functionality of multi-criteria calculations for basic model structure with weights methods with crisp data and correlation of weights
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
            "node_type": "correlation",
            "extension": "crisp",
            "method": "WEIGHTS SIMILARITY",
            "connections_from": [2, 3],
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

    assert payload['response'][2]['node_type'] == 'weights'
    assert type(payload['response'][2]['data'][0]) is dict
    assert len(payload['response'][2]['data'][0]['weights']) == 3
    assert payload['response'][2]['method'] == 'ENTROPY'

    assert type(payload['response'][3]['data'][0]) is dict
    assert payload['response'][3]['node_type'] == 'correlation'

def test_results_calculation_crisp_mcda_method_ranking_correlation(client):
    """
        Test verifying the functionality of multi-criteria calculations for basic model structure with mcda methods with crisp data and correlation of rankings
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
            "connections_to": [5],
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
            "connections_to": [6],
            "kwargs": [{"matrix_id": 1, "normalization_function": "max_normalization"}],
            "position_x": 40,
            "position_y": 40,
        },
        {
            "id": 5,
            "node_type": "ranking",
            "extension": "crisp",
            "method": "rank",
            "connections_from": [3],
            "connections_to": [7],
            "position_x": 50,
            "position_y": 50,
        },
        {
            "id": 6,
            "node_type": "ranking",
            "extension": "crisp",
            "method": "rank",
            "connections_from": [4],
            "connections_to": [7],
            "position_x": 60,
            "position_y": 60,
        },
        {
            "id": 7,
            "node_type": "correlation",
            "extension": "crisp",
            "method": "SPEARMAN",
            "connections_from": [5, 6],
            "connections_to": [],
            "position_x": 70,
            "position_y": 70,
        }
    ]

    response = client.post('/api/v1/calculations/calculate', headers={'locale': 'en'}, json={'data': data}, content_type='application/json')
    payload = json.loads(response.data.decode('utf-8'))

    assert response.status_code == 200
    assert 'response' in list(payload.keys())
    assert type(payload['response']) is list
    assert len(payload['response']) == 7
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
    assert payload['response'][3]['node_type'] == 'method'
    assert type(payload['response'][3]['data'][0]) is dict
    assert payload['response'][3]['method'] == 'TOPSIS'
    assert len(payload['response'][3]['data']) == 1
    assert type(payload['response'][4]['data'][0]) is dict
    assert payload['response'][4]['node_type'] == 'ranking'
    assert type(payload['response'][5]['data'][0]) is dict
    assert payload['response'][5]['node_type'] == 'ranking'
    assert type(payload['response'][6]['data'][0]) is dict
    assert payload['response'][6]['node_type'] == 'correlation'

def test_results_calculation_crisp_mcda_method_ranking_multiple_correlation(client):
    """
        Test verifying the functionality of multi-criteria calculations for basic model structure with mcda methods with crisp data and multiple correlations of rankings
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
            "connections_to": [5],
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
            "connections_to": [6],
            "kwargs": [{"matrix_id": 1, "normalization_function": "max_normalization"}],
            "position_x": 40,
            "position_y": 40,
        },
        {
            "id": 5,
            "node_type": "ranking",
            "extension": "crisp",
            "method": "rank",
            "connections_from": [3],
            "connections_to": [7, 8],
            "position_x": 50,
            "position_y": 50,
        },
        {
            "id": 6,
            "node_type": "ranking",
            "extension": "crisp",
            "method": "rank",
            "connections_from": [4],
            "connections_to": [7, 8],
            "position_x": 60,
            "position_y": 60,
        },
        {
            "id": 7,
            "node_type": "correlation",
            "extension": "crisp",
            "method": "WS RANK",
            "connections_from": [5, 6],
            "connections_to": [],
            "position_x": 70,
            "position_y": 70,
        },
        {
            "id": 8,
            "node_type": "correlation",
            "extension": "crisp",
            "method": "WEIGHTED SPEARMAN",
            "connections_from": [5, 6],
            "connections_to": [],
            "position_x": 80,
            "position_y": 80,
        }
    ]

    response = client.post('/api/v1/calculations/calculate', headers={'locale': 'en'}, json={'data': data}, content_type='application/json')
    payload = json.loads(response.data.decode('utf-8'))

    assert response.status_code == 200
    assert 'response' in list(payload.keys())
    assert type(payload['response']) is list
    assert len(payload['response']) == 8
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
    assert payload['response'][3]['node_type'] == 'method'
    assert type(payload['response'][3]['data'][0]) is dict
    assert payload['response'][3]['method'] == 'TOPSIS'
    assert len(payload['response'][3]['data']) == 1
    assert type(payload['response'][4]['data'][0]) is dict
    assert payload['response'][4]['node_type'] == 'ranking'
    assert type(payload['response'][5]['data'][0]) is dict
    assert payload['response'][5]['node_type'] == 'ranking'
    assert type(payload['response'][6]['data'][0]) is dict
    assert payload['response'][6]['node_type'] == 'correlation'
    assert type(payload['response'][7]['data'][0]) is dict
    assert payload['response'][7]['node_type'] == 'correlation'

def test_results_calculation_crisp_wrong_correlation(client):
    """
        Test verifying the functionality of multi-criteria calculations for basic model structure with wrong correlation method
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
            "connections_to": [5],
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
            "connections_to": [6],
            "kwargs": [{"matrix_id": 1, "normalization_function": "max_normalization"}],
            "position_x": 40,
            "position_y": 40,
        },
        {
            "id": 5,
            "node_type": "ranking",
            "extension": "crisp",
            "method": "rank",
            "connections_from": [3],
            "connections_to": [7, 8],
            "position_x": 50,
            "position_y": 50,
        },
        {
            "id": 6,
            "node_type": "ranking",
            "extension": "crisp",
            "method": "rank",
            "connections_from": [4],
            "connections_to": [7, 8],
            "position_x": 60,
            "position_y": 60,
        },
        {
            "id": 7,
            "node_type": "correlation",
            "extension": "crisp",
            "method": "WRONG METHOD",
            "connections_from": [5, 6],
            "connections_to": [],
            "position_x": 70,
            "position_y": 70,
        },
        {
            "id": 8,
            "node_type": "correlation",
            "extension": "crisp",
            "method": "WEIGHED SPEARMAN",
            "connections_from": [5, 6],
            "connections_to": [],
            "position_x": 80,
            "position_y": 80,
        }
    ]

    response = client.post('/api/v1/calculations/calculate', headers={'locale': 'en'}, json={'data': data}, content_type='application/json')
    payload = json.loads(response.data.decode('utf-8'))

    assert response.status_code == 400
    assert 'message' in list(payload.keys())