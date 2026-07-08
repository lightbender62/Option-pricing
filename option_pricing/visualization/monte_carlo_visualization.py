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
    
    def barrier_paths(self, H, barrier_type, num_paths=50):
        """Plot simulated paths, highlighting which ones cross the barrier."""

        if "down" in barrier_type and H >= self.S:
            raise ValueError("For down barriers, H must be less than S.")
        if "up" in barrier_type and H <= self.S:
            raise ValueError("For up barriers, H must be greater than S.")

        all_paths = simulate_paths(
            self.S,
            self.T,
            self.r,
            self.sigma,
            self.N,
            self.M,
        )

        time_steps = np.linspace(0, self.T, self.N + 1)

        if "down" in barrier_type:
            crossed = np.any(all_paths <= H, axis=0)
        elif "up" in barrier_type:
            crossed = np.any(all_paths >= H, axis=0)
        else:
            raise ValueError(
                "Invalid barrier type. Choose from "
                "'down-and-out', 'down-and-in', "
                "'up-and-out', 'up-and-in'."
            )

        plt.figure(figsize=(10, 5))

        plotted = 0
        for i in range(self.M):
            if plotted >= num_paths:
                break
            color = "red" if crossed[i] else "steelblue"
            plt.plot(
                time_steps,
                all_paths[:, i],
                linewidth=0.8,
                alpha=0.6,
                color=color,
            )
            plotted += 1

        plt.axhline(
            H,
            color="black",
            linestyle="--",
            linewidth=1.5,
            label=f"Barrier ({H})",
        )

        plt.axhline(
            self.S,
            color="green",
            linestyle="--",
            linewidth=1.5,
            label=f"Initial Price ({self.S})",
        )

        plt.plot([], [], color="red", linewidth=2, label="Crossed barrier")
        plt.plot([], [], color="steelblue", linewidth=2, label="Never crossed")

        plt.title(f"Barrier Path Visualization ({barrier_type})")
        plt.xlabel("Time (Years)")
        plt.ylabel("Stock Price")
        plt.legend()
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.show()

    def lookback_paths(self, num_paths=10):
        """Plot simulated paths with their running max and min highlighted."""

        all_paths = simulate_paths(
            self.S,
            self.T,
            self.r,
            self.sigma,
            self.N,
            self.M,
        )

        time_steps = np.linspace(0, self.T, self.N + 1)
        n_shown = min(num_paths, self.M)

        plt.figure(figsize=(10, 5))

        for i in range(n_shown):
            path = all_paths[:, i]
            running_max = np.maximum.accumulate(path)
            running_min = np.minimum.accumulate(path)

            line, = plt.plot(time_steps, path, linewidth=1.0, alpha=0.7)
            plt.plot(
                time_steps,
                running_max,
                linestyle="--",
                linewidth=0.8,
                alpha=0.5,
                color=line.get_color(),
            )
            plt.plot(
                time_steps,
                running_min,
                linestyle=":",
                linewidth=0.8,
                alpha=0.5,
                color=line.get_color(),
            )

        plt.plot([], [], color="gray", linestyle="-", label="Path")
        plt.plot([], [], color="gray", linestyle="--", label="Running max")
        plt.plot([], [], color="gray", linestyle=":", label="Running min")

        plt.title(f"Lookback Path Visualization (n={n_shown})")
        plt.xlabel("Time (Years)")
        plt.ylabel("Stock Price")
        plt.legend()
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.show()

    def asian_average(self, num_paths=10):
        """Plot simulated paths with their running average overlaid."""

        all_paths = simulate_paths(
            self.S,
            self.T,
            self.r,
            self.sigma,
            self.N,
            self.M,
        )

        time_steps = np.linspace(0, self.T, self.N + 1)
        n_shown = min(num_paths, self.M)

        plt.figure(figsize=(10, 5))

        for i in range(n_shown):
            path = all_paths[:, i]
            running_avg = np.cumsum(path) / np.arange(1, len(path) + 1)

            line, = plt.plot(time_steps, path, linewidth=1.0, alpha=0.5)
            plt.plot(
                time_steps,
                running_avg,
                linestyle="--",
                linewidth=1.3,
                color=line.get_color(),
            )

        plt.axhline(
            self.K,
            color="black",
            linestyle=":",
            linewidth=1.5,
            label=f"Strike ({self.K})",
        )

        plt.plot([], [], color="gray", linestyle="-", label="Path")
        plt.plot([], [], color="gray", linestyle="--", label="Running average")

        plt.title(f"Asian Average Visualization (n={n_shown})")
        plt.xlabel("Time (Years)")
        plt.ylabel("Stock Price")
        plt.legend()
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.show()

    def plot(self, kind='all', num_paths=50, H=None, barrier_type=None):
        if kind == 'paths':
            self.paths(num_paths)
        elif kind == 'distribution':
            self.terminal_distribution()
        elif kind == 'barrier':
            if H is None or barrier_type is None:
                raise ValueError("kind='barrier' requires H and barrier_type")
            self.barrier_paths(H, barrier_type, num_paths)
        elif kind == 'lookback':
            self.lookback_paths(num_paths)
        elif kind == 'asian':
            self.asian_average(num_paths)
        elif kind == 'all':
            self.paths(num_paths)
            self.terminal_distribution()
        else:
            raise ValueError(
                f"Unknown kind '{kind}'. Choose from: "
                "'paths', 'distribution', 'barrier', 'lookback', 'asian', 'all'"
            )