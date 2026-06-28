"""
option_pricing

A Python package for pricing European options using
Black-Scholes, Binomial Tree, and Monte Carlo methods,
along with option Greeks and implied volatility calculations.
"""

from .models import Calculate_Price, Binomial_model, Monte_Carlo
from .analytics import Greeks, Implied_vol

__version__ = "1.0.0"

__all__ = [
    "Calculate_Price",
    "Binomial_model",
    "Monte_Carlo",
    "Greeks",
    "Implied_vol",
]