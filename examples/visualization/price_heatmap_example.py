"""
Example demonstrating PriceHeatmap: option price across a stock price x
volatility grid.

Run from the project root:
    python examples/visualization/price_heatmap_example.py
"""

from option_pricing import PriceHeatmap

heatmap = PriceHeatmap(S=100, K=100, T=1, r=0.05, sigma=0.2)

heatmap.plot(option="call")
heatmap.plot(option="put")