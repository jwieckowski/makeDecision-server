# Copyright (c) 2023 Jakub Więckowski

import numpy as np
from pyfdm.helpers import rank

from ..errors import get_error_message

class Ranking():

    # calculation of ranking based on preferences and order
    def _rank_preferences(self, locale, preferences, order):
        """
            Calculates criteria weights based on the decision matrix and given weights method

            Parameters
            ----------
                locale : string
                    User application language

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
        except Exception:
            raise ValueError(f'{get_error_message(locale, "ranking-unexpected-error")}')

    def calculate_ranking(self, locale, methods, results):
        """
            Calculates ranking order from the results data determined in the methods parameters

            Parameters
            ----------
                locale : string
                    User application language
                    
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

                    for data, result in zip(method['data'], results[idx]):
                        
                        # match methods with results data
                        if data['method'].upper() == result['method'].upper() and data['weights'].upper() == result['weights'].upper() and data['ranking'] == True:

                            # retrieve ranking order       
                            order = data['order']

                            # verification of ranking order
                            if order.lower() not in ['ascending', 'descending']:
                                raise ValueError(f'{order} {get_error_message(locale, "ranking-order-error")}')
                                
                            else:
                                # calculation of ranking
                                try:
                                    methods_data = data
                                    methods_data['additionals'] = result['additional'] 

                                    item.append({
                                        'ranking': self._rank_preferences(locale, np.array(result['preference']), order),
                                        'methods': methods_data
                                    })

                                # catching error if occured
                                except Exception:
                                    raise ValueError(f'{get_error_message(locale, "ranking-preference-error")}')
                                        
                    ranking_item.append(item)
                rankings.append(ranking_item)

            return rankings
        except Exception:
            raise ValueError(f'{get_error_message(locale, "ranking-unexpected-error")}')

