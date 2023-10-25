# Copyright (c) 2023 Jakub Więckowski

from flask_restx import Resource
from werkzeug.exceptions import BadRequest

# PARSERS
from parsers import get_request_calculation_parser

# MODELS
from models import get_response_calculation_model

# CALCULATIONS
from calculations.structure import CalculationStructure

# HELPERS
from helpers import validate_locale

# NAMESPACE
from .namespaces import v1 as api

# MODELS
response_calculation_model = get_response_calculation_model(api)

# ARGUMENTS PARSERS
calculation_parser = get_request_calculation_parser()

@api.route('/calculations/calculate')
class CalculationResults(Resource):
    @api.expect(calculation_parser)
    @api.marshal_with(response_calculation_model, skip_none=True)
    def post(self):
        args = calculation_parser.parse_args()
        # ARGUMENTS
        locale = validate_locale(args['locale'])
        data = args['data']

        try:
            # CALCULATE
            calculation = CalculationStructure(data, locale)
            response = calculation.calculate()

            return {
                "response": response
            }

        except Exception as err:
            api.logger.info(str(err))
            e = BadRequest(str(err))
            raise e