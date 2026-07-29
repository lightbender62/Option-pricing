"""
Example demonstrating VolatilitySurface: volatility smile and 3D surface
built from real market option chain data.

Requires an internet connection (fetches live data via yfinance).

Run from the project root:
    python examples/visualization/vol_surface_example.py
"""

from option_pricing import VolatilitySurface
import matplotlib.pyplot as plt

vs = VolatilitySurface(ticker="AAPL", r=0.05)

expiries = vs.available_expiries()
print(f"Available expiries: {expiries[:5]} ... ({len(expiries)} total)")

vs.smile(expiry=expiries[2])
plt.show()
fig = vs.surface(num_expiries=10)
fig.show()