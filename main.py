from Implied_Volatility import Implied_vol
from Monte_Carlo import Monte_Carlo
from Greeks import Greeks
from black_scholes import Calculate_Price
from Binomial_model import Binomial_model

S = float(input("Enter stock price (S): "))
K = float(input("Enter strike price (K): "))
T = float(input("Enter time to maturity (T): "))
r = float(input("Enter risk-free rate (r): "))
vol = float(input("Enter volatility (sigma): "))
N = int(input("Enter number of time steps (N): "))
M = int(input("Enter number of Monte Carlo simulations (M): "))

C_monte , P_monte = Monte_Carlo(S , K , r , T , vol , N , M)
C_black , P_black = Calculate_Price(S , K , T , r , vol)
C_binomial , P_binomial = Binomial_model(S , K , T ,r , vol , N)

delta_call , delta_put , gamma , theta_call , theta_put , vega , rho_call , rho_put = Greeks(S , K , T , r , vol)

iv_call , iv_put = Implied_vol(S , K , T , r , C_black , P_black)

#input parameteres
print("=" * 60)
print("          OPTION PRICING MODELS")
print("=" * 60)
print(f"\nInput Parameters")
print("-" * 60)
print(f"Stock Price (S)        : {S:.2f}")
print(f"Strike Price (K)       : {K:.2f}")
print(f"Time to Maturity (T)   : {T:.4f}")
print(f"Risk-Free Rate (r)     : {r:.4f}")
print(f"Volatility (σ)         : {vol:.4f}")
print(f"Binomial Steps (N)     : {N}")
print(f"Monte Carlo Paths (M)  : {M:,}")

#Prices
print("\n" + "=" * 60)
print(f"{'PRICING RESULTS':^60}")
print("=" * 60)

print(f"{'Model':<20}{'Call':>15}{'Put':>15}")
print("-" * 50)

print(f"{'Black-Scholes':<20}{C_black:>15.6f}{P_black:>15.6f}")
print(f"{'Monte Carlo':<20}{C_monte:>15.6f}{P_monte:>15.6f}")
print(f"{'Binomial':<20}{C_binomial:>15.6f}{P_binomial:>15.6f}")

#greeks
print("\n" + "=" * 60)
print(f"{'GREEKS':^60}")
print("=" * 60)

print(f"{'Call Delta':<20}: {delta_call:>10.6f}")
print(f"{'Put Delta':<20}: {delta_put:>10.6f}")
print(f"{'Gamma':<20}: {gamma:>10.6f}")
print(f"{'Call Theta':<20}: {theta_call:>10.6f}")
print(f"{'Put Theta':<20}: {theta_put:>10.6f}")
print(f"{'Vega':<20}: {vega:>10.6f}")
print(f"{'Call Rho':<20}: {rho_call:>10.6f}")
print(f"{'Put Rho':<20}: {rho_put:>10.6f}")

#implied volatility

print("\n" + "=" * 60)
print(f"{'IMPLIED VOLATILITY':^60}")
print("=" * 60)

print(f"Call IV : {iv_call:.6f}")
print(f"Put  IV : {iv_put:.6f}")