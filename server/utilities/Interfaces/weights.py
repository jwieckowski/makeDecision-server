import numpy as np
import pymcdm.weights as crisp_weights
import pyfdm.weights as fuzzy_weights

class Weights():
    def __init__(self, extension, types):
        """
            Initialize weights object with extension and types values

            Parameters
            ----------
                extension : string (crisp or fuzzy)
                    Extension of decision matrix.

                types : ndarray
                    Vector of criteria types formatted as numpy array. Number of types should correspond to number of weights.

        """

        self.extension=extension
        self.types=types

        self.weights_methods = {
            'ANGLE': {
                'crisp': crisp_weights.angle_weights
            },
            'CILOS': {
                'crisp': crisp_weights.cilos_weights
            },
            'CRITIC': {
                'crisp': crisp_weights.critic_weights,
            },
            'ENTROPY': {
                'crisp': crisp_weights.entropy_weights,
                'fuzzy': fuzzy_weights.shannon_entropy_weights
            },
            'EQUAL': {
                'crisp': crisp_weights.equal_weights,
                'fuzzy': fuzzy_weights.equal_weights
            },
            'GINI': {
                'crisp': crisp_weights.gini_weights
            },
            'IDOCRIW': {
                'crisp': crisp_weights.idocriw_weights
            },
            'MEREC': {
                'crisp': crisp_weights.merec_weights
            },
            'STANDARD DEVIATION': {
                'crisp': crisp_weights.standard_deviation_weights,
                'fuzzy': fuzzy_weights.standard_deviation_weights
            },
            'VARIANCE': {
                'crisp': crisp_weights.variance_weights,
                'fuzzy': fuzzy_weights.variance_weights
            }
        }

    def calculate_weights(self, matrix, method):
        """
            Calculates criteria weights based on the decision matrix and given weights method

            Parameters
            ----------
                matrix : ndarray
                    Decision matrix formatted as numpy array. Rows represent alternatives and columns represent criteria. The matrix should be 2 dimensional for crisp data, and 3 dimensional for fuzzy data.

                method : string 
                    Name of the weighting method.

            Raises
            ------
                ValueError Exception
                    If method name was not found in the dictionary or calculation process did not finish successfully, the exception is thrown

            Returns
            -------
                ndarray
                    Vector of criteria weights calculated with the given weighting method

        """

        try:
            weights = np.array([])
            if self.extension not in self.weights_methods[method].keys():
                raise ValueError(f'Extension {self.extension} not found for method {method}')
            else:
                if method in ['MEREC', 'CILOS', 'IDOCRIW']:
                    weights = self.weights_methods[method][self.extension](matrix, self.types)
                else:
                    weights = self.weights_methods[method][self.extension](matrix)

            return weights.tolist(),
        except Exception as err:
            raise ValueError(f'Error in calculating criteria weights: {err}')
        

if __name__ == '__main__':
    matrix = np.array([
        [1, 2, 3, 4, 5],
        [5, 4, 3, 4, 3],
        [1, 1, 3, 1, 3],
        [4, 1, 3, 5, 2],
        [4, 2, 4, 2, 3]
    ])

    types = np.array([-1, 1, -1, 1, -1])

    method = 'Entropy'
    extension = 'crisp'

    weights = Weights(method, extension, types)
    print(weights.calculate_weights(matrix))