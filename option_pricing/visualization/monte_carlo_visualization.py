"""
Monte Carlo simulation visualizations.
"""

import numpy as np
import matplotlib.pyplot as plt
from option_pricing._core import simulate_paths

class MonteCarloVisualization:
    def __init__(self, S, K, T, r, sigma, N, M):
        self.S = S
        self.K = K
        self.T = T
        self.r = r
        self.sigma = sigma
        self.N = N
        self.M = M

    def terminal_distribution(self):
        """Plot histogram of terminal stock prices."""

        paths = simulate_paths(
            self.S,
            self.T,
            self.r,
            self.sigma,
            self.N,
            self.M,
        )

        ST = paths[-1]

        plt.figure(figsize=(10, 5))

        plt.hist(
            ST,
            bins=40,
            edgecolor="black",
            alpha=0.7,
        )

        plt.axvline(
            np.mean(ST),
            color="red",
            linestyle="--",
            linewidth=2,
            label=f"Mean ({np.mean(ST):.2f})",
        )

        plt.axvline(
            self.S,
            color="green",
            linestyle="--",
            linewidth=2,
            label=f"Initial Price ({self.S:.2f})",
        )

        plt.axvline(
            self.K,
            color="navy",
            linestyle=":",
            linewidth=2,
            label=f"Strike ({self.K:.2f})",
        )

        plt.title("Terminal Stock Price Distribution")
        plt.xlabel("Terminal Stock Price")
        plt.ylabel("Frequency")

        plt.legend()
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.show()

    
    def paths(self, num_paths=50):
        """Plot simulated stock price paths."""

        all_paths = simulate_paths(
            self.S,
            self.T,
            self.r,
            self.sigma,
            self.N,
            self.M,
        )

        time_steps = np.linspace(0, self.T, self.N + 1)

        plt.figure(figsize=(10, 5))

        for i in range(min(num_paths, self.M)):
            plt.plot(
                time_steps,
                all_paths[:, i],
                linewidth=0.8,
                alpha=0.6,
            )

        plt.axhline(
            self.K,
            color="black",
            linestyle="--",
            linewidth=1.5,
            label=f"Strike ({self.K})",
        )

        plt.axhline(
            self.S,
            color="red",
            linestyle="--",
            linewidth=1.5,
            label=f"Initial Price ({self.S})",
        )

        plt.title(f"Simulated Stock Price Paths (n={num_paths})")
        plt.xlabel("Time (Years)")
        plt.ylabel("Stock Price")
        plt.legend()
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.show()
    
    def plot(self, kind='all', num_paths=50):
        if kind == 'paths':
            self.paths(num_paths)
        elif kind == 'distribution':
            self.terminal_distribution()
        elif kind == 'all':
            self.paths(num_paths)
            self.terminal_distribution()
        else:
            raise ValueError(f"Unknown kind '{kind}'. Choose from: 'paths', 'distribution', 'all'")
        