# Copyright (c) 2023 - 2024 Jakub Więckowski

from flask_restx import Resource
import json

from config import dir_path

# PARSERS
from parsers import get_locale_parser, get_survey_usage_parser, get_survey_rating_parser

# DB
from db import get_mongo_db

# MODELS
from models import get_survey_usage_model, get_survey_usage_items, get_survey_rating_items

# HELPERS
from helpers import validate_locale

# NAMESPACE
from .namespaces import v1 as api

# MODELS
survey_usage_model = get_survey_usage_model(api)
survey_usage_response = get_survey_usage_items(api)
survey_rating_response = get_survey_rating_items(api)

# ARGUMENTS PARSERS
locale_parser = get_locale_parser()
survey_usage_parser = get_survey_usage_parser()
survey_rating_parser = get_survey_rating_parser()

@api.route('/surveys/usage-survey')
class SurveysUsage(Resource):
    @api.expect(locale_parser)
    @api.marshal_with(survey_usage_model)
    def get(self):

        args = locale_parser.parse_args()
        locale = validate_locale(args['locale'])
        
        with open(dir_path+f'public/surveys/usage-{locale}.json',  encoding='utf-8') as file:
            data = json.load(file)
        
        return {
            "response": data
        }

@api.route('/surveys/usage')
class SurveysUsageData(Resource):
    @api.marshal_with(survey_usage_response)
    def get(self):
        db = get_mongo_db()
        result = db.get_usage_survey_results()
        
        return {
            "response": result
        }

    @api.expect(survey_usage_parser)
    def post(self):
        args = survey_usage_parser.parse_args()
        option = args['option']
        name = args['name']
        
        db = get_mongo_db()
        result = db.add_usage_survey_item(option, name)
        
        return {
            "response": result
        }

@api.route('/surveys/rating')
class SurveysRatingData(Resource):
    @api.marshal_with(survey_rating_response)
    def get(self):
        db = get_mongo_db()
        result = db.get_rating_survey_results()
        
        return {
            "response": result
        }

    @api.expect(survey_rating_parser)
    def post(self):
        args = survey_rating_parser.parse_args()
        survey_item = {
            "helpful": args['helpful'],
            "easyInterface": args['easyInterface'],
            "changeSuggestion": args['changeSuggestion'],
            "easeOfUse": args['easeOfUse'],
            "overallRating": args['overallRating'],
            "features": args['features'],
        }
        
        db = get_mongo_db()
        result = db.add_rating_survey_item(survey_item)
        
        return {
            "response": result
        }