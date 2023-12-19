from flask_restx import fields

def get_dictionary_model(api):
    dictionary_additional_data_item_model = api.model("AdditionalDataItem", {
        "id": fields.Integer(description='Element id'),
        "method": fields.String(description="Name of technique used in Multi-Criteria Decision Analysis method for additional measures"),
        "parameter": fields.String(description='Name of parameter used in evaluations package in Python'),
        "default": fields.String(description='Default technique used in Multi-Criteria Decision Analysis method calculation for given parameter'),
        "type": fields.String(description='Type of parameters to represent graphically in GUI'),
        "min": fields.Float(description='Optional, minimum acceptable value of types (input, array)', skip_none=True),
        "max": fields.Float(description='Optional, maximum acceptable value of types (input, array)', skip_none=True),
        "dimension": fields.Integer(description='Optional, dimension of array type', skip_none=True),
        "required": fields.Boolean(description='Optional, information about array data required', skip_none=True)
    })

    dictionary_additional_data_model = api.model("AdditionalData", {
        "extension": fields.String(description="Data type representation"),
        "data": fields.List(fields.Nested(dictionary_additional_data_item_model, skip_none=True))
    })

    dictionary_data_model = api.model('DictionaryData', {
        "id": fields.Integer(description='Element id'),
        "name": fields.String(description='Name of method variant'),
        "abbreviation": fields.String(description='Full name of the method'),
        "extensions": fields.List(fields.String(description="Data type representation")),
        "order": fields.String(description="Order for ranking calculation"),
        "functionName": fields.String(description="Name of parameter used in evaluations package in Pythonn"),
        "inputConnections": fields.List(fields.String(description="List of methods type that can be used as the input data for the element")),
        "outputConnections": fields.List(fields.String(description="List of methods type that can be used as the output data for the element")),
        "kwargs": fields.List(fields.Nested(dictionary_additional_data_model, skip_none=True)),
        "hints": fields.String(description="Hints for user about how to use given method")
    })

    dictionary_model = api.model('Dictionary', {
        'id': fields.Integer(description='Element id'),
        "key": fields.String(description="Name of the method categories"),
        "label": fields.String(description="Label representing the variant of method categories used for visualization purposes"),
        "type": fields.String(description="Type of method category"),
        "function": fields.String(description="Information about the scope of items from category"),
        "data": fields.List(fields.Nested(dictionary_data_model, skip_none=True))
    })

    response_model = api.model('ResponseDictionary', {
        "response": fields.List(fields.Nested(dictionary_model))
    })
    return response_model