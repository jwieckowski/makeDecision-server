import pymcdm.correlations as corr

correlation_methods = {
    'DRASTIC': corr.draws,
    'GOODMAN-KRUSKALL': corr.goodman_kruskal_gamma,
    'KENDALL-TAU': corr.kendall_tau,
    'PEARSON': corr.pearson,
    'SPEARMAN': corr.spearman,
    'WEIGHTED SPEARMAN': corr.weighted_spearman,
    'WS RANK': corr.rank_similarity_coef,
    'WEIGHTS SIMILARITY': corr.wsc,
    'WEIGHTS SIMILARITY 2': corr.wsc2
}