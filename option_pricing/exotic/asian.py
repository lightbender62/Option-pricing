"""
Asian option pricing via Monte Carlo (arithmetic and geometric average).
"""
from option_pricing._core import asian_price_arithmetic, asian_price_geometric
from option_pricing.base import BaseOption


class AsianOption(BaseOption):

    def call(self, average='arithmetic', steps=100, paths=100000):
        if average == 'arithmetic':
            call, _ = asian_price_arithmetic(self.S, self.K, self.T, self.r, self.sigma, steps, paths)
        elif average == 'geometric':
            call, _ = asian_price_geometric(self.S, self.K, self.T, self.r, self.sigma, steps, paths)
        else:
            raise ValueError(f"Unknown average '{average}'. Choose from: 'arithmetic', 'geometric'")
        return call

    def put(self, average='arithmetic', steps=100, paths=100000):
        if average == 'arithmetic':
            _, put = asian_price_arithmetic(self.S, self.K, self.T, self.r, self.sigma, steps, paths)
        elif average == 'geometric':
            _, put = asian_price_geometric(self.S, self.K, self.T, self.r, self.sigma, steps, paths)
        else:
            raise ValueError(f"Unknown average '{average}'. Choose from: 'arithmetic', 'geometric'")
        return put