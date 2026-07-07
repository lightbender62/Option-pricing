"""
option_pricing

A Python library for options pricing and quantitative finance analytics.
"""

from .european import EuropeanOption
from .american import AmericanOption
from .visualization import VolatilitySurface, PayoffDiagram, PricingCurves, GreeksProfile, MonteCarloVisualization,ConvergenceAnalysis,PriceHeatmap

__version__ = "1.0.0"

__all__ = [
    "EuropeanOption",
    "VolatilitySurface",
    "PayoffDiagram",
    "PricingCurves",
    "GreeksProfile",
    "MonteCarloVisualization",
    "ConvergenceAnalysis",
    "PriceHeatmap",
]