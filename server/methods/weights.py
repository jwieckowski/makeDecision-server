import pymcdm.weights as crisp_weights
import pyfdm.weights as fuzzy_weights

weights_methods = {
    'ANGLE': {
        'crisp': crisp_weights.angle_weights
    },
    'CILOS': {
        'crisp': crisp_weights.cilos_weights
    },
    'CRITIC': {
        'crisp': crisp_weights.critic_weights,
    },
    'ENTROPY': {
        'crisp': crisp_weights.entropy_weights,
        'fuzzy': fuzzy_weights.shannon_entropy_weights
    },
    'EQUAL': {
        'crisp': crisp_weights.equal_weights,
        'fuzzy': fuzzy_weights.equal_weights
    },
    'GINI': {
        'crisp': crisp_weights.gini_weights
    },
    'IDOCRIW': {
        'crisp': crisp_weights.idocriw_weights
    },
    'MEREC': {
        'crisp': crisp_weights.merec_weights
    },
    'STANDARD DEVIATION': {
        'crisp': crisp_weights.standard_deviation_weights,
        'fuzzy': fuzzy_weights.standard_deviation_weights
    },
    'VARIANCE': {
        'crisp': crisp_weights.variance_weights,
        'fuzzy': fuzzy_weights.variance_weights
    }
}