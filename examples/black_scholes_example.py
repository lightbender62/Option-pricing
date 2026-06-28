"""
Example demonstrating the Black-Scholes option pricing model.

Run from the project root:
    python examples/black_scholes_example.py
"""

from option_pricing import Calculate_Price

S = 100
K = 100
T = 1
r = 0.05
vol = 0.20

Call , Put = Calculate_Price(S , K , T , r , vol)
print("Black-Scholes Pricing Example")
print(f"Call Option Price : {Call:.6f}")
print(f"Put Option Price  : {Put:.6f}")