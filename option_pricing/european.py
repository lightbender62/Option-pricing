"""
European option pricing, Greeks, and implied volatility.
"""
from option_pricing._core import (
    calculate_price,
    binomial_price,
    european_price,
    calculate_greeks,
    calculate_iv
)
from option_pricing.base import BaseOption


class EuropeanOption(BaseOption):

    def call(self, model='black_scholes', steps=100, paths=100000):
        if model == 'black_scholes':
            call, _ = calculate_price(self.S, self.K, self.T, self.r, self.sigma)
        elif model == 'binomial':
            call, _ = binomial_price(self.S, self.K, self.T, self.r, self.sigma, steps)
        elif model == 'montecarlo':
            call, _ = european_price(self.S, self.K, self.T, self.r, self.sigma, steps, paths)
        else:
            raise ValueError(f"Unknown model '{model}'. Choose from: 'black_scholes', 'binomial', 'montecarlo'")
        return call

    def put(self, model='black_scholes', steps=100, paths=100000):
        if model == 'black_scholes':
            _, put = calculate_price(self.S, self.K, self.T, self.r, self.sigma)
        elif model == 'binomial':
            _, put = binomial_price(self.S, self.K, self.T, self.r, self.sigma, steps)
        elif model == 'montecarlo':
            _, put = european_price(self.S, self.K, self.T, self.r, self.sigma, steps, paths)
        else:
            raise ValueError(f"Unknown model '{model}'. Choose from: 'black_scholes', 'binomial', 'montecarlo'")
        return put

    def delta(self):
        delta_call, delta_put, _, _, _, _, _, _ = calculate_greeks(self.S, self.K, self.T, self.r, self.sigma)
        return delta_call, delta_put

    def gamma(self):
        _, _, gamma, _, _, _, _, _ = calculate_greeks(self.S, self.K, self.T, self.r, self.sigma)
        return gamma

    def theta(self):
        _, _, _, theta_call, theta_put, _, _, _ = calculate_greeks(self.S, self.K, self.T, self.r, self.sigma)
        return theta_call, theta_put

    def vega(self):
        _, _, _, _, _, vega, _, _ = calculate_greeks(self.S, self.K, self.T, self.r, self.sigma)
        return vega

    def rho(self):
        _, _, _, _, _, _, rho_call, rho_put = calculate_greeks(self.S, self.K, self.T, self.r, self.sigma)
        return rho_call, rho_put

    def greeks(self):
        delta_call, delta_put, gamma, theta_call, theta_put, vega, rho_call, rho_put = calculate_greeks(self.S, self.K, self.T, self.r, self.sigma)
        return {
            'delta_call': delta_call,
            'delta_put': delta_put,
            'gamma': gamma,
            'theta_call': theta_call,
            'theta_put': theta_put,
            'vega': vega,
            'rho_call': rho_call,
            'rho_put': rho_put
        }

    def implied_vol(self, call_price=None, put_price=None):
        if call_price is None and put_price is None:
            raise ValueError("Provide at least one of call_price or put_price")
        iv_call, iv_put = calculate_iv(self.S, self.K, self.T, self.r,
                                        call_price or 0, put_price or 0)
        if call_price is not None and put_price is not None:
            return iv_call, iv_put
        elif call_price is not None:
            return iv_call
        else:
            return iv_put