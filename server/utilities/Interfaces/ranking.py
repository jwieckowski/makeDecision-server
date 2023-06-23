import numpy as np
from pyfdm.helpers import rank

class Ranking():

    # calculation of ranking based on preferences and order
    def _rank_preferences(self, preferences, order):
        """
            Calculates criteria weights based on the decision matrix and given weights method

            Parameters
            ----------
                preferences : ndarray
                    Vector of preference values

                order : string (ascending or descending)
                    Order determining the direction of ranking sorting
                    

            Raises
            ------
                ValueError Exception
                    If order name was not found in or calculation process did not finish successfully, the exception is thrown

            Returns
            -------
                ndarray
                    Vector of ranking calculated with the given order

        """

        try:
            if order == 'ascending':
                return rank(preferences, False).tolist()
            else:
                return rank(preferences).tolist()
        except Exception as err:
            raise ValueError(f'Unexpected error in ranking calculation: {err}')

    def calculate_ranking(self, methods, results):
        """
            Calculates ranking order from the results data determined in the methods parameters

            Parameters
            ----------
                methods : dictionary
                    Structure containing parameters for calculation of MCDA method, criteria weights vector, and ranking order
                    
                results : dictionary
                    Structure containing results from MCDA method, criteria weights vector, and preference values

            Raises
            ------
                ValueError Exception
                    If order name was not found in or calculation process did not finish successfully, the exception is thrown

            Returns
            -------
                ndarray
                    Vector of rankings calculated with the given orders

        """

        try:
            rankings = []

            for idx, methods_set in enumerate(methods):

                ranking_item = []
                for method in methods_set:
                    
                    item = []
                    for data in method['data']:

                        for result in results[idx]:
                            # match methods with results data
                            # what if are the same in data (?) - TODO CHECK
                            if data['method'].upper() == result['method'] and data['weights'].upper() == result['weights']:

                                # retrieve ranking order       
                                order = data['order']

                                # verification of ranking order
                                if order.lower() not in ['ascending', 'descending']:
                                    raise ValueError('Given ranking order not found')
                                    
                                else:
                                    # calculation of ranking
                                    try:
                                        item.append({
                                            'ranking': self._rank_preferences(np.array(result['preference']), order),
                                            'methods': data
                                        })
                                    # catching error if occured
                                    except Exception as err:
                                        raise ValueError('Error while calculating ranking for preferences')
                                        
                    ranking_item.append(item)
                rankings.append(ranking_item)

            return rankings
        except Exception as err:
            raise ValueError(f'Unexpected error in ranking calculation: {err}')

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

    method = 'Ascending'

    ranking = Ranking(method)
    print(ranking.calculate_ranking(matrix))