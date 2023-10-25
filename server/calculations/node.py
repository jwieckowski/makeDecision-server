# Copyright (C) Jakub Więckowski 2023

from abc import ABC
import numpy as np
from pymcdm.helpers import correlation_matrix

# CONST
from methods import weights_methods, mcda_methods, correlation_methods

# HELPERS
from .parameters import get_parameters

class Node(ABC):
    def __init__(self, id, node_type, extension, connections_from, connections_to, position_x, position_y) -> None:
        self.id = id
        self.node_type = node_type
        self.extension = extension.lower()
        if self.extension not in ['crisp', 'fuzzy']:
            raise ValueError(f"Extension '{self.extension}' not found")
        self.connections_from = connections_from
        self.connections_to = connections_to
        self.position_x = position_x
        self.position_y = position_y

    def get_response(self):
        return {
            "id": self.id,
            "node_type": self.node_type,
            "extension": self.extension,
        }

class MatrixNode(Node):
    def __init__(self, id, node_type, extension, connections_from, connections_to, position_x, position_y, matrix, criteria_types, method) -> None:
        
        super().__init__(id, node_type, extension, connections_from, connections_to, position_x, position_y)

        self.matrix = np.array(matrix)
        self.method = method.upper()
        self.criteria_types = np.array(criteria_types)

    def get_response(self):
        response = super().get_response()
        
        return response | {
            "method": self.method,
            "data": [
                {
                    "matrix": self.matrix.tolist(),
                    "criteria_types": self.criteria_types.tolist(),
                }
            ]
        }

class WeightsNode(Node):
    def __init__(self, id, node_type, extension, connections_from, connections_to, position_x, position_y, weights, method) -> None:
        
        super().__init__(id, node_type, extension, connections_from, connections_to, position_x, position_y)

        self.weights = np.array(weights)
        self.method = method.upper()
        if self.method != 'INPUT' and self.method not in list(weights_methods.keys()):
            raise ValueError(f"Method '{self.method}' not found")
            
        self.calculation_data = []

    def calculate(self, matrix_node, precision=3):
        if self.method != 'INPUT':
            self.method_obj = weights_methods[self.method][self.extension]
            
            kwargs = {
                'matrix': matrix_node.matrix
            }

            if self.method in ['MEREC', 'CILOS', 'IDOCRIW']:
                kwargs = kwargs | {"types": matrix_node.criteria_types}
            
            weights = np.round(self.method_obj(**kwargs), precision)
        else:
            weights = self.weights

        if len([data for data in self.calculation_data if data['matrix_id'] == matrix_node.id]) == 0:
            self.calculation_data.append({
                "matrix_id": matrix_node.id,
                "weights": weights.tolist(),
            })
        
        return weights
    
    def get_response(self):
        response = super().get_response()

        return response | {
            "method": self.method,
            "data": self.calculation_data
        }

class MethodNode(Node):
    def __init__(self, id, node_type, extension, connections_from, connections_to, position_x, position_y, method, kwargs) -> None:
        
        super().__init__(id, node_type, extension, connections_from, connections_to, position_x, position_y)

        self.method = method.upper()
        if self.method not in list(mcda_methods.keys()):
            raise ValueError(f"Method '{self.method}' not found")
            
        self.kwargs = kwargs
        self.calculation_data = []

    def calculate(self, matrix_node, weights_node, precision=3):

        criteria_weights = weights_node.calculate(matrix_node)
        init_kwargs = get_parameters(self.kwargs, self.extension, matrix_node, criteria_weights)
        method_obj = mcda_methods[self.method][self.extension](**init_kwargs)
        pref = np.round(method_obj(matrix_node.matrix, criteria_weights, matrix_node.criteria_types), precision)

        self.calculation_data.append({
            "matrix_id": matrix_node.id,
            "method_obj": method_obj,
            "weights_node": weights_node,
            "preference": pref.tolist(),
            "kwargs": self.kwargs
        })

        return pref

    def rank(self, matrix_id):

        # TODO: handle if error
        data = [data for data in self.calculation_data if data['matrix_id'] == matrix_id][0]
        if self.extension == 'crisp':
            ranking = data['method_obj'].rank(data['preference'])
        elif self.extension == 'fuzzy':
            ranking = data['method_obj'].rank()
        
        return ranking, data

    def get_response(self):
        response = super().get_response()

        data = []
        for cdata in self.calculation_data:
            data.append({
                "matrix_id": cdata['matrix_id'],
                "weights_method": cdata['weights_node'].method,
                "preference": cdata['preference'],
                "kwargs": cdata['kwargs']
            })

        return response | {
            "method": self.method,
            "data": data
        }

class RankingNode(Node):
    def __init__(self, id, node_type, extension, connections_from, connections_to, position_x, position_y, **kwargs) -> None:
        
        super().__init__(id, node_type, extension, connections_from, connections_to, position_x, position_y)

        self.calculation_data = []

    def calculate(self, method_node, matrix_node):
        
        ranking, data = method_node.rank(matrix_node.id)

        self.calculation_data.append({
            "matrix_id": matrix_node.id,
            "method": method_node.method,
            "weights": data['weights_node'].method,
            "ranking": ranking,
            "kwargs": data['kwargs']
        })

        return ranking

    def get_response(self):
        response = super().get_response()

        return response | {
            "data": self.calculation_data
        }


class CorrelationNode(Node):
    def __init__(self, id, node_type, extension, connections_from, connections_to, position_x, position_y, method) -> None:
        
        super().__init__(id, node_type, extension, connections_from, connections_to, position_x, position_y)
        
        self.method = method.upper()
        if self.method not in list(correlation_methods.keys()):
            raise ValueError(f"Method '{self.method}' not found")
            
        self.calculation_data = []

    def _calculate_correlation(self, nodes, node_type, matrix_id):
        corr_data, corr_labels = [], []

        data_field = node_type
        if node_type == 'method':
            data_field = 'preference'

        filtered_nodes = [node for node in nodes if node.node_type == node_type]
        if len(filtered_nodes) > 0:
            for node in filtered_nodes:
                for data in node.calculation_data:
                    if data['matrix_id'] == matrix_id:
                        corr_data.append(data[data_field])
                        if data_field == 'ranking':
                            corr_labels.append(data['method'])
                        else:
                            corr_labels.append(node.method)

        return corr_data, corr_labels

    def calculate(self, nodes, matrix_node, precision=3):

        corr_matrix = []

        for node_type in ['weights', 'method', 'ranking']:
            corr_data, corr_labels = self._calculate_correlation(nodes, node_type, matrix_node.id)

            if len(corr_data) > 0:
                correlation_obj = correlation_methods[self.method]

                corr_matrix = np.round(correlation_matrix(np.array(corr_data), correlation_obj), precision)
                
                self.calculation_data.append({
                    "matrix_id": matrix_node.id,
                    "correlation": corr_matrix.tolist(),
                    "labels": corr_labels
                })  

        return corr_matrix if len(corr_matrix) > 0 else []

    def get_response(self):
        response = super().get_response()

        return response | {
            "method": self.method,
            "data": self.calculation_data
        }

