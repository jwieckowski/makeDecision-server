# Copyright (C) Jakub Więckowski 2023 - 2024

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
            elif node_type == 'visualization':
                nodes.append(VisualizationNode(**node))
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
            'weights': ['method', 'correlation', 'visualization'],
            'method': ['ranking', 'correlation'],
            'ranking': ['correlation', 'visualization'],
            "correlation": ['visualization'],
            "visualization": []
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
        print('Matrix nodes')
        print(matrix_nodes)
        
        calculated_input_ranks_id = []

        # second step - get weights for matrices
        for matrix_node in matrix_nodes:
            
            weights_nodes = self._get_connected_nodes(matrix_node)

            if len(weights_nodes) == 0:
                raise ValueError(f'No blocks were connected to matrix with ID {matrix_node.id}')

            print('Weights nodes')
            print(weights_nodes)

            for weights_node_idx, weights_node in enumerate(weights_nodes):
                if weights_node is None:
                    raise ValueError(f'Weights block with ID {matrix_node.connections_to[weights_node_idx]} not found')
                
                # Validate input weights
                if weights_node.method == 'INPUT':
                    validate_user_weights(self.locale, weights_node, matrix_node.extension)
                
                methods_nodes = self._get_connected_nodes(weights_node, node_type='method')
                
                # if len(methods_nodes) == 0:
                #     raise ValueError(f'No blocks were connected to weights with ID {weights_node.id}')

                print('Methods nodes')
                print(methods_nodes)

                # only weights given
                if len(methods_nodes) == 0:
                    weights_node.calculate(matrix_node)
                else:
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
                            
                            ranking_node.calculate(method_node, matrix_node, weights_node)
                            # for input nodes
                            ranking_connected_nodes = [input_node for input_node in self._get_connected_nodes(ranking_node, output=False) if input_node.method.lower() == 'input']

                            if len(set([*[len(data['ranking']) for data in ranking_node.calculation_data], *[len(input_pref.kwargs[0]['preference']) for input_pref in ranking_connected_nodes]])) > 1:
                                raise ValueError(f'Data for ranking calculation should have the same size')

                            if len(ranking_connected_nodes) > 0:
                                for input_ranking_node in ranking_connected_nodes:
                                    if input_ranking_node.id not in calculated_input_ranks_id:
                                        calculated_input_ranks_id.append(input_ranking_node.id)
                                        RankingNode.calculate_input(input_ranking_node, ranking_node, matrix_node.id)

                        
            # CORRELATION FROM MATRIX
            correlation_nodes = self._find_node_by_type('correlation')
            for correlation_node in correlation_nodes:
                connected_nodes = self._get_connected_nodes(correlation_node, output=False)
                print('correlation connected nodes')
                print(connected_nodes)
                correlation_node.calculate(connected_nodes, matrix_node)

            # VISUALIZATIONS FROM MATRIX
            visualization_nodes = self._find_node_by_type('visualization')
            for visualization_node in visualization_nodes:
                connected_nodes = self._get_connected_nodes(visualization_node, output=False)

                visualization_node.generate(connected_nodes, matrix_node)
        response = self._create_response()
        return response