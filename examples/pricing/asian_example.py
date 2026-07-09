"""
Example demonstrating the AsianOption class, comparing arithmetic vs
geometric averaging.

Run from the project root:
    python examples/pricing/asian_example.py
"""

from option_pricing import AsianOption

opt = AsianOption(S=100, K=100, T=1, r=0.05, sigma=0.2)

print("Asian Option Example")
print("-" * 50)
print(f"{'Average':<15}{'Call':>15}{'Put':>15}")
print("-" * 50)
for average in ("arithmetic", "geometric"):
    call = opt.call(average=average)
    put = opt.put(average=average)
    print(f"{average:<15}{call:>15.6f}{put:>15.6f}")

print("\nNote: geometric-average call is typically <= arithmetic-average call,")
print("since the geometric mean of a path is always <= its arithmetic mean.")