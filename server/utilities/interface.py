from .Interfaces.correlations import Correlation
from .Interfaces.preferences import Preferences
from .Interfaces.ranking import Ranking
from .Interfaces.additional import Additional

class Calculations():

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
            return Additional.generate_random_matrix(alternatives, criteria, extension)
        except Exception as err:
            raise ValueError(err)

    @staticmethod
    def calculate_preference_correlations(methods, results):
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
            correlation_obj = Correlation()
            return correlation_obj.calculate_preferences_correlation(methods, results)

        except Exception as err:
            raise ValueError(err)
        

    @staticmethod
    def calculate_ranking_correlations(methods, results):
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
            correlation_obj = Correlation()
            return correlation_obj.calculate_ranking_correlation(methods, results)

        except Exception as err:
            raise ValueError(err)

    @staticmethod
    def calculate_preferences(matrixes, extensions, types, methods, params=None):
        """
            Calculates correlation of preferences values of data in matrix with given methods

            Parameters
            ----------
                matrixes : ndarray
                    Vector of decision matrixes formatted as numpy array. In each matrix, rows represent alternatives and columns represent criteria. The matrix should be 2 dimensional for crisp data, and 3 dimensional for fuzzy data.

                extensions : ndarray
                    Vector of data extensions (crisp or fuzzy) represented as string
                
                types : ndarray
                    Vector of criteria types formatted as numpy arrays.
                    
                methods : ndarray
                    Vector of dictionaries with MCDA method and weights method that are used in multi-criteria assessment

                params : ndarray, default=None
                    Vector of dictionaries with additional parameters that are used in the multi-criteria assessment, like methods normalization, defuzzification or distances
                
            Raises
            -------
                ValueError Exception
                    If the error in the multi-criteria assessment occurs, the exception is thrown
            
            Returns
            -------
                ndarray
                    Vector of dictionaries including the results from multi-criteria assessment 
        """


        try:
            preferences_object = Preferences(matrixes, extensions, types)
            return preferences_object.calculate_preferences(methods, params)
        except Exception as err:
            raise ValueError(err)
        

    @staticmethod
    def calculate_ranking(methods, results):
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
            ranking_obj = Ranking()
            return ranking_obj.calculate_ranking(methods, results)
        except Exception as err:
            raise ValueError(err)
        
        