"""
Example demonstrating GreeksProfile: sensitivity curves across stock price.

Run from the project root:
    python examples/visualization/greeks_profile_example.py
"""

from option_pricing import GreeksProfile

profile = GreeksProfile(S=100, K=100, T=1, r=0.05, sigma=0.2)

for greek in ("delta", "gamma", "theta", "vega", "rho"):
    profile.plot(greek=greek)
# Or plot all five at once:
# profile.plot(greek="all")