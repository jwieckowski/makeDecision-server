# Copyright (c) 2023 Jakub Więckowski

from .server import app
import json
import pytest

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_results_calculation_angle_method_crisp(client):
    """
        Test verifying the functionality of multi-criteria calculations for basic model structure with ANGLE weights method with crisp data
    """
    matrix = [
        [1, 2, 3],
        [4, 5, 3],
        [6, 2, 1],
    ]
    types = [1, -1, 1]
    extensions = ['crisp']
    method = [
        {
            'method': "TOPSIS",
            'weights': "ANGLE"
        }
    ]
    params = [{}]

    response = client.post('/api/v1/results', headers={'locale': 'en'}, json={'matrix': [matrix],'extensions': extensions,'types': [types],'method': [method], 'params': [params]}, content_type='application/json')
    payload = json.loads(response.data.decode('utf-8'))

    assert response.status_code == 200
    assert type(payload) is dict
    assert 'matrices' in payload.keys()
    assert 'method' in payload.keys()
    assert 'methodCorrelations' in payload.keys()
    assert 'methodRankings' in payload.keys()
    assert 'methodCorrelations' in payload.keys()

def test_results_calculation_cilos_method_crisp(client):
    """
        Test verifying the functionality of multi-criteria calculations for basic model structure with CILOS weights method with crisp data
    """
    matrix = [
        [1, 2, 3],
        [4, 5, 3],
        [6, 2, 1],
    ]
    types = [1, -1, 1]
    extensions = ['crisp']
    method = [
        {
            'method': "TOPSIS",
            'weights': "CILOS"
        }
    ]
    params = [{}]

    response = client.post('/api/v1/results', headers={'locale': 'en'}, json={'matrix': [matrix],'extensions': extensions,'types': [types],'method': [method], 'params': [params]}, content_type='application/json')
    payload = json.loads(response.data.decode('utf-8'))

    assert response.status_code == 200
    assert type(payload) is dict
    assert 'matrices' in payload.keys()
    assert 'method' in payload.keys()
    assert 'methodCorrelations' in payload.keys()
    assert 'methodRankings' in payload.keys()
    assert 'methodCorrelations' in payload.keys()

def test_results_calculation_critic_method_crisp(client):
    """
        Test verifying the functionality of multi-criteria calculations for basic model structure with CRITIC weights method with crisp data
    """
    matrix = [
        [1, 2, 3],
        [4, 5, 3],
        [6, 2, 1],
    ]
    types = [1, -1, 1]
    extensions = ['crisp']
    method = [
        {
            'method': "TOPSIS",
            'weights': "CRITIC"
        }
    ]
    params = [{}]

    response = client.post('/api/v1/results', headers={'locale': 'en'}, json={'matrix': [matrix],'extensions': extensions,'types': [types],'method': [method], 'params': [params]}, content_type='application/json')
    payload = json.loads(response.data.decode('utf-8'))

    assert response.status_code == 200
    assert type(payload) is dict
    assert 'matrices' in payload.keys()
    assert 'method' in payload.keys()
    assert 'methodCorrelations' in payload.keys()
    assert 'methodRankings' in payload.keys()
    assert 'methodCorrelations' in payload.keys()

def test_results_calculation_entropy_method_crisp(client):
    """
        Test verifying the functionality of multi-criteria calculations for basic model structure with ENTROPY weights method with crisp data
    """
    matrix = [
        [1, 2, 3],
        [4, 5, 3],
        [6, 2, 1],
    ]
    types = [1, -1, 1]
    extensions = ['crisp']
    method = [
        {
            'method': "TOPSIS",
            'weights': "ENTROPY"
        }
    ]
    params = [{}]

    response = client.post('/api/v1/results', headers={'locale': 'en'}, json={'matrix': [matrix],'extensions': extensions,'types': [types],'method': [method], 'params': [params]}, content_type='application/json')
    payload = json.loads(response.data.decode('utf-8'))

    assert response.status_code == 200
    assert type(payload) is dict
    assert 'matrices' in payload.keys()
    assert 'method' in payload.keys()
    assert 'methodCorrelations' in payload.keys()
    assert 'methodRankings' in payload.keys()
    assert 'methodCorrelations' in payload.keys()

def test_results_calculation_equal_method_crisp(client):
    """
        Test verifying the functionality of multi-criteria calculations for basic model structure with EQUAL weights method with crisp data
    """
    matrix = [
        [1, 2, 3],
        [4, 5, 3],
        [6, 2, 1],
    ]
    types = [1, -1, 1]
    extensions = ['crisp']
    method = [
        {
            'method': "TOPSIS",
            'weights': "EQUAL"
        }
    ]
    params = [{}]

    response = client.post('/api/v1/results', headers={'locale': 'en'}, json={'matrix': [matrix],'extensions': extensions,'types': [types],'method': [method], 'params': [params]}, content_type='application/json')
    payload = json.loads(response.data.decode('utf-8'))

    assert response.status_code == 200
    assert type(payload) is dict
    assert 'matrices' in payload.keys()
    assert 'method' in payload.keys()
    assert 'methodCorrelations' in payload.keys()
    assert 'methodRankings' in payload.keys()
    assert 'methodCorrelations' in payload.keys()

def test_results_calculation_gini_method_crisp(client):
    """
        Test verifying the functionality of multi-criteria calculations for basic model structure with GINI weights method with crisp data
    """
    matrix = [
        [1, 2, 3],
        [4, 5, 3],
        [6, 2, 1],
    ]
    types = [1, -1, 1]
    extensions = ['crisp']
    method = [
        {
            'method': "TOPSIS",
            'weights': "GINI"
        }
    ]
    params = [{}]

    response = client.post('/api/v1/results', headers={'locale': 'en'}, json={'matrix': [matrix],'extensions': extensions,'types': [types],'method': [method], 'params': [params]}, content_type='application/json')
    payload = json.loads(response.data.decode('utf-8'))

    assert response.status_code == 200
    assert type(payload) is dict
    assert 'matrices' in payload.keys()
    assert 'method' in payload.keys()
    assert 'methodCorrelations' in payload.keys()
    assert 'methodRankings' in payload.keys()
    assert 'methodCorrelations' in payload.keys()

def test_results_calculation_idocriw_method_crisp(client):
    """
        Test verifying the functionality of multi-criteria calculations for basic model structure with IDOCRIW weights method with crisp data
    """
    matrix = [
        [1, 2, 3],
        [4, 5, 3],
        [6, 2, 1],
    ]
    types = [1, -1, 1]
    extensions = ['crisp']
    method = [
        {
            'method': "TOPSIS",
            'weights': "IDOCRIW"
        }
    ]
    params = [{}]

    response = client.post('/api/v1/results', headers={'locale': 'en'}, json={'matrix': [matrix],'extensions': extensions,'types': [types],'method': [method], 'params': [params]}, content_type='application/json')
    payload = json.loads(response.data.decode('utf-8'))

    assert response.status_code == 200
    assert type(payload) is dict
    assert 'matrices' in payload.keys()
    assert 'method' in payload.keys()
    assert 'methodCorrelations' in payload.keys()
    assert 'methodRankings' in payload.keys()
    assert 'methodCorrelations' in payload.keys()

def test_results_calculation_input_method_crisp(client):
    """
        Test verifying the functionality of multi-criteria calculations for basic model structure with INPUT weights method with crisp data
    """
    matrix = [
        [1, 2, 3],
        [4, 5, 3],
        [6, 2, 1],
    ]
    types = [1, -1, 1]
    extensions = ['crisp']
    method = [
        {
            'method': "TOPSIS",
            'weights': [0.1, 0.4, 0.5]
        }
    ]
    params = [{}]

    response = client.post('/api/v1/results', headers={'locale': 'en'}, json={'matrix': [matrix],'extensions': extensions,'types': [types],'method': [method], 'params': [params]}, content_type='application/json')
    payload = json.loads(response.data.decode('utf-8'))

    assert response.status_code == 200
    assert type(payload) is dict
    assert 'matrices' in payload.keys()
    assert 'method' in payload.keys()
    assert 'methodCorrelations' in payload.keys()
    assert 'methodRankings' in payload.keys()
    assert 'methodCorrelations' in payload.keys()

def test_results_calculation_merec_method_crisp(client):
    """
        Test verifying the functionality of multi-criteria calculations for basic model structure with MEREC weights method with crisp data
    """
    matrix = [
        [1, 2, 3],
        [4, 5, 3],
        [6, 2, 1],
    ]
    types = [1, -1, 1]
    extensions = ['crisp']
    method = [
        {
            'method': "TOPSIS",
            'weights': "MEREC"
        }
    ]
    params = [{}]

    response = client.post('/api/v1/results', headers={'locale': 'en'}, json={'matrix': [matrix],'extensions': extensions,'types': [types],'method': [method], 'params': [params]}, content_type='application/json')
    payload = json.loads(response.data.decode('utf-8'))

    assert response.status_code == 200
    assert type(payload) is dict
    assert 'matrices' in payload.keys()
    assert 'method' in payload.keys()
    assert 'methodCorrelations' in payload.keys()
    assert 'methodRankings' in payload.keys()
    assert 'methodCorrelations' in payload.keys()

def test_results_calculation_std_method_crisp(client):
    """
        Test verifying the functionality of multi-criteria calculations for basic model structure with STANDARD DEVIATION weights method with crisp data
    """
    matrix = [
        [1, 2, 3],
        [4, 5, 3],
        [6, 2, 1],
    ]
    types = [1, -1, 1]
    extensions = ['crisp']
    method = [
        {
            'method': "TOPSIS",
            'weights': "STANDARD DEVIATION"
        }
    ]
    params = [{}]

    response = client.post('/api/v1/results', headers={'locale': 'en'}, json={'matrix': [matrix],'extensions': extensions,'types': [types],'method': [method], 'params': [params]}, content_type='application/json')
    payload = json.loads(response.data.decode('utf-8'))

    assert response.status_code == 200
    assert type(payload) is dict
    assert 'matrices' in payload.keys()
    assert 'method' in payload.keys()
    assert 'methodCorrelations' in payload.keys()
    assert 'methodRankings' in payload.keys()
    assert 'methodCorrelations' in payload.keys()

def test_results_calculation_variance_method_crisp(client):
    """
        Test verifying the functionality of multi-criteria calculations for basic model structure with VARIANCE weights method with crisp data
    """
    matrix = [
        [1, 2, 3],
        [4, 5, 3],
        [6, 2, 1],
    ]
    types = [1, -1, 1]
    extensions = ['crisp']
    method = [
        {
            'method': "TOPSIS",
            'weights': "VARIANCE"
        }
    ]
    params = [{}]

    response = client.post('/api/v1/results', headers={'locale': 'en'}, json={'matrix': [matrix],'extensions': extensions,'types': [types],'method': [method], 'params': [params]}, content_type='application/json')
    payload = json.loads(response.data.decode('utf-8'))

    assert response.status_code == 200
    assert type(payload) is dict
    assert 'matrices' in payload.keys()
    assert 'method' in payload.keys()
    assert 'methodCorrelations' in payload.keys()
    assert 'methodRankings' in payload.keys()
    assert 'methodCorrelations' in payload.keys()

def test_results_calculation_entropy_method_fuzzy(client):
    """
        Test verifying the functionality of multi-criteria calculations for basic model structure with ENTROPY weights method with fuzzy data
    """
    matrix = [
        [
            [[1, 2, 3], [4, 5, 6], [6, 7, 8]],
            [[4, 5, 7], [1, 2, 4], [6, 8, 9]],
            [[4, 5, 6], [2, 2, 3], [3, 3, 4]],
        ],
    ]
    types = [1, -1, 1]
    extensions = ['fuzzy']
    method = [
        {
            'method': "TOPSIS",
            'weights': "ENTROPY"
        }
    ]
    params = [{}]

    response = client.post('/api/v1/results', headers={'locale': 'en'}, json={'matrix': matrix,'extensions': extensions,'types': [types],'method': [method], 'params': [params]}, content_type='application/json')
    payload = json.loads(response.data.decode('utf-8'))

    assert response.status_code == 200
    assert type(payload) is dict
    assert 'matrices' in payload.keys()
    assert 'method' in payload.keys()
    assert 'methodCorrelations' in payload.keys()
    assert 'methodRankings' in payload.keys()
    assert 'methodCorrelations' in payload.keys()

def test_results_calculation_equal_method_fuzzy(client):
    """
        Test verifying the functionality of multi-criteria calculations for basic model structure with EQUAL weights method with fuzzy data
    """
    matrix = [
        [
            [[1, 2, 3], [4, 5, 6], [6, 7, 8]],
            [[4, 5, 7], [1, 2, 4], [6, 8, 9]],
            [[4, 5, 6], [2, 2, 3], [3, 3, 4]],
        ],
    ]
    types = [1, -1, 1]
    extensions = ['fuzzy']
    method = [
        {
            'method': "TOPSIS",
            'weights': "EQUAL"
        }
    ]
    params = [{}]

    response = client.post('/api/v1/results', headers={'locale': 'en'}, json={'matrix': matrix,'extensions': extensions,'types': [types],'method': [method], 'params': [params]}, content_type='application/json')
    payload = json.loads(response.data.decode('utf-8'))

    assert response.status_code == 200
    assert type(payload) is dict
    assert 'matrices' in payload.keys()
    assert 'method' in payload.keys()
    assert 'methodCorrelations' in payload.keys()
    assert 'methodRankings' in payload.keys()
    assert 'methodCorrelations' in payload.keys()

def test_results_calculation_input_method_fuzzy(client):
    """
        Test verifying the functionality of multi-criteria calculations for basic model structure with INPUT weights method with fuzzy data
    """
    matrix = [
        [
            [[1, 2, 3], [4, 5, 6], [6, 7, 8]],
            [[4, 5, 7], [1, 2, 4], [6, 8, 9]],
            [[4, 5, 6], [2, 2, 3], [3, 3, 4]],
        ],
    ]
    types = [1, -1, 1]
    extensions = ['fuzzy']
    method = [
        {
            'method': "TOPSIS",
            'weights': [0.4, 0.2, 0.4]
        }
    ]
    params = [{}]

    response = client.post('/api/v1/results', headers={'locale': 'en'}, json={'matrix': matrix,'extensions': extensions,'types': [types],'method': [method], 'params': [params]}, content_type='application/json')
    payload = json.loads(response.data.decode('utf-8'))

    assert response.status_code == 200
    assert type(payload) is dict
    assert 'matrices' in payload.keys()
    assert 'method' in payload.keys()
    assert 'methodCorrelations' in payload.keys()
    assert 'methodRankings' in payload.keys()
    assert 'methodCorrelations' in payload.keys()

def test_results_calculation_std_method_fuzzy(client):
    """
        Test verifying the functionality of multi-criteria calculations for basic model structure with STANDARD DEVIATION weights method with fuzzy data
    """
    matrix = [
        [
            [[1, 2, 3], [4, 5, 6], [6, 7, 8]],
            [[4, 5, 7], [1, 2, 4], [6, 8, 9]],
            [[4, 5, 6], [2, 2, 3], [3, 3, 4]],
        ],
    ]
    types = [1, -1, 1]
    extensions = ['fuzzy']
    method = [
        {
            'method': "TOPSIS",
            'weights': "STANDARD DEVIATION"
        }
    ]
    params = [{}]

    response = client.post('/api/v1/results', headers={'locale': 'en'}, json={'matrix': matrix,'extensions': extensions,'types': [types],'method': [method], 'params': [params]}, content_type='application/json')
    payload = json.loads(response.data.decode('utf-8'))

    assert response.status_code == 200
    assert type(payload) is dict
    assert 'matrices' in payload.keys()
    assert 'method' in payload.keys()
    assert 'methodCorrelations' in payload.keys()
    assert 'methodRankings' in payload.keys()
    assert 'methodCorrelations' in payload.keys()

def test_results_calculation_variance_method_fuzzy(client):
    """
        Test verifying the functionality of multi-criteria calculations for basic model structure with VARIANCE weights method with fuzzy data
    """
    matrix = [
        [
            [[1, 2, 3], [4, 5, 6], [6, 7, 8]],
            [[4, 5, 7], [1, 2, 4], [6, 8, 9]],
            [[4, 5, 6], [2, 2, 3], [3, 3, 4]],
        ],
    ]
    types = [1, -1, 1]
    extensions = ['fuzzy']
    method = [
        {
            'method': "TOPSIS",
            'weights': "VARIANCE"
        }
    ]
    params = [{}]

    response = client.post('/api/v1/results', headers={'locale': 'en'}, json={'matrix': matrix,'extensions': extensions,'types': [types],'method': [method], 'params': [params]}, content_type='application/json')
    payload = json.loads(response.data.decode('utf-8'))

    assert response.status_code == 200
    assert type(payload) is dict
    assert 'matrices' in payload.keys()
    assert 'method' in payload.keys()
    assert 'methodCorrelations' in payload.keys()
    assert 'methodRankings' in payload.keys()
    assert 'methodCorrelations' in payload.keys()

def test_results_calculation_unhandled_method_crisp(client):
    """
        Test verifying the functionality of multi-criteria calculations for basic model structure with not available weights method with crisp data
    """
    matrix = [
        [1, 2, 3],
        [4, 5, 3],
        [6, 2, 1],
    ]
    types = [1, -1, 1]
    extensions = ['crisp']
    method = [
        {
            'method': "TOPSIS",
            'weights': "ABC"
        }
    ]
    params = [{}]

    response = client.post('/api/v1/results', headers={'locale': 'en'}, json={'matrix': [matrix],'extensions': extensions,'types': [types],'method': [method], 'params': [params]}, content_type='application/json')
    payload = json.loads(response.data.decode('utf-8'))

    assert response.status_code == 400
    assert type(payload) is dict
    assert 'message' in payload.keys()

def test_results_calculation_wrong_input_method_crisp(client):
    """
        Test verifying the functionality of multi-criteria calculations for basic model structure with wrong INPUT weights method with crisp data
    """
    matrix = [
        [1, 2, 3],
        [4, 5, 3],
        [6, 2, 1],
    ]
    types = [1, -1, 1]
    extensions = ['crisp']
    method = [
        {
            'method': "TOPSIS",
            'weights': ['a', 'b', 'c']
        }
    ]
    params = [{}]

    response = client.post('/api/v1/results', headers={'locale': 'en'}, json={'matrix': [matrix],'extensions': extensions,'types': [types],'method': [method], 'params': [params]}, content_type='application/json')
    payload = json.loads(response.data.decode('utf-8'))

    assert response.status_code == 400
    assert type(payload) is dict
    assert 'message' in payload.keys()

def test_results_calculation_wrong_sum_input_method_crisp(client):
    """
        Test verifying the functionality of multi-criteria calculations for basic model structure with wrong sum of weights from INPUT weights method with crisp data
    """
    matrix = [
        [1, 2, 3],
        [4, 5, 3],
        [6, 2, 1],
    ]
    types = [1, -1, 1]
    extensions = ['crisp']
    method = [
        {
            'method': "TOPSIS",
            'weights': [0.1, 0.2, 0.1]
        }
    ]
    params = [{}]

    response = client.post('/api/v1/results', headers={'locale': 'en'}, json={'matrix': [matrix],'extensions': extensions,'types': [types],'method': [method], 'params': [params]}, content_type='application/json')
    payload = json.loads(response.data.decode('utf-8'))

    assert response.status_code == 400
    assert type(payload) is dict
    assert 'message' in payload.keys()

def test_results_calculation_wrong_size_input_method_crisp(client):
    """
        Test verifying the functionality of multi-criteria calculations for basic model structure with wrong size of weights from INPUT weights method with crisp data
    """
    matrix = [
        [1, 2, 3],
        [4, 5, 3],
        [6, 2, 1],
    ]
    types = [1, -1, 1]
    extensions = ['crisp']
    method = [
        {
            'method': "TOPSIS",
            'weights': [0.1, 0.2]
        }
    ]
    params = [{}]

    response = client.post('/api/v1/results', headers={'locale': 'en'}, json={'matrix': [matrix],'extensions': extensions,'types': [types],'method': [method], 'params': [params]}, content_type='application/json')
    payload = json.loads(response.data.decode('utf-8'))

    assert response.status_code == 400
    assert type(payload) is dict
    assert 'message' in payload.keys()

def test_results_calculation_unhandled_method_fuzzy(client):
    """
        Test verifying the functionality of multi-criteria calculations for basic model structure with not available weights method with fuzzy data
    """
    matrix = [
        [
            [[1, 2, 3], [4, 5, 6], [6, 7, 8]],
            [[4, 5, 7], [1, 2, 4], [6, 8, 9]],
            [[4, 5, 6], [2, 2, 3], [3, 3, 4]],
        ],
    ]
    types = [1, -1, 1]
    extensions = ['fuzzy']
    method = [
        {
            'method': "TOPSIS",
            'weights': "ANGLE"
        }
    ]
    params = [{}]

    response = client.post('/api/v1/results', headers={'locale': 'en'}, json={'matrix': matrix,'extensions': extensions,'types': [types],'method': [method], 'params': [params]}, content_type='application/json')
    payload = json.loads(response.data.decode('utf-8'))

    assert response.status_code == 400
    assert type(payload) is dict
    assert 'message' in payload.keys()

