"""
Example demonstrating MonteCarloVisualization.lookback_paths: paths with
running max/min overlaid.

Run from the project root:
    python examples/visualization/monte_carlo/lookback_paths_example.py
"""

from option_pricing import MonteCarloVisualization

mc = MonteCarloVisualization(S=100, K=100, T=1, r=0.05, sigma=0.2, N=100, M=2000)

mc.plot(kind="lookback", num_paths=8)