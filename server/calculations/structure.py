# Copyright (C) Jakub Więckowski 2023

from .node import *

# VALIDATOR
from utils.validator import validate_user_weights


class CalculationStructure:
    def __init__(self, data, locale) -> None:
        self.nodes = CalculationStructure._create_nodes_structure(data) # array of calculationNode
        self.calculation_data = [] # results calculated for each node in the structure
        self.locale = locale # app language

    @staticmethod
    def _create_nodes_structure(data):
        nodes = []
        for node in data:
            node_type = node['node_type']
            if node_type == 'matrix':
                nodes.append(MatrixNode(**node))
            elif node_type == 'weights':
                nodes.append(WeightsNode(**node))
            elif node_type == 'method':
                nodes.append(MethodNode(**node))
            elif node_type == 'ranking':
                nodes.append(RankingNode(**node))
            elif node_type == 'correlation':
                nodes.append(CorrelationNode(**node))
            else:
                raise ValueError(f"Block type '{node_type}' not allowed. Check the block with ID {node['id']}")
        return nodes

    def _create_response(self):
        response = []
        for node in self.nodes:
            response.append(node.get_response())
        return response

    def _find_node_by_id(self, id):
        node = [n for n in self.nodes if n.id == id]
        return node[0] if len(node) > 0 else None    

    def _find_node_by_type(self, node_type):
        node = [n for n in self.nodes if n.node_type == node_type]
        return node if len(node) > 0 else [] 

    def _get_connected_nodes(self, node, node_type=None, output=True):
        if output:
            nodes = [self._find_node_by_id(id) for id in node.connections_to]
        else:
            nodes = [self._find_node_by_id(id) for id in node.connections_from]
        
        if node_type is not None:
            nodes = [node for node in nodes if node is not None and node.node_type == node_type]

        return nodes

    def _validate_connections(self):
        connections = {
            'matrix': ['weights'],
            'weights': ['method', 'correlation'],
            'method': ['ranking', 'correlation'],
            'ranking': ['correlation'],
            "correlation": []
        }
        for node in self.nodes:
            connected_nodes_types = [connected_node.node_type for connected_node in self._get_connected_nodes(node) if connected_node is not None]
            diff = set(connected_nodes_types).difference(set(connections[node.node_type]))
            if len(diff) > 0:
                return False, [node.node_type, list(diff)]

        return True, ''

    def calculate(self):
        # Validate connections
        flag, message = self._validate_connections()
        if not flag:
            raise ValueError(f'Connection structure is wrong. Check the connection between {message[0]} and {message[1]}')

        # first step - get matrices
        matrix_nodes = self._find_node_by_type('matrix')

        # second step - get weights for matrices
        for matrix_node in matrix_nodes:
            
            weights_nodes = self._get_connected_nodes(matrix_node)

            if len(weights_nodes) == 0:
                raise ValueError(f'No blocks were connected to matrix with ID {matrix_node.id}')


            for weights_node_idx, weights_node in enumerate(weights_nodes):
                if weights_node is None:
                    raise ValueError(f'Weights block with ID {matrix_node.connections_to[weights_node_idx]} not found')
                
                # Validate input weights
                if weights_node.method == 'INPUT':
                    validate_user_weights(self.locale, weights_node, matrix_node.extension)
                
                methods_nodes = self._get_connected_nodes(weights_node, node_type='method')
                
                if len(methods_nodes) == 0:
                    raise ValueError(f'No blocks were connected to weights with ID {weights_node.id}')

                # third step - calculate preferences
                for method_node_idx, method_node in enumerate(methods_nodes):
                    if method_node is None:
                        raise ValueError(f'Method block with ID {weights_node.connections_to[method_node_idx]} not found')
                    
                    method_node.calculate(matrix_node, weights_node)

                    # fourth.one step - calculate ranking
                    ranking_nodes = self._get_connected_nodes(method_node, node_type='ranking')

                    for ranking_node_idx, ranking_node in enumerate(ranking_nodes):
                        if ranking_node is None:
                            raise ValueError(f'Ranking block with ID {matrix_node.connections_to[ranking_node_idx]} not found')
                        
                        ranking_node.calculate(method_node, matrix_node)
                        
            # CORRELATION FROM MATRIX
            correlation_nodes = self._find_node_by_type('correlation')
            for correlation_node in correlation_nodes:
                connected_nodes = self._get_connected_nodes(correlation_node, output=False)
                
                correlation_node.calculate(connected_nodes, matrix_node)


        response = self._create_response()
        return response