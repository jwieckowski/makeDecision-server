from flask_restx import fields

def get_description_model(api):
    """
    Defines the model for describing methods and their categories.

    Parameters
    ----------
    api : flask_restx.Api
        The Flask-RESTX API instance.

    Returns
    -------
    Model
        The data model for the response containing descriptions of methods and their categories.
    """
    description_item = api.model('Description', {
        'id': fields.Integer(description='Element id'),
        'text': fields.String(description="Description content")
    })

    method_data_item = api.model('MethodData', {
        "id": fields.Integer(description='Element id'),
        "name": fields.String(description="Name of the method"),
        "description": fields.List(fields.Nested(description_item))
    })

    methods_description_item = api.model('MethodsDescription', {
        "id": fields.Integer(description='Element id'),
        "key": fields.String(description="Name of the method categories"),
        "data": fields.List(fields.Nested(method_data_item))
    })

    response_model = api.model('ResponseDescription', {
        "response": fields.List(fields.Nested(methods_description_item))
    })
    return response_model