# Copyright (c) 2023 Jakub Więckowski

from flask_restx import Resource
import json

from config import dir_path

# PARSERS
from parsers import get_locale_parser

# MODELS
from models import get_description_model

# HELPERS
from helpers import validate_locale

# NAMESPACE
from .namespaces import v1 as api

# MODELS
description_model = get_description_model(api)

# ARGUMENTS PARSERS
locale_parser = get_locale_parser()

@api.route('/descriptions/methods')
class MethodsDescription(Resource):
    @api.expect(locale_parser)
    @api.marshal_list_with(description_model)
    def get(self):
        args = locale_parser.parse_args()
        locale = validate_locale(args['locale'])
        
        with open(dir_path+f'public/descriptions/methods-{locale}.json', encoding='utf-8') as file:
            data = json.load(file)
        
        return {
            "response": data
        }