"""
Barrier option pricing via Monte Carlo.
"""
from option_pricing._core import barrier_price
from option_pricing.base import BaseOption
 
 
class BarrierOption(BaseOption):
 
    def __init__(self, S, K, T, r, sigma, H, barrier_type):
        super().__init__(S, K, T, r, sigma)
        self.H = H
        self.barrier_type = barrier_type
        # Caches the (call, put) pair per (steps, paths) combo, so a
        # call()+put() pair with matching args reuses one simulation instead
        # of running simulate_paths() twice.
        self._mc_cache = {}

    def _mc_prices(self, steps, paths):
        key = (steps, paths)
        if key not in self._mc_cache:
            self._mc_cache[key] = barrier_price(self.S, self.K, self.T, self.r, self.sigma, steps, paths, self.H, self.barrier_type)
        return self._mc_cache[key]

    def call(self, steps=100, paths=100000):
        call, _ = self._mc_prices(steps, paths)
        return call
 
    def put(self, steps=100, paths=100000):
        _, put = self._mc_prices(steps, paths)
        return put