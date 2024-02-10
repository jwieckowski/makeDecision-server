# Copyright (C) Jakub Więckowski 2023 - 2024

from abc import ABC
import numpy as np
from pymcdm.helpers import correlation_matrix, rrankdata

# CONST
from methods import weights_methods, mcda_methods, correlation_methods
from graphs import graphs_methods, generate_graph

# HELPERS
from .parameters import get_parameters, get_call_kwargs

class Node(ABC):
    def __init__(self, id, node_type, extension, connections_from, connections_to, position_x, position_y) -> None:
        self.id = id
        self.node_type = node_type.lower()
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

        try:
            if ',' in matrix[0][0]:
                matrix = [[col.split(',') for col in row] for row in matrix]
        except:
            raise ValueError(f'Error in matrix node ({self.id}). Check the format of matrix.')
        self.matrix = np.array(matrix, dtype=float)
        self.method = method.upper()
        self.criteria_types = np.array(criteria_types, dtype=float)

    def _convert_matrix_to_string(self):
        str_matrix = []
        if np.array(self.matrix).ndim == 3:
            str_matrix = [[', '.join([str(c) for c in col]) for col in row] for row in self.matrix]
        else:
            str_matrix = np.array(self.matrix, dtype=str).tolist()

        return str_matrix

    def get_response(self):
        response = super().get_response()
        
        return response | {
            "method": self.method,
            "data": [
                {
                    "matrix": self._convert_matrix_to_string(),
                    "criteria_types": self.criteria_types.tolist(),
                }
            ]
        }

class WeightsNode(Node):
    def __init__(self, id, node_type, extension, connections_from, connections_to, position_x, position_y, weights, method) -> None:
        
        super().__init__(id, node_type, extension, connections_from, connections_to, position_x, position_y)

        self.weights = np.array(weights, dtype=float)
        self.method = method.upper()
        if self.method != 'INPUT' and self.method not in list(weights_methods.keys()):
            raise ValueError(f"Method '{self.method}' not found")
            
        self.calculation_data = []

    def calculate(self, matrix_node, precision=3):
        print(self.method)
        if self.method != 'INPUT':
            try: 
                self.method_obj = weights_methods[self.method][matrix_node.extension]
                
                print('matrix')
                print(matrix_node.matrix)
                kwargs = {
                    'matrix': matrix_node.matrix
                }

                print('criteria types')
                print(matrix_node.criteria_types)
                if self.method in ['MEREC', 'CILOS', 'IDOCRIW']:
                    kwargs = kwargs | {"types": matrix_node.criteria_types}
                
                print(kwargs)
                weights = np.round(self.method_obj(**kwargs), precision)
                print('weights')
                print(weights)
                if len(weights) != len(matrix_node.matrix[0]):
                    raise ValueError(f'{self.method} method produced wrong weights') 
            except Exception as err:
                raise ValueError(f'Error in weights calculation ({self.method})')
        else:
            weights = self.weights
            print(weights)

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

        if self.method == 'INPUT':
            print('tutaj-------------------------------')
            method_obj = None
            weights_node = None
            pref = list(self.kwargs[0]['preference'])
            # TODO: think about preferences range
            # if any([p < 0 or p > 1 for p in pref]):
            #     raise ValueError(f'Input preferences outside range [0, 1]')
        else:
            print('calculate method mcda')
            criteria_weights = weights_node.calculate(matrix_node)
            print('criteria_weights')
            print(criteria_weights)
            print('method kwargs')
            print(self.kwargs)
            init_kwargs = get_parameters(self.kwargs, matrix_node.extension, matrix_node, criteria_weights)
            print('init kwargs')
            print(init_kwargs)

            call_kwargs = get_call_kwargs(self.method, init_kwargs)

            print('call kwargs')
            print(call_kwargs)
            try: 
                method_obj = mcda_methods[self.method][matrix_node.extension](**init_kwargs)
            except Exception as err:
                # TODO message
                raise ValueError('Object creation error')
            print('method object')
            print(method_obj)
            print(matrix_node.criteria_types)

            try: 
                pref = np.round(method_obj(matrix_node.matrix, criteria_weights, matrix_node.criteria_types, **call_kwargs), precision)
                print(pref)
                if np.isnan(pref).any() or np.isinf(pref).any():
                    # TODO message
                    raise ValueError('Not numeric values in results')
            except ValueError as err:
                raise ValueError(err)
            except Exception as err:
                # TODO message
                print(err)
                raise ValueError('Method calculation error')
            
            print(pref)
            if self.method == 'VIKOR' and np.array(pref).ndim == 2:
                pref = pref[2]
            print('preference')
            print(pref)

        self.calculation_data.append({
            "matrix_id": matrix_node.id,
            "method_obj": method_obj,
            "weights_node": weights_node,
            "preference": pref.tolist(),
            "kwargs": self.kwargs
        })

        return pref

    def rank(self, matrix_id, weights_id, extension):

        try:
            data = [data for data in self.calculation_data if data['matrix_id'] == matrix_id and data['weights_node'].id == weights_id][0]
            if data['method_obj'] == None:
                print('tutaj rank')
                ranking = rrankdata(data['preference'])
            else:
                if extension == 'crisp':
                    ranking = data['method_obj'].rank(data['preference']).tolist()
                elif extension == 'fuzzy':
                    ranking = data['method_obj'].rank().tolist()
                    if self.method == 'VIKOR' and np.array(ranking).ndim == 2:
                        ranking = ranking[2]
        except Exception as err:
            # TODO message
            raise ValueError('Ranking error')

        return ranking, data

    def get_response(self):
        response = super().get_response()

        data = []
        for cdata in self.calculation_data:
            kwargs = [kwarg for kwarg in cdata['kwargs'] if kwarg['matrix_id'] == cdata['matrix_id'] and len(kwarg.values()) > 1]
            kwargs = [{k:v for k, v in kwarg.items() if v != ''} for kwarg in kwargs]
            data.append({
                "matrix_id": cdata['matrix_id'],
                "weights_method": cdata['weights_node'].method,
                "preference": cdata['preference'],
                "kwargs": kwargs
            })

        return response | {
            "method": self.method,
            "data": data
        }

class RankingNode(Node):
    def __init__(self, id, node_type, extension, connections_from, connections_to, position_x, position_y, **kwargs) -> None:
        
        super().__init__(id, node_type, extension, connections_from, connections_to, position_x, position_y)

        if 'kwargs' in list(kwargs.keys()):
            self.kwargs = kwargs['kwargs']
        self.method = kwargs['method'].lower()
        self.calculation_data = []

    def calculate(self, method_node, matrix_node, weights_node):
        
        ranking, data = method_node.rank(matrix_node.id, weights_node.id, matrix_node.extension)

        self.calculation_data.append({
            "matrix_id": matrix_node.id,
            "method": method_node.method,
            "weights_method": data['weights_node'].method,
            "ranking": ranking,
            "kwargs": data['kwargs']
        })

        return ranking

    @staticmethod
    def calculate_input(method_node, ranking_node, matrix_id):

        ranking = rrankdata(np.array(method_node.kwargs[0]['preference'], dtype=float)).tolist()

        ranking_node.calculation_data.append({
            "matrix_id": matrix_id,
            "method": method_node.method,
            "weights_method": '',
            "ranking": ranking,
            "kwargs": method_node.kwargs
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

        print('corr fun')
        try:
            filtered_nodes = [node for node in nodes if node.node_type == node_type]
            if len(filtered_nodes) > 0:
                for node in filtered_nodes:
                    print('node')
                    print(node)
                    if node_type in ['method', 'ranking'] and node.method.lower() == 'input':
                        print('a tu')
                        corr_labels.append(node.method.upper())
                        print(node.kwargs)
                        corr_data.append(node.kwargs[0][data_field])
                    else:
                        print('tu')
                        for data in node.calculation_data:
                            if data['matrix_id'] == matrix_id:
                                corr_data.append(data[data_field])
                                if data_field == 'ranking':
                                    if 'weights_method' in data.keys():
                                        corr_labels.append(f'{data["method"]} | {data["weights_method"]}')
                                    else:
                                        corr_labels.append(data['method'])
                                else:
                                    if 'weights_node' in data.keys():
                                        corr_labels.append(f'{node.method} | {data["weights_node"].method}')
                                    else:
                                        corr_labels.append(node.method)
        except Exception as err:
            # TODO message
            print(err)
            raise ValueError(f"Error in generating correlation data ({self.method})")

        return corr_data, corr_labels

    def calculate(self, nodes, matrix_node, precision=3):

        corr_matrix = []

        for node_type in ['weights', 'method', 'ranking']:
            corr_data, corr_labels = self._calculate_correlation(nodes, node_type, matrix_node.id)

            print('node type')
            print(node_type)
            print('corr data')
            print(corr_data)
            print(corr_labels)
            print(len(corr_data))
            if len(corr_data) > 0:
                if len(set([len(row) for row in corr_data])) > 1:
                    raise ValueError(f'Data for correlation calculation should have the same size')

                correlation_obj = correlation_methods[self.method]

                try:
                    corr_matrix = np.round(correlation_matrix(np.array(corr_data, dtype=float), correlation_obj), precision)
                except Exception as err:
                    # TODO message
                    raise ValueError(f"Error in calculating correlation data ({self.method})")
                
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

class VisualizationNode(Node):
    def __init__(self, id, node_type, extension, connections_from, connections_to, position_x, position_y, method) -> None:
        
        super().__init__(id, node_type, extension, connections_from, connections_to, position_x, position_y)
        
        self.method = method.upper()
        if self.method not in list(graphs_methods.keys()):
            raise ValueError(f"Method '{self.method}' not found")
            
        self.calculation_data = []

    def _get_graph_data(self, nodes, node_type, matrix_node):

        # TODO: check if data and labels the same size

        calculation_data = []
        try:
            for node in nodes:
                for data in node.calculation_data:
                    if data['matrix_id'] == matrix_node.id:
                        if isinstance(node, RankingNode):
                            calculation_data.append([data, data['method']]) # TODO add params from kwarg to label
                        else:
                            calculation_data.append([data, node.method])
        except Exception as err:
            # TODO message
            raise ValueError(f"Error in retrieving visualization data ({self.method})")

        print('calculation_data')
        print(calculation_data)

        graph_data, graph_labels, metrics_names = [], [], []
        try:
            if node_type == 'weights':
                temp_data, temp_labels = [], []
                for item in calculation_data:
                    temp_data.append(item[0]['weights'])
                    temp_labels.append(item[1])
                graph_data.append(temp_data)
                graph_labels.append(temp_labels)
            elif node_type == 'ranking':
                temp_data, temp_labels = [], []
                if 'SCATTER' in self.method:
                    if len(calculation_data) != 2:
                        # TODO change error from dict
                        raise ValueError('Only two rankings can be visualized with scatter plot')

                for item in calculation_data:
                    temp_labels.append(item[0]['method'])
                    temp_data.append(item[0]['ranking'])
                    # elif 'CORRELATION' in self.method:
                    #     temp_data.append()    
                    #     temp_labels.append(item[0]['method'])
                    # else:
                    #     temp_data.append(item[0]['ranking'])
                    #     temp_labels.append(item[0]['method'])
                graph_data.append(temp_data)
                graph_labels.append(temp_labels)
                        
            elif node_type == 'correlation':
                for item in calculation_data:
                    if 'HEATMAP' in self.method:
                        graph_data.append(item[0]['correlation'])
                    else:
                        graph_data.append(item[0]['correlation'][0])
                    graph_labels.append(item[0]['labels'])
                    metrics_names.append(item[1])
        except Exception as err:
            # TODO message
            if 'Only two rankings' in str(err):
                raise ValueError(err)

            raise ValueError(f"Error in preparing visualization data ({self.method})")

        return graph_data, graph_labels, metrics_names

    def generate(self, nodes, matrix_node):

        node_types = [node.node_type for node in nodes]
        if len(set(node_types)) != 1:
            raise ValueError(f'Graphs should be generated for nodes with the same type')

        node_type = nodes[0].node_type
        try:
            graph_data, graph_labels, metrics_names = self._get_graph_data(nodes, node_type, matrix_node)
        except Exception as err:
            # TODO message
            if 'Only two rankings' in str(err) or 'Error in preparing' in str(err):
                raise ValueError(err)
            raise ValueError(f"Error in generating graph ({self.method})")

        for idx, (data, labels) in enumerate(zip(graph_data, graph_labels)):
            metric = None
            if len(metrics_names) == len(graph_data):
                metric = metrics_names[idx]
            self.calculation_data.append(
                {
                    "matrix_id": matrix_node.id,
                    "img": generate_graph(data, labels, self.method),
                    'metric': metric 
                }
            )
        
    
    def get_response(self):
        response = super().get_response()

        return response | {
            "method": self.method,
            "data": self.calculation_data
        }
