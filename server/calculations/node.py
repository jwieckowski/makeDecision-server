# Copyright (C) Jakub Więckowski 2023 - 2024

from abc import ABC
import numpy as np
from pymcdm.helpers import correlation_matrix, rrankdata

# CONST
from methods import weights_methods, mcda_methods, correlation_methods
from graphs import graphs_methods, generate_graph

# HELPERS
from .parameters import get_parameters, get_call_kwargs

from utils.errors import get_error_message

class Node(ABC):
    def __init__(self, locale, id, node_type, extension, connections_from, connections_to, position_x, position_y) -> None:
        self.locale = locale
        self.id = id
        self.node_type = node_type.lower()
        self.extension = extension.lower()
        if self.extension not in ['crisp', 'fuzzy']:
            raise ValueError(f"'{self.extension}': {get_error_message(self.locale, 'extension-not-found')}")
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
    def __init__(self, locale, id, node_type, extension, connections_from, connections_to, position_x, position_y, matrix, criteria_types, method) -> None:
        
        super().__init__(locale, id, node_type, extension, connections_from, connections_to, position_x, position_y)

        if isinstance(matrix[0][0], str):
            try:
                if ',' in matrix[0][0]:
                    matrix = [[col.split(',') for col in row] for row in matrix]
            except:
                raise ValueError(f'{get_error_message(self.locale, "matrix-data-error")} ({self.id})')
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
    def __init__(self, locale, id, node_type, extension, connections_from, connections_to, position_x, position_y, weights, method) -> None:
        
        super().__init__(locale, id, node_type, extension, connections_from, connections_to, position_x, position_y)

        self.weights = np.array(weights, dtype=float)
        self.method = method.upper()
        if self.method != 'INPUT' and self.method not in list(weights_methods.keys()):
            raise ValueError(f"'{self.method}': {get_error_message(self.locale, 'method-name-not-found')}")
            
        self.calculation_data = []

    def calculate(self, matrix_node, precision=3):
        if self.method != 'INPUT':
            try: 
                self.method_obj = weights_methods[self.method][matrix_node.extension]
                kwargs = {
                    'matrix': matrix_node.matrix
                }

                if self.method in ['MEREC', 'CILOS', 'IDOCRIW']:
                    kwargs = kwargs | {"types": matrix_node.criteria_types}
                
                weights = np.round(self.method_obj(**kwargs), precision)
                if len(weights) != len(matrix_node.matrix[0]):
                    raise ValueError(f'{self.method} {get_error_message(self.locale, "matrix-weights-size-error")}') 
            except Exception as err:
                raise ValueError(f'{get_error_message(self.locale, "weights-error-calculation")} ({self.method})')
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
    def __init__(self, locale, id, node_type, extension, connections_from, connections_to, position_x, position_y, method, kwargs) -> None:
        
        super().__init__(locale, id, node_type, extension, connections_from, connections_to, position_x, position_y)

        self.method = method.upper()
        if self.method not in list(mcda_methods.keys()):
            raise ValueError(f"'{self.method}': {get_error_message(self.locale, 'method-name-not-found')}")
            
        self.kwargs = kwargs
        self.calculation_data = []

    def calculate(self, matrix_node, weights_node, precision=3):

        if self.method == 'INPUT':
            method_obj = None
            weights_node = None
            pref = list(self.kwargs[0]['preference'])
        else:
            criteria_weights = weights_node.calculate(matrix_node)
            init_kwargs = get_parameters(self.kwargs, matrix_node.extension, matrix_node, criteria_weights, self.locale)
            
            call_kwargs = get_call_kwargs(self.method, init_kwargs, self.extension, self.locale)

            try: 
                method_obj = mcda_methods[self.method][matrix_node.extension](**init_kwargs)
            except Exception as err:
                raise ValueError(get_error_message(self.locale, "mcda-method-object-error"))

            try: 
                pref = np.round(method_obj(matrix_node.matrix, criteria_weights, matrix_node.criteria_types, **call_kwargs), precision)
                if np.isnan(pref).any() or np.isinf(pref).any():
                    raise ValueError(get_error_message(self.locale, 'not-numeric-results'))
            except ValueError as err:
                raise ValueError(err)
            except Exception as err:
                raise ValueError(get_error_message(self.locale, 'method-calculation-error'))
            
            if self.method == 'VIKOR' and np.array(pref).ndim == 2:
                pref = pref[2]

        if matrix_node:
            self.calculation_data.append({
                "matrix_id": matrix_node.id,
                "method_obj": method_obj,
                "weights_node": weights_node,
                "preference": pref.tolist(),
                "kwargs": self.kwargs
            })
        else:
            self.calculation_data.append({
                "matrix_id": 0,
                "method_obj": method_obj,
                "weights_node": weights_node,
                "preference": pref,
                "kwargs": self.kwargs
            })

        return pref

    def rank(self, matrix_id=None, weights_id=None, extension=None):

        if matrix_id and weights_id and extension:
            try:
                data = [data for data in self.calculation_data if data['matrix_id'] == matrix_id and data['weights_node'].id == weights_id][0]
                if data['method_obj'] == None:
                    ranking = rrankdata(data['preference'])
                else:
                    if extension == 'crisp':
                        ranking = data['method_obj'].rank(data['preference']).tolist()
                    elif extension == 'fuzzy':
                        ranking = data['method_obj'].rank().tolist()
                        if self.method == 'VIKOR' and np.array(ranking).ndim == 2:
                            ranking = ranking[2]
            except Exception as err:
                raise ValueError(get_error_message(self.locale, 'ranking-calculation-error'))
        else:
            data = self.calculation_data[0]
            ranking = list(rrankdata(data['preference']))

        return ranking, data

    def get_response(self):
        response = super().get_response()

        data = []
        for cdata in self.calculation_data:
            if self.method.lower() == 'input':
                data.append({
                    "matrix_id": 0,
                    "weights_method": '',
                    "preference": cdata['preference'],
                    "kwargs": cdata['kwargs']
                })
            else:
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
    def __init__(self, locale, id, node_type, extension, connections_from, connections_to, position_x, position_y, **kwargs) -> None:
        
        super().__init__(locale, id, node_type, extension, connections_from, connections_to, position_x, position_y)

        if 'kwargs' in list(kwargs.keys()):
            self.kwargs = kwargs['kwargs']
        self.method = kwargs['method'].lower()
        self.calculation_data = []

    def calculate(self, method_node, matrix_node=None, weights_node=None):
        
        if matrix_node and weights_node:
            ranking, data = method_node.rank(matrix_node.id, weights_node.id, matrix_node.extension)
            
            self.calculation_data.append({
                "matrix_id": matrix_node.id,
                "method": method_node.method,
                "weights_method": data['weights_node'].method,
                "ranking": ranking,
                "kwargs": data['kwargs']
            })
        else:
            ranking, data = method_node.rank()
            self.calculation_data.append({
                "matrix_id": 0,
                "method": method_node.method,
                "weights_method": '',
                "ranking": list(ranking),
                "kwargs": data['kwargs']
            })

        return ranking

    def get_input_rank(self):
        self.calculation_data.append({
            "matrix_id": 0,
            "method": 'INPUT RANK',
            "weights_method": '',
            "ranking": self.kwargs[0]['ranking'],
            "kwargs": self.kwargs
        })

        return np.array(self.kwargs[0]['ranking'])

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
    def __init__(self, locale, id, node_type, extension, connections_from, connections_to, position_x, position_y, method) -> None:
        
        super().__init__(locale, id, node_type, extension, connections_from, connections_to, position_x, position_y)
        
        self.method = method.upper()
        if self.method not in list(correlation_methods.keys()):
            raise ValueError(f"'{self.method}': {get_error_message(self.locale, 'method-name-not-found')}")
            
        self.calculation_data = []

    def _calculate_correlation(self, nodes, node_type, matrix_id):
        corr_data, corr_labels = [], []

        data_field = node_type
        if node_type == 'method':
            data_field = 'preference'

        try:
            filtered_nodes = [node for node in nodes if node.node_type == node_type]
            if len(filtered_nodes) > 0:
                for node in filtered_nodes:
                    if node_type in ['method', 'ranking'] and node.method.lower() == 'input':
                        corr_labels.append(node.method.upper())
                        corr_data.append(node.kwargs[0][data_field])
                    else:
                        for data in node.calculation_data:
                            if data['matrix_id'] == matrix_id:
                                corr_data.append(data[data_field])
                                if data_field == 'ranking':
                                    if 'weights_method' in data.keys():
                                        corr_labels.append(f'{data["method"]}\n{data["weights_method"]}')
                                    else:
                                        corr_labels.append(data['method'])
                                else:
                                    if 'weights_node' in data.keys():
                                        corr_labels.append(f'{node.method}\n{data["weights_node"].method}')
                                    else:
                                        corr_labels.append(node.method)
        except Exception as err:
            raise ValueError(f"{get_error_message(self.locale, 'correlation-generating-error')} ({self.method})")

        return corr_data, corr_labels

    def calculate(self, nodes, matrix_node=None, precision=3):

        corr_matrix = []

        if matrix_node:
            for node_type in ['weights', 'method', 'ranking']:
                corr_data, corr_labels = self._calculate_correlation(nodes, node_type, matrix_node.id)
                if len(corr_data) > 0:
                    if len(set([len(row) for row in corr_data])) > 1:
                        raise ValueError(get_error_message(self.locale, 'correlation-same-size-error'))

                    correlation_obj = correlation_methods[self.method]

                    try:
                        corr_matrix = np.round(correlation_matrix(np.array(corr_data, dtype=float), correlation_obj), precision)
                    except Exception as err:
                        raise ValueError(f"{get_error_message(self.locale, 'correlation-calculation-error')} ({self.method})")

                    self.calculation_data.append({
                        "matrix_id": matrix_node.id,
                        "correlation": corr_matrix.tolist(),
                        "labels": corr_labels
                    })  
        else:
            corr_key = 'preference'
            if nodes[0].node_type == 'ranking':
                corr_key = 'ranking'
            corr_data = [list(conn_node.calculation_data[0][corr_key]) for conn_node in nodes]
            if corr_key == 'preference':
                corr_labels = [f'INPUT (ID {conn_node.id})' for conn_node in nodes]
            else:
                corr_labels = [f'INPUT (ID {conn_node.id})' if conn_node.method == 'input' else f'INPUT RANK (ID {conn_node.id})' for conn_node in nodes]
                
            if len(corr_data) > 0:
                if len(set([len(row) for row in corr_data])) > 1:
                    raise ValueError(get_error_message(self.locale, 'correlation-same-size-error'))

                correlation_obj = correlation_methods[self.method]

                try:
                    corr_matrix = np.round(correlation_matrix(np.array(corr_data, dtype=float), correlation_obj), precision)
                except Exception as err:
                    raise ValueError(f"{get_error_message(self.locale, 'correlation-calculation-error')} ({self.method})")

                self.calculation_data.append({
                    "matrix_id": 0,
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
    def __init__(self, locale, id, node_type, extension, connections_from, connections_to, position_x, position_y, method) -> None:
        
        super().__init__(locale, id, node_type, extension, connections_from, connections_to, position_x, position_y)
        
        self.method = method.upper()
        if self.method not in list(graphs_methods.keys()):
            raise ValueError(f"'{self.method}': {get_error_message(self.locale, 'method-name-not-found')}")
            
        self.calculation_data = []

    def _get_graph_data(self, nodes, node_type, matrix_node=None):

        calculation_data = []
        try:
            for node in nodes:
                for data in node.calculation_data:
                    if matrix_node:
                        if data['matrix_id'] == matrix_node.id:
                            if isinstance(node, RankingNode):
                                calculation_data.append([data, data['method']])
                            else:
                                calculation_data.append([data, node.method])
                    else:
                        if isinstance(node, RankingNode):
                            calculation_data.append([data, f"{data['method']} (ID {node.id})"])
                        else:
                            calculation_data.append([data, f"{node.method} (ID {node.id})"])
        except Exception as err:
            raise ValueError(f"{get_error_message(self.locale, 'visualization-data-error')} ({self.method})")

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
                        raise ValueError(get_error_message(self.locale, 'scatter-ranking-limit'))

                for item in calculation_data:
                    if item[0]['weights_method'] == '' or item[0]['weights_method'] == None:
                        temp_labels.append(item[-1])
                    else:
                        temp_labels.append(f"{item[0]['method']}\n({item[0]['weights_method']})")
                    temp_data.append(list(np.array(item[0]['ranking']).astype(float)))
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
            if get_error_message('en', "scatter-ranking-limit") in str(err):
                raise ValueError(err)

            raise ValueError(f"{get_error_message(self.locale, 'visualization-calculation-error')} ({self.method})")

        return graph_data, graph_labels, metrics_names

    def generate(self, nodes, matrix_node=None):

        node_types = [node.node_type for node in nodes]
        if len(set(node_types)) != 1:
            raise ValueError(f'{get_error_message(self.locale, "graphs-same-type")}')

        node_type = nodes[0].node_type
        try:
            graph_data, graph_labels, metrics_names = self._get_graph_data(nodes, node_type, matrix_node)
        except Exception as err:
            if 'Only two rankings' in str(err) or 'Tylko dwa rankingi' in str(err) or 'Error in preparing' in str(err) or 'przygotowywania danych wizualizacji' in str(err):
                raise ValueError(err)
            raise ValueError(f"{get_error_message(self.locale, 'graph-generation-error')} ({self.method})")

        for idx, (data, labels) in enumerate(zip(graph_data, graph_labels)):
            metric = None
            if len(metrics_names) == len(graph_data):
                metric = metrics_names[idx]
            self.calculation_data.append(
                {
                    "matrix_id": matrix_node.id if matrix_node else 0,
                    "img": generate_graph(data, labels, self.method, self.locale),
                    'metric': metric 
                }
            )
        
    
    def get_response(self):
        response = super().get_response()

        return response | {
            "method": self.method,
            "data": self.calculation_data
        }
