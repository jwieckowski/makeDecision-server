# Copyright (c) 2023 Jakub Więckowski

import numpy as np
import pyfdm

from ..errors import get_error_message

class Additional():

    @staticmethod
    def generate_random_matrix(locale, alternatives, criteria, extension):
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
                return np.random.random((alternatives, criteria))
            elif extension == 'fuzzy':
                return pyfdm.helpers.generate_fuzzy_matrix(alternatives, criteria)
            else:
                raise ValueError(f'{get_error_message(locale, "random-matrix-extension-error")} {extension}')
        except Exception:
            raise ValueError(f'{get_error_message(locale, "random-matrix-unexpected-error")}')