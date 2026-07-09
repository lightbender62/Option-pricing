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

        plt.figure(figsize=(10, 5))
        plt.plot(S_range, calls, color='green', linewidth=2, label='Call')
        plt.plot(S_range, puts, color='red', linewidth=2, label='Put')
        plt.axvline(x=self.S, color='gray', linestyle='--', label=f'Current S ({self.S})')
        plt.axvline(x=self.K, color='black', linestyle='--', label=f'Strike ({self.K})')
        plt.title('Option Price vs Stock Price')
        plt.xlabel('Stock Price')
        plt.ylabel('Option Price')
        plt.legend()
        plt.grid(True, alpha=0.3)
        plt.tight_layout()

    def _vs_volatility(self):
        sigma_range = np.linspace(0.01, 1.0, 200)
        calls, puts = zip(*[calculate_price(self.S, self.K, self.T, self.r, s) for s in sigma_range])

        plt.figure(figsize=(10, 5))
        plt.plot(sigma_range * 100, calls, color='green', linewidth=2, label='Call')
        plt.plot(sigma_range * 100, puts, color='red', linewidth=2, label='Put')
        plt.axvline(x=self.sigma * 100, color='gray', linestyle='--', label=f'Current σ ({self.sigma*100:.0f}%)')
        plt.title('Option Price vs Volatility')
        plt.xlabel('Volatility (%)')
        plt.ylabel('Option Price')
        plt.legend()
        plt.grid(True, alpha=0.3)
        plt.tight_layout()

    def _vs_time(self):
        T_range = np.linspace(0.01, 2.0, 200)
        calls, puts = zip(*[calculate_price(self.S, self.K, t, self.r, self.sigma) for t in T_range])

        plt.figure(figsize=(10, 5))
        plt.plot(T_range, calls, color='green', linewidth=2, label='Call')
        plt.plot(T_range, puts, color='red', linewidth=2, label='Put')
        plt.axvline(x=self.T, color='gray', linestyle='--', label=f'Current T ({self.T})')
        plt.title('Option Price vs Time to Maturity')
        plt.xlabel('Time to Maturity (Years)')
        plt.ylabel('Option Price')
        plt.legend()
        plt.grid(True, alpha=0.3)
        plt.tight_layout()

    def _vs_rate(self):
        r_range = np.linspace(0.0, 0.2, 200)
        calls, puts = zip(*[calculate_price(self.S, self.K, self.T, r, self.sigma) for r in r_range])

        plt.figure(figsize=(10, 5))
        plt.plot(r_range * 100, calls, color='green', linewidth=2, label='Call')
        plt.plot(r_range * 100, puts, color='red', linewidth=2, label='Put')
        plt.axvline(x=self.r * 100, color='gray', linestyle='--', label=f'Current r ({self.r*100:.0f}%)')
        plt.title('Option Price vs Interest Rate')
        plt.xlabel('Interest Rate (%)')
        plt.ylabel('Option Price')
        plt.legend()
        plt.grid(True, alpha=0.3)
        plt.tight_layout()

    def plot(self, param='all'):
        options = {
            'stock': self._vs_stock,
            'volatility': self._vs_volatility,
            'time': self._vs_time,
            'rate': self._vs_rate,
        }

        if param == 'all':
            for fn in options.values():
                fn()
            plt.show()
        elif param in options:
            options[param]()
            plt.show()
        else:
            raise ValueError(f"Unknown param '{param}'. Choose from: 'stock', 'volatility', 'time', 'rate', 'all'")