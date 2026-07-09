"""
Example demonstrating Greeks via EuropeanOption's built-in methods.
 
Run from the project root:
    python examples/analytics/greeks_example.py
"""
from option_pricing import EuropeanOption
opt = EuropeanOption(100 , 100 , 1 , 0.05 , 0.2)

print("Greeks Example")
print("-" * 40)
 
delta_call, delta_put = opt.delta()
print(f"Delta (call, put) : {delta_call:.6f}, {delta_put:.6f}")
 
print(f"Gamma              : {opt.gamma():.6f}")
 
theta_call, theta_put = opt.theta()
print(f"Theta (call, put)  : {theta_call:.6f}, {theta_put:.6f}")
 
print(f"Vega               : {opt.vega():.6f}")
 
rho_call, rho_put = opt.rho()
print(f"Rho (call, put)    : {rho_call:.6f}, {rho_put:.6f}")
 
print("\nAll Greeks as a dict:")
for name, value in opt.greeks().items():
    print(f"  {name:<12}: {value:.6f}")