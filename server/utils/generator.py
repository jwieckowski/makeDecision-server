import numpy as np
import pyfdm

from .errors import get_error_message

# LOGGER
from routes.namespaces import v1 as api

def generate_random_matrix(locale, alternatives, criteria, extension, lower_bound=None, upper_bound=None, precision=None):
    """
        Generates random matrix with given extension and given shape

        Parameters
        ----------
            locale : string
                User application language

            alternatives : int
                Number of alternatives in decision matrix

            criteria : int
                Number of criteria in decision matrix
            
            extension : string (crisp or fuzzy)
                Name of the extension 
            
            lower_bound : float, default=None
                Lower bound of the randomly generated values in matrix 
            
            upper_bound : float, default=None
                Upper bound of the randomly generated values in matrix
            
            precision : int or None
                Precision of data representation
            
        Raises
        -------
            ValueError Exception
                If the error in the random matrix generation occurs, the exception is thrown
        
        Returns
        -------
            ndarray
                Randomly generated decision matrix with given shape and given extension
    """


    try:
        if extension == 'crisp':
            if precision is None:
                precision = 3

            lower, upper = 0, 1
            if lower_bound is not None:
                lower = lower_bound
            if upper_bound is not None:
                upper = upper_bound
            
            if lower_bound is not None or upper_bound is not None:
                if lower >= upper:
                    raise ValueError(get_error_message(locale, 'matrix-generation-bounds-error'))
            
            return np.round(np.random.uniform(low=lower, high=upper, size=(alternatives, criteria)), precision)
        elif extension == 'fuzzy':
            return np.round(pyfdm.helpers.generate_fuzzy_matrix(alternatives, criteria, lower_bound, upper_bound), precision)
        else:
            raise ValueError(f'{get_error_message(locale, "random-matrix-extension-error")} {extension}')
    except Exception as err:  
        api.logger.info(str(err))
        raise ValueError(err)


def generate_random_criteria_types(locale, criteria):
    """
        Generate random criteria types for Multi-Criteria Decision Analysis (MCDA).

        This function generates random criteria types for use in Multi-Criteria Decision Analysis (MCDA).
        MCDA involves assessing and comparing alternatives based on multiple criteria, where criteria types
        indicate whether each criterion is a benefit (+1) or a cost (-1). The function returns an array
        of randomly generated criteria types.

        Parameters:
        -----------
            locale : string
                User application language
                
            criteria (int): 
                The number of criteria for which random types need to be generated.

        Returns:
        --------
            numpy.ndarray: An array containing randomly generated criteria types for the given number of criteria.

        Raises:
        -------
            ValueError: If the 'criteria' parameter is less than or equal to 0.

        Example:
        --------
        >>> generate_random_criteria_types(5)
        array([-1,  1, -1, -1,  1])
        
        Note:
        -----
        Criteria types are used in MCDA to specify whether a criterion is beneficial (+1) or detrimental (-1)
        for an alternative. Randomly generated criteria types can be used in MCDA simulations and experiments.
    """

    if criteria <= 0:
        raise ValueError(get_error_message(locale, 'criteria-types-generation-error'))

    types_values = np.array([-1, 1])
    return np.random.choice(types_values, criteria)


def generate_method_items(method: str, data: dict, locale: str) -> list:
    """
        Generate list of items that could be used for the given method as a configuration parameters.

        Parameters:
        -----------
        method : str
            The name of the MCDA method for which to generate items.
        
        data : dict
            The dictionary with functionalities available in the application
            
        locale : str
            User application language.

        Returns:
        --------
        list
            A list containing dictionaries with information about randomly generated criteria types for the given method.

        Raises:
        -------
        ValueError
            If the specified method is not found in the dictionary.

        Example:
        --------
        >>> generate_method_items("example_method", "en")
        [
            {
                "extension": "extension_value",
                "label": "param_name_1",
                "type": "param_type_1",
                "parameter": "param_value_1",
                "default": "default_value_1",
                "items": [{"value": "item_value_1", "label": "item_label_1"}, ...]
            },
            ...
        ]

        Note:
        -----
        Different parameters could be used for different methods, since some of them uses normalization, other use a distance metrics, etc.
        This function produces a list of methods that could be used for the given parameter for the given method.
    """

    try:
        methods = [d for d in data if d['type'] == 'method'][0]
        methods_kwargs = [m for m in methods['data'] if m['name'].lower() == method.lower()][0]['kwargs']
    except:
        raise ValueError(f'{param["method"]} method not found')

    kwargs_list_items = []
    for mkw in methods_kwargs:
        for param in mkw['data']:
            item = {
                    "extension": mkw['extension'],
                    "label": param['method'],
                    "type": param['type'],
                    "parameter": param['parameter'],
                    "default": param['default'],
                }

            items = None
            # param['type']: select, input, array, bool
            if param['type'] == 'select':
                param_method = param['method']
                if param_method == 'expert function':
                    param_method = 'expert_function'
                elif param_method == 'preference function':
                    param_method = 'preference_function'

                try:
                    param_method = [d for d in data if param_method.lower() == d['type'].lower()][0]
                    param_method_list = [p for p in param_method['data'] if mkw['extension'] in p['extensions']]
                    
                    items = [{"value": item['functionName'] if 'functionName' in list(item.keys()) else item['name'], "label": item['name']} for item in param_method_list]
                except:
                    raise ValueError(f'Parameters of type "{param_method}" for {param["method"]} method not found')

            elif param['type'] == 'bool': 
                items = [
                    {
                        'value': "false",
                        "label": "False"
                    },
                    {
                        'value': "true",
                        "label": "True"
                    },
                ]

            if items is not None:
                item = item | {
                    "items": items
                }

            for additional_props in ['min', 'max', 'dimension', 'required']:
                if additional_props in list(param.keys()):
                    item = item | {
                        additional_props: param[additional_props]
                    }

            kwargs_list_items.append(item)

    return kwargs_list_items