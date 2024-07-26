from flask_restx import fields

def get_survey_usage_model(api):
    """
    Defines the model for representing survey usage data, including options and their details.

    Parameters
    ----------
    api : flask_restx.Api
        The Flask-RESTX API instance.

    Returns
    -------
    flask_restx.Model
        The data model for the response containing survey usage details.
    """
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
    """
    Defines the model for representing individual items in survey usage results.

    Parameters
    ----------
    api : flask_restx.Api
        The Flask-RESTX API instance.

    Returns
    -------
    flask_restx.Model
        The data model for the response containing survey usage results.
    """
    results_item = api.model('ResultsSurveyUsageItem', {
        'id': fields.Integer(description='Answer ID'),
        'option': fields.String(description='Answer option'),
        'name': fields.String(description='Answer name'),
    })

    response_item = api.model('ResultsSurveyUsage', {
        "response": fields.Nested(results_item)
    })

    return response_item

def get_survey_rating_items(api):
    """
    Defines the model for representing individual items in survey rating results.

    Parameters
    ----------
    api : flask_restx.Api
        The Flask-RESTX API instance.

    Returns
    -------
    flask_restx.Model
        The data model for the response containing survey rating results.
    """
    results_item = api.model('ResultsSurveyRatingItem', {
        'id': fields.Integer(description='Answer ID'),
        'helpful': fields.String(description='Rating aspect name'),
        'easyInterface': fields.String(description='Rating aspect name'),
        'changeSuggestion': fields.String(description='Rating aspect name'),
        'easeOfUse': fields.Integer(description='Rating aspect name'),
        'overallRating': fields.Integer(description='Rating aspect name'),
        'features': fields.String(description='Rating aspect name'),
    })

    response_item = api.model('ResultsSurveyRating', {
        "response": fields.Nested(results_item)
    })

    return response_item
