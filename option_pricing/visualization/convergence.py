"""
Convergence analysis: Monte Carlo and Binomial Tree vs Black-Scholes.
"""

import numpy as np
import matplotlib.pyplot as plt
from option_pricing._core import calculate_price, binomial_price, european_price


class ConvergenceAnalysis:

    def __init__(self, S, K, T, r, sigma):
        self.S = S
        self.K = K
        self.T = T
        self.r = r
        self.sigma = sigma

    # Package default kept at full fidelity (100,000 paths) for anyone
    # depending on this library directly. Callers on constrained infra
    # (e.g. the web portal) can pass a smaller `path_counts` to _mc_convergence
    # / plot() instead of this class silently downgrading for everyone.
    DEFAULT_MC_PATH_COUNTS = [100, 500, 1000, 5000, 10000, 50000, 100000]

    def _mc_convergence(self, path_counts=None):
        bs_call, _ = calculate_price(self.S, self.K, self.T, self.r, self.sigma)

        path_counts = path_counts or self.DEFAULT_MC_PATH_COUNTS
        mc_prices = []

        for M in path_counts:
            call, _ = european_price(self.S, self.K, self.T, self.r, self.sigma, N=252, M=M)
            mc_prices.append(call)

        fig, ax = plt.subplots(figsize=(10, 5))
        ax.plot(path_counts, mc_prices, color='navy', linewidth=2, marker='o', label='MC Price')
        ax.axhline(y=bs_call, color='red', linestyle='--', linewidth=1.5, label=f'BS Price ({bs_call:.4f})')
        ax.set_xscale('log')
        ax.set_title('Monte Carlo Convergence')
        ax.set_xlabel('Number of Paths (log scale)')
        ax.set_ylabel('Call Price')
        ax.legend()
        ax.grid(True, alpha=0.3)
        fig.tight_layout()

        return fig

    def _binomial_convergence(self):
        bs_call, _ = calculate_price(self.S, self.K, self.T, self.r, self.sigma)

        step_counts = [5, 10, 20, 50, 100, 200, 500, 1000]
        bin_prices = []

        for N in step_counts:
            call, _ = binomial_price(self.S, self.K, self.T, self.r, self.sigma, N)
            bin_prices.append(call)

        fig, ax = plt.subplots(figsize=(10, 5))
        ax.plot(step_counts, bin_prices, color='green', linewidth=2, marker='o', label='Binomial Price')
        ax.axhline(y=bs_call, color='red', linestyle='--', linewidth=1.5, label=f'BS Price ({bs_call:.4f})')
        ax.set_title('Binomial Tree Convergence')
        ax.set_xlabel('Number of Steps')
        ax.set_ylabel('Call Price')
        ax.legend()
        ax.grid(True, alpha=0.3)
        fig.tight_layout()

        return fig

    def plot(self, kind='all', mc_path_counts=None):
        options = {
            'mc': lambda: self._mc_convergence(path_counts=mc_path_counts),
            'binomial': self._binomial_convergence,
        }

        if kind == 'all':
            return {name: fn() for name, fn in options.items()}
        elif kind in options:
            return options[kind]()
        else:
            raise ValueError(f"Unknown kind '{kind}'. Choose from: 'mc', 'binomial', 'all'")