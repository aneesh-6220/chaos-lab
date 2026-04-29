import numpy as np


def simulate_random_walks(step_count, path_count, step_size, drift, random_seed):
    """
    Simulate several one-dimensional random walks.

    Each step is either positive or negative, then drift is added. Drift is a
    steady push, while the plus-or-minus part is the random movement.
    """
    random_generator = np.random.default_rng(random_seed)

    paths = np.zeros((path_count, step_count + 1))

    for path_index in range(path_count):
        position = 0

        for step_index in range(1, step_count + 1):
            direction = random_generator.choice([-1, 1])
            step = direction * step_size + drift
            position = position + step
            paths[path_index, step_index] = position

    return paths
