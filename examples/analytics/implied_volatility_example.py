"""
Example demonstrating implied volatility recovery via EuropeanOption's
built-in .implied_vol() method.

Run from the project root:
    python examples/analytics/implied_volatility_example.py
"""

from option_pricing import EuropeanOption

opt = EuropeanOption(S=100, K=100, T=1, r=0.05, sigma=0.2)

# Ground truth: price it ourselves at the known sigma=0.2
market_call = opt.call(model="black_scholes")
market_put = opt.put(model="black_scholes")
print("Implied Volatility Example")
print("-" * 45)
print(f"Priced at true sigma = 0.20 -> call={market_call:.6f}, put={market_put:.6f}")

# Now recover sigma from those prices, as if they were observed market quotes
iv_call, iv_put = opt.implied_vol(call_price=market_call, put_price=market_put)
print(f"\nRecovered IV from call price : {iv_call:.6f}")
print(f"Recovered IV from put price  : {iv_put:.6f}")
print("(both should be very close to the true sigma = 0.20)")

print("\nSingle-sided lookup also works:")
print(f"IV from call only : {opt.implied_vol(call_price=market_call):.6f}")
print(f"IV from put only  : {opt.implied_vol(put_price=market_put):.6f}")