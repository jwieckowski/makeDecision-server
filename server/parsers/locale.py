from flask_restx import reqparse

def get_locale_parser():
    parser = reqparse.RequestParser()
    parser.add_argument('locale', location='headers', required=True)
 
    return parser