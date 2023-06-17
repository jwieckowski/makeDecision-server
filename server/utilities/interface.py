from .Interfaces.correlations import Correlation
from .Interfaces.preferences import Preferences
from .Interfaces.ranking import Ranking
from .Interfaces.additional import Additional
class Calculations():
    def __init__(self):
        pass

    @staticmethod
    def generate_random_matrix(alternatives, criteria, extension):
        try:
            return Additional.generate_random_matrix(alternatives, criteria, extension)
        except Exception as err:
            raise ValueError(err)

    @staticmethod
    def calculate_preference_correlations(methods, results):

        try:
            correlation_obj = Correlation()
            return correlation_obj.calculate_preferences_correlation(methods, results)

        except Exception as err:
            raise ValueError(err)
        

    @staticmethod
    def calculate_ranking_correlations(methods, results):

        try:
            correlation_obj = Correlation()
            return correlation_obj.calculate_ranking_correlation(methods, results)

        except Exception as err:
            raise ValueError(err)

    @staticmethod
    def calculate_preferences(matrixes, extensions, types, methods, params=None):

        try:
            preferences_object = Preferences(matrixes, extensions, types)
            return preferences_object.calculate_preferences(methods, params)
        except Exception as err:
            raise ValueError(err)
        

    @staticmethod
    def calculate_ranking(methods, results):

        try:
            ranking_obj = Ranking()
            return ranking_obj.calculate_ranking(methods, results)
        except Exception as err:
            raise ValueError(err)
        
        