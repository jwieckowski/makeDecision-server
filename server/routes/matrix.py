from flask_restx import Resource
from werkzeug.utils import secure_filename
from werkzeug.exceptions import BadRequest

# PARSERS
from parsers import get_matrix_parser

# MODELS
from models import get_description_model

from utilities.files import Files
from helpers import validate_locale

# NAMESPACE
from .namespaces import v1 as api

# MODELS
description_model = get_description_model(api)
# ARGUMENTS PARSERS
matrix_parser = get_matrix_parser()


@api.route('/matrix/upload')
class MatrixConverter(Resource):
    @api.expect(matrix_parser)
    # @ns.marshal_with(matrix_data_item)
    def post(self):
        args = matrix_parser.parse_args()
        locale = validate_locale(args['locale'])

        matrix = args['matrix']
        extension = args['extension']
        filename = secure_filename(matrix.filename)

        items = filename.split('.')
        try:
            m, ct = Files.read_matrix_from_file(locale, matrix, items[-1], extension)

            return {
                "matrix": m.tolist(),
                "criteriaTypes": ct.tolist()
            }
        except Exception as err:
            api.logger.info(str(err))
            e = BadRequest(str(err))
            raise e
