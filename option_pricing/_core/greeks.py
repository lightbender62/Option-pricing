"""
Options Greeks: analytical sensitivities derived from Black-Scholes.
"""
import math
from scipy.stats import norm
from option_pricing._core.black_scholes import calculate_d1_d2


def calculate_greeks(S, K, T, r, sigma):
    if S <= 0:
        raise ValueError(f"S must be positive, got {S}")
    if K <= 0:
        raise ValueError(f"K must be positive, got {K}")
    if T < 0:
        raise ValueError(f"T must be non-negative, got {T}")
    if sigma < 0:
        raise ValueError(f"sigma must be non-negative, got {sigma}")
    if T == 0 or sigma == 0:
        # No time value or no uncertainty left: delta is the intrinsic
        # step function, and all other Greeks collapse to 0
        delta_call = 1.0 if S > K else (0.0 if S < K else 0.5)
        delta_put = delta_call - 1
        gamma = 0.0
        theta_call = 0.0
        theta_put = 0.0
        vega = 0.0
        rho_call = 0.0
        rho_put = 0.0
        return delta_call, delta_put, gamma, theta_call, theta_put, vega, rho_call, rho_put
    d1, d2 = calculate_d1_d2(S, K, T, r, sigma)

    # delta
    delta_call = norm.cdf(d1)
    delta_put = norm.cdf(d1) - 1

    # gamma
    gamma = norm.pdf(d1) / (S * sigma * math.sqrt(T))

    # theta (daily)
    theta_call = (-(S * norm.pdf(d1) * sigma) / (2 * math.sqrt(T)) - r * K * math.exp(-r * T) * norm.cdf(d2)) / 365
    theta_put = (-(S * norm.pdf(d1) * sigma) / (2 * math.sqrt(T)) + r * K * math.exp(-r * T) * norm.cdf(-d2)) / 365

    # vega
    vega = S * norm.pdf(d1) * math.sqrt(T)

    # rho
    rho_call = K * T * math.exp(-r * T) * norm.cdf(d2)
    rho_put = -K * T * math.exp(-r * T) * norm.cdf(-d2)

    return delta_call, delta_put, gamma, theta_call, theta_put, vega, rho_call, rho_put


def calculate_vega(S, K, T, r, sigma):
    if S <= 0:
        raise ValueError(f"S must be positive, got {S}")
    if K <= 0:
        raise ValueError(f"K must be positive, got {K}")
    if T < 0:
        raise ValueError(f"T must be non-negative, got {T}")
    if sigma < 0:
        raise ValueError(f"sigma must be non-negative, got {sigma}")
    if T == 0 or sigma == 0:
        return 0.0
    
    d1, _ = calculate_d1_d2(S, K, T, r, sigma)
    return S * norm.pdf(d1) * math.sqrt(T)