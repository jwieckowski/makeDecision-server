# GRAPHS
from graphs.correlations import *
from graphs.rankings import *
from graphs.weights import *

graphs_methods = {
    'WEIGHTS DISTRIBUTION': get_weights_plot,
    'POLAR WEIGHTS': get_polar_weights_plot,
    'RANKING BAR': get_ranking_bar_plot,
    'RANKING FLOW': get_ranking_flow_plot,
    'POLAR RANKING': get_ranking_polar_plot,
    'SCATTER RANKING': get_ranking_scatter_plot,
    'RANKING CORRELATION': get_ranking_polar_plot,
    'CORRELATION HEATMAP': get_correlation_heatmap_plot,
    'CORRELATION FLOW': get_correlation_plot
}