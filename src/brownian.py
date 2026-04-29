import numpy as np


def simulate_brownian_motion(particle_count, step_count, step_size, random_seed):
    """
    Simulate two-dimensional Brownian motion.

    A Brownian particle receives many small random pushes. We model that by
    adding a normally distributed x-step and y-step at every moment.
    """
    random_generator = np.random.default_rng(random_seed)

    x_positions = np.zeros((particle_count, step_count + 1))
    y_positions = np.zeros((particle_count, step_count + 1))

    for particle_index in range(particle_count):
        x_position = 0
        y_position = 0

        for step_index in range(1, step_count + 1):
            x_step = random_generator.normal(loc=0, scale=step_size)
            y_step = random_generator.normal(loc=0, scale=step_size)

            x_position = x_position + x_step
            y_position = y_position + y_step

            x_positions[particle_index, step_index] = x_position
            y_positions[particle_index, step_index] = y_position

    return x_positions, y_positions
