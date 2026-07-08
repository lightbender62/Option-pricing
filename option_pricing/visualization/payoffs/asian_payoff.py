"""
Payoff diagram for Asian options.

Unlike european payoffs, the Asian payoff depends on the whole price path
average, not just the terminal price. This simulates paths and scatters
the realized payoff against each path's average price.
"""

import numpy as np
import matplotlib.pyplot as plt
from option_pricing._core import simulate_paths


class AsianPayoff:
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

    def plot(self, average='arithmetic'):
        """Scatter Asian call/put payoff against the path's average price."""

        paths = simulate_paths(self.S, self.T, self.r, self.sigma, self.N, self.M)

        if average == 'arithmetic':
            avg_price = np.mean(paths[1:], axis=0)
        elif average == 'geometric':
            avg_price = np.exp(np.mean(np.log(paths[1:]), axis=0))
        else:
            raise ValueError(f"Unknown average '{average}'. Choose from: 'arithmetic', 'geometric'")

        call_payoff = np.maximum(avg_price - self.K, 0)
        put_payoff = np.maximum(self.K - avg_price, 0)

        plt.figure(figsize=(10, 5))
        plt.scatter(avg_price, call_payoff, s=8, alpha=0.4, color='green', label='Call payoff')
        plt.scatter(avg_price, put_payoff, s=8, alpha=0.4, color='navy', label='Put payoff')
        plt.axvline(self.K, color='gray', linestyle='--', label=f'Strike ({self.K})')

        plt.title(f'Asian Option Payoff ({average} average)')
        plt.xlabel('Average Price Over Path')
        plt.ylabel('Payoff')
        plt.legend()
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.show()