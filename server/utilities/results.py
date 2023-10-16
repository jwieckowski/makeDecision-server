from werkzeug.exceptions import BadRequest
import numpy as np

# UTILS
from utilities.interface import Calculations
from utilities.validator import Validator

def preprocess_input_data(matrix, extension, locale, types):
    inputMatrix = None
    inputTypes = types
    
    # random
    if np.array(matrix).ndim == 1 and len(matrix) == 2:
        inputMatrix = Calculations.generate_random_matrix(locale, matrix[0], matrix[1], extension)
    
    # input
    else:

        temp_matrix = matrix
        # fuzzy
        if isinstance(matrix[0][0], str):
            temp_matrix = [[[float(c.replace(',', '')) for c in col.split(',')] for col in row] for row in matrix]

        inputMatrix = np.array(temp_matrix, dtype=float)
        
        try:
            Validator.validate_matrix(locale, inputMatrix, extension)
        except Exception as err:
            raise ValueError(err)

        try:
            Validator.validate_types(locale, types)
        except Exception as err:
            raise ValueError(err)

        try:
            Validator.validate_dimensions(locale, inputMatrix, types)
        except Exception as err:
            raise ValueError(err)
    
    return inputMatrix, inputTypes

def get_calculation_results(matrices, extensions, types, method, params, methodCorrelations, methodRankings, rankingCorrelations, locale):
    results = {
        'matrices': [], 
        'method': [],
        'methodCorrelations': [],
        'methodRankings': [],
        'rankingCorrelations': [],
    }

    try:
        results['matrices'] = [matrix.tolist() for matrix in matrices]
        results['method'] = Calculations.calculate_preferences(locale, matrices, extensions, types, method, params)
        
        if methodCorrelations and len(methodCorrelations) > 0:
            results['methodCorrelations'] = Calculations.calculate_preference_correlations(locale, methodCorrelations, results['method'])

        if methodRankings and len(methodRankings) > 0:
            results['methodRankings'] = Calculations.calculate_ranking(locale, methodRankings, results['method'])
        
        if rankingCorrelations and len(rankingCorrelations) > 0:
            results['rankingCorrelations'] = Calculations.calculate_ranking_correlations(locale, rankingCorrelations, results['methodRankings'])
        
        return results
    except Exception as err:
        e = BadRequest(str(err))
        raise e