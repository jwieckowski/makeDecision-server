from flask_restx import reqparse

def get_survey_usage_parser():
    parser = reqparse.RequestParser()
    parser.add_argument('option', type=int, location='json')
    parser.add_argument('name', type=str, location='json')
 
    return parser

def get_survey_rating_parser():
    parser = reqparse.RequestParser()
    parser.add_argument('helpful', type=str, location='json')
    parser.add_argument('easyInterface', type=str, location='json')
    parser.add_argument('changeSuggestion', type=str, location='json')
    parser.add_argument('easeOfUse', type=int, location='json')
    parser.add_argument('overallRating', type=int, location='json')
    parser.add_argument('features', type=str, location='json')
 
    return parser