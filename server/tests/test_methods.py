# Copyright (c) 2023 Jakub Więckowski

from server import app
import json
import pytest

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_results_calculation_aras_method_crisp(client):
    """
        Test verifying the functionality of multi-criteria calculations for ARAS method with crisp data
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
            'method': "ARAS",
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

def test_results_calculation_cocoso_method_crisp(client):
    """
        Test verifying the functionality of multi-criteria calculations for COCOSO method with crisp data
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
            'method': "COCOSO",
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

def test_results_calculation_codas_method_crisp(client):
    """
        Test verifying the functionality of multi-criteria calculations for CODAS method with crisp data
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
            'method': "CODAS",
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

def test_results_calculation_comet_method_crisp(client):
    """
        Test verifying the functionality of multi-criteria calculations for COMET method with crisp data
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
            'method': "COMET",
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

def test_results_calculation_copras_method_crisp(client):
    """
        Test verifying the functionality of multi-criteria calculations for COPRAS method with crisp data
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
            'method': "COPRAS",
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

def test_results_calculation_edas_method_crisp(client):
    """
        Test verifying the functionality of multi-criteria calculations for EDAS method with crisp data
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
            'method': "EDAS",
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

def test_results_calculation_mabac_method_crisp(client):
    """
        Test verifying the functionality of multi-criteria calculations for MABAC method with crisp data
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
            'method': "MABAC",
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

def test_results_calculation_mairca_method_crisp(client):
    """
        Test verifying the functionality of multi-criteria calculations for MAIRCA method with crisp data
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
            'method': "MAIRCA",
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

def test_results_calculation_marcos_method_crisp(client):
    """
        Test verifying the functionality of multi-criteria calculations for MARCOS method with crisp data
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
            'method': "MARCOS",
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

def test_results_calculation_moora_method_crisp(client):
    """
        Test verifying the functionality of multi-criteria calculations for MOORA method with crisp data
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
            'method': "MOORA",
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

def test_results_calculation_ocra_method_crisp(client):
    """
        Test verifying the functionality of multi-criteria calculations for OCRA method with crisp data
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
            'method': "OCRA",
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

def test_results_calculation_promethee_method_crisp(client):
    """
        Test verifying the functionality of multi-criteria calculations for PROMETHEE method with crisp data
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
            'method': "PROMETHEE",
            'weights': "ANGLE"
        }
    ]
    params = [{'extension': 'crisp', 'additional': {}, 'method': 'promethee'}]

    response = client.post('/api/v1/results', headers={'locale': 'en'}, json={'matrix': [matrix],'extensions': extensions,'types': [types],'method': [method], 'params': [params]}, content_type='application/json')
    payload = json.loads(response.data.decode('utf-8'))

    assert response.status_code == 200
    assert type(payload) is dict
    assert 'matrices' in payload.keys()
    assert 'method' in payload.keys()
    assert 'methodCorrelations' in payload.keys()
    assert 'methodRankings' in payload.keys()
    assert 'methodCorrelations' in payload.keys()

def test_results_calculation_spotis_method_crisp(client):
    """
        Test verifying the functionality of multi-criteria calculations for SPOTIS method with crisp data
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
            'method': "SPOTIS",
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

def test_results_calculation_topsis_method_crisp(client):
    """
        Test verifying the functionality of multi-criteria calculations for TOPSIS method with crisp data
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

def test_results_calculation_vikor_method_crisp(client):
    """
        Test verifying the functionality of multi-criteria calculations for VIKOR method with crisp data
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
            'method': "VIKOR",
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

def test_results_calculation_unhandled_method_crisp(client):
    """
        Test verifying the functionality of multi-criteria calculations for unhandled method with crisp data
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
            'method': "ABC",
            'weights': "ANGLE"
        }
    ]
    params = [{}]

    response = client.post('/api/v1/results', headers={'locale': 'en'}, json={'matrix': [matrix],'extensions': extensions,'types': [types],'method': [method], 'params': [params]}, content_type='application/json')
    payload = json.loads(response.data.decode('utf-8'))

    assert response.status_code == 400
    assert type(payload) is dict
    assert 'message' in payload.keys()

def test_results_calculation_aras_method_fuzzy(client):
    """
        Test verifying the functionality of multi-criteria calculations for model with ARAS method with fuzzy data
    """
    matrix = [
        [
            [[1, 2, 3], [4, 5, 6], [6, 7, 8]],
            [[4, 5, 7], [1, 2, 4], [6, 8, 9]],
            [[4, 5, 6], [2, 2, 3], [3, 3, 4]],
        ],
    ]
    types = [[1, -1, 1]]
    extensions = ['fuzzy']
    method = [
        {
            'method': "ARAS",
            'weights': "ENTROPY"
        },
    ]
    params = [{}]

    response = client.post('/api/v1/results', headers={'locale': 'en'}, json={'matrix': matrix,'extensions': extensions,'types': types,'method': [method], 'params': [params]}, content_type='application/json')
    payload = json.loads(response.data.decode('utf-8'))

    assert response.status_code == 200
    assert type(payload) is dict
    assert 'matrices' in payload.keys()
    assert 'method' in payload.keys()
    assert 'methodCorrelations' in payload.keys()
    assert 'methodRankings' in payload.keys()
    assert 'methodCorrelations' in payload.keys()

def test_results_calculation_codas_method_fuzzy(client):
    """
        Test verifying the functionality of multi-criteria calculations for model with CODAS method with fuzzy data
    """
    matrix = [
        [
            [[1, 2, 3], [4, 5, 6], [6, 7, 8]],
            [[4, 5, 7], [1, 2, 4], [6, 8, 9]],
            [[4, 5, 6], [2, 2, 3], [3, 3, 4]],
        ],
    ]
    types = [[1, -1, 1]]
    extensions = ['fuzzy']
    method = [
        {
            'method': "CODAS",
            'weights': "ENTROPY"
        },
    ]
    params = [{}]

    response = client.post('/api/v1/results', headers={'locale': 'en'}, json={'matrix': matrix,'extensions': extensions,'types': types,'method': [method], 'params': [params]}, content_type='application/json')
    payload = json.loads(response.data.decode('utf-8'))

    assert response.status_code == 200
    assert type(payload) is dict
    assert 'matrices' in payload.keys()
    assert 'method' in payload.keys()
    assert 'methodCorrelations' in payload.keys()
    assert 'methodRankings' in payload.keys()
    assert 'methodCorrelations' in payload.keys()

def test_results_calculation_copras_method_fuzzy(client):
    """
        Test verifying the functionality of multi-criteria calculations for model with COPRAS method with fuzzy data
    """
    matrix = [
        [
            [[1, 2, 3], [4, 5, 6], [6, 7, 8]],
            [[4, 5, 7], [1, 2, 4], [6, 8, 9]],
            [[4, 5, 6], [2, 2, 3], [3, 3, 4]],
        ],
    ]
    types = [[1, -1, 1]]
    extensions = ['fuzzy']
    method = [
        {
            'method': "COPRAS",
            'weights': "ENTROPY"
        },
    ]
    params = [{}]

    response = client.post('/api/v1/results', headers={'locale': 'en'}, json={'matrix': matrix,'extensions': extensions,'types': types,'method': [method], 'params': [params]}, content_type='application/json')
    payload = json.loads(response.data.decode('utf-8'))

    assert response.status_code == 200
    assert type(payload) is dict
    assert 'matrices' in payload.keys()
    assert 'method' in payload.keys()
    assert 'methodCorrelations' in payload.keys()
    assert 'methodRankings' in payload.keys()
    assert 'methodCorrelations' in payload.keys()

def test_results_calculation_edas_method_fuzzy(client):
    """
        Test verifying the functionality of multi-criteria calculations for model with EDAS method with fuzzy data
    """
    matrix = [
        [
            [[1, 2, 3], [4, 5, 6], [6, 7, 8]],
            [[4, 5, 7], [1, 2, 4], [6, 8, 9]],
            [[4, 5, 6], [2, 2, 3], [3, 3, 4]],
        ],
    ]
    types = [[1, -1, 1]]
    extensions = ['fuzzy']
    method = [
        {
            'method': "EDAS",
            'weights': "ENTROPY"
        },
    ]
    params = [{}]

    response = client.post('/api/v1/results', headers={'locale': 'en'}, json={'matrix': matrix,'extensions': extensions,'types': types,'method': [method], 'params': [params]}, content_type='application/json')
    payload = json.loads(response.data.decode('utf-8'))

    assert response.status_code == 200
    assert type(payload) is dict
    assert 'matrices' in payload.keys()
    assert 'method' in payload.keys()
    assert 'methodCorrelations' in payload.keys()
    assert 'methodRankings' in payload.keys()
    assert 'methodCorrelations' in payload.keys()

def test_results_calculation_mabac_method_fuzzy(client):
    """
        Test verifying the functionality of multi-criteria calculations for model with MABAC method with fuzzy data
    """
    matrix = [
        [
            [[1, 2, 3], [4, 5, 6], [6, 7, 8]],
            [[4, 5, 7], [1, 2, 4], [6, 8, 9]],
            [[4, 5, 6], [2, 2, 3], [3, 3, 4]],
        ],
    ]
    types = [[1, -1, 1]]
    extensions = ['fuzzy']
    method = [
        {
            'method': "MABAC",
            'weights': "ENTROPY"
        },
    ]
    params = [{}]

    response = client.post('/api/v1/results', headers={'locale': 'en'}, json={'matrix': matrix,'extensions': extensions,'types': types,'method': [method], 'params': [params]}, content_type='application/json')
    payload = json.loads(response.data.decode('utf-8'))

    assert response.status_code == 200
    assert type(payload) is dict
    assert 'matrices' in payload.keys()
    assert 'method' in payload.keys()
    assert 'methodCorrelations' in payload.keys()
    assert 'methodRankings' in payload.keys()
    assert 'methodCorrelations' in payload.keys()

def test_results_calculation_mairca_method_fuzzy(client):
    """
        Test verifying the functionality of multi-criteria calculations for model with MAIRCA method with fuzzy data
    """
    matrix = [
        [
            [[1, 2, 3], [4, 5, 6], [6, 7, 8]],
            [[4, 5, 7], [1, 2, 4], [6, 8, 9]],
            [[4, 5, 6], [2, 2, 3], [3, 3, 4]],
        ],
    ]
    types = [[1, -1, 1]]
    extensions = ['fuzzy']
    method = [
        {
            'method': "MAIRCA",
            'weights': "ENTROPY"
        },
    ]
    params = [{}]

    response = client.post('/api/v1/results', headers={'locale': 'en'}, json={'matrix': matrix,'extensions': extensions,'types': types,'method': [method], 'params': [params]}, content_type='application/json')
    payload = json.loads(response.data.decode('utf-8'))

    assert response.status_code == 200
    assert type(payload) is dict
    assert 'matrices' in payload.keys()
    assert 'method' in payload.keys()
    assert 'methodCorrelations' in payload.keys()
    assert 'methodRankings' in payload.keys()
    assert 'methodCorrelations' in payload.keys()

def test_results_calculation_moora_method_fuzzy(client):
    """
        Test verifying the functionality of multi-criteria calculations for model with MOORA method with fuzzy data
    """
    matrix = [
        [
            [[1, 2, 3], [4, 5, 6], [6, 7, 8]],
            [[4, 5, 7], [1, 2, 4], [6, 8, 9]],
            [[4, 5, 6], [2, 2, 3], [3, 3, 4]],
        ],
    ]
    types = [[1, -1, 1]]
    extensions = ['fuzzy']
    method = [
        {
            'method': "MOORA",
            'weights': "ENTROPY"
        },
    ]
    params = [{}]

    response = client.post('/api/v1/results', headers={'locale': 'en'}, json={'matrix': matrix,'extensions': extensions,'types': types,'method': [method], 'params': [params]}, content_type='application/json')
    payload = json.loads(response.data.decode('utf-8'))

    assert response.status_code == 200
    assert type(payload) is dict
    assert 'matrices' in payload.keys()
    assert 'method' in payload.keys()
    assert 'methodCorrelations' in payload.keys()
    assert 'methodRankings' in payload.keys()
    assert 'methodCorrelations' in payload.keys()

def test_results_calculation_ocra_method_fuzzy(client):
    """
        Test verifying the functionality of multi-criteria calculations for model with OCRA method with fuzzy data
    """
    matrix = [
        [
            [[1, 2, 3], [4, 5, 6], [6, 7, 8]],
            [[4, 5, 7], [1, 2, 4], [6, 8, 9]],
            [[4, 5, 6], [2, 2, 3], [3, 3, 4]],
        ],
    ]
    types = [[1, -1, 1]]
    extensions = ['fuzzy']
    method = [
        {
            'method': "OCRA",
            'weights': "ENTROPY"
        },
    ]
    params = [{}]

    response = client.post('/api/v1/results', headers={'locale': 'en'}, json={'matrix': matrix,'extensions': extensions,'types': types,'method': [method], 'params': [params]}, content_type='application/json')
    payload = json.loads(response.data.decode('utf-8'))

    assert response.status_code == 200
    assert type(payload) is dict
    assert 'matrices' in payload.keys()
    assert 'method' in payload.keys()
    assert 'methodCorrelations' in payload.keys()
    assert 'methodRankings' in payload.keys()
    assert 'methodCorrelations' in payload.keys()

def test_results_calculation_topsis_method_fuzzy(client):
    """
        Test verifying the functionality of multi-criteria calculations for model with TOPSIS method with fuzzy data
    """
    matrix = [
        [
            [[1, 2, 3], [4, 5, 6], [6, 7, 8]],
            [[4, 5, 7], [1, 2, 4], [6, 8, 9]],
            [[4, 5, 6], [2, 2, 3], [3, 3, 4]],
        ],
    ]
    types = [[1, -1, 1]]
    extensions = ['fuzzy']
    method = [
        {
            'method': "TOPSIS",
            'weights': "ENTROPY"
        },
    ]
    params = [{}]

    response = client.post('/api/v1/results', headers={'locale': 'en'}, json={'matrix': matrix,'extensions': extensions,'types': types,'method': [method], 'params': [params]}, content_type='application/json')
    payload = json.loads(response.data.decode('utf-8'))

    assert response.status_code == 200
    assert type(payload) is dict
    assert 'matrices' in payload.keys()
    assert 'method' in payload.keys()
    assert 'methodCorrelations' in payload.keys()
    assert 'methodRankings' in payload.keys()
    assert 'methodCorrelations' in payload.keys()

def test_results_calculation_vikor_method_fuzzy(client):
    """
        Test verifying the functionality of multi-criteria calculations for model with VIKOR method with fuzzy data
    """
    matrix = [
        [
            [[1, 2, 3], [4, 5, 6], [6, 7, 8]],
            [[4, 5, 7], [1, 2, 4], [6, 8, 9]],
            [[4, 5, 6], [2, 2, 3], [3, 3, 4]],
        ],
    ]
    types = [[1, -1, 1]]
    extensions = ['fuzzy']
    method = [
        {
            'method': "VIKOR",
            'weights': "ENTROPY"
        },
    ]
    params = [{}]

    response = client.post('/api/v1/results', headers={'locale': 'en'}, json={'matrix': matrix,'extensions': extensions,'types': types,'method': [method], 'params': [params]}, content_type='application/json')
    payload = json.loads(response.data.decode('utf-8'))

    assert response.status_code == 200
    assert type(payload) is dict
    assert 'matrices' in payload.keys()
    assert 'method' in payload.keys()
    assert 'methodCorrelations' in payload.keys()
    assert 'methodRankings' in payload.keys()
    assert 'methodCorrelations' in payload.keys()

def test_results_calculation_unhandled_method_fuzzy(client):
    """
        Test verifying the functionality of multi-criteria calculations for model with COCOSO method with fuzzy data
    """
    matrix = [
        [
            [[1, 2, 3], [4, 5, 6], [6, 7, 8]],
            [[4, 5, 7], [1, 2, 4], [6, 8, 9]],
            [[4, 5, 6], [2, 2, 3], [3, 3, 4]],
        ],
    ]
    types = [[1, -1, 1]]
    extensions = ['fuzzy']
    method = [
        {
            'method': "COCOSO",
            'weights': "ENTROPY"
        },
    ]
    params = [{}]

    response = client.post('/api/v1/results', headers={'locale': 'en'}, json={'matrix': matrix,'extensions': extensions,'types': types,'method': [method], 'params': [params]}, content_type='application/json')
    payload = json.loads(response.data.decode('utf-8'))

    assert response.status_code == 400
    assert type(payload) is dict
    assert 'message' in payload.keys()

def test_results_calculation_wrong_method_fuzzy(client):
    """
        Test verifying the functionality of multi-criteria calculations for model with wrong method with fuzzy data
    """
    matrix = [
        [
            [[1, 2, 3], [4, 5, 6], [6, 7, 8]],
            [[4, 5, 7], [1, 2, 4], [6, 8, 9]],
            [[4, 5, 6], [2, 2, 3], [3, 3, 4]],
        ],
    ]
    types = [[1, -1, 1]]
    extensions = ['fuzzy']
    method = [
        {
            'method': "ABC",
            'weights': "ENTROPY"
        },
    ]
    params = [{}]

    response = client.post('/api/v1/results', headers={'locale': 'en'}, json={'matrix': matrix,'extensions': extensions,'types': types,'method': [method], 'params': [params]}, content_type='application/json')
    payload = json.loads(response.data.decode('utf-8'))

    assert response.status_code == 400
    assert type(payload) is dict
    assert 'message' in payload.keys()

