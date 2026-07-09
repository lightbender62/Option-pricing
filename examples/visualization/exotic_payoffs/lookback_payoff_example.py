"""
Example demonstrating LookbackPayoff: payoff scatter for floating and
fixed strike variants.

Run from the project root:
    python examples/visualization/exotic_payoffs/lookback_payoff_example.py
"""

from option_pricing import LookbackPayoff

payoff = LookbackPayoff(S=100, K=100, T=1, r=0.05, sigma=0.2, N=100, M=2000)

payoff.plot(strike_type="floating")
payoff.plot(strike_type="fixed")