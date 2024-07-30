from flask_restx import reqparse

def get_survey_usage_parser():
    """
    Creates and returns a parser for handling survey usage requests.

    The parser extracts the following from the JSON body of the request:
    - 'option': Integer value representing the survey option.
    - 'name': String value representing the name associated with the option.

    Returns
    -------
    flask_restx.reqparse.RequestParser
        The configured request parser for survey usage.
    """
    parser = reqparse.RequestParser()
    parser.add_argument('option', type=int, location='json')
    parser.add_argument('name', type=str, location='json')
 
    return parser

def get_survey_rating_parser():
    """
    Creates and returns a parser for handling survey rating requests.

    The parser extracts the following from the JSON body of the request:
    - 'helpful': String value describing how helpful the survey was.
    - 'easyInterface': String value describing the ease of the interface.
    - 'changeSuggestion': String value for suggestions on changes.
    - 'easeOfUse': Integer value rating the ease of use.
    - 'overallRating': Integer value for the overall rating.
    - 'features': String value describing the features of the surveyed item.

    Returns
    -------
    flask_restx.reqparse.RequestParser
        The configured request parser for survey rating.
    """
    parser = reqparse.RequestParser()
    parser.add_argument('helpful', type=str, location='json')
    parser.add_argument('easyInterface', type=str, location='json')
    parser.add_argument('changeSuggestion', type=str, location='json')
    parser.add_argument('easeOfUse', type=int, location='json')
    parser.add_argument('overallRating', type=int, location='json')
    parser.add_argument('features', type=str, location='json')
 
    return parser