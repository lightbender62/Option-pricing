"""
Example demonstrating the calculation of option Greeks.

Run from the project root:
    python examples/greeks_example.py
"""

from option_pricing.analytics.greeks import Greeks

S = 100
K = 100
T = 1
r = 0.05
vol = 0.20

(
    delta_call,
    delta_put,
    gamma,
    theta_call,
    theta_put,
    vega,
    rho_call,
    rho_put,
) = Greeks(S, K, T, r, vol)

print("Greeks Example")
print(f"Call Delta : {delta_call:.6f}")
print(f"Put Delta  : {delta_put:.6f}")
print(f"Gamma      : {gamma:.6f}")
print(f"Call Theta : {theta_call:.6f}")
print(f"Put Theta  : {theta_put:.6f}")
print(f"Vega       : {vega:.6f}")
print(f"Call Rho   : {rho_call:.6f}")
print(f"Put Rho    : {rho_put:.6f}")