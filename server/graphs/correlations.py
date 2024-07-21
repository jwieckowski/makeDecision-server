import numpy as np
import pymcdm.visuals as vis
import matplotlib.pyplot as plt

def get_correlation_heatmap_plot(data, labels):
    size = (6, 6)
    if len(data) > 5 or len(data[0]) > 10:
        size = (9, 9)

    fig, ax = plt.subplots(tight_layout=True, figsize=size)
    vis.correlation_heatmap(np.array(data), np.array(labels), labeltop=True, cmap='Blues', adapt_text_colors=['k', 'w'], ax=ax)

    return fig

def get_correlation_plot(data, labels):
    size = (6, 3)
    if len(labels) > 5 or len(data) > 10:
        size = (10, 5)

    fig, ax = plt.subplots(tight_layout=True, figsize=size)
    vis.correlation_plot(np.array(data), labels=np.array(labels), ax=ax)

    return fig