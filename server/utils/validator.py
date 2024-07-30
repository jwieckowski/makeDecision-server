# Copyright (c) 2023 Jakub Więckowski

import numpy as np

from .errors import get_error_message

def validate_dimensions(locale: str, matrix: np.ndarray, types: np.ndarray, weights: None | np.ndarray =None):
    """
        Validates if shapes of matrix, types and weights (if given) match

        Parameters
        ----------
            locale : string,
                User application language

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
            raise ValueError(f'{get_error_message(locale, "criteria-types-number-error")} {matrix.shape[1]}, {types.shape[0]}')
    else:
        if len(np.unique([matrix.shape[1], weights.shape[0], types.shape[0]])) != 1:
            raise ValueError(f'{get_error_message(locale, "criteria-dimension-error")} {matrix.shape[1]}, {weights.shape[0]}, {types.shape[0]}')


def validate_orders_dimensions(locale: str, matrix: np.ndarray, orders: np.ndarray):
    """
        Validates if number of matrices and number of ranking orders match

        Parameters
        ----------
            locale : string,
                User application language

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
        raise ValueError(f'{get_error_message(locale, "criteria-dimension-error")} {matrix.shape[0]}, {orders.shape[0]}')


def validate_matrix(locale: str, matrix: np.ndarray, extension: str):
    """
        Validates the matrix format regarding the given extension

        Parameters
        ----------
            locale : string,
                User application language

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
            raise ValueError(f'{get_error_message(locale, "crisp-matrix-format-error")}')
        # numeric values
        if matrix.dtype not in [np.int32, np.int64, np.float32, np.float64]:
            raise ValueError(f'{get_error_message(locale, "crisp-matrix-not-numeric-error")}')
        # numeric values
    elif extension == 'fuzzy':
        # dimension
        if matrix.ndim != 3 or matrix.shape[2] != 3:
            raise ValueError(f'{get_error_message(locale, "fuzzy-matrix-format-error")}')
    else:
        raise ValueError(f'{extension} {get_error_message(locale, "data-extension-error")}')


        

def validate_user_weights(locale: str, weights_node: object, extension: str):
    """
        Validates if the weights vector given by user is correctly defined

        Parameters
        ----------
            locale : string,
                User application language

            weights : ndarray
                Vector of criteria weights defined by user.
                For crisp data, weights should sum up to 1.
                For the fuzzy data, weights should be given as Triangular Fuzzy Numbers.

            extension : string (crisp or fuzzy)
                Extension of decision matrix.

        Raises
        -------
            ValueError Exception
                If weights data is badly formatted regarding given extension, or do not meet the requirements, the exception is thrown
    """
    
    if extension == 'crisp':
        # crisp weights
        if weights_node.weights.ndim == 1 and np.round(np.sum(weights_node.weights), 4) != 1:
            raise ValueError(f'{get_error_message(locale, "weights-sum-error")} (ID {weights_node.id})')
    else:
        # crisp weights
        if weights_node.weights.ndim == 1 and np.round(np.sum(weights_node.weights), 4) != 1:
            raise ValueError(f'{get_error_message(locale, "weights-sum-error")} (ID {weights_node.id})')
        elif weights_node.weights.ndim != 1:
            # fuzzy weights
            if weights_node.weights.ndim != 2 or weights_node.weights.shape[1] != 3:
                raise ValueError(f'{get_error_message(locale, "fuzzy-weights-error")} (ID {weights_node.id})')

def validate_types(locale: str, types: np.ndarray, unique_values: bool =False):
    """
        Validates the vector of criteria types

        Parameters
        ----------
            locale : string,
                User application language

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
        raise ValueError(f'{get_error_message(locale, "criteria-types-values-error")}')
        
    # check if different types in array
    if unique_values:
        if len(np.unique(types)) == 1:
            raise ValueError(f'{get_error_message(locale, "criteria-types-not-unique-error")}')
