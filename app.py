import matplotlib.pyplot as plt
import numpy as np
import streamlit as st

from src.brownian import simulate_brownian_motion
from src.gambler import simulate_gamblers_ruin
from src.metrics import calculate_probability, mean, percentiles, standard_deviation
from src.random_walk import simulate_random_walks


MAX_DISPLAY_PATHS = 50
PAGES = [
    "Home",
    "Gambler's Ruin",
    "Random Walk",
    "Brownian Motion",
    "Intuition vs Reality",
]


def main():
    """Run the Streamlit app."""
    st.set_page_config(
        page_title="Chaos Lab",
        page_icon="CL",
        layout="wide",
    )

    apply_custom_styles()
    show_top_banner()
    selected_page = show_navigation()

    if selected_page == "Home":
        show_home_tab()
    elif selected_page == "Gambler's Ruin":
        show_gamblers_ruin_tab()
    elif selected_page == "Random Walk":
        show_random_walk_tab()
    elif selected_page == "Brownian Motion":
        show_brownian_motion_tab()
    else:
        show_intuition_tab()

    show_footer()


def apply_custom_styles():
    """Add a small amount of styling without making the app complicated."""
    st.markdown(
        """
        <style>
        .hero-card,
        .experiment-card,
        .explanation-box {
            background: #F8FAFC;
            color: #111827;
            border: 1px solid #D1D5DB;
            border-radius: 14px;
            padding: 1rem;
            margin-bottom: 1rem;
        }

        .hero-card *,
        .experiment-card *,
        .explanation-box * {
            color: #111827 !important;
        }

        .footer {
            color: #4B5563;
            font-size: 0.85rem;
            text-align: center;
            margin-top: 2rem;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def show_top_banner():
    st.markdown(
        """
        <div class="hero-card">
            <h1>Chaos Lab</h1>
            <p>
                A probability lab for exploring how simple random rules turn
                into surprising patterns.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def show_navigation():
    """Let users move between experiments from one clear control."""
    if "active_page" not in st.session_state:
        st.session_state.active_page = "Home"

    selected_page = st.radio(
        "Choose an experiment",
        PAGES,
        index=PAGES.index(st.session_state.active_page),
        horizontal=True,
    )

    # This is separate from the radio widget state, so Home buttons can safely
    # change pages later in the same Streamlit run.
    st.session_state.active_page = selected_page
    return selected_page


def show_footer():
    st.markdown(
        """
        <div class="footer">
            Educational simulation tool · Not financial or scientific advice · 
            <a href="https://github.com/aneesh-6220/chaos-lab" target="_blank">Source code</a>
        </div>
        """,
        unsafe_allow_html=True,
    )

def show_home_tab():
    st.header("Pick an experiment")
    st.write(
        "Chaos Lab is not about predicting one perfect answer. It is about "
        "testing many possible worlds and seeing what randomness usually does."
    )
    st.caption("Use the experiment selector above, or choose one of the options below.")

    first_row = st.columns(2)
    second_row = st.columns(2)

    with first_row[0]:
        show_experiment_card(
            title="Gambler's Ruin",
            hook="Can you survive randomness?",
            body=(
                "Run repeated bets and watch how starting money, target money, "
                "bet size, and win probability shape the chance of going broke."
            ),
            target_page="Gambler's Ruin",
        )

    with first_row[1]:
        show_experiment_card(
            title="Random Walk",
            hook="How far can random steps drift?",
            body=(
                "Send many paths walking left and right. Then compare the path "
                "cloud with the histogram of where they finish."
            ),
            target_page="Random Walk",
        )

    st.write("")

    with second_row[0]:
        show_experiment_card(
            title="Brownian Motion",
            hook="Chaos from tiny movements.",
            body=(
                "Release particles at the origin and let random x and y pushes "
                "draw tangled paths through space."
            ),
            target_page="Brownian Motion",
        )

    with second_row[1]:
        show_experiment_card(
            title="Intuition vs Reality",
            hook="Guess first, simulate after.",
            body=(
                "Make a probability guess before the result appears. The goal "
                "is not perfection; it is calibrating your intuition."
            ),
            target_page="Intuition vs Reality",
        )

    st.divider()
    explanation_box(
        "Why simulations matter",
        (
            "Simulations let us test thousands of possible worlds instead of "
            "trusting one guess. Repeated trials show patterns that a single "
            "example can hide."
        ),
    )


def show_gamblers_ruin_tab():
    experiment_intro(
        "Gambler's Ruin",
        "Try to reach a target before your money hits zero.",
        (
            "Each round is one bet. A win adds the bet size, and a loss subtracts it. "
            "The experiment stops at ruin, at the target, or at the max round limit."
        ),
    )

    with st.form("gambler_controls"):
        st.subheader("Set up the experiment")
        row1 = st.columns(4)
        starting_money = row1[0].number_input("Starting money", 1, 1000, 100, step=10)
        target_money = row1[1].number_input("Target money", 2, 2000, 200, step=10)
        bet_size = row1[2].number_input("Bet size", 1, 100, 1, step=1)
        win_probability = row1[3].slider("Win probability", 0.0, 1.0, 0.50, 0.01)

        row2 = st.columns(3)
        simulation_count = row2[0].slider("Simulations", 10, 1000, 200, step=10)
        max_steps = row2[1].slider("Max rounds", 10, 2000, 500, step=10)
        random_seed = row2[2].number_input("Random seed", 0, 999999, 42, step=1)

        st.form_submit_button("Run Gambler Simulation")

    results = simulate_gamblers_ruin(
        starting_money=starting_money,
        target_money=target_money,
        bet_size=bet_size,
        win_probability=win_probability,
        simulation_count=simulation_count,
        max_steps=max_steps,
        random_seed=random_seed,
    )

    paths = results["paths"]
    final_money = results["final_money"]
    steps_taken = results["steps_taken"]
    final_states = results["final_states"]

    ruin_probability = calculate_probability(final_states == "ruin")
    target_probability = calculate_probability(final_states == "target")

    st.divider()
    st.subheader("Results")
    metric_row = st.columns(4)
    metric_row[0].metric("Ruin probability", format_percent(ruin_probability))
    metric_row[1].metric("Target probability", format_percent(target_probability))
    metric_row[2].metric("Average ending money", f"${mean(final_money):.2f}")
    metric_row[3].metric("Average stopping round", f"{mean(steps_taken):.1f}")

    st.pyplot(
        create_gambler_plot(
            paths=paths,
            target_money=target_money,
            max_paths_to_show=MAX_DISPLAY_PATHS,
        )
    )

    interpretation_box(get_gambler_interpretation(ruin_probability, target_probability))
    try_this_box(
        [
            "Set win probability to 0.49 and compare it with 0.50.",
            "Increase the bet size and watch paths hit an ending faster.",
            "Move the target farther away and see whether survival gets harder.",
        ]
    )
    what_to_notice_box(
        [
            "A fair 50% game can still produce many losses if the target is far away.",
            "Tiny changes in win probability compound over repeated rounds.",
            "Short paths can look lucky or unlucky, but many paths reveal the pattern.",
        ]
    )


def show_random_walk_tab():
    experiment_intro(
        "Random Walk",
        "Release a crowd of paths and watch randomness spread them out.",
        (
            "Every path starts at zero. On each step, it moves up or down by "
            "the step size, then drift adds a steady push."
        ),
    )

    with st.form("walk_controls"):
        st.subheader("Set up the experiment")
        row1 = st.columns(5)
        step_count = row1[0].slider("Steps", 10, 2000, 200, step=10)
        path_count = row1[1].slider("Paths", 10, 1000, 100, step=10)
        step_size = row1[2].number_input("Step size", 0.1, 10.0, 1.0, step=0.1)
        drift = row1[3].number_input("Drift", -2.0, 2.0, 0.0, step=0.05)
        random_seed = row1[4].number_input("Random seed", 0, 999999, 7, step=1)

        st.form_submit_button("Run Walks")

    paths = simulate_random_walks(
        step_count=step_count,
        path_count=path_count,
        step_size=step_size,
        drift=drift,
        random_seed=random_seed,
    )
    final_positions = paths[:, -1]
    lower, middle, upper = percentiles(final_positions, [10, 50, 90])

    st.divider()
    st.subheader("Results")
    chart_col, hist_col = st.columns([2, 1])
    with chart_col:
        st.pyplot(create_random_walk_plot(paths, MAX_DISPLAY_PATHS))
    with hist_col:
        st.pyplot(create_final_position_histogram(final_positions))

    metric_row = st.columns(3)
    metric_row[0].metric("Mean final position", f"{mean(final_positions):.2f}")
    metric_row[1].metric("Standard deviation", f"{standard_deviation(final_positions):.2f}")
    metric_row[2].metric("10th / 50th / 90th", f"{lower:.1f}, {middle:.1f}, {upper:.1f}")

    explanation_box(
        "What is happening?",
        (
            "The paths are not trying to go anywhere. They are just collecting "
            "random plus and minus steps. The group view shows the real story: "
            "randomness creates spread."
        ),
    )
    try_this_box(
        [
            "Increase steps and watch the final-position histogram get wider.",
            "Set drift to 0.10 and notice the whole cloud shift upward.",
            "Set drift back to 0 and look for spread even without a push.",
        ]
    )
    what_to_notice_box(
        [
            "More steps usually means a wider spread of final positions.",
            "Drift shifts the center of the paths.",
            "Zero drift does not mean zero movement; it means no preferred direction.",
        ]
    )


def show_brownian_motion_tab():
    experiment_intro(
        "Brownian Motion",
        "A compact view of random motion in two dimensions.",
        (
            "Particles begin at the origin. At every moment, each one receives "
            "a random x push and a random y push. No one is steering them."
        ),
    )

    with st.form("brownian_controls"):
        st.subheader("Set up the experiment")
        row1 = st.columns(4)
        particle_count = row1[0].slider("Particles", 1, 30, 5, step=1)
        step_count = row1[1].slider("Steps", 20, 2000, 300, step=20)
        step_size = row1[2].number_input("Step size", 0.05, 5.0, 0.5, step=0.05)
        random_seed = row1[3].number_input("Random seed", 0, 999999, 123, step=1)

        st.form_submit_button("Run Brownian Motion")

    x_positions, y_positions = simulate_brownian_motion(
        particle_count=particle_count,
        step_count=step_count,
        step_size=step_size,
        random_seed=random_seed,
    )
    final_distances = np.sqrt(x_positions[:, -1] ** 2 + y_positions[:, -1] ** 2)

    st.divider()
    st.subheader("Results")
    path_col, info_col = st.columns([2.2, 1])
    with path_col:
        st.pyplot(create_brownian_plot(x_positions, y_positions))
    with info_col:
        st.metric("Average distance from origin", f"{mean(final_distances):.2f}")
        st.metric("Farthest particle distance", f"{np.max(final_distances):.2f}")
        st.pyplot(create_distance_histogram(final_distances))

    explanation_box(
        "What is happening?",
        (
            "Each particle receives tiny random pushes in x and y. No one is "
            "steering it, but the accumulated movement creates tangled paths."
        ),
    )
    try_this_box(
        [
            "Increase steps to give particles more time to wander.",
            "Increase step size to make each random push stronger.",
            "Increase particles to see a fuller cloud of possible paths.",
        ]
    )
    what_to_notice_box(
        [
            "All particles start together, then separate because their pushes differ.",
            "Final distance is not only about direction; it is about accumulated movement.",
            "This connects to diffusion, where particles spread out over time.",
        ]
    )


def show_intuition_tab():
    experiment_intro(
        "Intuition vs Reality",
        "A mini challenge: guess first, simulate after.",
        (
            "Probability intuition can be surprisingly slippery. Make your "
            "guess before running the experiment, then compare it with the simulation."
        ),
    )

    with st.form("intuition_controls"):
        st.subheader("Your challenge")
        guess_percent = st.slider(
            "Your guess: probability of ruin",
            min_value=0,
            max_value=100,
            value=50,
            step=1,
        )

        row1 = st.columns(3)
        starting_money = row1[0].number_input("Starting money", 1, 1000, 100, step=10)
        target_money = row1[1].number_input("Target money", 2, 2000, 200, step=10)
        win_probability = row1[2].slider("Win probability", 0.0, 1.0, 0.50, 0.01)

        row2 = st.columns(4)
        bet_size = row2[0].number_input("Bet size", 1, 100, 1, step=1)
        simulation_count = row2[1].slider("Simulations", 50, 1000, 300, step=50)
        max_steps = row2[2].slider("Max rounds", 50, 2000, 500, step=50)
        random_seed = row2[3].number_input("Random seed", 0, 999999, 99, step=1)

        submitted = st.form_submit_button("Reveal Simulation Result")

    if not submitted:
        st.info("Lock in your guess, then reveal the simulation result.")
        return

    results = simulate_gamblers_ruin(
        starting_money=starting_money,
        target_money=target_money,
        bet_size=bet_size,
        win_probability=win_probability,
        simulation_count=simulation_count,
        max_steps=max_steps,
        random_seed=random_seed,
    )

    actual_probability = calculate_probability(results["final_states"] == "ruin")
    guessed_probability = guess_percent / 100
    difference = abs(actual_probability - guessed_probability)

    st.divider()
    st.subheader("Result")
    metric_row = st.columns(3)
    metric_row[0].metric("Your guess", format_percent(guessed_probability))
    metric_row[1].metric("Simulated probability", format_percent(actual_probability))
    metric_row[2].metric("Error difference", format_percent(difference))

    challenge_feedback_box(get_guess_feedback(difference))
    explanation_box(
        "Why this matters",
        (
            "A few imagined examples can make a probability feel obvious. "
            "Simulation checks that feeling against hundreds of trials."
        ),
    )


def show_experiment_card(title, hook, body, target_page):
    st.markdown(
        f"""
        <div class="experiment-card">
            <h3>{title}</h3>
            <strong>{hook}</strong>
            <p>{body}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    if st.button(f"Open {target_page}", key=f"open_{target_page}"):
        st.session_state.active_page = target_page
        st.rerun()


def experiment_intro(title, hook, body):
    st.header(title)
    st.markdown(f"**{hook}**")
    st.write(body)


def explanation_box(title, body):
    st.markdown(
        f"""
        <div class="explanation-box">
            <strong>{title}</strong><br>
            {body}
        </div>
        """,
        unsafe_allow_html=True,
    )


def interpretation_box(body):
    st.markdown(
        f"""
        <div class="explanation-box">
            <strong>Interpretation</strong><br>
            {body}
        </div>
        """,
        unsafe_allow_html=True,
    )


def challenge_feedback_box(body):
    st.markdown(
        f"""
        <div class="explanation-box">
            <strong>Feedback</strong><br>
            {body}
        </div>
        """,
        unsafe_allow_html=True,
    )


def try_this_box(suggestions):
    suggestion_items = "".join(f"<li>{suggestion}</li>" for suggestion in suggestions)
    st.markdown(
        f"""
        <div class="explanation-box">
            <strong>What to try</strong>
            <ul>{suggestion_items}</ul>
        </div>
        """,
        unsafe_allow_html=True,
    )


def what_to_notice_box(points):
    point_items = "".join(f"<li>{point}</li>" for point in points)
    st.markdown(
        f"""
        <div class="explanation-box">
            <strong>What to notice</strong>
            <ul>{point_items}</ul>
        </div>
        """,
        unsafe_allow_html=True,
    )


def get_gambler_interpretation(ruin_probability, target_probability):
    if ruin_probability > 0.70:
        return (
            "This setup is very risky. In most simulated worlds, the player "
            "goes broke before reaching the target."
        )
    if target_probability > 0.70:
        return (
            "This setup strongly favors survival. The target is reached in "
            "most simulated worlds."
        )
    return (
        "Outcomes are mixed. The same rules can lead to very different endings, "
        "which is exactly why running many trials is useful."
    )


def get_guess_feedback(difference):
    if difference <= 0.05:
        return "Very close. Your intuition was well calibrated for this setup."
    if difference <= 0.15:
        return "Decent intuition. You were in the right neighborhood."
    return "Randomness fooled you. That is the point of the challenge."


def create_gambler_plot(paths, target_money, max_paths_to_show):
    fig, ax = plt.subplots(figsize=(10, 5))
    paths_to_show = paths[:max_paths_to_show]

    for path in paths_to_show:
        final_value = path[-1]
        if final_value <= 0:
            line_color = "#dc2626"
        elif final_value >= target_money:
            line_color = "#16a34a"
        else:
            line_color = "#2563eb"
        ax.plot(path, color=line_color, alpha=0.35, linewidth=1.2)
        ax.scatter(len(path) - 1, final_value, color=line_color, s=18, alpha=0.8)

    ax.axhline(0, color="#dc2626", linestyle="--", linewidth=1.2, label="Ruin")
    ax.axhline(target_money, color="#16a34a", linestyle="--", linewidth=1.2, label="Target")
    ax.set_title("Sample paths: each line is one possible game")
    ax.set_xlabel("Round")
    ax.set_ylabel("Money")
    ax.grid(True, alpha=0.22)
    ax.legend()
    fig.tight_layout()
    return fig


def create_random_walk_plot(paths, max_paths_to_show):
    fig, ax = plt.subplots(figsize=(10, 5))
    paths_to_show = paths[:max_paths_to_show]

    for path in paths_to_show:
        ax.plot(path, alpha=0.32, linewidth=1.1)

    ax.axhline(0, color="black", linewidth=1, alpha=0.7)
    ax.set_title("Random walk paths: a cloud of possible journeys")
    ax.set_xlabel("Step")
    ax.set_ylabel("Position")
    ax.grid(True, alpha=0.22)
    fig.tight_layout()
    return fig


def create_final_position_histogram(final_positions):
    fig, ax = plt.subplots(figsize=(5, 5))
    ax.hist(final_positions, bins=20, color="#2563eb", edgecolor="white", alpha=0.9)
    ax.axvline(mean(final_positions), color="#f97316", linewidth=2, label="Mean")
    ax.set_title("Where the paths finished")
    ax.set_xlabel("Final position")
    ax.set_ylabel("Paths")
    ax.grid(True, axis="y", alpha=0.22)
    ax.legend()
    fig.tight_layout()
    return fig


def create_brownian_plot(x_positions, y_positions):
    fig, ax = plt.subplots(figsize=(8.5, 8.5))
    color_map = plt.colormaps["tab10"]
    particle_count = x_positions.shape[0]

    for particle_index in range(particle_count):
        color = color_map(particle_index % 10)
        ax.plot(
            x_positions[particle_index],
            y_positions[particle_index],
            color=color,
            linewidth=2.0,
            alpha=0.88,
        )
        ax.scatter(
            x_positions[particle_index, -1],
            y_positions[particle_index, -1],
            color=color,
            s=85,
            edgecolor="black",
            linewidth=0.8,
            zorder=3,
        )

    ax.scatter(0, 0, color="black", s=120, marker="*", label="Start", zorder=4)
    ax.set_title("Brownian motion: tiny random pushes, tangled paths")
    ax.set_xlabel("x position")
    ax.set_ylabel("y position")
    ax.grid(True, alpha=0.22)
    ax.set_aspect("equal", adjustable="datalim")
    ax.legend()
    fig.tight_layout()
    return fig


def create_distance_histogram(final_distances):
    fig, ax = plt.subplots(figsize=(5, 4))
    ax.hist(final_distances, bins=12, color="#16a34a", edgecolor="white", alpha=0.9)
    ax.set_title("Final distance from origin")
    ax.set_xlabel("Distance")
    ax.set_ylabel("Particles")
    ax.grid(True, axis="y", alpha=0.22)
    fig.tight_layout()
    return fig


def format_percent(value):
    return f"{100 * value:.1f}%"


if __name__ == "__main__":
    main()
