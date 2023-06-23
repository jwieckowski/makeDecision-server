import numpy as np
import pyfdm

class Additional():

    @staticmethod
    def generate_random_matrix(alternatives, criteria, extension):
        """
            Generates random matrix with given extension and given shape

            Parameters
            ----------
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
                raise ValueError(f'Cannot generate random matrix for {extension} extension')
        except Exception as err:
            raise ValueError(f'Unexpected error in random matrix generation: {err}')