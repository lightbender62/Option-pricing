"""
Example demonstrating PricingCurves: option price vs stock/vol/time/rate.

Run from the project root:
    python examples/visualization/pricing_curves_example.py
"""

from option_pricing import PricingCurves

curves = PricingCurves(S=100, K=100, T=1, r=0.05, sigma=0.2)

curves.plot(param="stock")
curves.plot(param="volatility")
curves.plot(param="time")
curves.plot(param="rate")
# Or plot all four at once:
# curves.plot(param="all")