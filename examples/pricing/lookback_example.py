"""
Example demonstrating the LookbackOption class, comparing floating vs
fixed strike variants.

Run from the project root:
    python examples/pricing/lookback_example.py
"""

from option_pricing import LookbackOption

opt = LookbackOption(S=100, K=100, T=1, r=0.05, sigma=0.2)

print("Lookback Option Example")
print("-" * 50)
print(f"{'Strike Type':<15}{'Call':>15}{'Put':>15}")
print("-" * 50)
for strike_type in ("floating", "fixed"):
    call = opt.call(strike_type=strike_type)
    put = opt.put(strike_type=strike_type)
    print(f"{strike_type:<15}{call:>15.6f}{put:>15.6f}")

print("\nNote:")
print("• Floating-strike call payoff = S_T − running minimum (no strike required).")
print("• Fixed-strike call payoff    = max(running maximum − K, 0).")
print("• Lookback options are generally more valuable than vanilla options")
print("  because they benefit from the most favorable price observed")
print("  during the option's lifetime.")