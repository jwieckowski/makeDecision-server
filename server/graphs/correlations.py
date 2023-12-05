import numpy as np
import pymcdm.visuals as vis
import matplotlib.pyplot as plt

def get_correlation_heatmap_plot(data, labels):
    
    fig, ax = plt.subplots(tight_layout=True)
    vis.correlation_heatmap(np.array(data), np.array(labels), labeltop=True, cmap='Blues', adapt_text_colors=['k', 'w'], ax=ax)

    return fig

def get_correlation_plot(data, labels):

    fig, ax = plt.subplots(tight_layout=True)
    vis.correlation_plot(np.array(data), labels=np.array(labels), ax=ax)

    return fig