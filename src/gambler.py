import numpy as np


def simulate_gamblers_ruin(
    starting_money,
    target_money,
    bet_size,
    win_probability,
    simulation_count,
    max_steps,
    random_seed,
):
    """
    Simulate many games of gambler's ruin.

    The function returns arrays that the Streamlit app can graph and measure.
    Keeping this logic outside app.py makes the simulation easier to test and
    easier to understand without reading Streamlit code at the same time.
    """
    random_generator = np.random.default_rng(random_seed)

    paths = []
    final_money = np.zeros(simulation_count)
    steps_taken = np.zeros(simulation_count, dtype=int)
    final_states = np.empty(simulation_count, dtype=object)

    for simulation_index in range(simulation_count):
        money = starting_money
        path = [money]

        for step_index in range(max_steps):
            random_value = random_generator.random()

            if random_value < win_probability:
                money = money + bet_size
            else:
                money = money - bet_size

            path.append(money)

            # We stop early because the game has reached one of its endings.
            if money <= 0 or money >= target_money:
                break

        paths.append(np.array(path))
        final_money[simulation_index] = money
        steps_taken[simulation_index] = len(path) - 1
        final_states[simulation_index] = label_final_state(money, target_money)

    return {
        "paths": paths,
        "final_money": final_money,
        "steps_taken": steps_taken,
        "final_states": final_states,
    }


def label_final_state(money, target_money):
    """Classify how one simulation ended."""
    if money <= 0:
        return "ruin"
    if money >= target_money:
        return "target"
    return "timeout"
