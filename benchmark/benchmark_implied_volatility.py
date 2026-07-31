"""
Benchmark for Implied Volatility calculation.

Run:
    python benchmark/benchmark_implied_volatility.py
"""

from time import perf_counter
from statistics import mean

from option_pricing._core import calculate_iv
from option_pricing._core import calculate_price

# Test Parameters
S = 100
K = 100
T = 1
r = 0.05
vol = 0.20

# Generate market prices using Black-Scholes
Cm, Pm = calculate_price(S, K, T, r, vol)

ITERATIONS = 1000

# Warm-up
for _ in range(20):
    calculate_iv(S, K, T, r, Cm, Pm)

times = []

for _ in range(ITERATIONS):
    start = perf_counter()
    implied_call_vol, implied_put_vol = calculate_iv(S, K, T, r, Cm, Pm)
    end = perf_counter()

    times.append((end - start) * 1e3)  # milliseconds

print("=" * 50)
print("Implied Volatility Benchmark")
print("=" * 50)
print(f"Iterations        : {ITERATIONS}")
print(f"Call IV           : {implied_call_vol:.6f}")
print(f"Put IV            : {implied_put_vol:.6f}")
print(f"Average Runtime   : {mean(times):.3f} ms")
print(f"Minimum Runtime   : {min(times):.3f} ms")
print(f"Maximum Runtime   : {max(times):.3f} ms")
print("=" * 50)