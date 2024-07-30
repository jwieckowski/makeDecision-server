from flask_restx import fields

def get_matrix_model(api):
    """
    Defines the model for representing matrix data and its related attributes.

    Parameters
    ----------
    api : flask_restx.Api
        The Flask-RESTX API instance.

    Returns
    -------
    flask_restx.Model
        The data model for the response containing matrix data and related attributes.
    """
    matrix_item = api.model('Matrix', {
        'matrix': fields.List(fields.List(fields.Raw()), description='2D Matrix with data represented as floats for crisp data and 3D matrix with strings in cells for fuzzy data'),
        'criteria_types': fields.List(fields.Integer(description="1D array of criteria types containing -1 for cost type and 1 for profit criteria")),
        'extension': fields.String(description="Type of data for calculations"),
    })

    response_item = api.model('ResponseMatrix', {
        "response": fields.Nested(matrix_item)
    })

    return response_item