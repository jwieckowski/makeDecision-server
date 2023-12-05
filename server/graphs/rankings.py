import numpy as np
import pymcdm.visuals as vis
import matplotlib.pyplot as plt

def get_ranking_bar_plot(data, labels):

    fig, ax = plt.subplots(tight_layout=True)
    vis.ranking_bar(np.array(data), np.array(labels), ax=ax)

    return fig

def get_ranking_flow_plot(data, labels):

    fig, ax = plt.subplots(tight_layout=True)
    vis.ranking_flows(np.array(data), np.array(labels), ax=ax)

    return fig

def get_ranking_polar_plot(data, labels):
    
    fig, ax = plt.subplots(tight_layout=True)
    vis.polar_plot(np.array(data), np.array(labels), ax=ax)

    return fig
    
def get_ranking_scatter_plot(data, **args):
    # ranking_1, ranking_2
    
    fig, ax = plt.subplots(tight_layout=True)
    vis.ranking_scatter(np.array(data[0]), np.array(data[1]), ax=ax)

    return fig
    

def get_ranking_correlation_plot(data, labels):
    # data[0] = rankings, data[1] = 1D corr
    
    fig, ax = plt.subplots(tight_layout=True)
    vis.ranking_scatter(np.array(data[0]), np.array(data[1]), labels=labels, correlation_plot_kwargs=dict(space_multiplier=0.5, ylim=(0.95, 1.01)), ax=ax)

    return fig
    