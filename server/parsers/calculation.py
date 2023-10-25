from flask_restx import reqparse

from models.calculations import get_request_calculation_model

def get_request_calculation_parser():
    def my_type(data):
        '''Parse my type'''

        required_keys = ['id', 'node_type', 'extension', 'connections_from', 'connections_to', 'position_x', 'position_y']
        optional_keys = ['matrix', 'criteria_types', 'method', 'weights', 'kwargs']

        if len(data) == 0:
            # TODO: return error from dict of errors
            raise ValueError('Empty data object given')

        for node_idx, node in enumerate(data):
            required_set = set(required_keys)
            keys_set = set(node.keys())

            if not required_set.issubset(keys_set):
                missing_keys = [key for key in required_set if key not in keys_set]
                raise ValueError(f"Not all required keys are given. Missing keys: '{missing_keys}'. Check the element at index {node_idx}")

            optional_set = set(optional_keys)
            difference_set = keys_set.difference(required_set)
            union_set = optional_set.union(difference_set)

            if len(union_set) > len(optional_set):

                # TODO: return error from dict of errors
                # show which index of node and what key is not allowed
                raise ValueError('Not allowed keys used')
            
        return data

    parser = reqparse.RequestParser()
    parser.add_argument('locale', location='headers', required=True)
    # parser.add_argument('data', required=True, type=list, location='json')
    parser.add_argument('data', required=True, type=my_type, location='json')
    # parser.add_argument('data', required=True, type=get_request_calculation_model, location='json')
    

    # # Swagger documentation
    # my_type.__schema__ = {'type': 'array', 'items': {
    #     'id': {'type': 'integer', "example": "1", 'description': 'The type of your custom format'},
    #     'node_type': {'type': 'string', "example": "matrix", 'description': 'A description of your custom format'}
    # }}

    # my_type.__schema__ = {
    #       'type': 'array',
    #         'items': {
    #             'type': 'object',
    #             'properties': {
    #                 'field1': {'type': 'string'},
    #                 'field2': {'type': 'integer'},
    #             },
    #             'required': ['field1', 'field2']
    #         }
    #     }
    
    return parser


