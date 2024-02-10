from flask_restx import fields

def get_survey_usage_model(api):
    base_option_item = api.model('baseOptionItem', {
        'id': fields.Integer(description='Option ID'),
        'label': fields.String(description='Option label'),
        "name": fields.String(description='Option name unified for all languages'),
        'type': fields.String(description='Option type'),
    })

    complex_option_item = api.model('complexOptionItem', {
        'id': fields.Integer(description='Option ID'),
        'label': fields.String(description='Option label'),
        'type': fields.String(description='Option type'),
        "name": fields.String(description='Option name unified for all languages'),
        "title": fields.String(description='Sub-option label', skip_none = True),
        "options": fields.List(fields.Nested(base_option_item, skip_none=True))
    })

    usage_item = api.model('surveyUsage', {
        'title': fields.String(description="Type of data for calculations"),
        'options': fields.List(fields.Nested(complex_option_item, skip_none=True))
    })

    response_item = api.model('ResponseSurveyUsage', {
        "response": fields.Nested(usage_item)
    })

    return response_item


def get_survey_usage_items(api):
    results_item = api.model('ResultsSurveyUsageItem', {
        'id': fields.Integer(description='Answer ID'),
        'option': fields.String(description='Answer option'),
        'name': fields.String(description='Answer name'),
    })

    response_item = api.model('ResultsSurveyUsage', {
        "response": fields.Nested(results_item)
    })

    return response_item
