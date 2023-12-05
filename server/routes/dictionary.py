# Copyright (c) 2023 Jakub Więckowski

from flask_restx import Resource
import json

from config import dir_path

# PARSERS
from parsers import get_locale_parser

# MODELS
from models import get_dictionary_model

# HELPERS
from helpers import validate_locale

# NAMESPACE
from .namespaces import v1 as api

# MODELS
dictionary_model = get_dictionary_model(api)

# ARGUMENTS PARSERS
locale_parser = get_locale_parser()

@api.route('/dictionary/all-methods')
class AllMethodsDictionary(Resource):
    @api.expect(locale_parser)
    @api.marshal_with(dictionary_model)
    def get(self):
        args = locale_parser.parse_args()
        locale = validate_locale(args['locale'])
        
        with open(dir_path+f'public/dictionary/all-methods-{locale}.json',  encoding='utf-8') as file:
            data = json.load(file)

        # filtering keys
        # filters = ['Visualization']
        # data = [d for d in data if d['key'] not in filters]
        
        return {
            "response": data
        }
