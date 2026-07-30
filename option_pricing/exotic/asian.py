"""
Asian option pricing via Monte Carlo (arithmetic and geometric average).
"""
from option_pricing._core import asian_price_arithmetic, asian_price_geometric
from option_pricing.base import BaseOption


class AsianOption(BaseOption):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Caches the (call, put) pair per (average, steps, paths) combo, so a
        # call()+put() pair with matching args reuses one simulation instead
        # of running simulate_paths() twice.
        self._mc_cache = {}

    def _mc_prices(self, average, steps, paths):
        key = (average, steps, paths)
        if key not in self._mc_cache:
            if average == 'arithmetic':
                self._mc_cache[key] = asian_price_arithmetic(self.S, self.K, self.T, self.r, self.sigma, steps, paths)
            elif average == 'geometric':
                self._mc_cache[key] = asian_price_geometric(self.S, self.K, self.T, self.r, self.sigma, steps, paths)
            else:
                raise ValueError(f"Unknown average '{average}'. Choose from: 'arithmetic', 'geometric'")
        return self._mc_cache[key]

    def call(self, average='arithmetic', steps=100, paths=100000):
        call, _ = self._mc_prices(average, steps, paths)
        return call

    def put(self, average='arithmetic', steps=100, paths=100000):
        _, put = self._mc_prices(average, steps, paths)
        return put