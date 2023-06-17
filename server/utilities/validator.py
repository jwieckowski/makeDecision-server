import numpy as np

class Validator():

    @staticmethod
    def validate_dimensions(matrix, types, weights=None):
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

        # check dimensions match
        if len(np.unique([matrix.shape[0], orders.shape[0]])) != 1:
            raise ValueError(f'Number of arrays and orders should be the same, not {matrix.shape[0]}, {orders.shape[0]}')

    @staticmethod
    def validate_matrix(matrix, extension):
        
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
        
        # crisp weights
        if weights.ndim == 1 and np.round(np.sum(weights), 4) != 1:
            raise ValueError('Weights should sum up to 1')

        # fuzzy weights
        if weights.ndim != 2 or weights.shape[1] != 3:
            raise ValueError('Fuzzy weights should be given as Triangular Fuzzy Numbers')

    @staticmethod
    def validate_types(types, unique_values=False):

        # check if types in [-1, 1]
        if any([t not in [-1, 1] for t in types]):
            raise ValueError('Criteria types should be given as -1 for cost or 1 for profit')
            
        # check if different types in array
        if unique_values:
            if len(np.unique(types)) == 1:
                raise ValueError('Criteria types should not be the same')
