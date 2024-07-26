# Copyright (C) Jakub Więckowski 2023 - 2024

from .node import *

# VALIDATOR
from utils.validator import validate_user_weights
from utils.errors import get_error_message

class CalculationStructure:
    def __init__(self, data, locale) -> None:
        """
        Initializes the CalculationStructure object.

        Parameters
        ----------
        data : list
            List of node data dictionaries to create the structure.
        locale : str
            User application language.
        """
        self.nodes = CalculationStructure._create_nodes_structure(data, locale) # array of calculationNode
        self.calculation_data = [] # results calculated for each node in the structure
        self.locale = locale # app language

    @staticmethod
    def _create_nodes_structure(data, locale):
        """
        Creates the nodes structure from provided data.

        Parameters
        ----------
        data : list
            List of node data dictionaries to create the structure.
        locale : str
            User application language.

        Returns
        -------
        list
            List of nodes created based on the provided data.

        Raises
        ------
        ValueError
            If an invalid node type is encountered.
        """
        nodes = []
        for node in data:
            node_type = node['node_type']
            if node_type == 'matrix':
                nodes.append(MatrixNode(**node, locale=locale))
            elif node_type == 'weights':
                nodes.append(WeightsNode(**node, locale=locale))
            elif node_type == 'method':
                nodes.append(MethodNode(**node, locale=locale))
            elif node_type == 'ranking':
                nodes.append(RankingNode(**node, locale=locale))
            elif node_type == 'correlation':
                nodes.append(CorrelationNode(**node, locale=locale))
            elif node_type == 'visualization':
                nodes.append(VisualizationNode(**node, locale=locale))
            else:
                raise ValueError(f"'{node_type}'{get_error_message(locale, 'block-type-error')} {node['id']}")
        return nodes

    def _create_response(self):
        """
        Creates a response from the calculated data of each node.

        Returns
        -------
        list
            List of responses from each node.
        """
        response = []
        for node in self.nodes:
            response.append(node.get_response())
        return response

    def _find_node_by_id(self, id):
        """
        Finds a node by its ID.

        Parameters
        ----------
        id : str
            The ID of the node to find.

        Returns
        -------
        object
            The node object with the specified ID, or None if not found.
        """
        node = [n for n in self.nodes if n.id == id]
        return node[0] if len(node) > 0 else None    

    def _find_node_by_type(self, node_type, node_method = None):
        """
        Finds nodes by their type and optionally by method.

        Parameters
        ----------
        node_type : str
            The type of the node to find.
        node_method : str, optional
            The method of the node to find (default is None).

        Returns
        -------
        list
            List of nodes with the specified type and method.
        """
        node = [n for n in self.nodes if n.node_type == node_type]
        if node_method:
            node = [n for n in node if n.method.lower() == node_method]
        return node if len(node) > 0 else [] 

    def _get_connected_nodes(self, node, node_type=None, output=True):
        """
        Retrieves nodes connected to a given node.

        Parameters
        ----------
        node : object
            The node to find connections for.
        node_type : str, optional
            The type of nodes to filter by (default is None).
        output : bool, optional
            If True, retrieves nodes connected to the output, otherwise retrieves nodes connected from the input (default is True).

        Returns
        -------
        list
            List of connected nodes, optionally filtered by type.
        """
        if output:
            nodes = [self._find_node_by_id(id) for id in node.connections_to]
        else:
            nodes = [self._find_node_by_id(id) for id in node.connections_from]
        
        if node_type is not None:
            nodes = [node for node in nodes if node is not None and node.node_type == node_type]

        return nodes

    def _validate_connections(self):
        """
        Validates the connections between nodes.

        Returns
        -------
        tuple
            (bool, str) indicating whether the connections are valid and any error messages.

        Raises
        ------
        ValueError
            If invalid connections are found.
        """
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
        """
        Executes the calculation process for the structure.

        Raises
        ------
        ValueError
            If any validation or calculation error occurs.

        Returns
        -------
        list
            The calculation results.
        """
        # Validate connections
        flag, message = self._validate_connections()
        if not flag:
            raise ValueError(f'{get_error_message(self.locale, "connection-structure-error")} ({message[0]}, {message[1]})')

        # first step - get matrices
        matrix_nodes = self._find_node_by_type('matrix')

        if len(matrix_nodes) > 0:
            calculated_input_ranks_id = []

            # second step - get weights for matrices
            for matrix_node in matrix_nodes:
                
                weights_nodes = self._get_connected_nodes(matrix_node)

                if len(weights_nodes) == 0:
                    raise ValueError(f'{get_error_message(self.locale, "matrix-no-connections")} {matrix_node.id}')

                for weights_node in weights_nodes:
                    if weights_node is None:
                        raise ValueError(f'{get_error_message(self.locale, "weights-not-found")} {matrix_node.id}')
                    
                    # Validate input weights
                    if weights_node.method == 'INPUT':
                        validate_user_weights(self.locale, weights_node, matrix_node.extension)
                    
                    methods_nodes = self._get_connected_nodes(weights_node, node_type='method')
                
                    # only weights given
                    if len(methods_nodes) == 0:
                        weights_node.calculate(matrix_node)
                    else:
                        # third step - calculate preferences
                        for method_node_idx, method_node in enumerate(methods_nodes):
                            if method_node is None:
                                raise ValueError(f'{get_error_message(self.locale, "method-not-found")} {weights_node.connections_to[method_node_idx]}')
                            
                            method_node.calculate(matrix_node, weights_node)

                            # fourth.one step - calculate ranking
                            ranking_nodes = self._get_connected_nodes(method_node, node_type='ranking')

                            for ranking_node_idx, ranking_node in enumerate(ranking_nodes):
                                if ranking_node is None:
                                    raise ValueError(f'{get_error_message(self.locale, "ranking-not-found")} {matrix_node.connections_to[ranking_node_idx]}')
                                
                                ranking_node.calculate(method_node, matrix_node, weights_node)
                                # for input nodes
                                ranking_connected_nodes = [input_node for input_node in self._get_connected_nodes(ranking_node, output=False) if input_node.method.lower() == 'input']

                                if len(set([*[len(data['ranking']) for data in ranking_node.calculation_data], *[len(input_pref.kwargs[0]['preference']) for input_pref in ranking_connected_nodes]])) > 1:
                                    raise ValueError(f'{get_error_message(self.locale, "ranking-calculation-size")}')

                                if len(ranking_connected_nodes) > 0:
                                    for input_ranking_node in ranking_connected_nodes:
                                        if input_ranking_node.id not in calculated_input_ranks_id:
                                            calculated_input_ranks_id.append(input_ranking_node.id)
                                            RankingNode.calculate_input(input_ranking_node, ranking_node, matrix_node.id)

                            
                # CORRELATION FROM MATRIX
                correlation_nodes = self._find_node_by_type('correlation')
                for correlation_node in correlation_nodes:
                    connected_nodes = self._get_connected_nodes(correlation_node, output=False)
                    correlation_node.calculate(connected_nodes, matrix_node)

                # VISUALIZATIONS FROM MATRIX
                visualization_nodes = self._find_node_by_type('visualization')
                for visualization_node in visualization_nodes:
                    connected_nodes = self._get_connected_nodes(visualization_node, output=False)

                    visualization_node.generate(connected_nodes, matrix_node)
        else:
            # input preferences
            user_prefs_nodes = self._find_node_by_type('method', 'input')
            for user_pref_node in user_prefs_nodes:
                user_pref_node.calculate(None, None)
                rankings_of_user_prefs = self._get_connected_nodes(user_pref_node, node_type='ranking') 
                if len(rankings_of_user_prefs) > 0:
                    rankings_of_user_prefs[0].calculate(user_pref_node)

            # input rankings
            user_ranks_nodes = self._find_node_by_type('ranking', 'input')
            for user_rank_node in user_ranks_nodes:
                user_rank_node.get_input_rank()

            # CORRELATION
            correlation_nodes = self._find_node_by_type('correlation')
            for correlation_node in correlation_nodes:
                connected_nodes = self._get_connected_nodes(correlation_node, output=False)
                correlation_node.calculate(connected_nodes)

            # VISUALIZATION
            visualization_nodes = self._find_node_by_type('visualization')
            for visualization_node in visualization_nodes:
                connected_nodes = self._get_connected_nodes(visualization_node, output=False)
                visualization_node.generate(connected_nodes)

        response = self._create_response()
        return response