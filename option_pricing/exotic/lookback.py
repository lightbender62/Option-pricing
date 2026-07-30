"""
Lookback option pricing via Monte Carlo (floating and fixed strike).
"""
from option_pricing._core import lookback_price_floating, lookback_price_fixed
from option_pricing.base import BaseOption
 
 
class LookbackOption(BaseOption):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Caches the (call, put) pair per (strike_type, steps, paths) combo,
        # so a call()+put() pair with matching args reuses one simulation
        # instead of running simulate_paths() twice.
        self._mc_cache = {}

    def _mc_prices(self, strike_type, steps, paths):
        key = (strike_type, steps, paths)
        if key not in self._mc_cache:
            if strike_type == 'floating':
                self._mc_cache[key] = lookback_price_floating(self.S, self.T, self.r, self.sigma, steps, paths)
            elif strike_type == 'fixed':
                self._mc_cache[key] = lookback_price_fixed(self.S, self.K, self.T, self.r, self.sigma, steps, paths)
            else:
                raise ValueError(f"Unknown strike_type '{strike_type}'. Choose from: 'floating', 'fixed'")
        return self._mc_cache[key]

    def call(self, strike_type='floating', steps=100, paths=100000):
        call, _ = self._mc_prices(strike_type, steps, paths)
        return call
 
    def put(self, strike_type='floating', steps=100, paths=100000):
        _, put = self._mc_prices(strike_type, steps, paths)
        return put