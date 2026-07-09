"""
Example demonstrating AsianPayoff: payoff scatter against path average.

Run from the project root:
    python examples/visualization/exotic_payoffs/asian_payoff_example.py
"""

from option_pricing import AsianPayoff

payoff = AsianPayoff(S=100, K=100, T=1, r=0.05, sigma=0.2, N=100, M=2000)

payoff.plot(average="arithmetic")
payoff.plot(average="geometric")