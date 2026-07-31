"""
Benchmark for the Black-Scholes pricing model.

Run:
    python benchmark/benchmark_black_scholes.py
"""

from time import perf_counter
from statistics import mean

from option_pricing._core import calculate_price


# Test Parameters
S = 100
K = 100
T = 1
r = 0.05
vol = 0.20

# Number of benchmark iterations
ITERATIONS = 10000

# Warm-up (avoids first-run overhead)
for _ in range(100):
    calculate_price(S, K, T, r, vol)

times = []

for _ in range(ITERATIONS):
    start = perf_counter()
    call_price, put_price = calculate_price(S, K, T, r, vol)
    end = perf_counter()

    times.append((end - start) * 1e6)   # microseconds

print("=" * 50)
print("Black-Scholes Benchmark")
print("=" * 50)
print(f"Iterations        : {ITERATIONS}")
print(f"Call Price        : {call_price:.6f}")
print(f"Put Price         : {put_price:.6f}")
print(f"Average Runtime   : {mean(times):.2f} μs")
print(f"Minimum Runtime   : {min(times):.2f} μs")
print(f"Maximum Runtime   : {max(times):.2f} μs")
print("=" * 50)