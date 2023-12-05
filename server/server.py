# Copyright (c) 2023 Jakub Więckowski

from flask import Flask
from flask_cors import CORS
import logging
import matplotlib
# Agg, is a non-interactive backend that can only write to files.
matplotlib.use('agg')

# ROUTES
from routes import api

# # CALCULATIONS
# from calculations.structure import CalculationStructure

# ROOT LOGGER
logging.basicConfig(level=logging.INFO)

app = Flask(__name__)
app.config['RESTX_VALIDATE'] = True

# ENABLE CORS
CORS(app, resources={r'/*': {'origins': '*'}})

api.init_app(app)

if __name__ == '__main__':
    app.run(debug=True)

    # data = [
    #     {
    #         "id": 1,
    #         "node_type": "matrix",
    #         "extension": "crisp",
    #         "matrix": [
    #             [1, 2, 3],
    #             [3, 1, 2],
    #             [2, 3, 1],
    #         ],
    #         "criteria_types": [1, -1, 1],
    #         "method": "input",
    #         "connections_from": [],
    #         "connections_to": [2, 3],
    #         "position_x": 10,
    #         "position_y": 10,
    #     },
    #     {
    #         "id": 2,
    #         "node_type": "weights",
    #         "extension": "crisp",
    #         "weights": [0.4, 0.45, 0.15],
    #         "method": "input",
    #         "connections_from": [1],
    #         "connections_to": [4, 5, 6, 8],
    #         "position_x": 20,
    #         "position_y": 20,
    #     },
    #     {
    #         "id": 3,
    #         "node_type": "weights",
    #         "extension": "crisp",
    #         "weights": [],
    #         "method": "IDOCRIW",
    #         "connections_from": [1],
    #         "connections_to": [4, 5, 6, 8],
    #         "position_x": 30,
    #         "position_y": 30,
    #     },
    #     {
    #         "id": 4,
    #         "node_type": "method",
    #         "extension": "crisp",
    #         "kwargs": [
    #             {
    #                 "matrix_id": "1",
    #                 "normalization_function": "max_normalization"
    #             }
    #         ],
    #         "method": "ARAS",
    #         "connections_from": [2, 3],
    #         "connections_to": [],
    #         "position_x": 40,
    #         "position_y": 40,
    #     },
    #     {
    #         "id": 5,
    #         "node_type": "method",
    #         "extension": "crisp",
    #         "kwargs": [
    #             {
    #                 "matrix_id": "1",
    #                 "normalization_function": "linear_normalization"
    #             }
    #         ],
    #         "method": "EDAS",
    #         "connections_from": [2, 3],
    #         "connections_to": [],
    #         "position_x": 50,
    #         "position_y": 50,
    #     },
    #     {
    #         "id": 6,
    #         "node_type": "method",
    #         "extension": "crisp",
    #         "kwargs": [
    #             {
    #                 "matrix_id": "1",
    #                 "normalization_function": "sum_normalization"
    #             }
    #         ],
    #         "method": "TOPSIS",
    #         "connections_from": [2, 3],
    #         "connections_to": [],
    #         "position_x": 60,
    #         "position_y": 60,
    #     },
    #     {
    #         "id": 7,
    #         "node_type": "correlation",
    #         "extension": "crisp",
    #         "method": "pearson",
    #         "connections_from": [4, 6],
    #         "connections_to": [9],
    #         "position_x": 70,
    #         "position_y": 70,
    #     },
    #     {
    #         "id": 8,
    #         "node_type": "visualization",
    #         "extension": "crisp",
    #         "method": "Weights distribution",
    #         "connections_from": [2, 3],
    #         "connections_to": [],
    #         "position_x": 70,
    #         "position_y": 70,
    #     },
    #     {
    #         "id": 9,
    #         "node_type": "visualization",
    #         "extension": "crisp",
    #         "method": "Correlation heatmap",
    #         "connections_from": [7],
    #         "connections_to": [],
    #         "position_x": 70,
    #         "position_y": 70,
    #     }
    # ]
    # print(data)

# calculation = CalculationStructure(data)

# response2 = calculation.calculate()

# for r in response2:
#     print(r)
