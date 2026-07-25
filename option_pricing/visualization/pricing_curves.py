"""
Pricing curves: option price vs various parameters.
"""

import numpy as np
import matplotlib.pyplot as plt
from option_pricing._core import calculate_price


class PricingCurves:

    def __init__(self, S, K, T, r, sigma):
        self.S = S
        self.K = K
        self.T = T
        self.r = r
        self.sigma = sigma

    def _vs_stock(self):
        S_range = np.linspace(0.5 * self.S, 1.5 * self.S, 200)
        calls, puts = zip(*[calculate_price(s, self.K, self.T, self.r, self.sigma) for s in S_range])

        fig, ax = plt.subplots(figsize=(10, 5))
        ax.plot(S_range, calls, color='green', linewidth=2, label='Call')
        ax.plot(S_range, puts, color='red', linewidth=2, label='Put')
        ax.axvline(x=self.S, color='gray', linestyle='--', label=f'Current S ({self.S})')
        ax.axvline(x=self.K, color='black', linestyle='--', label=f'Strike ({self.K})')
        ax.set_title('Option Price vs Stock Price')
        ax.set_xlabel('Stock Price')
        ax.set_ylabel('Option Price')
        ax.legend()
        ax.grid(True, alpha=0.3)
        fig.tight_layout()

        return fig

    def _vs_volatility(self):
        sigma_range = np.linspace(0.01, 1.0, 200)
        calls, puts = zip(*[calculate_price(self.S, self.K, self.T, self.r, s) for s in sigma_range])

        fig, ax = plt.subplots(figsize=(10, 5))
        ax.plot(sigma_range * 100, calls, color='green', linewidth=2, label='Call')
        ax.plot(sigma_range * 100, puts, color='red', linewidth=2, label='Put')
        ax.axvline(x=self.sigma * 100, color='gray', linestyle='--', label=f'Current σ ({self.sigma*100:.0f}%)')
        ax.set_title('Option Price vs Volatility')
        ax.set_xlabel('Volatility (%)')
        ax.set_ylabel('Option Price')
        ax.legend()
        ax.grid(True, alpha=0.3)
        fig.tight_layout()

        return fig

    def _vs_time(self):
        T_range = np.linspace(0.01, 2.0, 200)
        calls, puts = zip(*[calculate_price(self.S, self.K, t, self.r, self.sigma) for t in T_range])

        fig, ax = plt.subplots(figsize=(10, 5))
        ax.plot(T_range, calls, color='green', linewidth=2, label='Call')
        ax.plot(T_range, puts, color='red', linewidth=2, label='Put')
        ax.axvline(x=self.T, color='gray', linestyle='--', label=f'Current T ({self.T})')
        ax.set_title('Option Price vs Time to Maturity')
        ax.set_xlabel('Time to Maturity (Years)')
        ax.set_ylabel('Option Price')
        ax.legend()
        ax.grid(True, alpha=0.3)
        fig.tight_layout()

        return fig

    def _vs_rate(self):
        r_range = np.linspace(0.0, 0.2, 200)
        calls, puts = zip(*[calculate_price(self.S, self.K, self.T, r, self.sigma) for r in r_range])

        fig, ax = plt.subplots(figsize=(10, 5))
        ax.plot(r_range * 100, calls, color='green', linewidth=2, label='Call')
        ax.plot(r_range * 100, puts, color='red', linewidth=2, label='Put')
        ax.axvline(x=self.r * 100, color='gray', linestyle='--', label=f'Current r ({self.r*100:.0f}%)')
        ax.set_title('Option Price vs Interest Rate')
        ax.set_xlabel('Interest Rate (%)')
        ax.set_ylabel('Option Price')
        ax.legend()
        ax.grid(True, alpha=0.3)
        fig.tight_layout()

        return fig

    def plot(self, param='all'):
        options = {
            'stock': self._vs_stock,
            'volatility': self._vs_volatility,
            'time': self._vs_time,
            'rate': self._vs_rate,
        }

        if param == 'all':
            return {name: fn() for name, fn in options.items()}
        elif param in options:
            return options[param]()
        else:
            raise ValueError(f"Unknown param '{param}'. Choose from: 'stock', 'volatility', 'time', 'rate', 'all'")