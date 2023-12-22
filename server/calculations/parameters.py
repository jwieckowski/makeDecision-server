# Copyright (C) Jakub Więckowski 2023

import numpy as np
import pymcdm
import pyfdm
from pymcdm.methods import TOPSIS, SPOTIS, COMET
from pymcdm.methods.comet_tools import MethodExpert, ESPExpert, CompromiseExpert
from pymcdm.weights import equal_weights, gini_weights, standard_deviation_weights

# UTILS
# from utils.errors import get_error_message

# FOR ADDITIONAL PARAMETERS FOR FUZZY MCDA METHODS
def get_fuzzy_parameters(kwargs):
    """
        Retrieves additional parameters for given fuzzy MCDA method

        Parameters
        ----------
            locale : string
                User application language

            kwargs: 
                TODO

        Raises
        -------
            ValueError Exception
                If error in occurs in retrieving the additional data of MCDA parameter, the exception is thrown
        
        Returns
        -------
            dictionary
                Dictionary with additional parameters for given fuzzy MCDA method
    """
    init_kwargs = {}

    try:
        for key, value in kwargs.items():
            if key == 'matrix_id': continue
            elif key == 'normalization':
                init_kwargs[key] = getattr(pyfdm.methods.utils.normalizations, value)
            elif key in ['distance', 'distance_1', 'distance_2']:
                init_kwargs[key] = getattr(pyfdm.methods.utils.distances, value)
            elif key == 'defuzzify':
                init_kwargs[key] = getattr(pyfdm.methods.utils.defuzzifications, value)

        return init_kwargs
    except Exception as err:
        raise ValueError(err)

def get_crisp_parameters(kwargs, matrix_node, criteria_weights):
    """
        Retrieves additional parameters for given crisp MCDA method

        Parameters
        ----------
            locale : string
                User application language

            kwargs:
                TODO

        Raises
        -------
            ValueError Exception
                If error in occurs in retrieving the additional data of MCDA parameter, the exception is thrown
        
        Returns
        -------
            dictionary
                Dictionary with additional parameters for given crisp MCDA method
    """


    init_kwargs = {}
    try:

        # TODO check keys if allowed
        for key, value in kwargs.items():
            if key == 'matrix_id': continue
            elif key == 'normalization_function':
                init_kwargs[key] = getattr(pymcdm.normalizations, value)
            # COMET
            elif key == 'cvalues':
                if value != '':
                    init_kwargs[key] = np.array(value, dtype=float)
                else:
                    init_kwargs[key] = COMET.make_cvalues(matrix_node.matrix)
            elif key == 'expert_function':
                if value == 'method_expert':
                    expert_function = MethodExpert(TOPSIS(), criteria_weights, matrix_node.criteria_types)
                    init_kwargs[key] = expert_function

                elif value == 'esp_expert':
                    if 'esp' not in list(kwargs.keys()):
                        raise ValueError("Missing key 'esp' for the COMET method for the ESP Expert variant")
                    
                    bounds = SPOTIS.make_bounds(matrix_node.matrix)
                    # esps = np.array([[0.4, 0.4]])
                    esps = np.array(kwargs['esp'], dtype=float)
                    
                    expert_function = ESPExpert(esps, bounds, cvalues_psi=None)
                    init_kwargs[key] = expert_function

                elif value == 'compromise_expert':
                    topsis = TOPSIS()
                    evaluation_function = [
                            lambda co: topsis(co, equal_weights(matrix_node.matrix), matrix_node.criteria_types),
                            lambda co: topsis(co, gini_weights(matrix_node.matrix), matrix_node.criteria_types),
                            lambda co: topsis(co, standard_deviation_weights(matrix_node.matrix), matrix_node.criteria_types),
                            ]

                    expert_function = CompromiseExpert(evaluation_function)
                    init_kwargs[key] = expert_function
            # ERVD
            elif key == 'ref_point':
                init_kwargs[key] = np.array(value, dtype=float)
            elif key == 'lam':
                init_kwargs[key] = float(value)
            elif key == 'alpha':
                init_kwargs[key] = float(value)
            # PROBID
            elif key == 'sPROBID':
                init_kwargs[key] = value
            # PROMETHEE
            elif key == 'preference_function':
                init_kwargs[key] = value
            elif key  == 'p' and value != '':
                init_kwargs[key] = np.array(value, dtype=float)
            elif key  == 'q' and value != '':
                init_kwargs[key] = np.array(value, dtype=float)
            # RIM
            elif key == 'bounds':
                temp_bounds = np.array(value, dtype=float)
                init_kwargs[key] = np.array([[l, u] for l, u in zip(temp_bounds[0], temp_bounds[1])])
            elif key == 'ref_ideal':
                init_kwargs[key] = np.array(value, dtype=float)
            # SPOTIS
            elif key == 'esp' and value != '':
                if 'expert_function' not in kwargs.keys():
                    init_kwargs[key] = np.array(value, dtype=float)
            # VIKOR
            elif key == 'v':
                init_kwargs[key] = float(value)

        return init_kwargs
    except Exception as err:
        raise ValueError(err)

# RETRIEVE METHOD NAME FROM FUNCTION NAME
def get_methods_name(locale, dict):
    """
        Gets name of MCDA methods

        Parameters
        ----------
            locale : string
                User application language

            dict: dictionary
                Dictionary with MCDA methods
        
        Returns
        -------
            dictionary
                Dictionary with MCDA methods names

    """
    try:
        names_dict = {}
        for key, val in dict.items():
            names_dict[key] = val.__name__
        return names_dict
    except Exception:
        pass
        # raise ValueError(f'{get_error_message(locale, "method-name-error")}')


def get_parameters(kwargs, extension, matrix_node, criteria_weights):

    init_kwargs = {}

    items = [item for item in kwargs if item['matrix_id'] == matrix_node.id]

    if len(items) > 0:

        if extension == 'crisp':
            init_kwargs = get_crisp_parameters(items[0], matrix_node, criteria_weights)
        elif extension == 'fuzzy':
            init_kwargs = get_fuzzy_parameters(items[0])

    return init_kwargs
