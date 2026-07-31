"""
Benchmark for the Binomial Tree pricing model.

Run:
    python benchmark/benchmark_binomial.py
"""

from time import perf_counter
from statistics import mean

from option_pricing._core import binomial_price


# Test Parameters
S = 100
K = 100
T = 1
r = 0.05
vol = 0.20
N = 500

# Number of benchmark iterations
ITERATIONS = 1000

# Warm-up
for _ in range(20):
    binomial_price(S, K, T, r, vol , N)

times = []

for _ in range(ITERATIONS):
    start = perf_counter()
    call_price, put_price = binomial_price(S, K, T, r, vol , N)
    end = perf_counter()

    times.append((end - start) * 1e3)  # milliseconds

print("=" * 50)
print("Binomial Tree Benchmark")
print("=" * 50)
print(f"Steps             : {N}")
print(f"Iterations        : {ITERATIONS}")
print(f"Call Price        : {call_price:.6f}")
print(f"Put Price         : {put_price:.6f}")
print(f"Average Runtime   : {mean(times):.3f} ms")
print(f"Minimum Runtime   : {min(times):.3f} ms")
print(f"Maximum Runtime   : {max(times):.3f} ms")
print("=" * 50)