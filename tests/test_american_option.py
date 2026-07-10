"""
Tests for option_pricing.american.AmericanOption
"""
import pytest

from option_pricing import AmericanOption, EuropeanOption


def test_american_put_gte_european_put(atm_american, atm_european):
    assert atm_american.put() >= atm_european.put(model="binomial") - 1e-6


def test_american_call_approx_european_call(atm_american, atm_european):
    assert atm_american.call() == pytest.approx(atm_european.call(model="binomial"), abs=0.1)


def test_deep_itm_american_put_shows_early_exercise_premium():
    american = AmericanOption(S=70, K=100, T=1, r=0.05, sigma=0.2)
    european = EuropeanOption(S=70, K=100, T=1, r=0.05, sigma=0.2)
    assert american.put() > european.put(model="binomial")


def test_negative_S_raises():
    with pytest.raises(ValueError):
        AmericanOption(S=-100, K=100, T=1, r=0.05, sigma=0.2).call()