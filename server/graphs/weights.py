import numpy as np
import pymcdm.visuals as vis
import matplotlib.pyplot as plt

def get_weights_plot(data, labels):

    fig, ax = plt.subplots(tight_layout=True)
    vis.weights_plot(np.array(data), np.array(labels), ax=ax)

    return fig


def get_polar_weights_plot(data, labels):

    fig, ax = plt.subplots(tight_layout=True, subplot_kw=dict(projection='polar'))
    vis.polar_weights(np.array(data), np.array(labels), ax=ax)

    return fig
