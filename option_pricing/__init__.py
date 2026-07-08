"""
option_pricing

A Python library for options pricing and quantitative finance analytics.
"""

from .european import EuropeanOption
from .american import AmericanOption
from .exotic import AsianOption, BarrierOption, LookbackOption
from .visualization import (
    VolatilitySurface,
    PayoffDiagram,
    PricingCurves,
    GreeksProfile,
    MonteCarloVisualization,
    ConvergenceAnalysis,
    PriceHeatmap,
    AsianPayoff,
    BarrierPayoff,
    LookbackPayoff,
)

__version__ = "1.0.0"

__all__ = [
    "EuropeanOption",
    "AmericanOption",
    "AsianOption",
    "BarrierOption",
    "LookbackOption",
    "VolatilitySurface",
    "PayoffDiagram",
    "PricingCurves",
    "GreeksProfile",
    "MonteCarloVisualization",
    "ConvergenceAnalysis",
    "PriceHeatmap",
    "AsianPayoff",
    "BarrierPayoff",
    "LookbackPayoff",
]