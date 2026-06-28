"""
Example demonstrating the Binomial-Tree option pricing model.

Run from the project root:
    python examples/binomial_model_example.py
"""

from option_pricing.models.binomial_model import Binomial_model

S = 100
K = 100
T = 1
r = 0.05
vol = 0.20
N = 500

Call, Put = Binomial_model(S, K, T, r, N, vol)

print("Binomial Model Example")
print(f"Call Option Price : {Call:.6f}")
print(f"Put Option Price  : {Put:.6f}")