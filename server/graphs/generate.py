import matplotlib.pyplot as plt

# WRAPPERS
from wrappers import graphs_wrapper

# METHODS
from .graphs import graphs_methods

# UTILS
from utils.errors import get_error_message

@graphs_wrapper
def generate_graph(data, labels, method_name, locale):
    """
    Generates a graph based on the specified method.

    Parameters
    ----------
    data : list of float or list of list of float
        The data to be plotted.
    labels : list of str
        The labels for the data.
    method_name : str
        The name of the graphing method to use.
    locale : str
        The locale for error messages.

    Returns
    -------
    matplotlib.figure.Figure
        The generated graph.

    Raises
    ------
    ValueError
        If the method name is not found in the graph methods.
    """
    method = graphs_methods[method_name]

    if method is None:
        raise ValueError(f"'{method_name}' {get_error_message(locale, 'method-name-not-found')}")

    if 'scatter' in method_name.lower():
        fig = method(data)
    else:
        fig = method(data, labels)

    plt.tight_layout()
    
    return fig

