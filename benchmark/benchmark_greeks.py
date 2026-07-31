"""
Benchmark for Greeks calculation.

Run:
    python benchmark/benchmark_greeks.py
"""

from time import perf_counter
from statistics import mean

from option_pricing._core import calculate_greeks

# Test Parameters
S = 100
K = 100
T = 1
r = 0.05
vol = 0.20

ITERATIONS = 10000

# Warm-up
for _ in range(100):
    calculate_greeks(S, K, T, r, vol)

times = []

for _ in range(ITERATIONS):
    start = perf_counter()
    results = calculate_greeks(S, K, T, r, vol)
    end = perf_counter()

    times.append((end - start) * 1e6)  # microseconds

(
    delta_call,
    delta_put,
    gamma,
    theta_call,
    theta_put,
    vega,
    rho_call,
    rho_put,
) = results

print("=" * 50)
print("Greeks Benchmark")
print("=" * 50)
print(f"Iterations        : {ITERATIONS}")
print(f"Delta (Call)      : {delta_call:.6f}")
print(f"Delta (Put)       : {delta_put:.6f}")
print(f"Gamma             : {gamma:.6f}")
print(f"Vega              : {vega:.6f}")
print(f"Average Runtime   : {mean(times):.2f} μs")
print(f"Minimum Runtime   : {min(times):.2f} μs")
print(f"Maximum Runtime   : {max(times):.2f} μs")
print("=" * 50)