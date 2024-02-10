from flask_restx import reqparse

def get_survey_usage_parser():
    parser = reqparse.RequestParser()
    parser.add_argument('option', type=int, location='json')
    parser.add_argument('name', type=str, location='json')
 
    return parser