# WRAPPERS
from wrappers import graphs_wrapper

# METHODS
from .graphs import graphs_methods

@graphs_wrapper
def generate_graph(data, labels, method_name):

    method = graphs_methods[method_name]

    if method is None:
        raise ValueError(f"Visualization method '{method_name}' not found")

    fig = method(data, labels)
    
    return fig

