import numpy as np
import pymcdm.visuals as vis
import matplotlib.pyplot as plt

def get_weights_plot(data, labels):
    """
    Generates a weights plot.

    Parameters
    ----------
    data : list of list of float
        The weights data to be plotted.
    labels : list of str
        The labels for the weights data.

    Returns
    -------
    matplotlib.figure.Figure
        The generated weights plot.
    """
    size = (6, 3)
    if len(data) > 5 or len(data[0]) > 10:
        size = (10, 5)

    fig, ax = plt.subplots(tight_layout=True, figsize=size)
    vis.weights_plot(np.array(data), np.array(labels), ax=ax)

    return fig


def get_polar_weights_plot(data, labels):
    """
    Generates a polar weights plot.

    Parameters
    ----------
    data : list of list of float
        The weights data to be plotted.
    labels : list of str
        The labels for the weights data.

    Returns
    -------
    matplotlib.figure.Figure
        The generated polar weights plot.
    """
    size = (6, 6)
    if len(data) > 5 or len(data[0]) > 10:
        size = (9, 9)

    fig, ax = plt.subplots(tight_layout=True, subplot_kw=dict(projection='polar'), figsize=size)
    vis.polar_weights(np.array(data), np.array(labels), ax=ax)

    return fig
