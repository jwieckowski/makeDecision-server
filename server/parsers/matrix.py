from flask_restx import reqparse
from werkzeug.datastructures import FileStorage

def get_upload_matrix_parser():
    parser = reqparse.RequestParser()
    parser.add_argument('locale', location='headers', required=True)
    parser.add_argument('matrix', type=FileStorage, location='files', required=True)
    parser.add_argument('extension', type=str, location='form', required=True)

    return parser

def get_generate_matrix_parser():
    parser = reqparse.RequestParser()
    parser.add_argument('locale', location='headers', required=True)
    parser.add_argument('extension', type=str, location='json', required=True)
    parser.add_argument('alternatives', type=int, location='json', required=True)
    parser.add_argument('criteria', type=int, location='json', required=True)
    parser.add_argument('lower_bound', type=float, location='json')
    parser.add_argument('upper_bound', type=float, location='json')
    parser.add_argument('precision', type=int, location='json')

    return parser