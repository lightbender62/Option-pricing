"""
Price heatmap: option price across stock price and volatility grid.
"""

import numpy as np
import matplotlib.pyplot as plt
from option_pricing._core import calculate_price


class PriceHeatmap:

    def __init__(self, S, K, T, r, sigma):
        self.S = S
        self.K = K
        self.T = T
        self.r = r
        self.sigma = sigma

    def plot(self, option='call'):
        if option not in ('call', 'put'):
            raise ValueError(f"Unknown option '{option}'. Choose from: 'call', 'put'")
        S_range = np.linspace(0.5 * self.S, 1.5 * self.S, 50)
        sigma_range = np.linspace(0.05, 0.8, 50)

        prices = np.zeros((len(sigma_range), len(S_range)))

        for i, sig in enumerate(sigma_range):
            for j, s in enumerate(S_range):
                call, put = calculate_price(s, self.K, self.T, self.r, sig)
                prices[i, j] = call if option == 'call' else put

        fig, ax = plt.subplots(figsize=(10, 6))
        contour = ax.contourf(S_range, sigma_range * 100, prices, levels=30, cmap='Blues')
        fig.colorbar(contour, ax=ax, label='Option Price')

        ax.axvline(x=self.S, color='red', linestyle='--', linewidth=1.5, label=f'Current S ({self.S})')
        ax.axvline(x=self.K, color='black', linestyle='--', linewidth=1.5, label=f'Strike ({self.K})')
        ax.axhline(y=self.sigma * 100, color='white', linestyle='--', linewidth=1.5, label=f'Current Vol ({self.sigma*100:.0f}%)')

        ax.set_title(f'{"Call" if option == "call" else "Put"} Price Heatmap — Stock Price × Volatility')
        ax.set_xlabel('Stock Price')
        ax.set_ylabel('Volatility (%)')
        ax.legend()
        fig.tight_layout()

        return fig