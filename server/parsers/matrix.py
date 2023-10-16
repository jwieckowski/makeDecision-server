from flask_restx import reqparse
from werkzeug.datastructures import FileStorage

def get_matrix_parser():
    parser = reqparse.RequestParser()
    parser.add_argument('locale', location='headers', required=True)
    parser.add_argument('matrix', type=FileStorage, location='files', required=True)
    parser.add_argument('extension', type=str, location='form', required=True)

    return parser