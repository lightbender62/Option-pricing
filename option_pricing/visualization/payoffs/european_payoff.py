"""
Payoff diagrams for European options.
"""

import numpy as np
import matplotlib.pyplot as plt

class PayoffDiagram:
    def __init__(self, K, premium=0):
        self.K = K
        self.premium = premium

    def call(self):
        S_range = np.linspace(0.5 * self.K, 1.5 * self.K, 300)
        call_payoff = np.maximum(S_range - self.K, 0) - self.premium
        breakeven = self.K + self.premium

        plt.figure(figsize=(10, 5))
        plt.plot(S_range, call_payoff, color='navy', linewidth=2, label='Call')
        plt.axhline(y=0, color='black', linewidth=0.8)
        plt.axvline(x=self.K, color='gray', linestyle='--', label='Strike')
        plt.axvline(breakeven, color="red", linestyle=":", label="Break-even")

        plt.title('Option Payoff Diagram')
        plt.xlabel('Stock Price at Expiry') 
        plt.ylabel('Profit / Loss')         
        plt.legend()                       
        plt.grid(True, alpha=0.3)         
        plt.tight_layout()                 
        plt.show()           

    def put(self):
        S_range = np.linspace(0.5 * self.K, 1.5 * self.K, 300)
        put_payoff = np.maximum(self.K - S_range, 0) - self.premium
        breakeven = self.K - self.premium

        plt.figure(figsize=(10, 5))
        plt.plot(S_range, put_payoff, color='navy', linewidth=2, label='Put')
        plt.axhline(y=0, color='black', linewidth=0.8)
        plt.axvline(x=self.K, color='gray', linestyle='--', label='Strike')
        plt.axvline(breakeven, color="red", linestyle=":", label="Break-even")

        plt.title('Option Payoff Diagram')
        plt.xlabel('Stock Price at Expiry') 
        plt.ylabel('Profit / Loss')         
        plt.legend()                       
        plt.grid(True, alpha=0.3)         
        plt.tight_layout()                 
        plt.show()          

    def both(self):
        S_range = np.linspace(0.5 * self.K, 1.5 * self.K, 300)
        call_payoff = np.maximum(S_range - self.K, 0) - self.premium
        put_payoff = np.maximum(self.K - S_range, 0) - self.premium
        put_breakeven = self.K - self.premium
        call_breakeven = self.K + self.premium

        plt.figure(figsize=(10, 5))
        plt.plot(S_range, call_payoff, color='green', linewidth=2, label='Call')
        plt.plot(S_range, put_payoff, color='navy', linewidth=2, label='Put')
        plt.axhline(y=0, color='black', linewidth=0.8)
        plt.axvline(x=self.K, color='gray', linestyle='--', label='Strike')
        plt.axvline(call_breakeven, color="red", linestyle=":", linewidth=1.8,label=f"Call B/E ({call_breakeven:.2f})")
        plt.axvline(put_breakeven, color="darkorange", linestyle=":", linewidth=1.8, label=f"Put B/E ({put_breakeven:.2f})")

        plt.title('Option Payoff Diagram')
        plt.xlabel('Stock Price at Expiry') 
        plt.ylabel('Profit / Loss')         
        plt.legend()                       
        plt.grid(True, alpha=0.3)         
        plt.tight_layout()                 
        plt.show()     