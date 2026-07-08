"""
Payoff diagram for Barrier options.

Simulates paths and scatters the realized call payoff against terminal
price, greying out paths that were voided (or never activated) by the
barrier condition.
"""

import numpy as np
import matplotlib.pyplot as plt
from option_pricing._core import simulate_paths


class BarrierPayoff:
    def __init__(self, S, K, T, r, sigma, N=100, M=2000):
        if K <= 0:
            raise ValueError(f"K must be positive, got {K}")
        self.S = S
        self.K = K
        self.T = T
        self.r = r
        self.sigma = sigma
        self.N = N
        self.M = M

    def plot(self, H, barrier_type):
        """Scatter barrier call payoff against terminal price, marking knocked paths."""

        paths = simulate_paths(self.S, self.T, self.r, self.sigma, self.N, self.M)
        ST = paths[-1]

        if "down" in barrier_type and H >= self.S:
            raise ValueError("For down barriers, H must be less than S.")
        if "up" in barrier_type and H <= self.S:
            raise ValueError("For up barriers, H must be greater than S.")

        call_payoff = np.maximum(ST - self.K, 0)

        if barrier_type in ("down-and-out", "down-and-in"):
            crossed = np.any(paths <= H, axis=0)
        elif barrier_type in ("up-and-out", "up-and-in"):
            crossed = np.any(paths >= H, axis=0)
        else:
            raise ValueError(
                "Invalid barrier type. Choose from "
                "'down-and-out', 'down-and-in', "
                "'up-and-out', 'up-and-in'."
            )

        knocked_out = "out" in barrier_type
        active = ~crossed if knocked_out else crossed

        call_realized = np.where(active, call_payoff, 0)

        plt.figure(figsize=(10, 5))
        plt.scatter(ST[active], call_realized[active], s=8, alpha=0.4, color='green', label='Call payoff (active)')
        plt.scatter(ST[~active], call_realized[~active], s=8, alpha=0.3, color='lightgray', label='Voided by barrier')
        plt.axvline(self.K, color='gray', linestyle='--', label=f'Strike ({self.K})')
        plt.axvline(H, color='black', linestyle=':', label=f'Barrier ({H})')

        plt.title(f'Barrier Option Payoff ({barrier_type})')
        plt.xlabel('Terminal Stock Price')
        plt.ylabel('Call Payoff')
        plt.legend()
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.show()