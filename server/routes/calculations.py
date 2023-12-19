# Copyright (c) 2023 Jakub Więckowski

from flask_restx import Resource
from werkzeug.exceptions import BadRequest
import json

# CONST
from config import dir_path

# PARSERS
from parsers import get_request_calculation_parser, get_kwargs_items_parser

# MODELS
from models import get_response_calculation_model

# CALCULATIONS
from calculations.structure import CalculationStructure

# UTILS
from utils.generator import generate_method_items

# HELPERS
from helpers import validate_locale

# NAMESPACE
from .namespaces import v1 as api

# MODELS
response_calculation_model = get_response_calculation_model(api)

# ARGUMENTS PARSERS
calculation_parser = get_request_calculation_parser()
items_parser = get_kwargs_items_parser()

@api.route('/calculations/calculate')
class CalculationResults(Resource):
    # @api.expect(calculation_parser)
    # @api.marshal_with(response_calculation_model)
    def post(self):
        args = calculation_parser.parse_args()
        # ARGUMENTS
        locale = validate_locale(args['locale'])

        data = args['data']
        print(data)

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

@api.route('/calculations/items')
class CalculationResults(Resource):
    @api.expect(calculation_parser)
    # @api.marshal_with(response_calculation_model)
    def post(self):
        args = items_parser.parse_args()
        # ARGUMENTS
        locale = validate_locale(args['locale'])

        method = args['method']

        with open(dir_path+f'public/dictionary/all-methods-{locale}.json',  encoding='utf-8') as file:
            data = json.load(file)

        try:
            response = generate_method_items(method, data, locale)

            return {
                "response": response
            }

        except Exception as err:
            api.logger.info(str(err))
            e = BadRequest(str(err))
            raise e

