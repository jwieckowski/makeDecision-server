import pymcdm.methods as crisp_methods
import pyfdm.methods as fuzzy_methods
import numpy as np

mcda_methods = {
    'ARAS': {
        'crisp': crisp_methods.ARAS,
        'fuzzy': fuzzy_methods.fARAS
    },
    'COCOSO': {
        'crisp': crisp_methods.COCOSO
    },
    'CODAS': {
        'crisp': crisp_methods.CODAS,
        'fuzzy': fuzzy_methods.fCODAS
    },
    'COMET': {
        'crisp': crisp_methods.COMET
    },
    'COPRAS': {
        'crisp': crisp_methods.COPRAS,
        'fuzzy': fuzzy_methods.fCOPRAS
    },
    'EDAS': {
        'crisp': crisp_methods.EDAS,
        'fuzzy': fuzzy_methods.fEDAS
    },
    'ERVD': {
        'crisp': crisp_methods.ERVD,
    },
    'INPUT': {},
    'MABAC': {
        'crisp': crisp_methods.MABAC,
        'fuzzy': fuzzy_methods.fMABAC
    },
    'MAIRCA': {
        'crisp': crisp_methods.MAIRCA,
        'fuzzy': fuzzy_methods.fMAIRCA
    },
    'MARCOS': {
        'crisp': crisp_methods.MARCOS
    },
    'MOORA': {
        'crisp': crisp_methods.MOORA,
        'fuzzy': fuzzy_methods.fMOORA
    },
    'OCRA': {
        'crisp': crisp_methods.OCRA,
        'fuzzy': fuzzy_methods.fOCRA
    },
    'PROBID': {
        'crisp': crisp_methods.PROBID,
    },
    'PROMETHEE': {
        'crisp': crisp_methods.PROMETHEE_II
    },
    'RIM': {
        'crisp': crisp_methods.RIM,
    },
    'SPOTIS': {
        'crisp': crisp_methods.SPOTIS
    },
    'TOPSIS': {
        'crisp': crisp_methods.TOPSIS,
        'fuzzy': fuzzy_methods.fTOPSIS
    },
    'VIKOR': {
        'crisp': crisp_methods.VIKOR,
        'fuzzy': fuzzy_methods.fVIKOR
    },
    "WASPAS": {
        'crisp': crisp_methods.WASPAS
    },
    'WPM': {
        'crisp': crisp_methods.WPM,
    },
    'WSM': {
        'crisp': crisp_methods.WSM,
    }
}

crisp_methods_default_metrics = {
    'ARAS': {
        'normalization_function': 'sum_normalization'
    },
    'COCOSO': {
        'normalization_function': 'minmax_normalization',
    },
    'CODAS': {
        'normalization_function': 'linear_normalization',
    },
    'COMET': {
        'cvalues': np.array([]),
        'expert_function': 'method_expert',
    },
    'ERVD': {
        'ref_point': None,
        'lam': 2.25,
        'alpha': 0.88
    },
    'MABAC': {
        'normalization_function': 'minmax_normalization',
    },
    'MAIRCA': {
        'normalization_function': 'minmax_normalization',
    },
    'MARCOS': {
        'normalization_function': 'sum_normalization'
    },
    'OCRA': {
        'normalization_function': 'sum_normalization'
    },
    'PROBID': {
        'sPROBID': False
    },
    'PROMETHEE': {
        'preference_function': 'usual',
        'p': None,
        'q': None
    },
    'RIM': {
        'bounds': np.array([]),
        'ref_ideal': None
    },
    'SPOTIS': {
        'bounds': np.array([]),
        'esp': None
    },
    'TOPSIS': {
        'normalization_function': 'minmax_normalization',
    },
    'VIKOR': {
        'normalization_function': "sum_normalization"
    },
    'WASPAS': {
        'normalization_function': 'linear_normalization'
    },
    'WPM': {
        'normalization_function': "sum_normalization"
    },
    'WSM': {
        'normalization_function': "sum_normalization"
    }
}

fuzzy_methods_default_metrics = {
    'ARAS': {
        'normalization': 'sum_normalization'
    },
    'CODAS': {
        'normalization': 'max_normalization',
        'distance_1': 'euclidean_distance',
        'distance_2': 'hamming_distance'
    },
    'COPRAS': {
        'normalization': "saw_normalization"
    },
    'EDAS': {
        'defuzzify': 'mean_defuzzification'
    },
    'MABAC': {
        'normalization': 'minmax_normalization',
        'defuzzify': 'mean_defuzzification'
    },
    'MAIRCA': {
        'normalization': 'vector_normalization',
        'distance': 'vertex_distance'
    },
    'MOORA': {
        'normalization': 'vector_normalization'
    },
    'OCRA': {
        'defuzzification': 'mean_defuzzification'
    },
    'TOPSIS': {
        'normalization': 'linear_normalization',
        'distance': 'vertex_distance'
    },
    'VIKOR': {
        'defuzzify': "mean_area_defuzzification"
    }
}