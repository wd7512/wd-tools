def print_dict_structure(d, indent=0):
    prefix = '  ' * indent
    if isinstance(d, dict):
        for k, v in d.items():
            print(f"{prefix}{k}: {type(v).__name__}")
            print_structure(v, indent + 1)
    elif isinstance(d, list):
        print(f"{prefix}list[{len(d)}]: {type(d[0]).__name__}" if d else f"{prefix}list: empty")
        if d:
            print_structure(d[0], indent + 1)

import numpy as np
import scipy.stats as stats

def find_best_distribution(data, distributions=None, alpha=0.05):
    """
    Fit multiple distributions to data and return the best fit by KS test p-value.
    
    Parameters:
        data (array-like): 1D data array
        distributions (list): list of scipy.stats distributions to test (optional)
        alpha (float): significance level to consider fit acceptable (default=0.05)
    
    Returns:
        dict: {
            'name': distribution name,
            'params': fitted parameters,
            'p_value': KS test p-value,
            'accepted': bool (p_value > alpha)
        }
    """
    if distributions is None:
        distributions = [
            stats.norm, stats.expon, stats.gamma, stats.beta,
            stats.lognorm, stats.weibull_min, stats.uniform
        ]

    best_fit = {'name': None, 'params': None, 'p_value': -np.inf, 'accepted': False}

    data = np.asarray(data)
    for dist in distributions:
        try:
            params = dist.fit(data)
            D, p = stats.kstest(data, dist.cdf, args=params)
            if p > best_fit['p_value']:
                best_fit.update({
                    'name': dist.name,
                    'params': params,
                    'p_value': p,
                    'accepted': p > alpha
                })
        except Exception:
            continue

    return best_fit
