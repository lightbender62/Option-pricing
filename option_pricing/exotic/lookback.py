"""
Lookback option pricing via Monte Carlo (floating and fixed strike).
"""
from option_pricing._core import lookback_price_floating, lookback_price_fixed
from option_pricing.base import BaseOption
 
 
class LookbackOption(BaseOption):
 
    def call(self, strike_type='floating', steps=100, paths=100000):
        if strike_type == 'floating':
            call, _ = lookback_price_floating(self.S, self.T, self.r, self.sigma, steps, paths)
        elif strike_type == 'fixed':
            call, _ = lookback_price_fixed(self.S, self.K, self.T, self.r, self.sigma, steps, paths)
        else:
            raise ValueError(f"Unknown strike_type '{strike_type}'. Choose from: 'floating', 'fixed'")
        return call
 
    def put(self, strike_type='floating', steps=100, paths=100000):
        if strike_type == 'floating':
            _, put = lookback_price_floating(self.S, self.T, self.r, self.sigma, steps, paths)
        elif strike_type == 'fixed':
            _, put = lookback_price_fixed(self.S, self.K, self.T, self.r, self.sigma, steps, paths)
        else:
            raise ValueError(f"Unknown strike_type '{strike_type}'. Choose from: 'floating', 'fixed'")
        return put