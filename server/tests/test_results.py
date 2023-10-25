# Copyright (c) 2023 Jakub Więckowski

from server import app
import json
import pytest

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_results_calculation_basic_model(client):
    """
        Test verifying the functionality of multi-criteria calculations for basic model structure
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

def test_results_calculation_missing_matrix_field(client):
    """
        Test verifying the functionality of multi-criteria calculations for model structure with missing matrix field
    """

    types = [1, -1, 1]
    extensions = ['crisp']
    method = [
        {
            'method': "TOPSIS",
            'weights': "ANGLE"
        }
    ]
    params = [{}]

    response = client.post('/api/v1/results', headers={'locale': 'en'}, json={'extensions': extensions,'types': [types],'method': [method], 'params': [params]}, content_type='application/json')
    payload = json.loads(response.data.decode('utf-8'))

    assert response.status_code == 400
    assert type(payload) is dict
    assert 'errors' in payload.keys()
    assert 'matrix' in payload['errors'].keys()

def test_results_calculation_missing_types_field(client):
    """
        Test verifying the functionality of multi-criteria calculations for model structure with missing types field
    """
    matrix = [
        [1, 2, 3],
        [4, 5, 3],
        [6, 2, 1],
    ]
    extensions = ['crisp']
    method = [
        {
            'method': "TOPSIS",
            'weights': "ANGLE"
        }
    ]
    params = [{}]

    response = client.post('/api/v1/results', headers={'locale': 'en'}, json={'matrix': [matrix],'extensions': extensions,'method': [method], 'params': [params]}, content_type='application/json')
    payload = json.loads(response.data.decode('utf-8'))

    assert response.status_code == 400
    assert type(payload) is dict
    assert 'errors' in payload.keys()
    assert 'types' in payload['errors'].keys()
    
def test_results_calculation_missing_extensions_field(client):
    """
        Test verifying the functionality of multi-criteria calculations for model structure with missing extensions field
    """
    matrix = [
        [1, 2, 3],
        [4, 5, 3],
        [6, 2, 1],
    ]
    types = [1, -1, 1]
    method = [
        {
            'method': "TOPSIS",
            'weights': "ANGLE"
        }
    ]
    params = [{}]

    response = client.post('/api/v1/results', headers={'locale': 'en'}, json={'matrix': [matrix],'types': [types],'method': [method], 'params': [params]}, content_type='application/json')
    payload = json.loads(response.data.decode('utf-8'))

    assert response.status_code == 400
    assert type(payload) is dict
    assert 'errors' in payload.keys()
    assert 'extensions' in payload['errors'].keys()

def test_results_calculation_missing_method_field(client):
    """
        Test verifying the functionality of multi-criteria calculations for model structure with missing method field
    """
    matrix = [
        [1, 2, 3],
        [4, 5, 3],
        [6, 2, 1],
    ]
    types = [1, -1, 1]
    extensions = ['crisp']
    params = [{}]

    response = client.post('/api/v1/results', headers={'locale': 'en'}, json={'matrix': [matrix],'extensions': extensions,'types': [types], 'params': [params]}, content_type='application/json')
    payload = json.loads(response.data.decode('utf-8'))

    assert response.status_code == 400
    assert type(payload) is dict
    assert 'errors' in payload.keys()
    assert 'method' in payload['errors'].keys()

def test_results_calculation_missing_params_field(client):
    """
        Test verifying the functionality of multi-criteria calculations for model structure with missing params field
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

    response = client.post('/api/v1/results', headers={'locale': 'en'}, json={'matrix': [matrix],'extensions': extensions,'types': [types],'method': [method]}, content_type='application/json')
    payload = json.loads(response.data.decode('utf-8'))

    assert response.status_code == 400
    assert type(payload) is dict
    assert 'errors' in payload.keys()
    assert 'params' in payload['errors'].keys()

def test_results_calculation_empty_matrix_given(client):
    """
        Test verifying the functionality of multi-criteria calculations for model structure with empty decision matrix
    """
    matrix = []
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

    assert response.status_code == 400
    assert type(payload) is dict
    assert 'message' in payload.keys()

def test_results_calculation_nonnumeric_matrix_given(client):
    """
        Test verifying the functionality of multi-criteria calculations for model structure with decision matrix that includes non numeric values
    """
    matrix = [
        ['a', 2, 3],
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

    assert response.status_code == 400
    assert type(payload) is dict
    assert 'message' in payload.keys()

def test_results_calculation_wrong_types_size(client):
    """
        Test verifying the functionality of multi-criteria calculations for model structure with decision matrix that includes non numeric values
    """
    matrix = [
        [2, 3, 1],
        [4, 5, 3],
        [6, 2, 1],
    ]
    types = [1, -1]
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

    assert response.status_code == 400
    assert type(payload) is dict
    assert 'message' in payload.keys()

def test_results_calculation_wrong_types_size(client):
    """
        Test verifying the functionality of multi-criteria calculations for model structure with different size of decision matrixes, criteria types vector and data extensions
    """
    matrix = [
        [2, 3, 1],
        [4, 5, 3],
        [6, 2, 1],
    ]
    types = [[1, -1, 1], [1, 2, 3]]
    extensions = ['crisp']
    method = [
        {
            'method': "TOPSIS",
            'weights': "ANGLE"
        }
    ]
    params = [{}]

    response = client.post('/api/v1/results', headers={'locale': 'en'}, json={'matrix': [matrix],'extensions': extensions,'types': types,'method': [method], 'params': [params]}, content_type='application/json')
    payload = json.loads(response.data.decode('utf-8'))

    assert response.status_code == 400
    assert type(payload) is dict
    assert 'message' in payload.keys()
    
def test_results_calculation_wrong_matrices_size(client):
    """
        Test verifying the functionality of multi-criteria calculations for model structure with different size of decision matrixes, criteria types vector and data extensions
    """
    matrix = [
        [
            [2, 3, 1],
            [4, 5, 3],
            [6, 2, 1],
        ],
        [
            [2, 3, 1],
            [4, 5, 3],
            [6, 2, 1],
        ],
    ]
    types = [[1, -1, 1]]
    extensions = ['crisp']
    method = [
        {
            'method': "TOPSIS",
            'weights': "ANGLE"
        }
    ]
    params = [{}]

    response = client.post('/api/v1/results', headers={'locale': 'en'}, json={'matrix': matrix,'extensions': extensions,'types': types,'method': [method], 'params': [params]}, content_type='application/json')
    payload = json.loads(response.data.decode('utf-8'))

    assert response.status_code == 400
    assert type(payload) is dict
    assert 'message' in payload.keys()

def test_results_calculation_wrong_extensions_size(client):
    """
        Test verifying the functionality of multi-criteria calculations for model structure with different size of decision matrixes, criteria types vector and data extensions
    """
    matrix = [
        [
            [2, 3, 1],
            [4, 5, 3],
            [6, 2, 1],
        ],
    ]
    types = [[1, -1, 1]]
    extensions = ['crisp', 'fuzzy']
    method = [
        {
            'method': "TOPSIS",
            'weights': "ANGLE"
        }
    ]
    params = [{}]

    response = client.post('/api/v1/results', headers={'locale': 'en'}, json={'matrix': matrix,'extensions': extensions,'types': types,'method': [method], 'params': [params]}, content_type='application/json')
    payload = json.loads(response.data.decode('utf-8'))

    assert response.status_code == 400
    assert type(payload) is dict
    assert 'message' in payload.keys()

def test_results_calculation_empty_method(client):
    """
        Test verifying the functionality of multi-criteria calculations for model structure with empty method settings
    """
    matrix = [
        [
            [2, 3, 1],
            [4, 5, 3],
            [6, 2, 1],
        ],
    ]
    types = [[1, -1, 1]]
    extensions = ['crisp']
    method = []
    params = [{}]

    response = client.post('/api/v1/results', headers={'locale': 'en'}, json={'matrix': matrix,'extensions': extensions,'types': types,'method': [method], 'params': [params]}, content_type='application/json')
    payload = json.loads(response.data.decode('utf-8'))

    assert response.status_code == 200
    assert type(payload) is dict

    assert 'method' in payload.keys()
    assert len(payload['method'][0]) == 0
    
    assert 'methodCorrelations' in payload.keys()
    assert len(payload['methodCorrelations']) == 0

    assert 'methodRankings' in payload.keys()
    assert len(payload['methodRankings']) == 0

    assert 'rankingCorrelations' in payload.keys()
    assert len(payload['rankingCorrelations']) == 0

def test_results_calculation_missing_mcda_method_field(client):
    """
        Test verifying the functionality of multi-criteria calculations for model structure with missing mcda method field
    """
    matrix = [
        [
            [2, 3, 1],
            [4, 5, 3],
            [6, 2, 1],
        ],
    ]
    types = [[1, -1, 1]]
    extensions = ['crisp']
    method = [
        {
            'weights': "ANGLE"
        }
    ]
    params = [{}]

    response = client.post('/api/v1/results', headers={'locale': 'en'}, json={'matrix': matrix,'extensions': extensions,'types': types,'method': [method], 'params': [params]}, content_type='application/json')
    payload = json.loads(response.data.decode('utf-8'))

    assert response.status_code == 400
    assert type(payload) is dict
    assert 'message' in payload.keys()
    assert 'method' in payload['message']

def test_results_calculation_empty_mcda_method_field(client):
    """
        Test verifying the functionality of multi-criteria calculations for model structure with empty mcda method field
    """
    matrix = [
        [
            [2, 3, 1],
            [4, 5, 3],
            [6, 2, 1],
        ],
    ]
    types = [[1, -1, 1]]
    extensions = ['crisp']
    method = [
        {
            'method': "",
            'weights': "ANGLE"
        }
    ]
    params = [{}]

    response = client.post('/api/v1/results', headers={'locale': 'en'}, json={'matrix': matrix,'extensions': extensions,'types': types,'method': [method], 'params': [params]}, content_type='application/json')
    payload = json.loads(response.data.decode('utf-8'))

    assert response.status_code == 400
    assert type(payload) is dict
    assert 'message' in payload.keys()
    assert 'method' in payload['message']

def test_results_calculation_unhandled_mcda_method(client):
    """
        Test verifying the functionality of multi-criteria calculations for model structure with unhandled mcda method in server functionalities
    """
    matrix = [
        [
            [2, 3, 1],
            [4, 5, 3],
            [6, 2, 1],
        ],
    ]
    types = [[1, -1, 1]]
    extensions = ['crisp']
    method = [
        {
            'method': "ABC",
            'weights': "ANGLE"
        }
    ]
    params = [{}]

    response = client.post('/api/v1/results', headers={'locale': 'en'}, json={'matrix': matrix,'extensions': extensions,'types': types,'method': [method], 'params': [params]}, content_type='application/json')
    payload = json.loads(response.data.decode('utf-8'))

    assert response.status_code == 400
    assert type(payload) is dict
    assert 'message' in payload.keys()
    assert 'method' in payload['message']

def test_results_calculation_multiple_method(client):
    """
        Test verifying the functionality of multi-criteria calculations for model structure with multiple assessment methods
    """
    matrix = [
        [
            [2, 3, 1],
            [4, 5, 3],
            [6, 2, 1],
        ],
    ]
    types = [[1, -1, 1]]
    extensions = ['crisp']
    method = [
        {
            'method': "TOPSIS",
            'weights': "ANGLE"
        },
        {
            'method': "MABAC",
            'weights': "ENTROPY"
        },
        {
            'method': "MOORA",
            'weights': "EQUAL"
        }
    ]
    params = [{}]

    response = client.post('/api/v1/results', headers={'locale': 'en'}, json={'matrix': matrix,'extensions': extensions,'types': types,'method': [method], 'params': [params]}, content_type='application/json')
    payload = json.loads(response.data.decode('utf-8'))

    assert response.status_code == 200
    assert type(payload) is dict

    assert 'method' in payload.keys()
    assert len(payload['method'][0]) == 3
    assert 'method' in payload['method'][0][0].keys()
    assert 'preference' in payload['method'][0][0].keys()
    assert 'weights' in payload['method'][0][0].keys()
    assert 'weights_value' in payload['method'][0][0].keys()
    assert 'extension' in payload['method'][0][0].keys()
    assert 'additional' in payload['method'][0][0].keys()
    
    assert 'methodCorrelations' in payload.keys()
    assert len(payload['methodCorrelations']) == 0

    assert 'methodRankings' in payload.keys()
    assert len(payload['methodRankings']) == 0

    assert 'rankingCorrelations' in payload.keys()
    assert len(payload['rankingCorrelations']) == 0

def test_results_calculation_multiple_method_with_params(client):
    """
        Test verifying the functionality of multi-criteria calculations for model structure with multiple assessment methods with params
    """
    matrix = [
        [
            [2, 3, 1],
            [4, 5, 3],
            [6, 2, 1],
        ],
    ]
    types = [[1, -1, 1]]
    extensions = ['crisp']
    method = [
        {
            'method': "TOPSIS",
            'weights': "ANGLE"
        },
        {
            'method': "MABAC",
            'weights': "ENTROPY"
        },
        {
            'method': "MOORA",
            'weights': "EQUAL"
        }
    ]
    params = [
        {
            'extension': 'crisp',
            'additional': {
                'normalization_function': "linear_normalization"
            },
            "method": "TOPSIS"
        }
    ]

    response = client.post('/api/v1/results', headers={'locale': 'en'}, json={'matrix': matrix,'extensions': extensions,'types': types,'method': [method], 'params': [params]}, content_type='application/json')
    payload = json.loads(response.data.decode('utf-8'))

    assert response.status_code == 200
    assert type(payload) is dict

    assert 'method' in payload.keys()
    assert len(payload['method'][0]) == 3
    assert 'method' in payload['method'][0][0].keys()
    assert 'preference' in payload['method'][0][0].keys()
    assert 'weights' in payload['method'][0][0].keys()
    assert 'weights_value' in payload['method'][0][0].keys()
    assert 'extension' in payload['method'][0][0].keys()
    assert 'additional' in payload['method'][0][0].keys()
    assert payload['method'][0][0]['additional']['normalization_function'] == 'linear_normalization'
    
    assert 'methodCorrelations' in payload.keys()
    assert len(payload['methodCorrelations']) == 0

    assert 'methodRankings' in payload.keys()
    assert len(payload['methodRankings']) == 0

    assert 'rankingCorrelations' in payload.keys()
    assert len(payload['rankingCorrelations']) == 0

def test_results_calculation_multiple_method_with_wrong_params_method(client):
    """
        Test verifying the functionality of multi-criteria calculations for model structure with multiple assessment methods with params and mcda method given in the wrong order
    """
    matrix = [
        [
            [2, 3, 1],
            [4, 5, 3],
            [6, 2, 1],
        ],
    ]
    types = [[1, -1, 1]]
    extensions = ['crisp']
    method = [
        {
            'method': "TOPSIS",
            'weights': "ANGLE"
        },
        {
            'method': "MABAC",
            'weights': "ENTROPY"
        },
        {
            'method': "MOORA",
            'weights': "EQUAL"
        }
    ]
    params = [
        {
            'extension': 'crisp',
            'additional': {
                'normalization_function': "linear_normalization"
            },
            "method": "MABAC"
        }
    ]

    response = client.post('/api/v1/results', headers={'locale': 'en'}, json={'matrix': matrix,'extensions': extensions,'types': types,'method': [method], 'params': [params]}, content_type='application/json')
    payload = json.loads(response.data.decode('utf-8'))

    assert response.status_code == 200
    assert type(payload) is dict

    assert 'method' in payload.keys()
    assert len(payload['method'][0]) == 3
    assert 'method' in payload['method'][0][0].keys()
    assert 'preference' in payload['method'][0][0].keys()
    assert 'weights' in payload['method'][0][0].keys()
    assert 'weights_value' in payload['method'][0][0].keys()
    assert 'extension' in payload['method'][0][0].keys()
    assert 'additional' in payload['method'][0][0].keys()
    assert 'normalization_function' not in payload['method'][0][0]['additional']
    
    assert 'methodCorrelations' in payload.keys()
    assert len(payload['methodCorrelations']) == 0

    assert 'methodRankings' in payload.keys()
    assert len(payload['methodRankings']) == 0

    assert 'rankingCorrelations' in payload.keys()
    assert len(payload['rankingCorrelations']) == 0

def test_results_calculation_multiple_method_with_wrong_additional_params_function(client):
    """
        Test verifying the functionality of multi-criteria calculations for model structure with multiple assessment methods with params and wrong function given in additional methods
    """
    matrix = [
        [
            [2, 3, 1],
            [4, 5, 3],
            [6, 2, 1],
        ],
    ]
    types = [[1, -1, 1]]
    extensions = ['crisp']
    method = [
        {
            'method': "TOPSIS",
            'weights': "ANGLE"
        },
        {
            'method': "MABAC",
            'weights': "ENTROPY"
        },
        {
            'method': "MOORA",
            'weights': "EQUAL"
        }
    ]
    params = [
        {
            'extension': 'crisp',
            'additional': {
                'bad_function': "linear_normalization"
            },
            "method": "TOPSIS"
        }
    ]

    response = client.post('/api/v1/results', headers={'locale': 'en'}, json={'matrix': matrix,'extensions': extensions,'types': types,'method': [method], 'params': [params]}, content_type='application/json')
    payload = json.loads(response.data.decode('utf-8'))

    assert response.status_code == 400
    assert type(payload) is dict
    assert 'message' in payload.keys()

def test_results_calculation_multiple_method_with_wrong_additional_params_function_method(client):
    """
        Test verifying the functionality of multi-criteria calculations for model structure with multiple assessment methods with params and wrong method for function given in additional methods
    """
    matrix = [
        [
            [2, 3, 1],
            [4, 5, 3],
            [6, 2, 1],
        ],
    ]
    types = [[1, -1, 1]]
    extensions = ['crisp']
    method = [
        {
            'method': "TOPSIS",
            'weights': "ANGLE"
        },
        {
            'method': "MABAC",
            'weights': "ENTROPY"
        },
        {
            'method': "MOORA",
            'weights': "EQUAL"
        }
    ]
    params = [
        {
            'extension': 'crisp',
            'additional': {
                'normalization_function': "bad method"
            },
            "method": "TOPSIS"
        }
    ]

    response = client.post('/api/v1/results', headers={'locale': 'en'}, json={'matrix': matrix,'extensions': extensions,'types': types,'method': [method], 'params': [params]}, content_type='application/json')
    payload = json.loads(response.data.decode('utf-8'))

    assert response.status_code == 400
    assert type(payload) is dict
    assert 'message' in payload.keys()

def test_results_calculation_wrong_fuzzy_matrix(client):
    """
        Test verifying the functionality of multi-criteria calculations for model structure with badly formatted fuzzy matrix
    """
    matrix = [
        [
            [2, 3, 1],
            [4, 5, 3],
            [6, 2, 1],
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

    assert response.status_code == 400
    assert type(payload) is dict
    assert 'message' in payload.keys()

def test_results_calculation_fuzzy_matrix(client):
    """
        Test verifying the functionality of multi-criteria calculations for model structure with correctly formatted fuzzy matrix
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

    assert 'method' in payload.keys()
    assert len(payload['method'][0]) == 1
    assert 'method' in payload['method'][0][0].keys()
    assert 'preference' in payload['method'][0][0].keys()
    assert 'weights' in payload['method'][0][0].keys()
    assert 'weights_value' in payload['method'][0][0].keys()
    assert 'extension' in payload['method'][0][0].keys()
    assert 'additional' in payload['method'][0][0].keys()
    
    assert 'methodCorrelations' in payload.keys()
    assert len(payload['methodCorrelations']) == 0

    assert 'methodRankings' in payload.keys()
    assert len(payload['methodRankings']) == 0

    assert 'rankingCorrelations' in payload.keys()
    assert len(payload['rankingCorrelations']) == 0

def test_results_calculation_ranking(client):
    """
        Test verifying the functionality of multi-criteria calculations for model structure with mcda method and ranking calculation
    """
    matrix = [
        [
            [2, 3, 1],
            [4, 5, 3],
            [6, 2, 1],
        ],
    ]
    types = [[1, -1, 1]]
    extensions = ['crisp']
    method = [
        {
            'method': "TOPSIS",
            'weights': "ANGLE"
        }
    ]
    params = [{}]
    methodRankings = [
        [
            {
                'data': [
                    {
                        'method': 'aras',
                        'weights': 'angle', 
                        'order': 'descending', 
                        'ranking': True
                    }
                ]
            }
        ]
    ]

    response = client.post('/api/v1/results', headers={'locale': 'en'}, json={'matrix': matrix,'extensions': extensions,'types': types,'method': [method], 'params': [params], 'methodRankings': methodRankings}, content_type='application/json')
    payload = json.loads(response.data.decode('utf-8'))

    assert response.status_code == 200
    assert type(payload) is dict
    
    assert 'method' in payload.keys()
    assert len(payload['method'][0]) == 1
    assert 'method' in payload['method'][0][0].keys()
    assert 'preference' in payload['method'][0][0].keys()
    assert 'weights' in payload['method'][0][0].keys()
    assert 'weights_value' in payload['method'][0][0].keys()
    assert 'extension' in payload['method'][0][0].keys()
    assert 'additional' in payload['method'][0][0].keys()
    
    assert 'methodCorrelations' in payload.keys()
    assert len(payload['methodCorrelations']) == 0

    assert 'methodRankings' in payload.keys()
    assert len(payload['methodRankings']) == 1

    assert 'rankingCorrelations' in payload.keys()
    assert len(payload['rankingCorrelations']) == 0

def test_results_calculation_methods_correlation(client):
    """
        Test verifying the functionality of multi-criteria calculations for model structure with mcda methods and correlation between their results
    """
    matrix = [
        [
            [2, 3, 1],
            [4, 5, 3],
            [6, 2, 1],
        ],
    ]
    types = [[1, -1, 1]]
    extensions = ['crisp']
    method = [
        {
            'method': "TOPSIS",
            'weights': "ANGLE"
        },
        {
            'method': "TOPSIS",
            "weights": "ENTROPY"
        }
    ]
    params = [{}]
    methodCorrelations = [
        [
            {
                'correlation': "pearson",
                'data': [
                    {
                        'method': "TOPSIS",
                        "weights": "ANGLE",
                        "correlation": True
                    },
                    {
                        'method': "TOPSIS",
                        "weights": "ENTROPY",
                        "correlation": True
                    }
                ]
            }
        ]
    ]

    response = client.post('/api/v1/results', headers={'locale': 'en'}, json={'matrix': matrix,'extensions': extensions,'types': types,'method': [method], 'params': [params], 'methodCorrelations': methodCorrelations}, content_type='application/json')
    payload = json.loads(response.data.decode('utf-8'))

    assert response.status_code == 200
    assert type(payload) is dict
    
    assert 'method' in payload.keys()
    assert len(payload['method'][0]) == 2
    assert 'method' in payload['method'][0][0].keys()
    assert 'preference' in payload['method'][0][0].keys()
    assert 'weights' in payload['method'][0][0].keys()
    assert 'weights_value' in payload['method'][0][0].keys()
    assert 'extension' in payload['method'][0][0].keys()
    assert 'additional' in payload['method'][0][0].keys()
    
    assert 'methodCorrelations' in payload.keys()
    assert len(payload['methodCorrelations']) == 1
    assert len(payload['methodCorrelations'][0]) == 1
    assert payload['methodCorrelations'][0][0]['correlation'] == 'PEARSON'
    assert len(payload['methodCorrelations'][0][0]['results']) == 2
    assert len(payload['methodCorrelations'][0][0]['results'][0]) == 2

    assert 'methodRankings' in payload.keys()
    assert len(payload['methodRankings']) == 0

    assert 'rankingCorrelations' in payload.keys()
    assert len(payload['rankingCorrelations']) == 0

def test_results_calculation_methods_ranking_correlation(client):
    """
        Test verifying the functionality of multi-criteria calculations for model structure with mcda methods and correlation between the rankings established based on the preference values
    """
    matrix = [
        [
            [2, 3, 1],
            [4, 5, 3],
            [6, 2, 1],
        ],
    ]
    types = [[1, -1, 1]]
    extensions = ['crisp']
    method = [
        {
            'method': "TOPSIS",
            'weights': "ANGLE"
        },
        {
            'method': "TOPSIS",
            "weights": "ENTROPY"
        }
    ]
    params = [{}]
    methodRankings = [
        [
            {
                'data': [
                    {
                        'method': 'TOPSIS',
                        'weights': 'ANGLE', 
                        'order': 'descending', 
                        'ranking': True
                    },
                    {
                        'method': 'TOPSIS',
                        'weights': 'ENTROPY', 
                        'order': 'descending', 
                        'ranking': True
                    },
                ]
            }
        ]
    ]
    rankingCorrelations = [
        [
            {
                'correlation': "ws rank similarity",
                'data': [
                    {
                        'method': "TOPSIS",
                        "weights": "ANGLE",
                        "correlation": True
                    },
                    {
                        'method': "TOPSIS",
                        "weights": "ENTROPY",
                        "correlation": True
                    }
                ]
            }
        ]
    ]

    response = client.post('/api/v1/results', headers={'locale': 'en'}, json={'matrix': matrix,'extensions': extensions,'types': types,'method': [method], 'params': [params], 'methodRankings': methodRankings, 'rankingCorrelations': rankingCorrelations}, content_type='application/json')
    payload = json.loads(response.data.decode('utf-8'))

    assert response.status_code == 200
    assert type(payload) is dict
    
    assert 'method' in payload.keys()
    assert len(payload['method'][0]) == 2
    assert 'method' in payload['method'][0][0].keys()
    assert 'preference' in payload['method'][0][0].keys()
    assert 'weights' in payload['method'][0][0].keys()
    assert 'weights_value' in payload['method'][0][0].keys()
    assert 'extension' in payload['method'][0][0].keys()
    assert 'additional' in payload['method'][0][0].keys()
    
    assert 'methodCorrelations' in payload.keys()
    assert len(payload['methodCorrelations']) == 0

    assert 'methodRankings' in payload.keys()
    assert len(payload['methodRankings']) == 1
    assert len(payload['methodRankings'][0][0]) == 2
    assert len(payload['methodRankings'][0][0][0]['ranking']) == 3
    assert payload['methodRankings'][0][0][0]['methods']['method'] == 'TOPSIS'
    assert payload['methodRankings'][0][0][0]['methods']['weights'] == 'ANGLE'
    assert payload['methodRankings'][0][0][0]['methods']['ranking'] == True

    assert 'rankingCorrelations' in payload.keys()
    assert len(payload['rankingCorrelations']) == 1
    assert len(payload['rankingCorrelations'][0]) == 1
    assert payload['rankingCorrelations'][0][0]['correlation'] == 'WS RANK SIMILARITY'
    assert len(payload['rankingCorrelations'][0][0]['results']) == 2
    assert payload['rankingCorrelations'][0][0]['methods'][0]['method'] == 'TOPSIS'
    assert payload['rankingCorrelations'][0][0]['methods'][0]['weights'] == 'ANGLE'
    assert payload['rankingCorrelations'][0][0]['methods'][1]['method'] == 'TOPSIS'
    assert payload['rankingCorrelations'][0][0]['methods'][1]['weights'] == 'ENTROPY'
