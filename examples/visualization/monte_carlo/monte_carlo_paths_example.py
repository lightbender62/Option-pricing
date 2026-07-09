"""
Example demonstrating MonteCarloVisualization: simulated paths and the
terminal price distribution.

Run from the project root:
    python examples/visualization/monte_carlo/monte_carlo_paths_example.py
"""

from option_pricing import MonteCarloVisualization

mc = MonteCarloVisualization(S=100, K=100, T=1, r=0.05, sigma=0.2, N=100, M=2000)

mc.plot(kind="paths", num_paths=50)
mc.plot(kind="distribution")