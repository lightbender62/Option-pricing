"""
Benchmark for the Monte Carlo pricing model.

Run:
    python benchmark/benchmark_monte_carlo.py
"""

from time import perf_counter
from statistics import mean

from option_pricing._core import european_price


# Test Parameters
S = 100
K = 100
T = 1
r = 0.05
vol = 0.20

N = 500         # Time steps
M = 100000       # Simulation paths

ITERATIONS = 20

# Warm-up
for _ in range(3):
    european_price(S, K, T , r , vol, N, M)

times = []

for _ in range(ITERATIONS):
    start = perf_counter()
    call_price, put_price = european_price(S, K, T , r, vol, N, M)
    end = perf_counter()

    times.append((end - start) * 1000)   # milliseconds

print("=" * 50)
print("Monte Carlo Benchmark")
print("=" * 50)
print(f"Time Steps        : {N}")
print(f"Simulation Paths  : {M}")
print(f"Iterations        : {ITERATIONS}")
print(f"Call Price        : {call_price:.6f}")
print(f"Put Price         : {put_price:.6f}")
print(f"Average Runtime   : {mean(times):.3f} ms")
print(f"Minimum Runtime   : {min(times):.3f} ms")
print(f"Maximum Runtime   : {max(times):.3f} ms")
print("=" * 50)