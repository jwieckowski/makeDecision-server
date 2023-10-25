import numpy as np
import pyfdm

from .errors import get_error_message

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
                    # TODO: change message to dict message
                    raise ValueError(f'Lower bound of the matrix values should not be greater than upper bound')
            
            return np.round(np.random.uniform(low=lower, high=upper, size=(alternatives, criteria)), precision)
        elif extension == 'fuzzy':
            return pyfdm.helpers.generate_fuzzy_matrix(alternatives, criteria, lower_bound, upper_bound)
        else:
            raise ValueError(f'{get_error_message(locale, "random-matrix-extension-error")} {extension}')
    except Exception as err:  
        raise ValueError(err)


def generate_random_criteria_types(criteria):
    """
        Generate random criteria types for Multi-Criteria Decision Analysis (MCDA).

        This function generates random criteria types for use in Multi-Criteria Decision Analysis (MCDA).
        MCDA involves assessing and comparing alternatives based on multiple criteria, where criteria types
        indicate whether each criterion is a benefit (+1) or a cost (-1). The function returns an array
        of randomly generated criteria types.

        Parameters:
        -----------
            criteria (int): The number of criteria for which random types need to be generated.

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
        # TODO: change message to dict message
        raise ValueError('Number of criteria should be greater than 0')

    types_values = np.array([-1, 1])
    return np.random.choice(types_values, criteria)
