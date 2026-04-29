import numpy as np


def mean(values):
    """Return the average value."""
    return float(np.mean(values))


def standard_deviation(values):
    """Return how spread out the values are."""
    return float(np.std(values))


def percentiles(values, percentile_values):
    """Return selected percentiles, such as the 10th, 50th, and 90th."""
    return np.percentile(values, percentile_values)


def calculate_probability(boolean_results):
    """
    Return the fraction of results that are True.

    In a simulation, probability is estimated by counting how often something
    happens and dividing by the total number of trials.
    """
    return float(np.mean(boolean_results))
