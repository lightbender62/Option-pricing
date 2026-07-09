"""
Example demonstrating the BarrierOption class across all four barrier
types, and verifying in/out parity against a vanilla European option.

Run from the project root:
    python examples/pricing/barrier_example.py
"""

from option_pricing import BarrierOption, EuropeanOption

S, K, T, r, sigma = 100, 100, 1, 0.05, 0.2

print("Barrier Option Example")
print("-" * 55)
print(f"{'Barrier Type':<20}{'H':>8}{'Call':>13}{'Put':>13}")
print("-" * 55)

down_out = BarrierOption(S=S, K=K, T=T, r=r, sigma=sigma,H=90, barrier_type="down-and-out")
down_in = BarrierOption(S=S, K=K, T=T, r=r, sigma=sigma,H=90, barrier_type="down-and-in")
up_out = BarrierOption(S=S, K=K, T=T, r=r, sigma=sigma,H=110, barrier_type="up-and-out")
up_in = BarrierOption(S=S, K=K, T=T, r=r, sigma=sigma,H=110, barrier_type="up-and-in")

results = []
for label, H, option in [
    ("down-and-out", 90, down_out),
    ("down-and-in", 90, down_in),
    ("up-and-out", 110, up_out),
    ("up-and-in", 110, up_in),
]:
    call = option.call()
    put = option.put()

    results.append({
        "label": label,
        "H": H,
        "call": call,
        "put": put,
    })

    print(f"{label:<20}{H:>8}{call:>13.6f}{put:>13.6f}")

# Cached values for parity
do = results[0]
di = results[1]
uo = results[2]
ui = results[3]

vanilla = EuropeanOption(S=S, K=K, T=T, r=r, sigma=sigma)

print("\nIn/Out Parity Check")
print("-" * 55)
print(f"{'Down-Out + Down-In Call':<32}: {do['call'] + di['call']:.6f}")
print(f"{'Vanilla European Call':<32}: {vanilla.call():.6f}")
print()

print(f"{'Down-Out + Down-In Put':<32}: {do['put'] + di['put']:.6f}")
print(f"{'Vanilla European Put':<32}: {vanilla.put():.6f}")

print("\nNote: In/Out parity holds theoretically. Small numerical differences arise because each barrier option is priced using an independent Monte Carlo simulation.")