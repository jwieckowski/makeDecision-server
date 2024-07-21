import numpy as np
import pymcdm.visuals as vis
import matplotlib.pyplot as plt

def get_ranking_bar_plot(data, labels):

    size = (6, 3)
    if len(data) > 5 or len(data[0]) > 10:
        size = (10, 5)

    fig, ax = plt.subplots(tight_layout=True, figsize=size)
    vis.ranking_bar(np.array(data), np.array(labels), ax=ax)

    return fig

def get_ranking_flow_plot(data, labels):

    size = (6, 3)
    if len(data) > 5 or len(data[0]) > 10:
        size = (10, 5)

    fig, ax = plt.subplots(tight_layout=True, figsize=size)
    vis.ranking_flows(np.array(data), np.array(labels), ax=ax)

    return fig

def get_ranking_polar_plot(data, labels):
    
    size = (6, 6)
    if len(data) > 5 or len(data[0]) > 10:
        size = (9, 9)

    fig, ax = plt.subplots(tight_layout=True, subplot_kw={'projection': 'polar'}, figsize=size)
    vis.polar_plot(np.array(data), np.array(labels), ax=ax)

    return fig
    
def get_ranking_scatter_plot(data, **args):
    # ranking_1, ranking_2
    size = (6, 6)
    if len(data[0]) > 10:
        size = (9, 9)

    fig, ax = plt.subplots(tight_layout=True, figsize=size)
    vis.ranking_scatter(np.array(data[0]), np.array(data[1]), ax=ax)

    return fig
    

def get_ranking_correlation_plot(data, labels):
    # data[0] = rankings, data[1] = 1D corr
    size = (6, 3)
    if len(data[0]) > 5 or len(data[0][0]) > 10:
        size = (10, 5)

    fig, ax = plt.subplots(tight_layout=True, figsize=size)
    vis.ranking_scatter(np.array(data[0]), np.array(data[1]), labels=labels, correlation_plot_kwargs=dict(space_multiplier=0.5, ylim=(0.95, 1.01)), ax=ax)

    return fig
    