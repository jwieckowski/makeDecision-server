# Copyright (C) Jakub Więckowski 2023

import numpy as np
import pymcdm
import pyfdm
from pymcdm.methods import COMET, TOPSIS, SPOTIS
from pymcdm.methods.comet_tools import MethodExpert, ESPExpert, CompromiseExpert

# UTILS
# from utils.errors import get_error_message

# FOR ADDITIONAL PARAMETERS FOR FUZZY MCDA METHODS
@staticmethod
def get_fuzzy_parameters(locale, kwargs, check_normalization=False, check_distance=False, check_defuzzify=False, check_distance_1=False, check_distance_2=False):
    """
        Retrieves additional parameters for given fuzzy MCDA method

        Parameters
        ----------
            locale : string
                User application language

            kwargs: 
                TODO

            check_normalization : bool, default=False
                Flag determining if normalization parameter should be retrieve

            check_distance : bool, default=False
                Flag determining if distance parameter should be retrieve
            
            check_defuzzify : bool, default=False
                Flag determining if defuzzify parameter should be retrieve
            
            check_distance_1 : bool, default=False
                Flag determining if distance_1 parameter should be retrieve
            
            check_distance_2 : bool, default=False
                Flag determining if distance_2 parameter should be retrieve
            
        Raises
        -------
            ValueError Exception
                If error in occurs in retrieving the additional data of MCDA parameter, the exception is thrown
        
        Returns
        -------
            dictionary
                Dictionary with additional parameters for given fuzzy MCDA method
    """

    
    
    kwargs = {}

    try:

        pass
        # # CHECK IF KEY IN AVAILABLE PARAMS
        # additional_keys = list(params['additional'].keys())
        # for key in additional_keys:
        #     if key not in ['normalization', 'distance', 'defuzzify', 'distance_1', 'distance_2']:
        #         raise ValueError(f'{get_error_message(locale, "additional-function-error")} {key}')
        
        # # ASSIGN MEASURES SELECTED BY USER TO DICTIONARY 
        # if mcda_method == params['method'].upper() and params['extension'].lower() == 'fuzzy' and len(list(params['additional'].keys())) != 0:
            
        #     if check_normalization == True and 'normalization' in list(params['additional'].keys()):
        #         try:
        #             normalization = getattr(pyfdm.methods.fuzzy_sets.tfn.normalizations, params['additional']['normalization'])
        #             kwargs['normalization'] = normalization
        #         except:
        #             raise ValueError(f'{params["additional"]["normalization"]} {get_error_message(locale, "fuzzy-normalization-method-error")}')

        #     if check_distance == True and 'distance' in list(params['additional'].keys()):
        #         try:
        #             distance = getattr(pyfdm.methods.fuzzy_sets.tfn.distances, params['additional']['distance'])
        #             kwargs['distance'] = distance
        #         except:
        #             raise ValueError(f'{params["additional"]["distance"]} {get_error_message(locale, "fuzzy-distance-method-error")}')

        #     if check_defuzzify == True and 'defuzzify' in list(params['additional'].keys()):
        #         try:
        #             defuzzify = getattr(pyfdm.methods.fuzzy_sets.tfn.defuzzifications, params['additional']['defuzzify'])
        #             kwargs['defuzzify'] = defuzzify
        #         except:
        #             raise ValueError(f'{params["additional"]["defuzzify"]} {get_error_message(locale, "fuzzy-defuzzification-method-error")}')

        #     if check_distance_1 == True and 'distance_1' in list(params['additional'].keys()):
        #         try:
        #             distance_1 = getattr(pyfdm.methods.fuzzy_sets.tfn.distances, params['additional']['distance_1'])
        #             kwargs['distance_1'] = distance_1
        #         except:
        #             raise ValueError(f'{params["additional"]["distance_1"]} {get_error_message(locale, "fuzzy-distance-method-error")}')

        #     if check_distance_2 == True and 'distance_2' in list(params['additional'].keys()): 
        #         try:
        #             distance_2 = getattr(pyfdm.methods.fuzzy_sets.tfn.distances, params['additional']['distance_2'])
        #             kwargs['distance_2'] = distance_2
        #         except:
        #             raise ValueError(f'{params["additional"]["distance_2"]} {get_error_message(locale, "fuzzy-distance-method-error")}')
        
        # # ASSIGN DEFAULT METRICS FOR MCDA METHODS IF NOT GIVEN BY USER
        # elif mcda_method == params['method'].upper() and params['extension'].lower() == 'fuzzy':
        #     if check_normalization == True:
        #         kwargs['normalization'] = getattr(pyfdm.methods.fuzzy_sets.tfn.normalizations, fuzzy_methods_default_metrics[mcda_method.upper()]['normalization'])
        #     if check_distance == True:
        #         kwargs['distance'] = getattr(pyfdm.methods.fuzzy_sets.tfn.distances, fuzzy_methods_default_metrics[mcda_method.upper()]['distance'])
        #     if check_defuzzify == True:
        #         kwargs['defuzzify'] = getattr(pyfdm.methods.fuzzy_sets.tfn.defuzzifications, fuzzy_methods_default_metrics[mcda_method.upper()]['defuzzify'])
        #     if check_distance_1 == True:
        #         kwargs['distance_1'] = getattr(pyfdm.methods.fuzzy_sets.tfn.distances, fuzzy_methods_default_metrics[mcda_method.upper()]['distance_1'])
        #     if check_distance_2 == True:
        #         kwargs['distance_2'] = getattr(pyfdm.methods.fuzzy_sets.tfn.distances, fuzzy_methods_default_metrics[mcda_method.upper()]['distance_2'])

        return kwargs
    except Exception as err:
        raise ValueError(err)


# FOR ADDITIONAL PARAMETERS FOR CRISP MCDA METHODS
def get_crisp_parameters(kwargs, matrix_node, criteria_weights):
    """
        Retrieves additional parameters for given crisp MCDA method

        Parameters
        ----------
            locale : string
                User application language

            kwargs:
                TODO

            check_normalization_function : bool, default=False
                Flag determining if normalization parameter should be retrieve

            check_preference_function : bool, default=False
                Flag determining if preference function parameter should be retrieve
            
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
                init_kwargs[key] = np.array(value)
            elif key == 'expert_function':
                if value == 'method_expert':
                    expert_function = MethodExpert(TOPSIS(), criteria_weights, matrix_node.criteria_types)
                    init_kwargs[key] = expert_function

                elif value == 'esp_expert':
                    if 'esp' not in list(kwargs.keys()):
                        raise ValueError("Missing key 'esp' for the COMET method for the ESP Expert variant")
                    
                    bounds = SPOTIS.make_bounds(matrix_node.matrix)
                    # esps = np.array([[0.4, 0.4]])
                    esps = np.array(kwargs['esp'])
                    
                    expert_function = ESPExpert(esps, bounds, cvalues_psi=None)
                    init_kwargs[key] = expert_function

                elif value == 'compromise_expert':
                    topsis = TOPSIS()
                    evaluation_function = [
                            lambda co: topsis(co, np.array([0.2, 0.3, 0.5]), matrix_node.criteria_types),
                            lambda co: topsis(co, np.array([0.3, 0.4, 0.3]), matrix_node.criteria_types),
                            lambda co: topsis(co, np.array([0.1, 0.5, 0.4]), matrix_node.criteria_types),
                            ]

                    expert_function = CompromiseExpert(evaluation_function)
                    init_kwargs[key] = expert_function
            # ERVD
            elif key == 'ref_point':
                init_kwargs[key] = np.array(value)
            elif key == 'lam':
                init_kwargs[key] = float(value)
            elif key == 'alpha':
                init_kwargs[key] = float(value)
            # PROBID
            elif key == 'sPROBID':
                init_kwargs[key] = value
            # PROMETHEE
            elif key == 'preference_function':
                init_kwargs[key] = getattr(pymcdm.methods.PROMETHEE_II._PreferenceFunctions, value)
            # RIM
            elif key == 'bounds':
                init_kwargs[key] = np.array(value)
            elif key == 'ref_ideal':
                init_kwargs[key] = np.array(value)
            # SPOTIS
            elif key == 'esp':
                if 'expert_function' not in kwargs.keys():
                    init_kwargs[key] = np.array(value)

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
            pass

    return init_kwargs
