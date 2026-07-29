"""
Example demonstrating PricingCurves: option price vs stock/vol/time/rate.

Run from the project root:
    python examples/visualization/pricing_curves_example.py
"""

from option_pricing import PricingCurves
import matplotlib.pyplot as plt

curves = PricingCurves(S=100, K=100, T=1, r=0.05, sigma=0.2)

curves.plot(param="stock")
plt.show()

curves.plot(param="volatility")
plt.show()

curves.plot(param="time")
plt.show()

curves.plot(param="rate")
plt.show()

# Or plot all four at once:
# curves.plot(param="all")