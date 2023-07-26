# Copyright (c) 2023 Jakub Więckowski

import numpy as np
import pymcdm
import pyfdm
import pymcdm.methods as crisp_methods
import pyfdm.methods as fuzzy_methods

from .weights import Weights
from ..validator import Validator
from ..errors import get_error_message

class Preferences():
    def __init__(self, matrixes, extensions, types):
        """
            Initializes the object with matrixes, extensions and criteria types from parametres

            Parameters
            ----------
                matrixes: ndarray
                    Vector of decision matrixes formatted as numpy arrays
                    
                extensions : ndarray
                    Vector of data extensions (crisp or fuzzy) represented as string
                
                types : ndarray
                    Vector of criteria types formatted as numpy arrays.

        """
        self.matrixes = matrixes
        self.extensions = extensions
        self.types = types

        self.mcda_methods = {
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
            'PROMETHEE': {
                'crisp': crisp_methods.PROMETHEE_II
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
            }
        }


    def calculate_preferences(self, locale, methods, params=None):
        """
            Calculates correlation of preferences values of data in matrix with given methods

            Parameters
            ----------
                locale : string
                    User application language

                methods : ndarray
                    Vector of dictionaries with MCDA method and weights method that are used in multi-criteria assessment

                params : ndarray, default=None
                    Vector of dictionaries with additional parameters that are used in the multi-criteria assessment, like methods normalization, defuzzification or distances
                
            Raises
            -------
                ValueError Exception
                    If the error in the multi-criteria assessment occurs, the exception is thrown
            
            Returns
            -------
                ndarray
                    Vector of dictionaries including the results from multi-criteria assessment 
        """
        # FOR ADDITIONAL PARAMETERS FOR FUZZY MCDA METHODS
        def _check_fuzzy_parameters(locale, mcda_method, matrix_idx, idx, check_normalization=False, check_distance=False, check_defuzzify=False, check_distance_1=False, check_distance_2=False):
            """
                Retrieves additional parameters for given fuzzy MCDA method

                Parameters
                ----------
                    locale : string
                        User application language

                    mcda_method : string
                        Name of MCDA method 

                    matrix_idx : int
                        Id of currently processed matrix
                    
                    idx : int
                        Id of currently processed method
                    
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

            methods_default_metrics = {
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
            
            try:
                kwargs = {}

                if params is not None and len(params[matrix_idx]) >= idx+1 and len(list(params[matrix_idx][idx].keys())) != 0:
                    additional_keys = list(params[matrix_idx][idx]['additional'].keys())
                    for key in additional_keys:
                        if key not in ['normalization', 'distance', 'defuzzify', 'distance_1', 'distance_2']:
                            raise ValueError(f'{get_error_message(locale, "additional-function-error")} {key}')
                    
                    if mcda_method == params[matrix_idx][idx]['method'].upper() and params[matrix_idx][idx]['extension'].lower() == 'fuzzy' and len(list(params[matrix_idx][idx]['additional'].keys())) != 0:
                        
                        if check_normalization == True and 'normalization' in list(params[matrix_idx][idx]['additional'].keys()):
                            try:
                                normalization = getattr(pyfdm.methods.fuzzy_sets.tfn.normalizations, params[matrix_idx][idx]['additional']['normalization'])
                                kwargs['normalization'] = normalization
                            except:
                                raise ValueError(f'{params[matrix_idx][idx]["additional"]["normalization"]} {get_error_message(locale, "fuzzy-normalization-method-error")}')

                        if check_distance == True and 'distance' in list(params[matrix_idx][idx]['additional'].keys()):
                            try:
                                distance = getattr(pyfdm.methods.fuzzy_sets.tfn.distances, params[matrix_idx][idx]['additional']['distance'])
                                kwargs['distance'] = distance
                            except:
                                raise ValueError(f'{params[matrix_idx][idx]["additional"]["distance"]} {get_error_message(locale, "fuzzy-distance-method-error")}')

                        if check_defuzzify == True and 'defuzzify' in list(params[matrix_idx][idx]['additional'].keys()):
                            try:
                                defuzzify = getattr(pyfdm.methods.fuzzy_sets.tfn.defuzzifications, params[matrix_idx][idx]['additional']['defuzzify'])
                                kwargs['defuzzify'] = defuzzify
                            except:
                                raise ValueError(f'{params[matrix_idx][idx]["additional"]["defuzzify"]} {get_error_message(locale, "fuzzy-defuzzification-method-error")}')

                        if check_distance_1 == True and 'distance_1' in list(params[matrix_idx][idx]['additional'].keys()):
                            try:
                                distance_1 = getattr(pyfdm.methods.fuzzy_sets.tfn.distances, params[matrix_idx][idx]['additional']['distance_1'])
                                kwargs['distance_1'] = distance_1
                            except:
                                raise ValueError(f'{params[matrix_idx][idx]["additional"]["distance_1"]} {get_error_message(locale, "fuzzy-distance-method-error")}')

                        if check_distance_2 == True and 'distance_2' in list(params[matrix_idx][idx]['additional'].keys()): 
                            try:
                                distance_2 = getattr(pyfdm.methods.fuzzy_sets.tfn.distances, params[matrix_idx][idx]['additional']['distance_2'])
                                kwargs['distance_2'] = distance_2
                            except:
                                raise ValueError(f'{params[matrix_idx][idx]["additional"]["distance_2"]} {get_error_message(locale, "fuzzy-distance-method-error")}')
                    
                    elif mcda_method == params[matrix_idx][idx]['method'].upper() and params[matrix_idx][idx]['extension'].lower() == 'fuzzy':
                        if check_normalization == True:
                            kwargs['normalization'] = getattr(pyfdm.methods.fuzzy_sets.tfn.normalizations, methods_default_metrics[mcda_method.upper()]['normalization'])
                        if check_distance == True:
                            kwargs['distance'] = getattr(pyfdm.methods.fuzzy_sets.tfn.distances, methods_default_metrics[mcda_method.upper()]['distance'])
                        if check_defuzzify == True:
                            kwargs['defuzzify'] = getattr(pyfdm.methods.fuzzy_sets.tfn.defuzzifications, methods_default_metrics[mcda_method.upper()]['defuzzify'])
                        if check_distance_1 == True:
                            kwargs['distance_1'] = getattr(pyfdm.methods.fuzzy_sets.tfn.distances, methods_default_metrics[mcda_method.upper()]['distance_1'])
                        if check_distance_2 == True:
                            kwargs['distance_2'] = getattr(pyfdm.methods.fuzzy_sets.tfn.distances, methods_default_metrics[mcda_method.upper()]['distance_2'])

                return kwargs
            except Exception as err:
                raise ValueError(err)

        # FOR ADDITIONAL PARAMETERS FOR CRISP MCDA METHODS
        def _check_crisp_parameters(locale, mcda_method, matrix_idx, idx, check_normalization_function=False, check_preference_function=False):
            """
                Retrieves additional parameters for given crisp MCDA method

                Parameters
                ----------
                    locale : string
                        User application language

                    mcda_method : string
                        Name of MCDA method 

                    matrix_idx : int
                        Id of currently processed matrix
                    
                    idx : int
                        Id of currently processed method
                    
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

            methods_default_metrics = {
                'ARAS': {
                    'normalization_function': 'sum_normalization'
                },
                'COCOSO': {
                    'normalization_function': 'minmax_normalization',
                },
                'CODAS': {
                    'normalization_function': 'linear_normalization',
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
                'PROMETHEE': {
                    'preference_function': 'usual'
                },
                'TOPSIS': {
                    'normalization_function': 'minmax_normalization',
                },
                'VIKOR': {
                    'normalization_function': "sum_normalization"
                }
            }

            try:
                kwargs = {}
                if params is not None and len(params[matrix_idx]) >= idx+1 and len(list(params[matrix_idx][idx].keys())) != 0:
                    additional_keys = list(params[matrix_idx][idx]['additional'].keys())
                    for key in additional_keys:
                        if key not in ['normalization_function', 'preference_function']:
                            raise ValueError(f'{get_error_message(locale, "additional-function-error")} {key}')
                    
                    if mcda_method == params[matrix_idx][idx]['method'].upper() and params[matrix_idx][idx]['extension'] == 'crisp' and len(list(params[matrix_idx][idx]['additional'].keys())) != 0:
                        if check_normalization_function == True and 'normalization_function' in list(params[matrix_idx][idx]['additional'].keys()):
                            try:
                                normalization = getattr(pymcdm.normalizations, params[matrix_idx][idx]['additional']['normalization_function'])
                                kwargs['normalization_function'] = normalization
                            except:
                                raise ValueError(f'{params[matrix_idx][idx]["additional"]["normalization_function"]} {get_error_message(locale, "crisp-normalization-method-error")}')
                        elif check_normalization_function == True:
                            kwargs = {'normalization_function': getattr(pymcdm.normalizations, 'sum_normalization')}

                        if check_preference_function == True and 'preference_function' in list(params[matrix_idx][idx]['additional'].keys()):
                            pref_fun = params[matrix_idx][idx]['additional']['preference_function'] 
                            if pref_fun in ['usual', 'ushape', 'vshape', 'level', 'vshape_2']:
                                kwargs['preference_function'] = pref_fun
                            else:
                                raise ValueError(f'{params[matrix_idx][idx]["additional"]["preference_function"]} {get_error_message(locale, "crisp-preference-function-error")}')
                        elif check_preference_function == True:
                            kwargs['preference_function'] = 'usual'

                    # DEFAULT METRICS
                    elif mcda_method == params[matrix_idx][idx]['method'].upper() and params[matrix_idx][idx]['extension'] == 'crisp':
                        if check_normalization_function == True:
                            kwargs['normalization_function'] = getattr(pymcdm.normalizations, methods_default_metrics[mcda_method.upper()]['normalization_function'])
                        if check_preference_function == True:
                            kwargs['preference_function'] = methods_default_metrics[mcda_method.upper()]['preference_function']
                
                return kwargs
            except Exception as err:
                raise ValueError(err)

        # RETRIEVE METHOD NAME FROM FUNCTION NAME
        def _get_methods_name(locale, dict):
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
                raise ValueError(f'{get_error_message(locale, "method-name-error")}')
            
        try:
            preferences = []
            for idx, (matrix, extension, types) in enumerate(zip(self.matrixes, self.extensions, self.types)):
                matrix_preferences = []
                for idx_method, method in enumerate(methods[idx]):
                    matrix = np.array(matrix)
                    types = np.array(types)

                    # GET METHODS FROM DICTIONARY
                    mcda_method = method['method'].upper()
                    if isinstance(method['weights'], str):
                        weights_method = method['weights'].upper()
                        weights_object = Weights(extension, types)

                        try:
                            weights_data = weights_object.calculate_weights(locale, matrix, weights_method)
                            weights = np.array(weights_data)[0]
                        except Exception as err:
                            raise ValueError(err)
                        
                    else:
                        weights_method = 'input'
                        weights_extension = 'crisp'
                        # crisp
                        if extension == 'crisp':
                            weights = np.array(method['weights'], dtype=float)
                        else:
                            # fuzzy

                            # TFN weights
                            if isinstance(method['weights'][0], str):
                                try:
                                    fuzzy_weights = [[float(c.replace(',', '')) for c in w.split()] for w in method['weights']]
                                    weights_extension = 'fuzzy'
                                except:
                                    raise ValueError(f'{get_error_message(locale, "fuzzy-weights-user-error")}')

                                weights = np.array(fuzzy_weights, dtype=float)
                            # crisp weights
                            else:
                                weights = np.array(method['weights'], dtype=float)
                            
                        try:
                            Validator.validate_user_weights(locale, weights, weights_extension)
                        except Exception as err:
                            raise ValueError(err)

                    # FUZZY CALCULATIONS
                    if extension == 'fuzzy':
                        # fuzzy -> call (matrix, weights, types)
                        # ARAS, COPRAS, MOORA -> normalization
                        if mcda_method in ['ARAS', 'COPRAS', 'MOORA']:
                            kwargs = _check_fuzzy_parameters(locale, mcda_method, idx, idx_method, check_normalization=True)

                        # fuzzy CODAS: normalization, distance_1, distance_2
                        elif mcda_method == 'CODAS':
                            kwargs = _check_fuzzy_parameters(locale, mcda_method, idx, idx_method, check_normalization=True, check_distance_1=True, check_distance_2=True)

                        # fuzzy MAIRCA: normalization, distance
                        # fuzzy TOPSIS: normalization, distance
                        elif mcda_method in ['MAIRCA', 'TOPSIS']:
                            kwargs = _check_fuzzy_parameters(locale, mcda_method, idx, idx_method, check_normalization=True, check_distance=True)

                        # fuzzy MABAC: normalization, defuzzify
                        elif mcda_method == 'MABAC':
                            kwargs = _check_fuzzy_parameters(locale, mcda_method, idx, idx_method, check_normalization=True, check_defuzzify=True)
                        
                        # fuzzy EDAS: defuzzify
                        # fuzzy OCRA: defuzzify
                        # fuzzy VIKOR: defuzzify
                        elif mcda_method in ['EDAS', 'OCRA', 'VIKOR']:
                            kwargs = _check_fuzzy_parameters(locale, mcda_method, idx, idx_method, check_defuzzify=True)

                        else:
                            raise ValueError(f'{mcda_method} {get_error_message(locale, "fuzzy-method-not-found")}')

                        try: 
                            body = self.mcda_methods[mcda_method][extension](**kwargs)
                            preference = body(matrix, weights, types)

                            if mcda_method == 'VIKOR':

                                preference = preference[2].tolist()
                            else:
                                preference = preference.tolist()

                            if np.nan in np.array(preference):
                                raise ValueError(f'{get_error_message(locale, "nan-preferences-error")}')

                            matrix_preferences.append({
                                "method": mcda_method,
                                "weights": weights_method,
                                "weights_value": weights.tolist(),
                                "preference": preference,
                                "extension": extension,
                                "additional": _get_methods_name(locale, kwargs)
                            })
                        except Exception:
                            raise ValueError(f'{get_error_message(locale, "fuzzy-assessment-error")}')
                    
                    elif extension == 'crisp':
                        # crisp -> matrix, types, weights
                        if mcda_method in ['ARAS', 'COCOSO', 'CODAS', 'COPRAS', 'EDAS', 'MABAC', 'MAIRCA', 'MARCOS', 'MOORA', 'OCRA', 'TOPSIS', 'VIKOR']:

                            kwargs = {}
                            if mcda_method in ['ARAS', 'COCOSO', 'CODAS', 'MABAC', 'MAIRCA', 'MARCOS', 'OCRA', 'TOPSIS', 'VIKOR']:
                                kwargs = _check_crisp_parameters(locale, mcda_method, idx, idx_method, check_normalization_function=True)

                            try:
                                body = self.mcda_methods[mcda_method][extension](**kwargs)

                            
                                if mcda_method == 'VIKOR':
                                    preference = body(matrix, weights, types, return_all=True)

                                    preference = preference[2].tolist()
                                    

                                else:
                                    preference = body(matrix, weights, types).tolist()

                                if np.nan in np.array(preference):
                                    raise ValueError(f'{get_error_message(locale, "nan-preferences-error")}')

                                matrix_preferences.append({
                                    "method": mcda_method,
                                    "preference": preference,
                                    "weights": weights_method,
                                    "weights_value": weights.tolist(),
                                    "extension": extension,
                                    "additional": _get_methods_name(locale, kwargs)
                                })
                            except Exception as err:
                                raise ValueError(f'{get_error_message(locale, "crisp-assessment-error")}')

                        # PROMETHEE -> matrix, weights, types, p, q, preference_function ('usual', 'ushape', 'vshape', 'level', 'vshape_2')
                        elif mcda_method == 'PROMETHEE':
                            kwargs = _check_crisp_parameters(locale, mcda_method, idx, idx_method, check_preference_function=True)

                            if 'preference_function' not in kwargs.keys():
                                raise ValueError(f'{get_error_message(locale, "no-preference-function-error")}')

                            try:
                                body = self.mcda_methods[mcda_method][extension](**kwargs)
                                matrix_preferences.append({
                                    "method": mcda_method,
                                    "preference": body(matrix, weights, types).tolist(),
                                    "weights": weights_method,
                                    "weights_value": weights.tolist(),
                                    "extension": extension,
                                    "additional": kwargs,
                                })
                            except Exception as err:
                                raise ValueError(f'{get_error_message(locale, "crisp-assessment-error")}')

                        # SPOTIS -> matrix, weights, types, bounds
                        elif mcda_method == 'SPOTIS':
                            try:
                                bounds =  np.vstack((
                                    np.min(matrix, axis=0),
                                    np.max(matrix, axis=0)
                                )).T

                                body = self.mcda_methods[mcda_method][extension]()
                                matrix_preferences.append({
                                    "method": mcda_method,
                                    "preference": body(matrix, weights, types, bounds).tolist(),
                                    "weights": weights_method,
                                    "weights_value": weights.tolist(),
                                    "extension": extension,
                                    "additional": {},
                                })
                            except Exception:
                                raise ValueError(f'{get_error_message(locale, "crisp-assessment-error")}')

                        # COMET -> matrix, weights, types, rate function
                        elif mcda_method == 'COMET':
                            try:
                                cvalues =  np.vstack((
                                    np.min(matrix, axis=0),
                                    np.mean(matrix, axis=0),
                                    np.max(matrix, axis=0)
                                )).T
                                body = self.mcda_methods[mcda_method][extension](cvalues, crisp_methods.COMET.topsis_rate_function(weights, types))
                                matrix_preferences.append({
                                    "method": mcda_method,
                                    "preference": body(matrix).tolist(),
                                    "weights": weights_method,
                                    "weights_value": weights.tolist(),
                                    "extension": extension,
                                    "additional": {},
                                })
                            except Exception:
                                raise ValueError(f'{get_error_message(locale, "crisp-assessment-error")}')
                        else:
                            raise ValueError(f'{mcda_method} {get_error_message(locale, "crisp-method-not-found")}')

                    else:
                        raise ValueError(f'{extension} {get_error_message(locale, "data-extension-error")}')
                
                preferences.append(matrix_preferences)
            return preferences

        except Exception as err:
            raise ValueError(err)
    