"""
Greeks profiles: sensitivity visualization across stock prices.
"""

import numpy as np
import matplotlib.pyplot as plt
from option_pricing._core import calculate_greeks


class GreeksProfile:

    def __init__(self, S, K, T, r, sigma):
        self.S = S
        self.K = K
        self.T = T
        self.r = r
        self.sigma = sigma

    def _plot_greek(self, call_values, put_values, title, ylabel):
        S_range = np.linspace(0.5 * self.S, 1.5 * self.S, 200)

        fig, ax = plt.subplots(figsize=(10, 5))
        ax.plot(S_range, call_values, color='green', linewidth=2, label='Call')
        ax.plot(S_range, put_values, color='red', linewidth=2, label='Put')
        ax.axvline(x=self.S, color='gray', linestyle='--', label=f'Current S ({self.S})')
        ax.axvline(x=self.K, color='black', linestyle='--', label=f'Strike ({self.K})')
        ax.set_title(title)
        ax.set_xlabel('Stock Price')
        ax.set_ylabel(ylabel)
        ax.legend()
        ax.grid(True, alpha=0.3)
        fig.tight_layout()

        return fig

    def _compute_all(self):
        S_range = np.linspace(0.5 * self.S, 1.5 * self.S, 200)
        results = [calculate_greeks(s, self.K, self.T, self.r, self.sigma) for s in S_range]

        delta_call = [r[0] for r in results]
        delta_put  = [r[1] for r in results]
        gamma      = [r[2] for r in results]
        theta_call = [r[3] for r in results]
        theta_put  = [r[4] for r in results]
        vega       = [r[5] for r in results]
        rho_call   = [r[6] for r in results]
        rho_put    = [r[7] for r in results]

        return delta_call, delta_put, gamma, theta_call, theta_put, vega, rho_call, rho_put

    def plot(self, greek='all'):
        delta_call, delta_put, gamma, theta_call, theta_put, vega, rho_call, rho_put = self._compute_all()

        options = {
            'delta':  lambda: self._plot_greek(delta_call, delta_put, 'Delta vs Stock Price', 'Delta'),
            'gamma':  lambda: self._plot_greek(gamma, gamma, 'Gamma vs Stock Price', 'Gamma'),
            'theta':  lambda: self._plot_greek(theta_call, theta_put, 'Theta vs Stock Price', 'Theta (daily)'),
            'vega':   lambda: self._plot_greek(vega, vega, 'Vega vs Stock Price', 'Vega'),
            'rho':    lambda: self._plot_greek(rho_call, rho_put, 'Rho vs Stock Price', 'Rho'),
        }

        if greek == 'all':
            return {name: fn() for name, fn in options.items()}
        elif greek in options:
            return options[greek]()
        else:
            raise ValueError(f"Unknown greek '{greek}'. Choose from: 'delta', 'gamma', 'theta', 'vega', 'rho', 'all'")