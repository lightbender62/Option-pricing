"""
Shared fixtures for the option_pricing test suite.
"""
import pytest

from option_pricing import (
    EuropeanOption,
    AmericanOption,
    AsianOption,
    BarrierOption,
    LookbackOption,
)

# Standard test parameters, reused across most tests for consistency.
S, K, T, r, sigma = 100, 100, 1, 0.05, 0.2


@pytest.fixture
def params():
    """Standard S, K, T, r, sigma as a dict for easy unpacking."""
    return dict(S=S, K=K, T=T, r=r, sigma=sigma)


@pytest.fixture
def atm_european():
    return EuropeanOption(S=S, K=K, T=T, r=r, sigma=sigma)


@pytest.fixture
def atm_american():
    return AmericanOption(S=S, K=K, T=T, r=r, sigma=sigma)


@pytest.fixture
def atm_asian():
    return AsianOption(S=S, K=K, T=T, r=r, sigma=sigma)


@pytest.fixture
def down_and_out_barrier():
    return BarrierOption(S=S, K=K, T=T, r=r, sigma=sigma, H=90, barrier_type="down-and-out")


@pytest.fixture
def down_and_in_barrier():
    return BarrierOption(S=S, K=K, T=T, r=r, sigma=sigma, H=90, barrier_type="down-and-in")


@pytest.fixture
def up_and_out_barrier():
    return BarrierOption(S=S, K=K, T=T, r=r, sigma=sigma, H=110, barrier_type="up-and-out")


@pytest.fixture
def up_and_in_barrier():
    return BarrierOption(S=S, K=K, T=T, r=r, sigma=sigma, H=110, barrier_type="up-and-in")


@pytest.fixture
def atm_lookback():
    return LookbackOption(S=S, K=K, T=T, r=r, sigma=sigma)