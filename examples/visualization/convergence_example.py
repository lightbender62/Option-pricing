"""
Example demonstrating ConvergenceAnalysis: Monte Carlo and Binomial Tree
convergence toward the Black-Scholes price.

Run from the project root:
    python examples/visualization/convergence_example.py
"""

from option_pricing import ConvergenceAnalysis

conv = ConvergenceAnalysis(S=100, K=100, T=1, r=0.05, sigma=0.2)

conv.plot(kind="mc")
conv.plot(kind="binomial")
# Or plot both at once:
# conv.plot(kind="all")