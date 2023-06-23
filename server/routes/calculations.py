from flask import request, jsonify
from __main__ import app

# from flask_expects_json import expects_json

import numpy as np

from utilities.interface import Calculations
from utilities.validator import Validator 
from utilities.files import Files

# CALCULATIONS
@app.route('/api/v1/results', methods=['POST'])
def calculation_results():

    data = request.get_json()
    matrixes = np.array(data['matrix'], dtype='object')
    extensions = np.array(data['extensions'])
    types = np.array(data['types'])
    method = np.array(data['method'])
    methodCorrelations = np.array(data['methodCorrelations'])
    methodRankings = np.array(data['methodRankings'])
    rankingCorrelations = np.array(data['rankingCorrelations'])

    calculationMatrixes = []
    calculationTypes = []
    # check if need to generate random matrix or process the data from file
    for idx, (m, ext) in enumerate(zip(matrixes, extensions)):
        # file
        if isinstance(m, str): 
            flag, a, b = Files.convert_file_to_matrix(m, ext)
            if flag == True:
                calculationMatrixes.append(a)
                calculationTypes.append(b)
            else:
                return a, 400
        # random
        elif np.array(m).ndim == 1 and len(m) == 2:
            calculationMatrixes.append(Calculations.generate_random_matrix(m[0], m[1], ext))
            calculationTypes.append(types[idx])
        # input
        else:
            # fuzzy
            if isinstance(m[0][0], str):
                fuzzy_matrix = [[[float(c.replace(',', '')) for c in col.split()] for col in row]for row in m]
                calculationMatrixes.append(np.array(fuzzy_matrix, dtype=float))
            # crisp
            else:
                calculationMatrixes.append(np.array(m, dtype=float))
            calculationTypes.append(types[idx])

    # verification of input data
    for m, ext in zip(calculationMatrixes, extensions):
        matrix_error = Validator.validate_matrix(m, ext)
        if matrix_error:
            return matrix_error, 400

    for m, t in zip(calculationMatrixes, calculationTypes):
        types_error = Validator.validate_types(t)
        if types_error:
            return types_error, 400

    # retrieve additional params for assessment
    try:
        params = np.array(data['params'])
    except:
        params = None
    
    for m, t in zip(calculationMatrixes, calculationTypes):
        dimension_error = Validator.validate_dimensions(m, t)
        if dimension_error:
            return dimension_error, 400

    results = {
        'matrices': [], 
        'method': [],
        'methodCorrelations': [],
        'methodRankings': [],
        'rankingCorrelations': []
    }

    if len(method) == 0:
        return jsonify(results)
        
    # return matrices
    results['matrices'] = [m.tolist() for m in calculationMatrixes]
    
    # MCDA evaluation
    try:
        results['method'] = Calculations.calculate_preferences(calculationMatrixes, extensions, calculationTypes, method, params)
    except Exception as e:
        calculation_error = {
            "error": e.args[0]
        }
        return jsonify(calculation_error), 400

    # MCDA preferences correlation
    if len(methodCorrelations) > 0:
        results['methodCorrelations'] = Calculations.calculate_preference_correlations(methodCorrelations, results['method'])

    # MCDA ranking calculation
    if len(methodRankings) > 0:
        results['methodRankings'] = Calculations.calculate_ranking(methodRankings, results['method'])

    # MCDA ranking correlation
    if len(rankingCorrelations) > 0:
        results['rankingCorrelations'] = Calculations.calculate_ranking_correlations(rankingCorrelations, results['methodRankings'])


    return jsonify(results)
