# Copyright (c) 2023 Jakub Więckowski

import numpy as np
import pymcdm.correlations as corr

from ..errors import get_error_message

class Correlation():
    def __init__(self):
        self.correlation_methods = {
            'GOODMAN-KRUSKALL': corr.goodman_kruskal_gamma,
            'KENDALL-TAU': corr.kendall_tau,
            'PEARSON': corr.pearson,
            'SPEARMAN': corr.spearman,
            'WEIGHTED SPEARMAN': corr.weighted_spearman,
            'WS RANK SIMILARITY': corr.rank_similarity_coef
        }

    def calculate_correlation(self, locale, matrix, methods):
        """
            Calculates correlation values of data in matrix with given methods

            Parameters
            ----------
                locale : string
                    User application language

                matrix : ndarray
                    Decision matrix formatted as numpy array. Rows represent alternatives and columns represent criteria. The matrix should be 2 dimensional for crisp data, and 3 dimensional for fuzzy data.

                methods : ndarray
                    Vector of string representing the name of correlation coefficients
                
            Raises
            -------
                ValueError Exception
                    If the error in the calculation of correlation values occurs, the exception is thrown
            
            Returns
            -------
                ndarray
                    Matrix of correlation values calculated with given methods
        """


        try:
            results = []
            for method in methods:
                if method not in self.correlation_methods.keys():
                    raise ValueError(f'{method} {get_error_message(locale, "correlation-method-error")}')
                else:
                    try:
                        correlation =  np.array([[self.correlation_methods[method](a, b) for b in matrix] for a in matrix])
                    except Exception:
                        raise ValueError(f'{get_error_message(locale, "correlation-unexpected-error")}')

                results.append({
                    'method': method,
                    'correlation': correlation.tolist()
                })

            return results
        except Exception:
            raise ValueError(f'{get_error_message(locale, "correlation-unexpected-error")}')


    def calculate_preferences_correlation(self, locale, methods, results):
        """
            Calculates correlation of preferences values of data in matrix with given methods

            Parameters
            ----------
                locale : string
                    User application language
                    

                methods : ndarray
                    Vector of dictionaries with correlation methods definitions 

                results : ndarray
                    Vector of dictionaries with calculated data regarding the MCDA method, weights method, preference values
                
            Raises
            -------
                ValueError Exception
                    If the error in the calculation of correlation of preference values occurs, the exception is thrown
            
            Returns
            -------
                ndarray
                    Matrix of correlation of preference values calculated with given methods
        """
        
        try:
            correlations = []
            for idx, methods_set in enumerate(methods):

                correlations_item = []
                for method in methods_set:

                    # retrieve correlation method
                    correlation_method = method['correlation'].upper()

                    # verification if correlation method is handled
                    if correlation_method not in self.correlation_methods.keys():
                        raise ValueError(f'{method} {get_error_message(locale, "correlation-method-error")}')

                    else:
                        # retrieve data for correlation
                        correlation_data = method['data']
                        correlation_matrix = []
                        methods_params = []
                
                        for data in correlation_data:
                            for result in results[idx]:

                                # match methods
                                if data['method'].upper() == result['method'].upper() and data['weights'].upper() == result['weights'].upper():       
                                    correlation_matrix.append(result['preference'])
                                    methods_params.append({'method': result['method'], 'weights': result['weights'], 'additionals': result['additional']})
                        # cast list to numpy array for correct calculations 
                        correlation_matrix = np.array(correlation_matrix)
                        
                        # calculation of preferences correlation 
                        res = [[self.correlation_methods[correlation_method](a, b) for b in correlation_matrix] for a in correlation_matrix]
                        correlations_item.append({
                            'correlation': correlation_method,
                            'results': res,
                            'methods': methods_params,
                        })

                correlations.append(correlations_item)

            return correlations
        except Exception:
            raise ValueError(f'{get_error_message(locale, "correlation-unexpected-error")}')


    def calculate_ranking_correlation(self, locale, methods, results):
        """
            Calculates correlation of ranking values of data in matrix with given methods

            Parameters
            ----------
                locale : string
                    User application language
                
                methods : ndarray
                    Vector of dictionaries with correlation methods definitions 

                results : ndarray
                    Vector of dictionaries with calculated data regarding the MCDA method, weights method, ranking values
                
            Raises
            -------
                ValueError Exception
                    If the error in the calculation of correlation of ranking values occurs, the exception is thrown
            
            Returns
            -------
                ndarray
                    Matrix of correlation of ranking values calculated with given methods
        """
        
        
        try:
            correlations = []
            for idx, methods_set in enumerate(methods):

                correlations_item = []
                for method in methods_set:

                    # retrieve correlation method
                    correlation_method = method['correlation'].upper()

                    # verification if correlation method is handled
                    if correlation_method not in self.correlation_methods.keys():
                        raise ValueError(f'{method} {get_error_message(locale, "correlation-method-error")}')

                    else:
                        # retrieve data for correlation
                        correlation_data = method['data']
                        correlation_matrix = []
                        methods_params = []

                        for data in correlation_data:
                            for ranking_result in results[idx]:
                                for result in ranking_result:
                                    # retrieve method for correlation calculation
                                    result_methods = result['methods'] 
                                    
                                    # match methods
                                    if data['method'].upper() == result_methods['method'].upper() and data['weights'].upper() == result_methods['weights'].upper() and data['correlation'] == True:       
                                        correlation_matrix.append(result['ranking'])
                                        methods_params.append({'method': result_methods['method'], 'weights': result_methods['weights'], 'additionals': result_methods['additionals']})

                        # cast list to numpy array for correct calculations 
                        correlation_matrix = np.array(correlation_matrix)

                        # calculation of ranking correlation 
                        res = [[self.correlation_methods[correlation_method](a, b) for b in correlation_matrix] for a in correlation_matrix]
                        correlations_item.append({
                            'correlation': correlation_method,
                            'results': res,
                            'methods': methods_params,
                        })

                correlations.append(correlations_item)

            return correlations
        except Exception:
            raise ValueError(f'{get_error_message(locale, "correlation-unexpected-error")}')
