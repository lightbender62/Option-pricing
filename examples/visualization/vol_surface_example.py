"""
Example demonstrating VolatilitySurface: volatility smile and 3D surface
built from real market option chain data.

Requires an internet connection (fetches live data via yfinance).

Run from the project root:
    python examples/visualization/vol_surface_example.py
"""

from option_pricing import VolatilitySurface

vs = VolatilitySurface(ticker="AAPL", r=0.05)

expiries = vs.available_expiries()
print(f"Available expiries: {expiries[:5]} ... ({len(expiries)} total)")

vs.smile(expiry=expiries[2])
vs.surface(num_expiries=10)