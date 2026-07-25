"""
Payoff diagram for Lookback options.

Simulates paths and scatters the realized call/put payoff against
terminal price, for both floating-strike and fixed-strike variants.
"""

import numpy as np
import matplotlib.pyplot as plt
from option_pricing._core import simulate_paths


class LookbackPayoff:
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

    def plot(self, strike_type='floating'):
        """Scatter lookback call/put payoff against terminal price."""

        paths = simulate_paths(self.S, self.T, self.r, self.sigma, self.N, self.M)
        ST = paths[-1]
        S_min = np.min(paths, axis=0)
        S_max = np.max(paths, axis=0)

        if strike_type == 'floating':
            call_payoff = ST - S_min
            put_payoff = S_max - ST
        elif strike_type == 'fixed':
            call_payoff = np.maximum(S_max - self.K, 0)
            put_payoff = np.maximum(self.K - S_min, 0)
        else:
            raise ValueError(f"Unknown strike_type '{strike_type}'. Choose from: 'floating', 'fixed'")

        fig, ax = plt.subplots(figsize=(10, 5))
        ax.scatter(ST, call_payoff, s=8, alpha=0.4, color='green', label='Call payoff')
        ax.scatter(ST, put_payoff, s=8, alpha=0.4, color='navy', label='Put payoff')
        if strike_type == 'fixed':
            ax.axvline(self.K, color='gray', linestyle='--', label=f'Strike ({self.K})')

        ax.set_title(f'Lookback Option Payoff ({strike_type} strike)')
        ax.set_xlabel('Terminal Stock Price')
        ax.set_ylabel('Payoff')
        ax.legend()
        ax.grid(True, alpha=0.3)
        fig.tight_layout()

        return fig