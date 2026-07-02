"""
Options Greeks: analytical sensitivities derived from Black-Scholes.
"""
import math
from scipy.stats import norm
from option_pricing._core.black_scholes import calculate_d1_d2


def calculate_greeks(S, K, T, r, sigma):
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
    d1, _ = calculate_d1_d2(S, K, T, r, sigma)
    return S * norm.pdf(d1) * math.sqrt(T)