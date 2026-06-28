"""
Example demonstrating the calculation of implied volatility.

Run from the project root:
    python examples/implied_volatility_example.py
"""

from option_pricing import Implied_vol

S = 100
K = 100
T = 1
r = 0.05

market_call = 10.450584
market_put = 5.573526

call_iv, put_iv = Implied_vol(S, K, T, r, market_call, market_put)

print("Implied Volatility Example")
print(f"Call IV : {call_iv:.6f}")
print(f"Put IV  : {put_iv:.6f}")