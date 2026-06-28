"""
Example demonstrating the Monte-Carlo option pricing model.

Run from the project root:
    python examples/monte_carlo_example.py
"""

from option_pricing.models.monte_carlo import Monte_Carlo

S = 100
K = 100
T = 1
r = 0.05
vol = 0.20
N = 252
M = 100000

call, put = Monte_Carlo(S, K, r, T, vol, N, M)

print("Monte Carlo Simulation Example")
print(f"Call Option Price : {call:.6f}")
print(f"Put Option Price  : {put:.6f}")

