"""
American option pricing using Binomial Tree with early exercise.
"""
from option_pricing._core import american_price
from option_pricing.base import BaseOption


class AmericanOption(BaseOption):

    def call(self, steps=500):
        call, _ = american_price(self.S, self.K, self.T, self.r, self.sigma, steps)
        return call

    def put(self, steps=500):
        _, put = american_price(self.S, self.K, self.T, self.r, self.sigma, steps)
        return put