"""
Example demonstrating MonteCarloVisualization.asian_average: paths with
their running average overlaid.

Run from the project root:
    python examples/visualization/monte_carlo/asian_average_example.py
"""

from option_pricing import MonteCarloVisualization

mc = MonteCarloVisualization(S=100, K=100, T=1, r=0.05, sigma=0.2, N=100, M=2000)

mc.plot(kind="asian", num_paths=8)