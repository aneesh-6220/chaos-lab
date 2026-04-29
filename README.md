# Chaos Lab

Live app: _Add your Streamlit Community Cloud link here after deployment._

Chaos Lab is an interactive probability playground for exploring randomness through gambler's ruin, random walks, Brownian motion, and intuition-testing simulations.

Built by Aneesh Mahatekar

The project is built for a Grade 10 Python learner who wants a visual, hands-on app that feels more like a math lab than a statistics dashboard. Each section is a small experiment: choose settings, run the simulation, study the chart, and read what to try next.

## Features

- Streamlit app with clear experiment navigation
- Controls placed inside each experiment instead of one global sidebar
- Gambler's ruin simulation with risk interpretation
- Random walk playground with path chart and final-position histogram
- Brownian motion explorer with colorful 2D particle paths
- Intuition vs Reality mini challenge with feedback
- Beginner-readable Python modules for simulation logic
- Simple custom CSS for a more polished visual identity
- Safe input limits for Streamlit Community Cloud

## Screenshots

Screenshots can be added to the `screenshots/` folder after running the app.

Suggested screenshots:

- Home page experiment cards
- Gambler's ruin sample paths and metrics
- Random walk path cloud and histogram
- Brownian motion particle paths
- Intuition vs Reality challenge result

## Experiments

### Gambler's Ruin

The player starts with money and repeatedly makes the same size bet. A win adds money; a loss subtracts money. The simulation stops when the player reaches zero, reaches the target, or hits the maximum number of rounds.

Things to try:

- Change win probability from `0.50` to `0.49`.
- Increase the bet size.
- Move the target farther away.

This experiment shows how small probability changes can matter when repeated many times.

### Random Walk

A path starts at zero. At every step, it moves up or down, with optional drift pushing it slightly in one direction.

Things to try:

- Increase the number of steps.
- Set drift to a small positive or negative value.
- Compare the path chart with the histogram of final positions.

This experiment shows how randomness creates spread, even when there is no preferred direction.

### Brownian Motion

Particles start at the origin. On each step, every particle receives a random x push and a random y push.

Things to try:

- Increase the number of steps.
- Increase the step size.
- Increase the number of particles.

This experiment connects to physics and diffusion. The paths look chaotic because many tiny random movements accumulate over time.

### Intuition vs Reality

The user guesses the probability of ruin before running the simulation. The app then reveals the simulated probability and gives feedback based on the error.

This turns probability into a small challenge and helps build better intuition.

## What I Learned

This project practices:

- Splitting Streamlit UI code from simulation logic
- Using NumPy to generate repeatable random simulations
- Building Matplotlib charts for paths and histograms
- Estimating probability by counting repeated outcomes
- Designing an app around exploration instead of only displaying results
- Writing explanations that help a beginner understand what to change and why

## How to Run Locally

1. Open a terminal.
2. Move into the project folder:

   ```bash
   cd chaos-lab
   ```

3. Create a virtual environment:

   ```bash
   python -m venv .venv
   ```

4. Activate the virtual environment:

   On macOS or Linux:

   ```bash
   source .venv/bin/activate
   ```

   On Windows:

   ```bash
   .venv\Scripts\activate
   ```

5. Install the required packages:

   ```bash
   pip install -r requirements.txt
   ```

6. Run the app:

   ```bash
   streamlit run app.py
   ```

## How to Deploy on Streamlit Community Cloud

1. Put this project in a GitHub repository.
2. Go to [Streamlit Community Cloud](https://streamlit.io/cloud).
3. Choose "New app".
4. Select the repository and branch.
5. Set the main file path to:

   ```text
   app.py
   ```

6. Click deploy.
7. Copy the deployed app link into the Live app section at the top of this README.

## Project Structure

```text
chaos-lab/
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
├── screenshots/
│   └── .gitkeep
└── src/
    ├── __init__.py
    ├── gambler.py
    ├── random_walk.py
    ├── brownian.py
    └── metrics.py
```

## Limitations

- Simulation results are estimates, not exact mathematical proofs.
- The input controls are capped so the app stays responsive.
- Brownian motion is simplified and does not model every detail of real physics.
- Streamlit forms mean changes apply after pressing the run button in each experiment.

## Future Improvements

- Add Brownian motion animation.
- Add exact gambler's ruin formulas for comparison.
- Add a two-dimensional grid random walk.
- Add downloadable simulation summaries.
- Add a quiz mode with multiple probability challenges.
