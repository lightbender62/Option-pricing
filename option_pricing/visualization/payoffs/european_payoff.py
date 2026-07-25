"""
Payoff diagrams for European options.
"""

import numpy as np
import matplotlib.pyplot as plt

class PayoffDiagram:
    def __init__(self, K, premium=0):
        if K <= 0:
            raise ValueError(f"K must be positive, got {K}")
        if premium < 0:
            raise ValueError(f"premium must be non-negative, got {premium}")
        self.K = K
        self.premium = premium

    def call(self):
        S_range = np.linspace(0.5 * self.K, 1.5 * self.K, 300)
        call_payoff = np.maximum(S_range - self.K, 0) - self.premium
        breakeven = self.K + self.premium

        fig, ax = plt.subplots(figsize=(10, 5))
        ax.plot(S_range, call_payoff, color='navy', linewidth=2, label='Call')
        ax.axhline(y=0, color='black', linewidth=0.8)
        ax.axvline(x=self.K, color='gray', linestyle='--', label='Strike')
        ax.axvline(breakeven, color="red", linestyle=":", label="Break-even")

        ax.set_title('Option Payoff Diagram')
        ax.set_xlabel('Stock Price at Expiry')
        ax.set_ylabel('Profit / Loss')
        ax.legend()
        ax.grid(True, alpha=0.3)
        fig.tight_layout()

        return fig

    def put(self):
        S_range = np.linspace(0.5 * self.K, 1.5 * self.K, 300)
        put_payoff = np.maximum(self.K - S_range, 0) - self.premium
        breakeven = self.K - self.premium

        fig, ax = plt.subplots(figsize=(10, 5))
        ax.plot(S_range, put_payoff, color='navy', linewidth=2, label='Put')
        ax.axhline(y=0, color='black', linewidth=0.8)
        ax.axvline(x=self.K, color='gray', linestyle='--', label='Strike')
        ax.axvline(breakeven, color="red", linestyle=":", label="Break-even")

        ax.set_title('Option Payoff Diagram')
        ax.set_xlabel('Stock Price at Expiry')
        ax.set_ylabel('Profit / Loss')
        ax.legend()
        ax.grid(True, alpha=0.3)
        fig.tight_layout()

        return fig

    def both(self):
        S_range = np.linspace(0.5 * self.K, 1.5 * self.K, 300)
        call_payoff = np.maximum(S_range - self.K, 0) - self.premium
        put_payoff = np.maximum(self.K - S_range, 0) - self.premium
        put_breakeven = self.K - self.premium
        call_breakeven = self.K + self.premium

        fig, ax = plt.subplots(figsize=(10, 5))
        ax.plot(S_range, call_payoff, color='green', linewidth=2, label='Call')
        ax.plot(S_range, put_payoff, color='navy', linewidth=2, label='Put')
        ax.axhline(y=0, color='black', linewidth=0.8)
        ax.axvline(x=self.K, color='gray', linestyle='--', label='Strike')
        ax.axvline(call_breakeven, color="red", linestyle=":", linewidth=1.8, label=f"Call B/E ({call_breakeven:.2f})")
        ax.axvline(put_breakeven, color="darkorange", linestyle=":", linewidth=1.8, label=f"Put B/E ({put_breakeven:.2f})")

        ax.set_title('Option Payoff Diagram')
        ax.set_xlabel('Stock Price at Expiry')
        ax.set_ylabel('Profit / Loss')
        ax.legend()
        ax.grid(True, alpha=0.3)
        fig.tight_layout()

        return fig