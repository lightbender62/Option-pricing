"""
Example demonstrating BarrierPayoff: payoff scatter against terminal
price, with knocked-out paths greyed.

Run from the project root:
    python examples/visualization/exotic_payoffs/barrier_payoff_example.py
"""

from option_pricing import BarrierPayoff

payoff = BarrierPayoff(S=100, K=100, T=1, r=0.05, sigma=0.2, N=100, M=2000)

payoff.plot(H=90, barrier_type="down-and-out")
payoff.plot(H=110, barrier_type="up-and-in")