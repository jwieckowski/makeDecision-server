import numpy as np
import pymcdm.correlations as corr

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

    def calculate_correlation(self, matrix, methods):
        """
            Calculates correlation values of data in matrix with given methods

            Parameters
            ----------
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
                    raise ValueError('Correlation coefficient method not found')
                else:
                    try:
                        correlation =  np.array([[self.correlation_methods[method](a, b) for b in matrix] for a in matrix])
                    except Exception as err:
                        raise ValueError(f'Unexpected error in correlation calculation: {err}')

                results.append({
                    'method': method,
                    'correlation': correlation.tolist()
                })

            return results
        except Exception as err:
            raise ValueError(f'Unexpected error in correlation calculation: {err}')


    def calculate_preferences_correlation(self, methods, results):
        """
            Calculates correlation of preferences values of data in matrix with given methods

            Parameters
            ----------
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
                        raise ValueError('Correlation coefficient method not found')

                    else:
                        # retrieve data for correlation
                        correlation_data = method['data']
                        correlation_matrix = []
                
                        for data in correlation_data:
                            for result in results[idx]:
                                # match methods
                                # what if methods are the same (?) - TODO CHECK
                                if data['method'].upper() == result['method'] and data['weights'].upper() == result['weights']:       
                                    correlation_matrix.append(result['preference'])

                        # cast list to numpy array for correct calculations 
                        correlation_matrix = np.array(correlation_matrix)
                        
                        # calculation of preferences correlation 
                        res = [[self.correlation_methods[correlation_method](a, b) for b in correlation_matrix] for a in correlation_matrix]
                        correlations_item.append({
                            'correlation': correlation_method,
                            'results': res,
                            'methods': method['data'],
                        })

                correlations.append(correlations_item)

            return correlations
        except Exception as err:
            raise ValueError(f'Unexpected error in preferences correlation calculation: {err}')


    def calculate_ranking_correlation(self, methods, results):
        """
            Calculates correlation of ranking values of data in matrix with given methods

            Parameters
            ----------
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
                        raise ValueError('Correlation coefficient method not found')

                    else:
                        # retrieve data for correlation
                        correlation_data = method['data']
                        correlation_matrix = []
                
                        for data in correlation_data:
                            for ranking_result in results[idx]:
                                for result in ranking_result:
                                    # retrieve method for correlation calculation
                                    result_methods = result['methods'] 
                                    
                                    # match methods
                                    # what if methods are the same (?) - TODO CHECK
                                    if data['method'].upper() == result_methods['method'].upper() and data['weights'].upper() == result_methods['weights'].upper() and data['order'].upper() == result_methods['order'].upper():       
                                        correlation_matrix.append(result['ranking'])
                        
                        # cast list to numpy array for correct calculations 
                        correlation_matrix = np.array(correlation_matrix)
                        
                        # calculation of ranking correlation 
                        res = [[self.correlation_methods[correlation_method](a, b) for b in correlation_matrix] for a in correlation_matrix]
                        correlations_item.append({
                            'correlation': correlation_method,
                            'results': res,
                            'methods': method['data'],
                        })

                correlations.append(correlations_item)

            return correlations
        except Exception as err:
            raise ValueError(f'Unexpected error in ranking correlation calculation: {err}')

if __name__ == '__main__':
    matrix = np.array([
        [1, 2, 3, 4, 5],
        [5, 4, 3, 4, 3],
        [1, 1, 3, 1, 3],
        [4, 1, 3, 5, 2],
        [4, 2, 4, 2, 3]
    ])
    matrix2 = np.array([
        [1, 2, 3, 4, 5],
        [5, 4, 3, 4, 3]
    ])

    method = 'WS rank similarity'

    correlation = Correlation()
    print(correlation.calculate_correlation(matrix, method))
    print(correlation.calculate_correlation(matrix2, method))