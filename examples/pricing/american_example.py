"""
Example demonstrating the AmericanOption class and comparing it against
EuropeanOption to show the early-exercise premium.

Run from the project root:
    python examples/pricing/american_example.py
"""

from option_pricing import AmericanOption, EuropeanOption

american = AmericanOption(S=100, K=100, T=1, r=0.05, sigma=0.2)
european = EuropeanOption(S=100, K=100, T=1, r=0.05, sigma=0.2)

print("American vs European Option Example")
print("-" * 50)
print(f"{'':<15}{'Call':>15}{'Put':>15}")
print("-" * 50)
print(f"{'American':<15}{american.call():>15.6f}{american.put():>15.6f}")
print(f"{'European':<15}{european.call(model='binomial'):>15.6f}{european.put(model='binomial'):>15.6f}")

premium_put = american.put() - european.put(model="binomial")
premium_call = american.call() - european.call(model="binomial")
print("\nEarly-exercise premium (American - European)")
print(f"Call premium : {premium_call:.6f}  (theoretically 0 for non-dividend-paying stocks)")
print(f"Put premium  : {premium_put:.6f}  (expected > 0)")