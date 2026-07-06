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
        S_range = np.linspace(0.5 * self.S, 1.5 * self.S, 50)
        sigma_range = np.linspace(0.05, 0.8, 50)

        prices = np.zeros((len(sigma_range), len(S_range)))

        for i, sig in enumerate(sigma_range):
            for j, s in enumerate(S_range):
                call, put = calculate_price(s, self.K, self.T, self.r, sig)
                prices[i, j] = call if option == 'call' else put

        plt.figure(figsize=(10, 6))
        plt.contourf(S_range, sigma_range * 100, prices, levels=30, cmap='Blues')
        plt.colorbar(label='Option Price')

        plt.axvline(x=self.S, color='red', linestyle='--', linewidth=1.5, label=f'Current S ({self.S})')
        plt.axvline(x=self.K, color='black', linestyle='--', linewidth=1.5, label=f'Strike ({self.K})')
        plt.axhline(y=self.sigma * 100, color='white', linestyle='--', linewidth=1.5, label=f'Current Vol ({self.sigma*100:.0f}%)')

        plt.title(f'{"Call" if option == "call" else "Put"} Price Heatmap — Stock Price × Volatility')
        plt.xlabel('Stock Price')
        plt.ylabel('Volatility (%)')
        plt.legend()
        plt.tight_layout()
        plt.show()