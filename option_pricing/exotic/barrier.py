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
 
    def call(self, steps=100, paths=100000):
        call, _ = barrier_price(self.S, self.K, self.T, self.r, self.sigma, steps, paths, self.H, self.barrier_type)
        return call
 
    def put(self, steps=100, paths=100000):
        _, put = barrier_price(self.S, self.K, self.T, self.r, self.sigma, steps, paths, self.H, self.barrier_type)
        return put