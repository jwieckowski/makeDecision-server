import numpy as np

class Validator():

    @staticmethod
    def validate_dimensions(matrix, types, weights=None):
        """
            Validates if shapes of matrix, types and weights (if given) match

            Parameters
            ----------
                matrix : ndarray
                    Decision matrix formatted as numpy array. Rows represent alternatives and columns represent criteria. The matrix should be 2 dimensional for crisp data, and 3 dimensional for fuzzy data.

                types : ndarray
                    Vector of criteria types formatted as numpy array. Number of types should correspond to number of columns in matrix.
                
                weights : ndarray, default=None
                    Vector of criteria weights formatted as numpy array. Number of criteria should correspond to number of columns in matrix and number of elements in types vector

                
            Raises
            -------
                ValueError Exception
                    If the data shapes is different, the exception is thrown
        """

        matrix = np.array(matrix)
        types = np.array(types)
        
        # check dimensions match
        if weights == None:
            if len(np.unique([matrix.shape[1], types.shape[0]])) != 1:
                raise ValueError(f'Number of criteria should equals number of types, not {matrix.shape[1]}, {types.shape[0]}')
        else:
            if len(np.unique([matrix.shape[1], weights.shape[0], types.shape[0]])) != 1:
                raise ValueError(f'Number of criteria should equals number of weights and types, not {matrix.shape[1]}, {weights.shape[0]}, {types.shape[0]}')
    
    @staticmethod
    def validate_orders_dimensions(matrix, orders):
        """
            Validates if number of matrices and number of ranking orders match

            Parameters
            ----------
                matrix : ndarray
                    Decision matrix formatted as numpy array. Rows represent alternatives and columns represent criteria. The matrix should be 2 dimensional for crisp data, and 3 dimensional for fuzzy data.

                orders : ndarray
                    Vector of ranking orders to calculate. Number of orders should correspond to number of matrices.
               
                
            Raises
            -------
                ValueError Exception
                    If the data shapes is different, the exception is thrown
        """

        # check dimensions match
        if len(np.unique([matrix.shape[0], orders.shape[0]])) != 1:
            raise ValueError(f'Number of arrays and orders should be the same, not {matrix.shape[0]}, {orders.shape[0]}')

    @staticmethod
    def validate_matrix(matrix, extension):
        """
            Validates the matrix format regarding the given extension

            Parameters
            ----------
                matrix : ndarray
                    Decision matrix formatted as numpy array. Rows represent alternatives and columns represent criteria. The matrix should be 2 dimensional for crisp data, and 3 dimensional for fuzzy data.

                extension : string (crisp or fuzzy)
                    Extension of decision matrix.

            Raises
            -------
                ValueError Exception
                    If matrix data is badly formatted regarding given extension, the exception is thrown
        """
        
        if extension == 'crisp':
            # dimension
            if matrix.ndim != 2:
                raise ValueError('Crisp matrix bad formatted')
            # numeric values
            if matrix.dtype not in [np.int32, np.int64, np.float32, np.float64]:
                raise ValueError('Not all elements in matrix are numeric')
            # numeric values
        elif extension == 'fuzzy':
            # dimension
            if matrix.ndim != 3 or matrix.shape[2] != 3:
                raise ValueError('Fuzzy matrix bad formatted')
        else:
            raise ValueError(f'Extension "{extension}" not handled')


            
    @staticmethod
    def validate_user_weights(weights):
        """
            Validates if the weights vector given by user is correctly defined

            Parameters
            ----------
                weights : ndarray
                    Vector of criteria weights defined by user.
                    For crisp data, weights should sum up to 1.
                    For the fuzzy data, weights should be given as Triangular Fuzzy Numbers.

            Raises
            -------
                ValueError Exception
                    If weights data is badly formatted regarding given extension, or do not meet the requirements, the exception is thrown
        """
        
        # crisp weights
        if weights.ndim == 1 and np.round(np.sum(weights), 4) != 1:
            raise ValueError('Weights should sum up to 1')

        # fuzzy weights
        if weights.ndim != 2 or weights.shape[1] != 3:
            raise ValueError('Fuzzy weights should be given as Triangular Fuzzy Numbers')

    @staticmethod
    def validate_types(types, unique_values=False):
        """
            Validates the vector of criteria types

            Parameters
            ----------
                types : ndarray
                    Vector of criteria types representing if column is directed to minimizing values (Cost as -1), or to maximizing values (Profit as 1)

                unique_values : bool, default=False
                    Flag representing if the criteria types could be the same

            Raises
            -------
                ValueError Exception
                    If vector of criteria weights has wrong values or are the same (for the unique_values flag), the exception is thrown
        """

        # check if types in [-1, 1]
        if any([t not in [-1, 1] for t in types]):
            raise ValueError('Criteria types should be given as -1 for cost or 1 for profit')
            
        # check if different types in array
        if unique_values:
            if len(np.unique(types)) == 1:
                raise ValueError('Criteria types should not be the same')
