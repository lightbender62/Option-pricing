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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Caches the (call, put) pair from european_price() per (steps, paths)
        # combo, so a call()+put() pair for the same montecarlo parameters
        # reuses one simulation instead of running simulate_paths() twice.
        self._mc_cache = {}

    def _mc_prices(self, steps, paths):
        key = (steps, paths)
        if key not in self._mc_cache:
            self._mc_cache[key] = european_price(self.S, self.K, self.T, self.r, self.sigma, steps, paths)
        return self._mc_cache[key]

    def call(self, model='black_scholes', steps=500, paths=100000):
        if model == 'black_scholes':
            call, _ = calculate_price(self.S, self.K, self.T, self.r, self.sigma)
        elif model == 'binomial':
            call, _ = binomial_price(self.S, self.K, self.T, self.r, self.sigma, steps)
        elif model == 'montecarlo':
            call, _ = self._mc_prices(steps, paths)
        else:
            raise ValueError(f"Unknown model '{model}'. Choose from: 'black_scholes', 'binomial', 'montecarlo'")
        return call

    def put(self, model='black_scholes', steps=500, paths=100000):
        if model == 'black_scholes':
            _, put = calculate_price(self.S, self.K, self.T, self.r, self.sigma)
        elif model == 'binomial':
            _, put = binomial_price(self.S, self.K, self.T, self.r, self.sigma, steps)
        elif model == 'montecarlo':
            _, put = self._mc_prices(steps, paths)
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
        iv_call, iv_put = calculate_iv(self.S, self.K, self.T, self.r, call_price, put_price)
        if call_price is not None and put_price is not None:
            return iv_call, iv_put
        elif call_price is not None:
            return iv_call
        else:
            return iv_put