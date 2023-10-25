# Copyright (c) 2023 Jakub Więckowski

from flask_restx import Resource
from werkzeug.utils import secure_filename
from werkzeug.exceptions import BadRequest

# PARSERS
from parsers import get_upload_matrix_parser, get_generate_matrix_parser

# MODELS
from models import get_matrix_model

# UTILS
from utils.files import Files
from utils.generator import generate_random_criteria_types, generate_random_matrix

# HELPERS
from helpers import validate_locale

# NAMESPACE
from .namespaces import v1 as api

# MODELS
matrix_model = get_matrix_model(api)

# ARGUMENTS PARSERS
upload_matrix_parser = get_upload_matrix_parser()
generate_matrix_parser = get_generate_matrix_parser()

@api.route('/matrix/upload')
class MatrixConverter(Resource):
    @api.expect(upload_matrix_parser)
    @api.marshal_with(matrix_model)
    def post(self):
        args = upload_matrix_parser.parse_args()
        locale = validate_locale(args['locale'])

        matrix = args['matrix']
        extension = args['extension']
        filename = secure_filename(matrix.filename)

        items = filename.split('.')
        try:
            m, ct = Files.read_matrix_from_file(locale, matrix, items[-1], extension)

            return {
                "response": {
                    "matrix": m.tolist(),
                    "criteria_types": ct.tolist(),
                    "extension": extension,
                }
            }
        except Exception as err:
            api.logger.info(str(err))
            e = BadRequest(str(err))
            raise e

@api.route('/matrix/generate')
class MatrixConverter(Resource):
    @api.expect(generate_matrix_parser)
    @api.marshal_with(matrix_model)
    def post(self):
        args = generate_matrix_parser.parse_args()
        locale = validate_locale(args['locale'])

        extension = args['extension']
        alternatives = args['alternatives']
        criteria = args['criteria']
        
        # OPTIONAL
        lower_bound = args['lower_bound']
        upper_bound = args['upper_bound']
        precision = args['precision']

        try:
            matrix = generate_random_matrix(locale, alternatives, criteria, extension, lower_bound, upper_bound, precision)
            criteria_types = generate_random_criteria_types(criteria)
            
            return {
                "response": {
                    "matrix": matrix.tolist(),
                    "criteria_types": criteria_types.tolist(),
                    "extension": extension,
                }
            }
        except Exception as err:
            api.logger.info(str(err))
            e = BadRequest(str(err))
            raise e
