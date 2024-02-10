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
            print(node)
            required_set = set(required_keys)
            keys_set = set(node.keys())

            if not required_set.issubset(keys_set):
                missing_keys = [key for key in required_set if key not in keys_set]
                raise ValueError(f"Not all required keys are given. Missing keys: '{missing_keys}'. Check the element at index {node_idx}")

            optional_set = set(optional_keys)
            difference_set = keys_set.difference(required_set)
            union_set = optional_set.union(difference_set)

            if len(union_set) > len(optional_set):

                bad_keys = union_set.difference(optional_keys)
                raise ValueError(f'Not allowed keys used: {list(bad_keys)}. Check the element at index {node_idx}')
            
        return data

    parser = reqparse.RequestParser()
    parser.add_argument('locale', location='headers', required=True)
    parser.add_argument('data', required=True, type=my_type, location='json')

    return parser

def get_kwargs_items_parser():
    parser = reqparse.RequestParser()
    parser.add_argument('locale', location='headers', required=True)
    parser.add_argument('method', type=str, location='json', required=True)

    return parser