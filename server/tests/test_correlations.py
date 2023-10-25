# Copyright (c) 2023 Jakub Więckowski

from server import app
import json
import pytest

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_results_calculation_goodman_kruskall_correlation(client):
    """
        Test verifying the functionality of multi-criteria calculations for correlation of Goodman-Kruskall coefficient
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
                'correlation': "goodman-kruskall",
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
    assert payload['methodCorrelations'][0][0]['correlation'] == 'GOODMAN-KRUSKALL'
    assert len(payload['methodCorrelations'][0][0]['results']) == 2
    assert len(payload['methodCorrelations'][0][0]['results'][0]) == 2

    assert 'methodRankings' in payload.keys()
    assert len(payload['methodRankings']) == 0

    assert 'rankingCorrelations' in payload.keys()
    assert len(payload['rankingCorrelations']) == 0

def test_results_calculation_kendall_tau_correlation(client):
    """
        Test verifying the functionality of multi-criteria calculations for correlation of Kendall-Tau coefficient
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
                'correlation': "kendall-tau",
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
    assert payload['methodCorrelations'][0][0]['correlation'] == 'KENDALL-TAU'
    assert len(payload['methodCorrelations'][0][0]['results']) == 2
    assert len(payload['methodCorrelations'][0][0]['results'][0]) == 2

    assert 'methodRankings' in payload.keys()
    assert len(payload['methodRankings']) == 0

    assert 'rankingCorrelations' in payload.keys()
    assert len(payload['rankingCorrelations']) == 0

def test_results_calculation_pearson_correlation(client):
    """
        Test verifying the functionality of multi-criteria calculations for correlation of PEARSON coefficient
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

def test_results_calculation_spearman_correlation(client):
    """
        Test verifying the functionality of multi-criteria calculations for correlation of SPEARMAN coefficient
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
                'correlation': "spearman",
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
    assert payload['methodCorrelations'][0][0]['correlation'] == 'SPEARMAN'
    assert len(payload['methodCorrelations'][0][0]['results']) == 2
    assert len(payload['methodCorrelations'][0][0]['results'][0]) == 2

    assert 'methodRankings' in payload.keys()
    assert len(payload['methodRankings']) == 0

    assert 'rankingCorrelations' in payload.keys()
    assert len(payload['rankingCorrelations']) == 0

def test_results_calculation_weighted_spearman_ranking_correlation(client):
    """
        Test verifying the functionality of multi-criteria calculations for model structure with mcda methods and WEIGHTED SPEARMAN correlation between the rankings established based on the preference values
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
                'correlation': "weighted spearman",
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
    assert payload['rankingCorrelations'][0][0]['correlation'] == 'WEIGHTED SPEARMAN'
    assert len(payload['rankingCorrelations'][0][0]['results']) == 2
    assert payload['rankingCorrelations'][0][0]['methods'][0]['method'] == 'TOPSIS'
    assert payload['rankingCorrelations'][0][0]['methods'][0]['weights'] == 'ANGLE'
    assert payload['rankingCorrelations'][0][0]['methods'][1]['method'] == 'TOPSIS'
    assert payload['rankingCorrelations'][0][0]['methods'][1]['weights'] == 'ENTROPY'

def test_results_calculation_ws_rank_similarity_ranking_correlation(client):
    """
        Test verifying the functionality of multi-criteria calculations for model structure with mcda methods and WS RANK SIMILARITY correlation between the rankings established based on the preference values
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

def test_results_calculation_wrong_ranking_correlation(client):
    """
        Test verifying the functionality of multi-criteria calculations for model structure with mcda methods and wrong correlation method between the rankings established based on the preference values
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
                'correlation': "ABC",
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

    assert response.status_code == 400
    assert type(payload) is dict
    assert 'message' in payload.keys()
    