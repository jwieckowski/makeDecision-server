from flask_restx import reqparse
from werkzeug.datastructures import FileStorage

def get_upload_matrix_parser():
    """
    Creates and returns a parser for handling matrix upload requests.

    The parser extracts the following from the request:
    - 'locale' from the headers
    - 'matrix' file upload from the files
    - 'extension' from the form data

    Returns
    -------
    flask_restx.reqparse.RequestParser
        The configured request parser for matrix upload.
    """
    parser = reqparse.RequestParser()
    parser.add_argument('locale', location='headers', required=True)
    parser.add_argument('matrix', type=FileStorage, location='files', required=True)
    parser.add_argument('extension', type=str, location='form', required=True)

    return parser

def get_generate_matrix_parser():
    """
    Creates and returns a parser for generating matrix requests.

    The parser extracts the following from the request:
    - 'locale' from the headers
    - 'extension' from the JSON body
    - 'alternatives' from the JSON body
    - 'criteria' from the JSON body
    - 'lower_bound' from the JSON body (optional)
    - 'upper_bound' from the JSON body (optional)
    - 'precision' from the JSON body (optional)

    Returns
    -------
    flask_restx.reqparse.RequestParser
        The configured request parser for generating matrices.
    """
    parser = reqparse.RequestParser()
    parser.add_argument('locale', location='headers', required=True)
    parser.add_argument('extension', type=str, location='json', required=True)
    parser.add_argument('alternatives', type=int, location='json', required=True)
    parser.add_argument('criteria', type=int, location='json', required=True)
    parser.add_argument('lower_bound', type=float, location='json')
    parser.add_argument('upper_bound', type=float, location='json')
    parser.add_argument('precision', type=int, location='json')

    return parser