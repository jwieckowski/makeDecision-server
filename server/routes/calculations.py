from flask_restx import Resource
from werkzeug.exceptions import BadRequest
import numpy as np

# PARSERS
from parsers import get_calculation_parser

# MODELS
from models import get_description_model

# UTILS
from utilities.errors import get_error_message
from utilities.validator import Validator
from utilities.results import preprocess_input_data, get_calculation_results

# HELPERS
from helpers import validate_locale

# NAMESPACE
from .namespaces import v1 as api

# MODELS
description_model = get_description_model(api)
# ARGUMENTS PARSERS
calculation_parser = get_calculation_parser()


@api.route('/calculations/calculate')
class CalculationResults(Resource):
    @api.expect(calculation_parser)
    # @ns.marshal_with(images_model)
    def post(self):
        args = calculation_parser.parse_args()
        # ARGUMENTS
        locale = validate_locale(args['locale'])
        matrixes = np.array([args['matrix']][0], dtype='object')
        extensions = np.array([args['extensions']][0])
        types = np.array([args['types']][0])
        method = np.array([args['method']][0], dtype='object')

        methodCorrelations = np.array(args['methodCorrelations'])
        methodRankings = np.array(args['methodRankings'])
        rankingCorrelations = np.array(args['rankingCorrelations'])

        # ERROR IF SHAPES NOT THE SAME SIZE
        if len(np.unique([len(matrixes), len(extensions), len(types)])) != 1:
            api.logger.info(f'{get_error_message(locale, "matrix-criteria-extensions-shapes-mismatch")}')
            e = BadRequest(f'{get_error_message(locale, "matrix-criteria-extensions-shapes-mismatch")}')
            raise e

        if len(method) == 0:
            api.logger.info(f'{get_error_message(locale, "no-assessment-method-error")}')
            e = BadRequest(f'{get_error_message(locale, "no-assessment-method-error")}')
            raise e

        calculationMatrixes = []
        calculationTypes = []

        # CHECK IF NEED TO GENERATE RANDOM MATRIX OR CONVERT INPUT MATRIX
        for idx, (matrix, extension) in enumerate(zip(matrixes, extensions)):
            if np.array(matrix).shape[0] == 0:
                api.logger.info(f'{get_error_message(locale, "empty-matrix")}')
                e = BadRequest(f'{get_error_message(locale, "empty-matrix")}')
                raise e
                
            try:
                inputMatrix, inputTypes = preprocess_input_data(matrix, extension, locale, types[idx])

                # VALIDATION OF INPUT DATA
                Validator.validate_matrix(locale, inputMatrix, extension)
                Validator.validate_types(locale, inputTypes)
                Validator.validate_dimensions(locale, inputMatrix, inputTypes)
                
                calculationMatrixes.append(inputMatrix)
                calculationTypes.append(inputTypes)

            except Exception as err:
                api.logger.info(str(err))
                e = BadRequest(str(err))
                raise e
            
        # RETRIEVE ADDITIONAL PARAMS FOR ASSESSMENT
        params = np.array([args['params']][0], dtype='object') if len(args['params']) > 0 else None

        try:
            results = get_calculation_results(calculationMatrixes, extensions, calculationTypes, method, params, methodCorrelations, methodRankings, rankingCorrelations, locale)
            return results
        except Exception as err: 
            api.logger.info(f'{get_error_message(locale, "assessment-error")}  {err}')
            e = BadRequest(str(err))
            raise e
        