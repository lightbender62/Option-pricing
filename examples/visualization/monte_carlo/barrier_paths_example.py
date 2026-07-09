"""
Example demonstrating MonteCarloVisualization.barrier_paths: paths colored
by whether they crossed the barrier.

Run from the project root:
    python examples/visualization/monte_carlo/barrier_paths_example.py
"""

from option_pricing import MonteCarloVisualization

mc = MonteCarloVisualization(S=100, K=100, T=1, r=0.05, sigma=0.2, N=100, M=2000)

mc.plot(kind="barrier", H=90, barrier_type="down-and-out", num_paths=60)