"""
Convergence analysis: Monte Carlo and Binomial Tree vs Black-Scholes.
"""

import numpy as np
import matplotlib.pyplot as plt
from option_pricing._core import calculate_price, binomial_price, monte_carlo_price


class ConvergenceAnalysis:

    def __init__(self, S, K, T, r, sigma):
        self.S = S
        self.K = K
        self.T = T
        self.r = r
        self.sigma = sigma

    def _mc_convergence(self):
        bs_call, _ = calculate_price(self.S, self.K, self.T, self.r, self.sigma)

        path_counts = [100, 500, 1000, 5000, 10000, 50000, 100000]
        mc_prices = []

        for M in path_counts:
            call, _ = monte_carlo_price(self.S, self.K, self.T, self.r, self.sigma, N=252, M=M)
            mc_prices.append(call)

        plt.figure(figsize=(10, 5))
        plt.plot(path_counts, mc_prices, color='navy', linewidth=2, marker='o', label='MC Price')
        plt.axhline(y=bs_call, color='red', linestyle='--', linewidth=1.5, label=f'BS Price ({bs_call:.4f})')
        plt.xscale('log')
        plt.title('Monte Carlo Convergence')
        plt.xlabel('Number of Paths (log scale)')
        plt.ylabel('Call Price')
        plt.legend()
        plt.grid(True, alpha=0.3)
        plt.tight_layout()

    def _binomial_convergence(self):
        bs_call, _ = calculate_price(self.S, self.K, self.T, self.r, self.sigma)

        step_counts = [5, 10, 20, 50, 100, 200, 500, 1000]
        bin_prices = []

        for N in step_counts:
            call, _ = binomial_price(self.S, self.K, self.T, self.r, self.sigma, N)
            bin_prices.append(call)

        plt.figure(figsize=(10, 5))
        plt.plot(step_counts, bin_prices, color='green', linewidth=2, marker='o', label='Binomial Price')
        plt.axhline(y=bs_call, color='red', linestyle='--', linewidth=1.5, label=f'BS Price ({bs_call:.4f})')
        plt.title('Binomial Tree Convergence')
        plt.xlabel('Number of Steps')
        plt.ylabel('Call Price')
        plt.legend()
        plt.grid(True, alpha=0.3)
        plt.tight_layout()

    def plot(self, kind='all'):
        options = {
            'mc': self._mc_convergence,
            'binomial': self._binomial_convergence,
        }

        if kind == 'all':
            for fn in options.values():
                fn()
        elif kind in options:
            options[kind]()
        else:
            raise ValueError(f"Unknown kind '{kind}'. Choose from: 'mc', 'binomial', 'all'")

        plt.show()