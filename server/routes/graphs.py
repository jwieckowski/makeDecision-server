# Copyright (c) 2023 Jakub Więckowski

from flask_restx import Resource
from flask import jsonify

# PARSERS
from parsers import get_locale_parser

# MODELS
from models import get_dictionary_model

# HELPERS
from helpers import validate_locale

# NAMESPACE
from .namespaces import v1 as api

# WRAPPERS
from wrappers import graphs_wrapper

from graphs.weights import get_weights_plot, get_polar_weights_plot
from graphs.correlations import get_correlation_heatmap_plot, get_correlation_plot

# MODELS
dictionary_model = get_dictionary_model(api)

# ARGUMENTS PARSERS
locale_parser = get_locale_parser()

@api.route('/graphs/plot')
class GraphsConverter(Resource):
    def get(self):
        @graphs_wrapper
        def get_data():
            data = [0.89, 0.94, 0.99]
            labels=['eadaA', 'Bdssa', 'Csa']
            fig = get_correlation_plot(data, labels)
            return fig
        

        return jsonify({'img': get_data()})