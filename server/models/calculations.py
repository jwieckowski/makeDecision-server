from flask_restx import fields

def get_request_calculation_model(api):

    node_item = api.model('Node', {
        "id": fields.Integer(description='Node id', example='1'),
        "node_type": fields.String(description="Type of node", example="matrix"),
        "extension": fields.String(description="Type of data for calculations", example="crisp"),
        "connections_from": fields.List(fields.Integer, description="List of id of nodes from which a given node has connections", example="2"),
        "connections_to": fields.List(fields.Integer, description="List of id of nodes to which a given not is connected to", example="3"),
        "position_x": fields.Integer(description="Position x of node in the GUI application", example="10"),
        "position_y": fields.Integer(description="Position y of node in the GUI application", example="10"),
    })

    data_model = api.model('Data', {
        "data": fields.List(fields.Nested(node_item))
    })

    return data_model

def get_response_calculation_model(api):
    kwargs_item = api.model('Kwargs', {
        "matrix_id": fields.Integer(description="ID of matrix used to calculate results within the node"),
        "normalization_function": fields.String(description=""),
        'cvalues': fields.List(fields.List(fields.Raw()), description=''),
        "expert_function": fields.String(description=""),
        "ref_point": fields.List(fields.Raw(), description=''),
        "lam": fields.Float(description=''),
        "alpha": fields.Float(description=''),
        "sPROBID": fields.Boolean(description=''),
        "preference_function": fields.String(description=''),
        'bounds': fields.List(fields.List(fields.Raw()), description=''),
        "ref_ideal": fields.List(fields.Raw(), description=''),
        'esp': fields.List(fields.List(fields.Raw()), description=''),
    })

    data_item = api.model('ResponseNodeData', {
        "matrix_id": fields.Integer(description="ID of matrix used to calculate results within the node"),
        'matrix': fields.List(fields.List(fields.Raw()), description='2D matrix with data represented as floats for crisp data and 3D matrix with strings in cells for fuzzy data', skip_none=True),
        'criteria_types': fields.List(fields.Integer(), description="1D array of criteria types containing -1 for cost type and 1 for profit criteria", skip_none=True),
        "weights": fields.List(fields.Raw(), description='1D array of crisp criteria weights or 2D array of fuzzy criteria weights', skip_none=True),
        "weights_method": fields.String(description='Method used to calculate criteria weights', skip_none=True),
        "preference": fields.List(fields.Float(), description='Calculated preferences of alternatives', skip_none=True),
        "kwargs": fields.List(fields.Nested(kwargs_item, skip_none=True), description='Additional parameters used for MCDA methods initialization'),
        "ranking": fields.List(fields.Integer(), description='1D array of ranking of alternatives', skip_none=True),
        "correlation": fields.List(fields.List(fields.Float()), description='2D array of calculated correlation values', skip_none=True),
        "labels": fields.List(fields.String(), description="1D array of labels to represent correlation of the compared methods"),
        "img": fields.String(description='')
    })

    node_item = api.model('ResponseNode', {
        "id": fields.Integer(description='Node id', example='1'),
        "node_type": fields.String(description="Type of node", example="matrix"),
        "extension": fields.String(description="Type of data for calculations", example="crisp"),
        "method": fields.String(description="Type of method used for node data processing", example="crisp"),
        "data": fields.List(fields.Nested(data_item, skip_none=True)),
    })

    response_model = api.model('ResponseModel', {
        'response': fields.List(fields.Nested(node_item))
    })

    return response_model
