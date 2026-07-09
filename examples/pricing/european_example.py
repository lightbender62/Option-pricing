"""
Example demonstrating the EuropeanOption class: pricing across all three
models (Black-Scholes, Binomial, Monte Carlo), plus Greeks and implied vol.

Run from the project root:
    python examples/pricing/european_example.py
"""

from option_pricing import EuropeanOption

opt = EuropeanOption(S=100, K=100, T=1, r=0.05, sigma=0.2)

print("European Option Example")
print("-" * 50)
print(f"{'Model':<15}{'Call':>15}{'Put':>15}")
print("-" * 50)
for model in ("black_scholes", "binomial", "montecarlo"):
    call = opt.call(model=model)
    put = opt.put(model=model)
    print(f"{model:<15}{call:>15.6f}{put:>15.6f}")

print("\nGreeks")
print("-" * 50)
greeks = opt.greeks()
for name, value in greeks.items():
    print(f"{name:<15}: {value:.6f}")

print("\nImplied Volatility (recovering sigma from the BS price)")
print("-" * 50)
market_call = opt.call(model="black_scholes")
market_put = opt.put(model="black_scholes")
iv_call, iv_put = opt.implied_vol(call_price=market_call, put_price=market_put)
print(f"Call IV : {iv_call:.6f}")
print(f"Put IV  : {iv_put:.6f}")