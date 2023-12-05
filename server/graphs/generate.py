# WRAPPERS
from wrappers import graphs_wrapper

# METHODS
from .graphs import graphs_methods

@graphs_wrapper
def generate_graph(data, labels, method_name):

    method = graphs_methods[method_name]

    if method is None:
        raise ValueError(f"Visualization method '{method_name}' not found")

    # data = [0.89, 0.94, 0.99]
    # labels=['eadaA', 'Bdssa', 'Csa']
    # fig = get_correlation_plot(data, labels)
    fig = method(data, labels)
    
    return fig

